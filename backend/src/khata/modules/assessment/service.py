"""Exam authoring, evaluation and review.

Every state change goes through :func:`khata.engines.workflow.transition`, and every
mark through :func:`khata.engines.scoring.score_item`. This module holds persistence
and permissions; it never re-implements a rule the engines already own.

The AI never finalises a mark. A suggestion moves an item to ``suggested``; only a
teacher decision moves it to ``confirmed`` or ``edited`` (spec 07 §4.1, ADR-011).
"""

from __future__ import annotations

import uuid
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from decimal import Decimal
from types import MappingProxyType

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from khata.core.errors import DomainError
from khata.core.models import utcnow
from khata.engines.errors import EngineError, IllegalTransition
from khata.engines.rubric import Rubric, validate_rubric
from khata.engines.scoring import CriterionDecision, ItemScore, TotalOverride, score_item
from khata.engines.workflow import ExamState, ItemState, transition
from khata.modules.aigateway.provider import (
    AnswerContext,
    MarkingProvider,
    ProviderError,
)
from khata.modules.assessment.models import (
    Exam,
    ExamCandidate,
    ExamItem,
    ItemResult,
    ItemRubric,
    Script,
)

#: Item states whose mark counts as decided by a teacher.
DECIDED_STATES = frozenset({ItemState.CONFIRMED.value, ItemState.EDITED.value})


@dataclass(frozen=True, slots=True)
class RubricRejected(Exception):
    """A rubric that cannot be saved or locked, with the engine's issues attached."""

    issues: tuple[dict[str, str], ...]

    def as_error(self) -> DomainError:
        return DomainError(
            "VALIDATION_FAILED",
            detail="The rubric is not valid.",
            extra={"errors": list(self.issues)},
        )


def _conflict(exc: EngineError) -> DomainError:
    """Map an illegal workflow transition to a 409 the client can act on."""
    if isinstance(exc, IllegalTransition):
        return DomainError(
            "CONFLICT",
            detail=exc.reason,
            extra={"from_state": exc.current.value, "to_state": exc.target.value},
        )
    return DomainError("CONFLICT", detail=str(exc))


# --------------------------------------------------------------------------- authoring


def create_exam(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    school_id: uuid.UUID,
    name: str,
    subject_code: str,
    class_level: int,
    created_by: uuid.UUID,
) -> Exam:
    exam = Exam(
        tenant_id=tenant_id,
        school_id=school_id,
        name=name,
        subject_code=subject_code,
        class_level=class_level,
        created_by=created_by,
    )
    session.add(exam)
    session.flush()
    return exam


def get_exam(session: Session, exam_id: uuid.UUID) -> Exam:
    exam = session.get(Exam, exam_id)
    if exam is None:
        raise DomainError("NOT_FOUND", detail="Exam not found.")
    return exam


def _require_draft(exam: Exam) -> None:
    if exam.state != ExamState.DRAFT.value:
        raise DomainError(
            "CONFLICT",
            detail="The exam structure can only change while it is a draft.",
            extra={"from_state": exam.state},
        )


def add_item(
    session: Session,
    *,
    exam: Exam,
    item_no: int,
    max_marks: Decimal,
    prompt_bn: str = "",
    prompt_en: str = "",
) -> ExamItem:
    _require_draft(exam)
    item = ExamItem(
        tenant_id=exam.tenant_id,
        exam_id=exam.id,
        item_no=item_no,
        prompt_bn=prompt_bn,
        prompt_en=prompt_en,
        max_marks=max_marks,
    )
    session.add(item)
    session.flush()
    _recalculate_total(session, exam)
    return item


def _recalculate_total(session: Session, exam: Exam) -> None:
    total = session.scalar(
        select(func.coalesce(func.sum(ExamItem.max_marks), 0)).where(ExamItem.exam_id == exam.id)
    )
    exam.total_marks = Decimal(total or 0)
    exam.updated_at = utcnow()


def get_item(session: Session, item_id: uuid.UUID) -> ExamItem:
    item = session.get(ExamItem, item_id)
    if item is None:
        raise DomainError("NOT_FOUND", detail="Question not found.")
    return item


