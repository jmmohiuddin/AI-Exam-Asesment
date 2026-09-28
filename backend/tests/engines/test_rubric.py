from __future__ import annotations

from decimal import Decimal
from typing import Any

import pytest
from pydantic import ValidationError

from khata.engines.rubric import (
    AnswerKind,
    Rubric,
    ValidationReport,
    validate_rubric,
)
from khata.engines.rubric_heuristics import is_unobservable


def physics_ga(**overrides: Any) -> Rubric:
    data: dict[str, Any] = {
        "item_id": "CQ3.ga",
        "criteria": [
            {
                "id": "formula",
                "text_en": "identifies correct formula v = u + at",
                "text_bn": "সঠিক সূত্র লেখে",
                "marks": 1,
                "type": "step",
            },
            {
                "id": "subst",
                "text_en": "substitutes values with units",
                "marks": 1,
                "type": "step",
            },
            {
                "id": "result",
                "text_en": "correct result with unit",
                "marks": 1,
                "type": "final_answer",
            },
        ],
        "model_answer": "v = 0 + 2 × 5 = 10 m/s",
        "ecf_policy": {"enabled": True, "steps": ["formula", "subst", "result"]},
        "answer_spec": {
            "kind": "numeric",
            "value": "10",
            "unit": "m/s",
            "tolerance": {"abs": "0.1"},
        },
    }
    data.update(overrides)
    return Rubric.model_validate(data)


def codes(report: ValidationReport, level: str) -> set[str]:
    return {issue.code for issue in getattr(report, level)}


def test_valid_rubric_is_ai_eligible_and_lockable() -> None:
    report = validate_rubric(physics_ga(), Decimal(3))
    assert report.errors == ()
    assert report.ai_eligible is True
    assert report.lockable is True


def test_rubric_models_are_frozen() -> None:
    rubric = physics_ga()
    with pytest.raises(ValidationError):
        rubric.item_id = "other"  # type: ignore[misc]
    with pytest.raises(ValidationError):
        Rubric.model_validate({"item_id": "x", "criteria": [], "unknown": 1})


def test_criteria_sum_mismatch_is_an_error() -> None:
    report = validate_rubric(physics_ga(), Decimal(4))
    assert "criteria_sum_mismatch" in codes(report, "errors")
    assert report.ai_eligible is False
    assert report.lockable is False


def test_missing_model_answer_is_warning_and_not_ai_eligible() -> None:
    for blank in (None, "", "   "):
        report = validate_rubric(physics_ga(model_answer=blank), Decimal(3))
        assert "missing_model_answer" in codes(report, "warnings")
        assert report.errors == ()
        assert report.ai_eligible is False
        assert report.lockable is True


def test_duplicate_ids_are_errors() -> None:
    rubric = physics_ga(
        criteria=[
            {"id": "a", "text_en": "writes formula", "marks": 1, "type": "step"},
            {"id": "a", "text_en": "writes unit", "marks": 2, "type": "unit"},
        ],
        ecf_policy={"enabled": False},
        deductions=[
            {"id": "d1", "text": "sign error", "marks": 1},
            {"id": "d1", "text": "unit error", "marks": 1},
        ],
    )
    report = validate_rubric(rubric, Decimal(3))
    dupes = [i for i in report.errors if i.code == "duplicate_id"]
    assert {i.path for i in dupes} == {"criteria[1].id", "deductions[1].id"}


def test_negative_marks_are_errors() -> None:
    rubric = physics_ga(
        criteria=[
            {"id": "a", "text_en": "writes formula F = ma", "marks": 4, "type": "step"},
            {"id": "b", "text_en": "writes unit N", "marks": -1, "type": "unit"},
        ],
        ecf_policy={"enabled": False},
        deductions=[{"id": "d", "text": "x", "marks": -1}],
        caps=[{"id": "c", "text": "cap", "max_marks": -1, "when_not_met": ["a"]}],
    )
    report = validate_rubric(rubric, Decimal(3))
    negatives = {i.path for i in report.errors if i.code == "negative_marks"}
    assert negatives == {"criteria[1].marks", "deductions[0].marks", "caps[0].max_marks"}


