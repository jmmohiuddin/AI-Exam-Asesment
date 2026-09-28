"""Sub-part -> question -> component aggregation and choice rules (FR-RES-01/06)."""

from __future__ import annotations

from decimal import Decimal
from typing import Any

import pytest
from pydantic import ValidationError

from khata.engines.errors import ResultInputError
from khata.engines.results.aggregate import aggregate_component
from khata.engines.results.structure import (
    ChoicePolicy,
    ChoiceRule,
    ComponentKind,
    ComponentMarks,
    ComponentSpec,
    QuestionSpec,
    SubPartMark,
    SubPartSpec,
)

D = Decimal


def question(qid: str, *parts: tuple[str, int]) -> QuestionSpec:
    return QuestionSpec(
        id=qid,
        sub_parts=tuple(SubPartSpec(id=f"{qid}.{p}", max_marks=D(m)) for p, m in parts),
    )


CQ_PARTS = (("ka", 1), ("kha", 2), ("ga", 3), ("gha", 4))


def cq_component(count: int = 8, answer: int | None = 5, **overrides: Any) -> ComponentSpec:
    questions = tuple(question(f"q{i}", *CQ_PARTS) for i in range(1, count + 1))
    data: dict[str, Any] = {
        "code": "cq",
        "kind": ComponentKind.CQ,
        "max_marks": D(10 * (answer if answer is not None else count)),
        "questions": questions,
        "choice": None if answer is None else ChoiceRule(answer=answer),
    }
    data.update(overrides)
    return ComponentSpec.model_validate(data)


def answered(qid: str, *marks: int) -> list[SubPartMark]:
    return [
        SubPartMark(sub_part_id=f"{qid}.{part}", marks=D(m))
        for (part, _), m in zip(CQ_PARTS, marks, strict=True)
    ]


def blank(qid: str) -> list[SubPartMark]:
    return [
        SubPartMark(sub_part_id=f"{qid}.{part}", marks=D(0), attempted=False)
        for part, _ in CQ_PARTS
    ]


class TestStructureValidation:
    def test_component_max_must_match_the_questions_without_choice(self) -> None:
        with pytest.raises(ValidationError):
            cq_component(count=3, answer=None, max_marks=D(99))

    def test_component_max_must_match_the_best_n_with_choice(self) -> None:
        with pytest.raises(ValidationError):
            cq_component(count=8, answer=5, max_marks=D(40))

    def test_choice_cannot_ask_for_more_questions_than_exist(self) -> None:
        with pytest.raises(ValidationError):
            cq_component(count=3, answer=5)

    def test_duplicate_sub_part_ids_are_rejected(self) -> None:
        with pytest.raises(ValidationError):
            ComponentSpec(
                code="cq",
                kind=ComponentKind.CQ,
                max_marks=D(4),
                questions=(
                    QuestionSpec(
                        id="q1",
                        sub_parts=(
                            SubPartSpec(id="dup", max_marks=D(2)),
                            SubPartSpec(id="dup", max_marks=D(2)),
                        ),
                    ),
                ),
            )

    def test_an_imported_component_declares_its_max_directly(self) -> None:
        spec = ComponentSpec(code="practical", kind=ComponentKind.PRACTICAL, max_marks=D(25))
        assert spec.max_marks == D(25)
        assert spec.questions == ()


