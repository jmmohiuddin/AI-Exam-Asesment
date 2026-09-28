"""Subject and overall results (FR-RES-01/02/03/06)."""

from __future__ import annotations

from decimal import Decimal

import pytest

from khata.engines.errors import ResultInputError
from khata.engines.marks import RoundingMode
from khata.engines.results.compute import (
    ResultPolicy,
    SubjectMarks,
    compute_overall_result,
    compute_subject_result,
)
from khata.engines.results.structure import (
    ComponentKind,
    ComponentMarks,
    ComponentSpec,
    PaperStructure,
    QuestionSpec,
    SubPartMark,
    SubPartSpec,
)

D = Decimal


def flat_component(code: str, kind: ComponentKind, total: int) -> ComponentSpec:
    """One question, one sub-part: the simplest way to drive a marked component."""
    return ComponentSpec(
        code=code,
        kind=kind,
        max_marks=D(total),
        questions=(
            QuestionSpec(
                id=f"{code}-q1", sub_parts=(SubPartSpec(id=f"{code}-q1.a", max_marks=D(total)),)
            ),
        ),
    )


def physics_paper() -> PaperStructure:
    """Physics: CQ 50 marked here, MCQ 25 and practical 25 imported. Total 100."""
    return PaperStructure(
        subject_id="physics",
        components=(
            flat_component("cq", ComponentKind.CQ, 50),
            ComponentSpec(code="mcq", kind=ComponentKind.MCQ, max_marks=D(25)),
            ComponentSpec(code="practical", kind=ComponentKind.PRACTICAL, max_marks=D(25)),
        ),
    )


def marks(cq: int | None, mcq: int | None, practical: int | None) -> SubjectMarks:
    components = []
    if cq is not None:
        components.append(
            ComponentMarks(
                component_code="cq", sub_parts=(SubPartMark(sub_part_id="cq-q1.a", marks=D(cq)),)
            )
        )
    else:
        components.append(ComponentMarks(component_code="cq", absent=True))
    for code, value in (("mcq", mcq), ("practical", practical)):
        components.append(
            ComponentMarks(
                component_code=code, marks=None if value is None else D(value), absent=value is None
            )
        )
    return SubjectMarks(subject_id="physics", components=tuple(components))