def set_rubric(
    session: Session, *, exam: Exam, item: ExamItem, rubric: Rubric, created_by: uuid.UUID
) -> ItemRubric:
    """Save a new rubric version for an item. Blocked once the rubric is locked."""
    _require_draft(exam)
    report = validate_rubric(rubric, item.max_marks)
    if not report.lockable:
        raise RubricRejected(
            tuple(
                {"code": issue.code, "path": issue.path, "message": issue.message}
                for issue in report.errors
            )
        )
    next_version = (
        session.scalar(
            select(func.coalesce(func.max(ItemRubric.version), 0)).where(
                ItemRubric.item_id == item.id
            )
        )
        or 0
    ) + 1
    stored = ItemRubric(
        tenant_id=exam.tenant_id,
        exam_id=exam.id,
        item_id=item.id,
        version=next_version,
        payload=rubric.model_copy(update={"version": next_version}).model_dump(mode="json"),
        ai_eligible=report.ai_eligible,
        created_by=created_by,
    )
    session.add(stored)
    session.flush()
    return stored


def latest_rubric(session: Session, item_id: uuid.UUID) -> ItemRubric | None:
    return session.scalar(
        select(ItemRubric)
        .where(ItemRubric.item_id == item_id)
        .order_by(ItemRubric.version.desc())
        .limit(1)
    )


def lock_rubrics(session: Session, exam: Exam) -> Exam:
    """Freeze every item's latest rubric and move the exam to ``rubric_locked``.

    Every item must have a rubric that passes validation; the engine guard refuses
    the transition otherwise.
    """
    items = list(session.scalars(select(ExamItem).where(ExamItem.exam_id == exam.id)))
    if not items:
        raise DomainError("CONFLICT", detail="Add at least one question before locking.")

    now = utcnow()
    missing: list[int] = []
    to_lock: list[ItemRubric] = []
    for item in items:
        rubric_row = latest_rubric(session, item.id)
        if rubric_row is None:
            missing.append(item.item_no)
            continue
        report = validate_rubric(Rubric.model_validate(rubric_row.payload), item.max_marks)
        if not report.lockable:
            missing.append(item.item_no)
            continue
        to_lock.append(rubric_row)

    try:
        exam.state = transition(
            ExamState(exam.state),
            ExamState.RUBRIC_LOCKED,
            rubric_validation_passed=not missing,
        ).value
    except EngineError as exc:
        error = _conflict(exc)
        if missing:
            raise DomainError(
                "CONFLICT",
                detail="Every question needs a valid rubric before locking.",
                extra={"items_without_valid_rubric": sorted(missing)},
            ) from exc
        raise error from exc

    for rubric_row in to_lock:
        rubric_row.locked_at = now
    exam.rubric_locked_at = now
    exam.updated_at = now
    return exam


# --------------------------------------------------------------------------- capture


def add_candidate(session: Session, *, exam: Exam, roll: str, name: str) -> ExamCandidate:
    candidate = ExamCandidate(tenant_id=exam.tenant_id, exam_id=exam.id, roll=roll, name=name)
    session.add(candidate)
    session.flush()
    return candidate


def _open_capture(exam: Exam) -> None:
    """Move ``rubric_locked -> capturing`` on the first submitted answer."""
    if exam.state == ExamState.RUBRIC_LOCKED.value:
        exam.state = transition(ExamState.RUBRIC_LOCKED, ExamState.CAPTURING).value
        exam.updated_at = utcnow()


def submit_answer(
    session: Session,
    *,
    exam: Exam,
    candidate: ExamCandidate,
    item: ExamItem,
    answer_text: str,
) -> ItemResult:
    """Record one captured answer, creating the candidate's script on first use."""
    if exam.state not in (ExamState.RUBRIC_LOCKED.value, ExamState.CAPTURING.value):
        raise DomainError(
            "CONFLICT",
            detail="Answers can only be captured after the rubric is locked.",
            extra={"from_state": exam.state},
        )
    _open_capture(exam)

    script = session.scalar(
        select(Script).where(Script.exam_id == exam.id, Script.candidate_id == candidate.id)
    )
    if script is None:
        script = Script(tenant_id=exam.tenant_id, exam_id=exam.id, candidate_id=candidate.id)
        session.add(script)
        session.flush()

    result = session.scalar(
        select(ItemResult).where(ItemResult.script_id == script.id, ItemResult.item_id == item.id)
    )
    if result is None:
        result = ItemResult(
            tenant_id=exam.tenant_id,
            script_id=script.id,
            item_id=item.id,
            state=ItemState.PENDING.value,
        )
        session.add(result)
    elif result.state not in (ItemState.PENDING.value, ItemState.UNMAPPED.value):
        raise DomainError(
            "CONFLICT",
            detail="This answer has already been processed.",
            extra={"from_state": result.state},
        )
    result.answer_text = answer_text
    result.updated_at = utcnow()
    session.flush()
    return result