class TestAggregation:
    def test_sub_parts_sum_into_a_question_and_questions_into_the_component(self) -> None:
        spec = cq_component(count=5, answer=None)
        marks = ComponentMarks(
            component_code="cq",
            sub_parts=tuple(p for i in range(1, 6) for p in answered(f"q{i}", 1, 2, 3, 4)),
        )
        result = aggregate_component(spec, marks)
        assert result.marks == D(50)
        assert result.max_marks == D(50)
        assert len(result.questions) == 5
        assert all(q.counted for q in result.questions)

    def test_partial_marks_add_up(self) -> None:
        spec = cq_component(count=1, answer=None)
        marks = ComponentMarks(component_code="cq", sub_parts=tuple(answered("q1", 1, 1, 2, 0)))
        assert aggregate_component(spec, marks).marks == D(4)

    def test_marks_above_the_sub_part_max_are_rejected(self) -> None:
        spec = cq_component(count=1, answer=None)
        marks = ComponentMarks(component_code="cq", sub_parts=tuple(answered("q1", 2, 2, 3, 4)))
        with pytest.raises(ResultInputError, match=r"q1\.ka"):
            aggregate_component(spec, marks)

    def test_a_missing_sub_part_is_rejected(self) -> None:
        spec = cq_component(count=1, answer=None)
        marks = ComponentMarks(component_code="cq", sub_parts=tuple(answered("q1", 1, 2, 3, 4)[:3]))
        with pytest.raises(ResultInputError, match=r"q1\.gha"):
            aggregate_component(spec, marks)

    def test_an_unknown_sub_part_is_rejected(self) -> None:
        spec = cq_component(count=1, answer=None)
        marks = ComponentMarks(
            component_code="cq",
            sub_parts=(*answered("q1", 1, 2, 3, 4), SubPartMark(sub_part_id="ghost", marks=D(1))),
        )
        with pytest.raises(ResultInputError, match="ghost"):
            aggregate_component(spec, marks)

    def test_marks_for_the_wrong_component_are_rejected(self) -> None:
        spec = cq_component(count=1, answer=None)
        marks = ComponentMarks(component_code="mcq", sub_parts=tuple(answered("q1", 1, 2, 3, 4)))
        with pytest.raises(ResultInputError, match="mcq"):
            aggregate_component(spec, marks)

    def test_a_not_attempted_sub_part_must_carry_zero(self) -> None:
        with pytest.raises(ValidationError):
            SubPartMark(sub_part_id="q1.ka", marks=D(1), attempted=False)


class TestChoiceRules:
    def test_first_attempted_counts_the_first_n_in_script_order(self) -> None:
        spec = cq_component(count=8, answer=5)
        # q1..q6 attempted, q6 is the best; the first five must be counted.
        sub_parts: list[SubPartMark] = []
        for i in range(1, 7):
            sub_parts += answered(f"q{i}", 1, 1, 1, 1) if i < 6 else answered("q6", 1, 2, 3, 4)
        for i in range(7, 9):
            sub_parts += blank(f"q{i}")
        result = aggregate_component(
            spec, ComponentMarks(component_code="cq", sub_parts=tuple(sub_parts))
        )
        assert result.counted_question_ids == ("q1", "q2", "q3", "q4", "q5")
        assert result.marks == D(20)
        excluded = [q for q in result.questions if not q.counted and q.attempted]
        assert [q.question_id for q in excluded] == ["q6"]
        assert excluded[0].excluded_reason == "choice_rule"

    def test_best_n_counts_the_highest_scoring_attempts(self) -> None:
        spec = cq_component(
            count=8, answer=5, choice=ChoiceRule(answer=5, policy=ChoicePolicy.BEST)
        )
        sub_parts: list[SubPartMark] = []
        for i in range(1, 7):
            sub_parts += answered(f"q{i}", 1, 1, 1, 1) if i < 6 else answered("q6", 1, 2, 3, 4)
        for i in range(7, 9):
            sub_parts += blank(f"q{i}")
        result = aggregate_component(
            spec, ComponentMarks(component_code="cq", sub_parts=tuple(sub_parts))
        )
        assert "q6" in result.counted_question_ids
        assert result.marks == D(26)

    def test_best_n_breaks_ties_by_script_order(self) -> None:
        spec = cq_component(
            count=3,
            answer=2,
            max_marks=D(20),
            choice=ChoiceRule(answer=2, policy=ChoicePolicy.BEST),
        )
        sub_parts = (
            answered("q1", 1, 1, 1, 1) + answered("q2", 1, 1, 1, 1) + answered("q3", 1, 1, 1, 1)
        )
        result = aggregate_component(
            spec, ComponentMarks(component_code="cq", sub_parts=tuple(sub_parts))
        )
        assert result.counted_question_ids == ("q1", "q2")

    def test_under_answering_counts_every_attempt(self) -> None:
        spec = cq_component(count=8, answer=5)
        sub_parts: list[SubPartMark] = []
        for i in range(1, 4):
            sub_parts += answered(f"q{i}", 1, 2, 3, 4)
        for i in range(4, 9):
            sub_parts += blank(f"q{i}")
        result = aggregate_component(
            spec, ComponentMarks(component_code="cq", sub_parts=tuple(sub_parts))
        )
        assert result.counted_question_ids == ("q1", "q2", "q3")
        assert result.marks == D(30)

    def test_a_question_attempted_in_one_sub_part_only_still_counts_as_attempted(self) -> None:
        spec = cq_component(count=8, answer=5)
        sub_parts: list[SubPartMark] = []
        sub_parts += [
            SubPartMark(sub_part_id="q1.ka", marks=D(1)),
            SubPartMark(sub_part_id="q1.kha", marks=D(0), attempted=False),
            SubPartMark(sub_part_id="q1.ga", marks=D(0), attempted=False),
            SubPartMark(sub_part_id="q1.gha", marks=D(0), attempted=False),
        ]
        for i in range(2, 9):
            sub_parts += blank(f"q{i}")
        result = aggregate_component(
            spec, ComponentMarks(component_code="cq", sub_parts=tuple(sub_parts))
        )
        assert result.counted_question_ids == ("q1",)
        assert result.marks == D(1)

    def test_a_fully_blank_script_scores_zero_and_counts_nothing(self) -> None:
        spec = cq_component(count=8, answer=5)
        sub_parts = [p for i in range(1, 9) for p in blank(f"q{i}")]
        result = aggregate_component(
            spec, ComponentMarks(component_code="cq", sub_parts=tuple(sub_parts))
        )
        assert result.counted_question_ids == ()
        assert result.marks == D(0)
        assert not result.is_pass