def test_fractional_marks_follow_half_mark_policy() -> None:
    crit = [
        {"id": "a", "text_en": "writes formula", "marks": "1.5", "type": "step"},
        {"id": "b", "text_en": "writes value 3", "marks": "1.5", "type": "final_answer"},
    ]
    whole = validate_rubric(physics_ga(criteria=crit, ecf_policy={}), Decimal(3))
    assert "marks_not_on_grid" in codes(whole, "errors")
    half = validate_rubric(
        physics_ga(criteria=crit, ecf_policy={}, half_marks_allowed=True), Decimal(3)
    )
    assert half.errors == ()
    quarter = [dict(c, marks="0.75") for c in crit]
    bad = validate_rubric(
        physics_ga(criteria=quarter, ecf_policy={}, half_marks_allowed=True), Decimal("1.5")
    )
    assert "marks_not_on_grid" in codes(bad, "errors")


def test_ecf_and_cap_references_must_exist() -> None:
    rubric = physics_ga(
        ecf_policy={"enabled": True, "steps": ["formula", "ghost"]},
        caps=[{"id": "c1", "text": "cap", "max_marks": 1, "when_not_met": ["nope"]}],
    )
    report = validate_rubric(rubric, Decimal(3))
    paths = {i.path for i in report.errors if i.code == "unknown_criterion_ref"}
    assert paths == {"ecf_policy.steps[1]", "caps[0].when_not_met[0]"}


def test_ecf_with_single_step_warns() -> None:
    report = validate_rubric(
        physics_ga(ecf_policy={"enabled": True, "steps": ["formula"]}), Decimal(3)
    )
    assert "ecf_too_few_steps" in codes(report, "warnings")


def test_empty_criteria_is_error() -> None:
    report = validate_rubric(physics_ga(criteria=[], ecf_policy={}), Decimal(3))
    assert "no_criteria" in codes(report, "errors")


def test_non_positive_item_max_is_error() -> None:
    report = validate_rubric(physics_ga(), Decimal(0))
    assert "invalid_item_max" in codes(report, "errors")


def test_alternative_method_sum_mismatch_is_error() -> None:
    rubric = physics_ga(
        alternatives=[
            {
                "id": "alt1",
                "kind": "method",
                "text": "uses s = ut + 1/2 at^2 then v^2 = u^2 + 2as",
                "criteria": [{"id": "m1", "text_en": "writes formula", "marks": 1, "type": "step"}],
            }
        ]
    )
    report = validate_rubric(rubric, Decimal(3))
    assert "alternative_sum_mismatch" in codes(report, "errors")


def test_alternative_answer_conflicting_with_deduction_is_error() -> None:
    rubric = physics_ga(
        deductions=[{"id": "d1", "text": "10 m", "marks": 1}],
        alternatives=[{"id": "a1", "kind": "answer", "text": "10 m"}],
    )
    report = validate_rubric(rubric, Decimal(3))
    assert "alternatives_conflict" in codes(report, "errors")


def test_duplicate_alternatives_and_kind_mismatch() -> None:
    rubric = physics_ga(
        alternatives=[
            {"id": "a1", "kind": "answer", "text": "10 m/s"},
            {"id": "a2", "kind": "answer", "text": " 10  M/S "},
            {
                "id": "a3",
                "kind": "answer",
                "text": "x",
                "answer_spec": {"kind": "expression", "value": "x"},
            },
        ]
    )
    report = validate_rubric(rubric, Decimal(3))
    assert "alternatives_conflict" in codes(report, "errors")
    assert "duplicate_alternative" in codes(report, "warnings")