class TestSubjectResult:
    def test_components_roll_up_into_a_subject_total(self) -> None:
        result = compute_subject_result(physics_paper(), marks(40, 20, 20))
        assert result.marks == D(80)
        assert result.max_marks == D(100)
        assert result.percent == D(80)
        assert result.letter == "A+"
        assert result.grade_point == D("5.0")
        assert result.is_pass

    def test_a_failed_component_fails_the_subject_even_when_the_total_passes(self) -> None:
        # CQ 15/50 is below 33%; total 60 is well above.
        result = compute_subject_result(physics_paper(), marks(15, 25, 20))
        assert result.marks == D(60)
        assert not result.is_pass
        assert result.letter == "F"
        assert result.grade_point == D(0)
        assert result.failed_components == ("cq",)

    def test_a_passing_total_with_all_components_passed_grades_normally(self) -> None:
        result = compute_subject_result(physics_paper(), marks(17, 9, 9))
        assert result.marks == D(35)
        assert result.is_pass
        assert result.letter == "D"

    def test_a_total_below_the_pass_mark_fails_even_with_components_passed(self) -> None:
        paper = PaperStructure(
            subject_id="physics",
            components=(
                ComponentSpec(
                    code="a", kind=ComponentKind.OTHER, max_marks=D(100), pass_percent=D(10)
                ),
            ),
        )
        subject_marks = SubjectMarks(
            subject_id="physics",
            components=(ComponentMarks(component_code="a", marks=D(20)),),
        )
        result = compute_subject_result(paper, subject_marks)
        assert result.failed_components == ()
        assert not result.is_pass
        assert result.letter == "F"

    def test_absence_in_any_component_makes_the_subject_absent(self) -> None:
        result = compute_subject_result(physics_paper(), marks(40, None, 20))
        assert result.absent
        assert not result.is_pass
        assert result.letter == "F"
        assert result.grade_point == D(0)
        assert result.absent_components == ("mcq",)

    def test_marks_for_an_unknown_component_are_rejected(self) -> None:
        subject_marks = SubjectMarks(
            subject_id="physics",
            components=(ComponentMarks(component_code="ghost", marks=D(1)),),
        )
        with pytest.raises(ResultInputError, match="ghost"):
            compute_subject_result(physics_paper(), subject_marks)

    def test_a_missing_component_is_rejected(self) -> None:
        subject_marks = SubjectMarks(
            subject_id="physics",
            components=(ComponentMarks(component_code="mcq", marks=D(20)),),
        )
        with pytest.raises(ResultInputError, match="cq"):
            compute_subject_result(physics_paper(), subject_marks)

    def test_marks_for_the_wrong_subject_are_rejected(self) -> None:
        subject_marks = marks(40, 20, 20).model_copy(update={"subject_id": "maths"})
        with pytest.raises(ResultInputError, match="maths"):
            compute_subject_result(physics_paper(), subject_marks)

    def test_the_subject_total_rounds_half_up_by_default(self) -> None:
        paper = PaperStructure(
            subject_id="physics",
            components=(flat_component("cq", ComponentKind.CQ, 50),),
        )
        subject_marks = SubjectMarks(
            subject_id="physics",
            components=(
                ComponentMarks(
                    component_code="cq",
                    sub_parts=(SubPartMark(sub_part_id="cq-q1.a", marks=D("40.5")),),
                ),
            ),
        )
        assert compute_subject_result(paper, subject_marks).marks == D(41)

    def test_the_rounding_rule_is_configurable(self) -> None:
        paper = PaperStructure(
            subject_id="physics",
            components=(flat_component("cq", ComponentKind.CQ, 50),),
        )
        subject_marks = SubjectMarks(
            subject_id="physics",
            components=(
                ComponentMarks(
                    component_code="cq",
                    sub_parts=(SubPartMark(sub_part_id="cq-q1.a", marks=D("40.5")),),
                ),
            ),
        )
        policy = ResultPolicy(subject_rounding=RoundingMode.DOWN)
        assert compute_subject_result(paper, subject_marks, policy=policy).marks == D(40)

    def test_the_grade_is_taken_from_the_rounded_total(self) -> None:
        # 39.5/50 = 79% before rounding, 40/50 = 80% after -> A+
        paper = PaperStructure(
            subject_id="physics",
            components=(flat_component("cq", ComponentKind.CQ, 50),),
        )
        subject_marks = SubjectMarks(
            subject_id="physics",
            components=(
                ComponentMarks(
                    component_code="cq",
                    sub_parts=(SubPartMark(sub_part_id="cq-q1.a", marks=D("39.5")),),
                ),
            ),
        )
        assert compute_subject_result(paper, subject_marks).letter == "A+"


class TestOverallResult:
    def subject(self, sid: str, cq: int, *, fourth: bool = False) -> object:
        paper = PaperStructure(
            subject_id=sid, components=(flat_component("cq", ComponentKind.CQ, 100),)
        )
        subject_marks = SubjectMarks(
            subject_id=sid,
            components=(
                ComponentMarks(
                    component_code="cq",
                    sub_parts=(SubPartMark(sub_part_id="cq-q1.a", marks=D(cq)),),
                ),
            ),
        )
        return compute_subject_result(paper, subject_marks, is_fourth_subject=fourth)

    def test_gpa_across_subjects(self) -> None:
        results = [self.subject("a", 85), self.subject("b", 75), self.subject("c", 65)]
        overall = compute_overall_result(results)  # type: ignore[arg-type]
        assert overall.gpa == D("4.17")
        assert overall.is_pass

    def test_the_fourth_subject_lifts_the_gpa_by_its_excess_over_two(self) -> None:
        results = [self.subject(f"m{i}", 85) for i in range(4)]
        results.append(self.subject("opt", 85, fourth=True))
        overall = compute_overall_result(results)  # type: ignore[arg-type]
        assert overall.gpa == D("5.00")

    def test_one_failed_subject_fails_the_whole_result(self) -> None:
        results = [self.subject("a", 85), self.subject("b", 20)]
        overall = compute_overall_result(results)  # type: ignore[arg-type]
        assert not overall.is_pass
        assert overall.gpa == D("0.00")
        assert overall.failed_subjects == ("b",)

    def test_totals_are_carried_for_the_ledger(self) -> None:
        results = [self.subject("a", 85), self.subject("b", 75)]
        overall = compute_overall_result(results)  # type: ignore[arg-type]
        assert overall.marks == D(160)
        assert overall.max_marks == D(200)
