"""Aggregate one component's marks (FR-RES-01, FR-RES-06).

``aggregate_component`` is the only place choice rules are applied. It validates
the marks against the structure first — bounds, missing sub-parts, unknown ids —
because a result computed from marks that do not fit the paper is worse than no
result at all (FR-RES-06).
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from decimal import Decimal

from khata.engines.base import FrozenModel
from khata.engines.errors import ResultInputError
from khata.engines.marks import RoundingMode, round_exact
from khata.engines.results.structure import (
    ChoicePolicy,
    ComponentKind,
    ComponentMarks,
    ComponentSpec,
    QuestionSpec,
    SubPartMark,
)

ZERO = Decimal(0)
PERCENT_QUANTUM = Decimal("0.01")
CHOICE_RULE = "choice_rule"


class SubPartResult(FrozenModel):
    sub_part_id: str
    max_marks: Decimal
    marks: Decimal
    attempted: bool


class QuestionResult(FrozenModel):
    question_id: str
    max_marks: Decimal
    marks: Decimal
    attempted: bool
    counted: bool
    excluded_reason: str | None = None
    sub_parts: tuple[SubPartResult, ...] = ()


class ComponentResult(FrozenModel):
    code: str
    kind: ComponentKind
    max_marks: Decimal
    marks: Decimal
    percent: Decimal
    pass_mark: Decimal
    is_pass: bool
    absent: bool
    questions: tuple[QuestionResult, ...] = ()
    counted_question_ids: tuple[str, ...] = ()


def aggregate_component(spec: ComponentSpec, marks: ComponentMarks) -> ComponentResult:
    if marks.component_code != spec.code:
        raise ResultInputError(
            f"marks are for component {marks.component_code!r}, not {spec.code!r}"
        )
    if marks.absent:
        return _result(spec, ZERO, absent=True)
    if spec.is_marked_in_platform:
        return _aggregate_questions(spec, marks.sub_parts)
    return _aggregate_imported(spec, marks)


def _aggregate_imported(spec: ComponentSpec, marks: ComponentMarks) -> ComponentResult:
    if marks.sub_parts:
        raise ResultInputError(
            f"component {spec.code!r} is not marked in the platform; "
            "supply a single mark, not sub-parts"
        )
    if marks.marks is None:
        raise ResultInputError(f"component {spec.code!r} has no mark and is not marked absent")
    if marks.marks > spec.max_marks:
        raise ResultInputError(
            f"component {spec.code!r}: {marks.marks} exceeds the maximum {spec.max_marks}"
        )
    return _result(spec, marks.marks)


def _aggregate_questions(spec: ComponentSpec, sub_parts: Sequence[SubPartMark]) -> ComponentResult:
    by_id = _marks_by_id(spec, sub_parts)
    questions = tuple(_question_result(q, by_id) for q in spec.questions)
    counted = _select(questions, spec)
    counted_ids = frozenset(q.question_id for q in counted)
    questions = tuple(
        q.model_copy(
            update={
                "counted": q.question_id in counted_ids,
                "excluded_reason": None if q.question_id in counted_ids else CHOICE_RULE,
            }
        )
        for q in questions
    )
    total = sum((q.marks for q in questions if q.counted), ZERO)
    return _result(
        spec,
        total,
        questions=questions,
        counted_question_ids=tuple(q.question_id for q in counted),
    )


def _marks_by_id(
    spec: ComponentSpec, sub_parts: Sequence[SubPartMark]
) -> Mapping[str, SubPartMark]:
    by_id: dict[str, SubPartMark] = {}
    for mark in sub_parts:
        if mark.sub_part_id in by_id:
            raise ResultInputError(f"sub-part {mark.sub_part_id!r} is marked twice")
        by_id[mark.sub_part_id] = mark
    expected = {p.id: p for q in spec.questions for p in q.sub_parts}
    unknown = sorted(set(by_id) - set(expected))
    if unknown:
        raise ResultInputError(f"component {spec.code!r}: unknown sub-parts {', '.join(unknown)}")
    missing = sorted(set(expected) - set(by_id))
    if missing:
        raise ResultInputError(f"component {spec.code!r}: missing marks for {', '.join(missing)}")
    for part_id, part in expected.items():
        awarded = by_id[part_id].marks
        if awarded > part.max_marks:
            raise ResultInputError(
                f"sub-part {part_id!r}: {awarded} exceeds the maximum {part.max_marks}"
            )
    return by_id


def _question_result(question: QuestionSpec, by_id: Mapping[str, SubPartMark]) -> QuestionResult:
    parts = tuple(
        SubPartResult(
            sub_part_id=spec.id,
            max_marks=spec.max_marks,
            marks=by_id[spec.id].marks,
            attempted=by_id[spec.id].attempted,
        )
        for spec in question.sub_parts
    )
    return QuestionResult(
        question_id=question.id,
        max_marks=question.max_marks,
        marks=sum((p.marks for p in parts), ZERO),
        attempted=any(p.attempted for p in parts),
        counted=False,
        sub_parts=parts,
    )


def _select(questions: Sequence[QuestionResult], spec: ComponentSpec) -> tuple[QuestionResult, ...]:
    """Which attempted questions count, in script order."""
    attempted = [q for q in questions if q.attempted]
    if spec.choice is None:
        return tuple(attempted)
    if spec.choice.policy is ChoicePolicy.BEST:
        order = {q.question_id: i for i, q in enumerate(questions)}
        chosen = sorted(attempted, key=lambda q: (-q.marks, order[q.question_id]))
        keep = frozenset(q.question_id for q in chosen[: spec.choice.answer])
        return tuple(q for q in questions if q.question_id in keep)
    return tuple(attempted[: spec.choice.answer])


def _result(
    spec: ComponentSpec,
    marks: Decimal,
    *,
    absent: bool = False,
    questions: tuple[QuestionResult, ...] = (),
    counted_question_ids: tuple[str, ...] = (),
) -> ComponentResult:
    exact = ZERO if absent else marks * Decimal(100) / spec.max_marks
    percent = round_exact(exact, PERCENT_QUANTUM, RoundingMode.HALF_UP)
    return ComponentResult(
        code=spec.code,
        kind=spec.kind,
        max_marks=spec.max_marks,
        marks=marks,
        percent=percent,
        pass_mark=spec.pass_mark,
        is_pass=not absent and marks >= spec.pass_mark,
        absent=absent,
        questions=questions,
        counted_question_ids=counted_question_ids,
    )