def test_answer_spec_checks() -> None:
    bad_numeric = physics_ga(answer_spec={"kind": "numeric", "value": "ten"})
    assert "invalid_answer_value" in codes(validate_rubric(bad_numeric, Decimal(3)), "errors")
    bangla_numeric = physics_ga(answer_spec={"kind": "numeric", "value": "৯.৮"})
    assert validate_rubric(bangla_numeric, Decimal(3)).errors == ()
    neg_tol = physics_ga(
        answer_spec={"kind": "numeric", "value": "1", "tolerance": {"rel": "-0.1"}}
    )
    assert "invalid_tolerance" in codes(validate_rubric(neg_tol, Decimal(3)), "errors")
    mcq = physics_ga(answer_spec={"kind": "mcq", "value": "E", "options": ["A", "B", "C", "D"]})
    assert "invalid_answer_value" in codes(validate_rubric(mcq, Decimal(3)), "errors")
    ok_mcq = physics_ga(answer_spec={"kind": "mcq", "value": "C", "options": ["A", "B", "C", "D"]})
    assert validate_rubric(ok_mcq, Decimal(3)).errors == ()
    assert ok_mcq.answer_spec is not None
    assert ok_mcq.answer_spec.kind is AnswerKind.MCQ


def test_cap_above_item_max_and_huge_deduction_warn() -> None:
    rubric = physics_ga(
        caps=[{"id": "c1", "text": "cap", "max_marks": 5, "when_not_met": ["result"]}],
        deductions=[{"id": "d1", "text": "no unit", "marks": 5}],
    )
    warnings = codes(validate_rubric(rubric, Decimal(3)), "warnings")
    assert {"cap_has_no_effect", "deduction_exceeds_item_max"} <= warnings


def test_unobservable_criterion_warns_in_both_languages() -> None:
    rubric = physics_ga(
        criteria=[
            {"id": "a", "text_en": "good explanation", "marks": 1, "type": "concept"},
            {"id": "b", "text_bn": "ভালো ব্যাখ্যা", "marks": 1, "type": "concept"},
            {"id": "c", "text_en": "writes the formula F = ma", "marks": 1, "type": "step"},
        ],
        ecf_policy={},
    )
    report = validate_rubric(rubric, Decimal(3))
    flagged = {i.path for i in report.warnings if i.code == "unobservable_criterion"}
    assert flagged == {"criteria[0]", "criteria[1]"}


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("good explanation", True),
        ("Explains properly", True),
        ("explains correctly", True),
        ("shows understanding", True),
        ("সঠিকভাবে", True),
        ("সঠিকভাবে ব্যাখ্যা করে", True),
        ("ভালো ব্যাখ্যা", True),
        ("যথাযথ উত্তর", False),  # names an observable object (উত্তর = answer)
        ("সঠিকভাবে সূত্র লেখে", False),
        ("properly labels the diagram", False),
        ("writes the unit m/s properly", False),
        ("correctly substitutes 5 into the formula", False),
        ("states Newton's second law", False),
        ("identifies correct formula", False),
        ("", False),
    ],
)
def test_unobservable_heuristic(text: str, expected: bool) -> None:
    assert is_unobservable(text) is expected


def test_evidence_expectation_can_make_criterion_observable() -> None:
    rubric = physics_ga(
        criteria=[
            {
                "id": "a",
                "text_en": "explains properly",
                "evidence_expectation": "writes the net force value 0 N",
                "marks": 3,
                "type": "concept",
            }
        ],
        ecf_policy={},
    )
    report = validate_rubric(rubric, Decimal(3))
    assert "unobservable_criterion" not in codes(report, "warnings")


def test_criterion_without_text_warns() -> None:
    rubric = physics_ga(
        criteria=[{"id": "a", "marks": 3, "type": "concept"}],
        ecf_policy={},
    )
    assert "criterion_text_missing" in codes(validate_rubric(rubric, Decimal(3)), "warnings")