class TestPassRulesAndAbsence:
    def test_pass_mark_defaults_to_33_percent_rounded_up(self) -> None:
        spec = ComponentSpec(code="mcq", kind=ComponentKind.MCQ, max_marks=D(25))
        result = aggregate_component(spec, ComponentMarks(component_code="mcq", marks=D(9)))
        assert result.pass_mark == D("8.25")
        assert result.is_pass

    def test_below_the_pass_mark_fails_the_component(self) -> None:
        spec = ComponentSpec(code="mcq", kind=ComponentKind.MCQ, max_marks=D(25))
        result = aggregate_component(spec, ComponentMarks(component_code="mcq", marks=D(8)))
        assert not result.is_pass

    def test_pass_percent_is_configurable(self) -> None:
        spec = ComponentSpec(
            code="practical",
            kind=ComponentKind.PRACTICAL,
            max_marks=D(25),
            pass_percent=D(40),
        )
        result = aggregate_component(spec, ComponentMarks(component_code="practical", marks=D(9)))
        assert result.pass_mark == D(10)
        assert not result.is_pass

    def test_absent_is_not_zero(self) -> None:
        spec = ComponentSpec(code="mcq", kind=ComponentKind.MCQ, max_marks=D(25))
        result = aggregate_component(spec, ComponentMarks(component_code="mcq", absent=True))
        assert result.absent
        assert result.marks == D(0)
        assert not result.is_pass

    def test_an_absent_component_may_not_carry_marks(self) -> None:
        with pytest.raises(ValidationError):
            ComponentMarks(component_code="mcq", marks=D(5), absent=True)

    def test_an_imported_component_needs_a_mark_or_absence(self) -> None:
        spec = ComponentSpec(code="mcq", kind=ComponentKind.MCQ, max_marks=D(25))
        with pytest.raises(ResultInputError, match="mcq"):
            aggregate_component(spec, ComponentMarks(component_code="mcq"))

    def test_an_imported_mark_above_the_component_max_is_rejected(self) -> None:
        spec = ComponentSpec(code="mcq", kind=ComponentKind.MCQ, max_marks=D(25))
        with pytest.raises(ResultInputError, match="25"):
            aggregate_component(spec, ComponentMarks(component_code="mcq", marks=D(26)))

    def test_sub_part_marks_may_not_be_supplied_for_an_imported_component(self) -> None:
        spec = ComponentSpec(code="mcq", kind=ComponentKind.MCQ, max_marks=D(25))
        marks = ComponentMarks(
            component_code="mcq", sub_parts=(SubPartMark(sub_part_id="x", marks=D(1)),)
        )
        with pytest.raises(ResultInputError):
            aggregate_component(spec, marks)