# --------------------------------------------------------------------------- evaluation


def evaluate_script(
    session: Session, provider: MarkingProvider, script: Script
) -> list[ItemResult]:
    """Run the provider over every pending answer on a script.

    An item whose rubric is not AI-eligible, or whose provider call fails, goes to a
    manual state instead of being guessed at.
    """
    exam = get_exam(session, script.exam_id)
    if exam.state == ExamState.CAPTURING.value:
        exam.state = transition(ExamState.CAPTURING, ExamState.PROCESSING).value
        exam.updated_at = utcnow()

    results = list(session.scalars(select(ItemResult).where(ItemResult.script_id == script.id)))
    for result in results:
        if result.state != ItemState.PENDING.value:
            continue
        _evaluate_one(session, provider, exam, result)

    _advance_to_reviewing(exam)
    return results


def _evaluate_one(
    session: Session, provider: MarkingProvider, exam: Exam, result: ItemResult
) -> None:
    item = get_item(session, result.item_id)
    rubric_row = latest_rubric(session, item.id)

    result.state = transition(ItemState.PENDING, ItemState.PROCESSING).value
    if rubric_row is None or not rubric_row.ai_eligible:
        # No AI for this item by design: the teacher marks it from the evidence.
        result.state = transition(ItemState.PROCESSING, ItemState.EVIDENCE_ONLY).value
        result.updated_at = utcnow()
        return

    rubric = Rubric.model_validate(rubric_row.payload)
    try:
        suggestion = provider.suggest(
            AnswerContext(
                item_id=str(item.id),
                prompt=item.prompt_en or item.prompt_bn,
                max_marks=item.max_marks,
                answer_text=result.answer_text,
                rubric=rubric,
            )
        )
    except ProviderError:
        result.state = transition(ItemState.PROCESSING, ItemState.FAILED).value
        result.state = transition(ItemState.FAILED, ItemState.MANUAL_READY).value
        result.updated_at = utcnow()
        return

    provisional = score_item(rubric, suggestion.decisions, item_max=item.max_marks)
    result.rubric_version = rubric_row.version
    result.ai_suggestion = {
        "decisions": [d.model_dump(mode="json") for d in suggestion.decisions],
        "rationale": suggestion.rationale,
        "evidence": list(suggestion.evidence),
        "prompt_version": suggestion.prompt_version,
        "provisional_score": provisional.model_dump(mode="json"),
    }
    result.ai_confidence = suggestion.confidence
    result.ai_model = suggestion.model
    # Suggested, never scored: `total` stays NULL until a teacher decides.
    result.state = transition(ItemState.PROCESSING, ItemState.SUGGESTED).value
    result.updated_at = utcnow()


#: How an exam reaches ``reviewing`` from where it is. An exam marked without AI
#: (FR-REV-10) still passes through ``processing``, which is what the state machine
#: models — going straight from ``capturing`` needs rolling mode, and pretending
#: otherwise would bend the machine rather than use it.
_PATH_TO_REVIEWING: Mapping[ExamState, tuple[ExamState, ...]] = MappingProxyType(
    {
        ExamState.CAPTURING: (ExamState.PROCESSING, ExamState.REVIEWING),
        ExamState.PROCESSING: (ExamState.REVIEWING,),
    }
)


def _advance_to_reviewing(exam: Exam) -> None:
    path = _PATH_TO_REVIEWING.get(ExamState(exam.state))
    if path is None:
        return
    state = ExamState(exam.state)
    for target in path:
        state = transition(state, target)
    exam.state = state.value
    exam.updated_at = utcnow()


# --------------------------------------------------------------------------- review


