"""Exam results from confirmed item marks (FR-RES-01/02/03).

The arithmetic lives in ``khata.engines.results`` and none of it is repeated here.
This module's only job is to describe the exam to that engine and read the answer
back — which is the point of keeping the engine pure: the rules that decide a
student's grade are tested without a database anywhere near them.

The exam model is still flat (one mark per question, no sub-parts or components:
FR-EXM-02 is partial), so a paper maps to a single CQ component whose questions
each have one sub-part. When the structure grows, only ``paper_structure`` changes.

Results are available before marks are locked, marked ``provisional``, because a
coordinator needs to watch the total form. A provisional total counts only decided
items and says how many are still outstanding, so it can never be mistaken for the
final one.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from khata.core.errors import DomainError
from khata.engines.results.compute import SubjectMarks, SubjectResult, compute_subject_result
from khata.engines.results.structure import (
    ComponentKind,
    ComponentMarks,
    ComponentSpec,
    PaperStructure,
    QuestionSpec,
    SubPartMark,
    SubPartSpec,
)
from khata.modules.assessment.models import Exam, ExamCandidate, ExamItem, ItemResult, Script

COMPONENT_CODE = "cq"


@dataclass(frozen=True, slots=True)
class CandidateResult:
    candidate: ExamCandidate
    script_id: uuid.UUID | None
    result: SubjectResult
    pending_items: int


@dataclass(frozen=True, slots=True)
class ExamResults:
    exam: Exam
    structure: PaperStructure
    candidates: tuple[CandidateResult, ...]

    @property
    def provisional(self) -> bool:
        return self.exam.marks_locked_at is None


def compute_exam_results(session: Session, exam: Exam) -> ExamResults:
    items = _items(session, exam.id)
    structure = paper_structure(exam, items)
    candidates = session.scalars(
        select(ExamCandidate).where(ExamCandidate.exam_id == exam.id).order_by(ExamCandidate.roll)
    ).all()
    scripts = {
        script.candidate_id: script
        for script in session.scalars(select(Script).where(Script.exam_id == exam.id))
    }
    return ExamResults(
        exam=exam,
        structure=structure,
        candidates=tuple(
            _candidate_result(session, structure, items, candidate, scripts.get(candidate.id))
            for candidate in candidates
        ),
    )


def paper_structure(exam: Exam, items: list[ExamItem]) -> PaperStructure:
    questions = tuple(
        QuestionSpec(
            id=str(item.id),
            sub_parts=(SubPartSpec(id=str(item.id), max_marks=item.max_marks),),
        )
        for item in items
    )
    total = sum((item.max_marks for item in items), Decimal(0))
    return PaperStructure(
        subject_id=exam.subject_code,
        components=(
            ComponentSpec(
                code=COMPONENT_CODE,
                kind=ComponentKind.CQ,
                max_marks=total,
                questions=questions,
            ),
        ),
    )


def _items(session: Session, exam_id: uuid.UUID) -> list[ExamItem]:
    items = list(
        session.scalars(
            select(ExamItem).where(ExamItem.exam_id == exam_id).order_by(ExamItem.item_no)
        )
    )
    if not items:
        raise DomainError("EXAM_HAS_NO_ITEMS")
    return items


def _candidate_result(
    session: Session,
    structure: PaperStructure,
    items: list[ExamItem],
    candidate: ExamCandidate,
    script: Script | None,
) -> CandidateResult:
    decided = _decided_marks(session, script)
    sub_parts = tuple(
        SubPartMark(
            sub_part_id=str(item.id),
            marks=decided.get(item.id, Decimal(0)),
            # An item nobody has decided yet is not an attempt. It scores nothing
            # and is counted in ``pending_items`` instead of being hidden.
            attempted=item.id in decided,
        )
        for item in items
    )
    marks = SubjectMarks(
        subject_id=structure.subject_id,
        components=(ComponentMarks(component_code=COMPONENT_CODE, sub_parts=sub_parts),),
    )
    return CandidateResult(
        candidate=candidate,
        script_id=script.id if script else None,
        result=compute_subject_result(structure, marks),
        pending_items=len(items) - len(decided),
    )


def _decided_marks(session: Session, script: Script | None) -> dict[uuid.UUID, Decimal]:
    if script is None:
        return {}
    rows = session.scalars(
        select(ItemResult).where(ItemResult.script_id == script.id, ItemResult.total.isnot(None))
    )
    return {row.item_id: row.total for row in rows if row.total is not None}
