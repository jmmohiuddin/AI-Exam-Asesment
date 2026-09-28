"""Subject and overall results (FR-RES-01/02/03/06).

The chain is component -> subject -> student. Two rules decide pass/fail and they
are independent (FR-RES-02): **every component** must reach its own pass mark, and
the **subject total** must reach the scale's pass percentage. Failing either fails
the subject, and a failed subject grades as the bottom band, not as its raw
percentage — a student who scored 60% overall but failed the practical does not
get an A-.

Absence is not zero (FR-RES-06): an absent component makes the subject absent,
which fails the result without pretending a mark was earned.
"""

from __future__ import annotations

from collections.abc import Sequence
from decimal import Decimal

from pydantic import Field

from khata.engines.base import FrozenModel
from khata.engines.errors import ResultInputError
from khata.engines.marks import RoundingMode, round_exact
from khata.engines.results.aggregate import ComponentResult, aggregate_component
from khata.engines.results.grading import (
    NCTB_GRADE_SCALE,
    GpaResult,
    GradeScale,
    SubjectGrade,
    gpa,
    grade_for_percent,
)
from khata.engines.results.structure import ComponentMarks, PaperStructure

ZERO = Decimal(0)
#: Percentages are reported to two places. Decimal division of exact values yields
#: forms like ``8E+1``, which is 80 but not something a client should have to parse.
PERCENT_QUANTUM = Decimal("0.01")


class ResultPolicy(FrozenModel):
    """School-configurable rules (FR-RES-02/03; defaults are the NCTB ones)."""

    grade_scale: GradeScale = NCTB_GRADE_SCALE
    subject_rounding: RoundingMode = RoundingMode.HALF_UP
    subject_quantum: Decimal = Field(default=Decimal(1), gt=0, allow_inf_nan=False)


DEFAULT_POLICY = ResultPolicy()


class SubjectMarks(FrozenModel):
    subject_id: str = Field(min_length=1)
    components: tuple[ComponentMarks, ...] = Field(min_length=1)


class SubjectResult(FrozenModel):
    subject_id: str
    components: tuple[ComponentResult, ...]
    marks: Decimal
    max_marks: Decimal
    percent: Decimal
    letter: str
    grade_point: Decimal
    is_pass: bool
    absent: bool
    is_fourth_subject: bool
    failed_components: tuple[str, ...]
    absent_components: tuple[str, ...]


class OverallResult(FrozenModel):
    subjects: tuple[SubjectResult, ...]
    marks: Decimal
    max_marks: Decimal
    gpa: Decimal
    is_pass: bool
    failed_subjects: tuple[str, ...]
    absent_subjects: tuple[str, ...]


def compute_subject_result(
    structure: PaperStructure,
    marks: SubjectMarks,
    *,
    policy: ResultPolicy = DEFAULT_POLICY,
    is_fourth_subject: bool = False,
) -> SubjectResult:
    if marks.subject_id != structure.subject_id:
        raise ResultInputError(
            f"marks are for subject {marks.subject_id!r}, not {structure.subject_id!r}"
        )
    components = _aggregate_all(structure, marks)
    total = round_exact(
        sum((c.marks for c in components), ZERO),
        policy.subject_quantum,
        policy.subject_rounding,
    )
    percent = total * Decimal(100) / structure.max_marks
    failed = tuple(c.code for c in components if not c.is_pass and not c.absent)
    absent = tuple(c.code for c in components if c.absent)

    grade = grade_for_percent(percent, policy.grade_scale)
    is_pass = grade.is_pass and not failed and not absent
    if not is_pass:
        grade = grade_for_percent(ZERO, policy.grade_scale)

    return SubjectResult(
        subject_id=structure.subject_id,
        components=components,
        marks=total,
        max_marks=structure.max_marks,
        # Quantised only after grading, so rounding can never change the band.
        percent=round_exact(percent, PERCENT_QUANTUM, RoundingMode.HALF_UP),
        letter=grade.letter,
        grade_point=grade.grade_point,
        is_pass=is_pass,
        absent=bool(absent),
        is_fourth_subject=is_fourth_subject,
        failed_components=failed,
        absent_components=absent,
    )


def compute_overall_result(subjects: Sequence[SubjectResult]) -> OverallResult:
    result: GpaResult = gpa(
        SubjectGrade(
            subject_id=s.subject_id,
            letter=s.letter,
            grade_point=s.grade_point,
            is_pass=s.is_pass,
            is_fourth_subject=s.is_fourth_subject,
            is_absent=s.absent,
        )
        for s in subjects
    )
    return OverallResult(
        subjects=tuple(subjects),
        marks=sum((s.marks for s in subjects), ZERO),
        max_marks=sum((s.max_marks for s in subjects), ZERO),
        gpa=result.gpa,
        is_pass=result.is_pass,
        failed_subjects=result.failed_subjects,
        absent_subjects=result.absent_subjects,
    )


def _aggregate_all(structure: PaperStructure, marks: SubjectMarks) -> tuple[ComponentResult, ...]:
    by_code: dict[str, ComponentMarks] = {}
    for component in marks.components:
        if component.component_code in by_code:
            raise ResultInputError(f"component {component.component_code!r} is marked twice")
        by_code[component.component_code] = component
    expected = {c.code: c for c in structure.components}
    unknown = sorted(set(by_code) - set(expected))
    if unknown:
        raise ResultInputError(
            f"subject {structure.subject_id!r}: unknown components {', '.join(unknown)}"
        )
    missing = sorted(set(expected) - set(by_code))
    if missing:
        raise ResultInputError(
            f"subject {structure.subject_id!r}: missing marks for {', '.join(missing)}"
        )
    return tuple(aggregate_component(spec, by_code[code]) for code, spec in expected.items())
