"""Assessment endpoints: authoring, capture, evaluation, review and locking."""

from __future__ import annotations

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Request, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from khata.core.errors import DomainError
from khata.engines.rubric import Rubric
from khata.modules.aigateway.provider import (
    LOW_CONFIDENCE_THRESHOLD,
    MarkingProvider,
)
from khata.modules.assessment import service
from khata.modules.assessment.models import ExamCandidate, ExamItem, ItemResult, Script
from khata.modules.assessment.schemas import (
    AnswerSubmit,
    CandidateCreate,
    CandidateOut,
    ExamCreate,
    ExamOut,
    ItemCreate,
    ItemOut,
    ItemResultOut,
    ReviewCard,
    ReviewDecision,
    ReviewQueue,
    RubricOut,
    RubricPut,
    ScriptOut,
)
from khata.modules.authz.deps import (
    CAN_AUTHOR_EXAM,
    CAN_MARK,
    CAN_PUBLISH,
    Principal,
    TenantSession,
)

router = APIRouter(tags=["assessment"])

AuthorDep = Annotated[Principal, Depends(CAN_AUTHOR_EXAM)]
MarkerDep = Annotated[Principal, Depends(CAN_MARK)]
PublisherDep = Annotated[Principal, Depends(CAN_PUBLISH)]


def get_provider(request: Request) -> MarkingProvider:
    provider: MarkingProvider = request.app.state.marking_provider
    return provider


ProviderDep = Annotated[MarkingProvider, Depends(get_provider)]


def _rubric_or_400(payload: RubricPut) -> Rubric:
    return payload.rubric


# --------------------------------------------------------------------------- authoring


@router.post("/exams", response_model=ExamOut, status_code=status.HTTP_201_CREATED)
def create_exam(payload: ExamCreate, principal: AuthorDep, session: TenantSession) -> ExamOut:
    exam = service.create_exam(
        session,
        tenant_id=principal.require_tenant(),
        school_id=payload.school_id,
        name=payload.name,
        subject_code=payload.subject_code,
        class_level=payload.class_level,
        created_by=principal.user_id,
    )
    return ExamOut.model_validate(exam, from_attributes=True)


@router.get("/exams/{exam_id}", response_model=ExamOut)
def read_exam(exam_id: uuid.UUID, principal: MarkerDep, session: TenantSession) -> ExamOut:
    return ExamOut.model_validate(service.get_exam(session, exam_id), from_attributes=True)


@router.post("/exams/{exam_id}/items", response_model=ItemOut, status_code=status.HTTP_201_CREATED)
def add_item(
    exam_id: uuid.UUID, payload: ItemCreate, principal: AuthorDep, session: TenantSession
) -> ItemOut:
    exam = service.get_exam(session, exam_id)
    item = service.add_item(
        session,
        exam=exam,
        item_no=payload.item_no,
        max_marks=payload.max_marks,
        prompt_bn=payload.prompt_bn,
        prompt_en=payload.prompt_en,
    )
    return ItemOut.model_validate(item, from_attributes=True)


@router.put("/exams/{exam_id}/items/{item_id}/rubric", response_model=RubricOut)
def put_rubric(
    exam_id: uuid.UUID,
    item_id: uuid.UUID,
    payload: RubricPut,
    principal: AuthorDep,
    session: TenantSession,
) -> RubricOut:
    exam = service.get_exam(session, exam_id)
    item = service.get_item(session, item_id)
    if item.exam_id != exam.id:
        raise DomainError("NOT_FOUND", detail="Question not found on this exam.")
    try:
        stored = service.set_rubric(
            session, exam=exam, item=item, rubric=payload.rubric, created_by=principal.user_id
        )
    except service.RubricRejected as rejected:
        raise rejected.as_error() from rejected
    return RubricOut.model_validate(stored, from_attributes=True)


@router.post("/exams/{exam_id}/lock-rubric", response_model=ExamOut)
def lock_rubric(exam_id: uuid.UUID, principal: AuthorDep, session: TenantSession) -> ExamOut:
    exam = service.lock_rubrics(session, service.get_exam(session, exam_id))
    return ExamOut.model_validate(exam, from_attributes=True)


# --------------------------------------------------------------------------- capture


@router.post(
    "/exams/{exam_id}/candidates",
    response_model=CandidateOut,
    status_code=status.HTTP_201_CREATED,
)
def add_candidate(
    exam_id: uuid.UUID, payload: CandidateCreate, principal: AuthorDep, session: TenantSession
) -> CandidateOut:
    exam = service.get_exam(session, exam_id)
    candidate = service.add_candidate(session, exam=exam, roll=payload.roll, name=payload.name)
    return CandidateOut.model_validate(candidate, from_attributes=True)