def review_item(
    session: Session,
    *,
    result: ItemResult,
    decisions: Sequence[CriterionDecision],
    deductions_applied: Sequence[str] = (),
    total_override: TotalOverride | None = None,
    decided_by: uuid.UUID,
    accepted_ai: bool,
) -> ItemResult:
    """Apply a teacher's decision and compute the mark with the scoring engine.

    ``accepted_ai`` distinguishes confirming the suggestion unchanged (``confirmed``)
    from changing it (``edited``); both mean the mark is teacher-decided.
    """
    item = get_item(session, result.item_id)
    rubric_row = latest_rubric(session, item.id)
    if rubric_row is None:
        raise DomainError("CONFLICT", detail="This question has no rubric.")

    rubric = Rubric.model_validate(rubric_row.payload)
    try:
        score: ItemScore = score_item(
            rubric,
            decisions,
            deductions_applied,
            total_override,
            item_max=item.max_marks,
        )
    except EngineError as exc:
        raise DomainError("VALIDATION_FAILED", detail=str(exc)) from exc

    state = _ready_to_mark(result)
    target = ItemState.CONFIRMED if accepted_ai and total_override is None else ItemState.EDITED
    try:
        result.state = transition(state, target).value
    except EngineError as exc:
        raise _conflict(exc) from exc

    now = utcnow()
    result.rubric_version = rubric_row.version
    result.score = score.model_dump(mode="json")
    result.total = score.total
    result.decided_by = decided_by
    result.decided_at = now
    result.updated_at = now
    _refresh_script_total(session, result.script_id)
    return result


def _ready_to_mark(result: ItemResult) -> ItemState:
    """Move an item the AI never touched into ``manual_ready`` first (FR-REV-10).

    An item sits at ``pending`` when no provider ran — AI is off for the cell, the
    teacher chose manual mode, or the student has no CT-2 consent. Marking must
    still work: the teacher decides every mark and the AI is optional (PP-1). The
    state machine already has the edge; nothing was taking it.
    """
    state = ItemState(result.state)
    if state is not ItemState.PENDING:
        return state
    result.state = transition(state, ItemState.MANUAL_READY).value
    return ItemState.MANUAL_READY


def _refresh_script_total(session: Session, script_id: uuid.UUID) -> None:
    script = session.get(Script, script_id)
    if script is None:
        return
    total = session.scalar(
        select(func.sum(ItemResult.total)).where(ItemResult.script_id == script_id)
    )
    script.total_marks = Decimal(total) if total is not None else None
    script.updated_at = utcnow()


# --------------------------------------------------------------------------- locking


def _undecided_items(session: Session, exam_id: uuid.UUID) -> int:
    return (
        session.scalar(
            select(func.count())
            .select_from(ItemResult)
            .join(Script, Script.id == ItemResult.script_id)
            .where(Script.exam_id == exam_id, ItemResult.state.notin_(DECIDED_STATES))
        )
        or 0
    )


def lock_marks(session: Session, exam: Exam) -> Exam:
    """Move the exam to ``marks_locked`` once every item is decided.

    Locking, not the first decision, is what ends capture. Teachers mark while the
    last bundles are still arriving, so an exam that was marked without ever being
    evaluated is walked through ``processing`` and ``reviewing`` here instead.
    """
    undecided = _undecided_items(session, exam.id)
    _advance_to_reviewing(exam)
    try:
        state = transition(
            ExamState(exam.state), ExamState.MODERATION, all_items_decided=undecided == 0
        )
        state = transition(
            state, ExamState.MARKS_LOCKED, completeness_ok=True, moderation_done=True
        )
    except EngineError as exc:
        if undecided:
            raise DomainError(
                "CONFLICT",
                detail="Every answer must be decided before marks can be locked.",
                extra={"undecided_items": undecided},
            ) from exc
        raise _conflict(exc) from exc

    now = utcnow()
    for result in session.scalars(
        select(ItemResult)
        .join(Script, Script.id == ItemResult.script_id)
        .where(Script.exam_id == exam.id)
    ):
        result.state = transition(ItemState(result.state), ItemState.LOCKED).value
        result.locked_at = now
        result.updated_at = now

    exam.state = state.value
    exam.marks_locked_at = now
    exam.updated_at = now
    return exam