@router.post(
    "/exams/{exam_id}/answers", response_model=ItemResultOut, status_code=status.HTTP_201_CREATED
)
def submit_answer(
    exam_id: uuid.UUID, payload: AnswerSubmit, principal: MarkerDep, session: TenantSession
) -> ItemResultOut:
    exam = service.get_exam(session, exam_id)
    candidate = session.get(ExamCandidate, payload.candidate_id)
    item = session.get(ExamItem, payload.item_id)
    if candidate is None or candidate.exam_id != exam.id:
        raise DomainError("NOT_FOUND", detail="Candidate not found on this exam.")
    if item is None or item.exam_id != exam.id:
        raise DomainError("NOT_FOUND", detail="Question not found on this exam.")
    result = service.submit_answer(
        session, exam=exam, candidate=candidate, item=item, answer_text=payload.answer_text
    )
    return ItemResultOut.model_validate(result, from_attributes=True)


def _get_script(session: Session, script_id: uuid.UUID) -> Script:
    script = session.get(Script, script_id)
    if script is None:
        raise DomainError("NOT_FOUND", detail="Script not found.")
    return script


@router.get("/exams/{exam_id}/scripts", response_model=list[ScriptOut])
def list_scripts(
    exam_id: uuid.UUID, principal: MarkerDep, session: TenantSession
) -> list[ScriptOut]:
    service.get_exam(session, exam_id)
    scripts = session.scalars(
        select(Script).where(Script.exam_id == exam_id).order_by(Script.created_at)
    )
    return [ScriptOut.model_validate(s, from_attributes=True) for s in scripts]


# --------------------------------------------------------------------------- evaluation


@router.post("/scripts/{script_id}/evaluate", response_model=list[ItemResultOut])
def evaluate(
    script_id: uuid.UUID,
    principal: MarkerDep,
    session: TenantSession,
    provider: ProviderDep,
) -> list[ItemResultOut]:
    """Run the marking provider over the script. Suggestions only — never a final mark."""
    script = _get_script(session, script_id)
    results = service.evaluate_script(session, provider, script)
    return [ItemResultOut.model_validate(r, from_attributes=True) for r in results]


# --------------------------------------------------------------------------- review


def _review_card(session: Session, result: ItemResult) -> ReviewCard:
    item = service.get_item(session, result.item_id)
    rubric_row = service.latest_rubric(session, item.id)
    payload = rubric_row.payload if rubric_row else {}
    suggestion = result.ai_suggestion or {}
    confidence = result.ai_confidence
    return ReviewCard(
        result_id=result.id,
        item_id=item.id,
        item_no=item.item_no,
        prompt_bn=item.prompt_bn,
        prompt_en=item.prompt_en,
        max_marks=item.max_marks,
        state=result.state,
        student_answer=result.answer_text,
        model_answer=payload.get("model_answer"),
        rubric=payload,
        rubric_version=result.rubric_version,
        ai_model=result.ai_model,
        ai_confidence=confidence,
        ai_low_confidence=confidence is not None and confidence < LOW_CONFIDENCE_THRESHOLD,
        ai_rationale=suggestion.get("rationale"),
        ai_evidence=list(suggestion.get("evidence", [])),
        ai_decisions=list(suggestion.get("decisions", [])),
        suggested_score=suggestion.get("provisional_score"),
        teacher_score=result.score,
        total=result.total,
        decided_at=result.decided_at,
    )


@router.get("/scripts/{script_id}/review", response_model=ReviewQueue)
def review_queue(script_id: uuid.UUID, principal: MarkerDep, session: TenantSession) -> ReviewQueue:
    """Everything needed to mark one script, in one request."""
    script = _get_script(session, script_id)
    exam = service.get_exam(session, script.exam_id)
    candidate = session.get(ExamCandidate, script.candidate_id)
    if candidate is None:  # pragma: no cover - guaranteed by the foreign key
        raise DomainError("NOT_FOUND", detail="Candidate not found.")
    results = session.scalars(select(ItemResult).where(ItemResult.script_id == script.id)).all()
    cards = sorted(
        (_review_card(session, result) for result in results), key=lambda card: card.item_no
    )
    return ReviewQueue(
        script_id=script.id,
        candidate=CandidateOut.model_validate(candidate, from_attributes=True),
        exam_state=exam.state,
        script_total=script.total_marks,
        items=cards,
    )


@router.post("/item-results/{result_id}/review", response_model=ReviewCard)
def decide_item(
    result_id: uuid.UUID,
    payload: ReviewDecision,
    principal: MarkerDep,
    session: TenantSession,
) -> ReviewCard:
    result = session.get(ItemResult, result_id)
    if result is None:
        raise DomainError("NOT_FOUND", detail="Answer not found.")
    service.review_item(
        session,
        result=result,
        decisions=payload.decisions,
        deductions_applied=payload.deductions_applied,
        total_override=payload.total_override,
        decided_by=principal.user_id,
        accepted_ai=payload.accepted_ai,
    )
    session.flush()
    return _review_card(session, result)


# --------------------------------------------------------------------------- locking


@router.post("/exams/{exam_id}/lock-marks", response_model=ExamOut)
def lock_marks(exam_id: uuid.UUID, principal: PublisherDep, session: TenantSession) -> ExamOut:
    exam = service.lock_marks(session, service.get_exam(session, exam_id))
    return ExamOut.model_validate(exam, from_attributes=True)
