from __future__ import annotations

from decimal import Decimal
from typing import Any

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from khata.engines.errors import ScoringInputError
from khata.engines.rubric import Rubric
from khata.engines.scoring import (
    CriterionDecision,
    Decision,
    TotalOverride,
    score_item,
)

D = Decimal


def rubric(**overrides: Any) -> Rubric:
    data: dict[str, Any] = {
        "item_id": "CQ1.gha",
        "criteria": [
            {"id": "s1", "text_en": "formula", "marks": 1, "type": "step"},
            {"id": "s2", "text_en": "substitution", "marks": 1, "type": "step"},
            {"id": "s3", "text_en": "calculation", "marks": 1, "type": "step"},
            {"id": "fa", "text_en": "final answer", "marks": 1, "type": "final_answer"},
        ],
        "model_answer": "...",
        "deductions": [
            {"id": "no_unit", "text": "unit missing", "marks": 1},
            {"id": "sign", "text": "sign slip", "marks": 1},
        ],
        "ecf_policy": {"enabled": True, "steps": ["s1", "s2", "s3", "fa"]},
    }
    data.update(overrides)
    return Rubric.model_validate(data)


def dec(cid: str, decision: str, marks: str | None = None, ecf: bool = False) -> CriterionDecision:
    return CriterionDecision(
        criterion_id=cid,
        decision=Decision(decision),
        marks=None if marks is None else D(marks),
        ecf_consistent=ecf,
    )


ALL_MET = [dec("s1", "met"), dec("s2", "met"), dec("s3", "met"), dec("fa", "met")]


def test_all_met_scores_full_marks() -> None:
    score = score_item(rubric(), ALL_MET)
    assert score.total == D(4)
    assert score.computed_total == D(4)
    assert score.needs_teacher is False
    assert score.item_max == D(4)
    assert [c.awarded for c in score.criteria] == [D(1)] * 4


def test_not_met_and_partly() -> None:
    decisions = [
        dec("s1", "met"),
        dec("s2", "partly", "0.5"),
        dec("s3", "not_met"),
        dec("fa", "not_met"),
    ]
    whole = score_item(rubric(), decisions)
    assert whole.criteria_total == D("1.5")
    assert whole.total == D(2)  # whole marks, half-up at item total
    half = score_item(rubric(half_marks_allowed=True), decisions)
    assert half.total == D("1.5")
    down = score_item(rubric(rounding_mode="down"), decisions)
    assert down.total == D(1)


def test_partly_requires_explicit_marks() -> None:
    with pytest.raises(ScoringInputError, match="partly"):
        score_item(rubric(), [dec("s1", "partly"), *ALL_MET[1:]])


def test_partly_marks_are_clamped_to_criterion_bounds() -> None:
    decisions = [dec("s1", "partly", "5"), dec("s2", "partly", "-2"), *ALL_MET[2:]]
    score = score_item(rubric(half_marks_allowed=True), decisions)
    assert [c.awarded for c in score.criteria[:2]] == [D(1), D(0)]
    assert score.total == D(3)


def test_inconsistent_marks_for_met_or_not_met_are_rejected() -> None:
    with pytest.raises(ScoringInputError, match="met"):
        score_item(rubric(), [dec("s1", "met", "0.5"), *ALL_MET[1:]])
    with pytest.raises(ScoringInputError, match="not_met"):
        score_item(rubric(), [dec("s1", "not_met", "1"), *ALL_MET[1:]])


def test_cannot_determine_scores_zero_and_needs_teacher() -> None:
    score = score_item(rubric(), [dec("s1", "cannot_determine"), *ALL_MET[1:]])
    assert score.total == D(3)
    assert score.needs_teacher is True


def test_missing_unknown_and_duplicate_decisions_are_errors() -> None:
    with pytest.raises(ScoringInputError, match="missing"):
        score_item(rubric(), ALL_MET[:3])
    with pytest.raises(ScoringInputError, match="unknown"):
        score_item(rubric(), [*ALL_MET, dec("zz", "met")])
    with pytest.raises(ScoringInputError, match="duplicate"):
        score_item(rubric(), [*ALL_MET, dec("s1", "met")])


def test_ecf_wrong_step_one_carried_through_loses_only_step_one() -> None:
    # FR-RUB-04 acceptance: wrong value in step 1, carried correctly through 2-3.
    decisions = [
        dec("s1", "not_met"),
        dec("s2", "not_met", ecf=True),
        dec("s3", "not_met", ecf=True),
        dec("fa", "not_met", ecf=True),
    ]
    score = score_item(rubric(), decisions)
    assert score.total == D(3)
    assert [c.ecf_credit for c in score.criteria] == [False, True, True, True]


def test_ecf_disabled_ignores_consistency_flag() -> None:
    decisions = [
        dec("s1", "not_met"),
        dec("s2", "not_met", ecf=True),
        dec("s3", "not_met", ecf=True),
        dec("fa", "not_met", ecf=True),
    ]
    score = score_item(rubric(ecf_policy={"enabled": False}), decisions)
    assert score.total == D(0)


def test_ecf_flag_on_first_step_or_non_step_gives_no_credit() -> None:
    decisions = [dec("s1", "not_met", ecf=True), *ALL_MET[1:]]
    score = score_item(rubric(), decisions)
    assert score.total == D(3)
    assert score.criteria[0].ecf_credit is False
    partial = rubric(ecf_policy={"enabled": True, "steps": ["s1", "s2"]})
    score2 = score_item(
        partial,
        [dec("s1", "not_met"), dec("s2", "met"), dec("s3", "met"), dec("fa", "not_met", ecf=True)],
    )
    assert score2.total == D(2)


def test_ecf_second_independent_error_is_also_penalised() -> None:
    decisions = [
        dec("s1", "not_met"),
        dec("s2", "not_met", ecf=True),
        dec("s3", "not_met"),  # a new error, not carried
        dec("fa", "not_met", ecf=True),
    ]
    assert score_item(rubric(), decisions).total == D(2)


def test_cannot_determine_never_gets_ecf_credit() -> None:
    decisions = [dec("s1", "not_met"), dec("s2", "cannot_determine", ecf=True), *ALL_MET[2:]]
    score = score_item(rubric(), decisions)
    assert score.total == D(2)
    assert score.needs_teacher is True


def test_deductions_apply_and_floor_at_zero() -> None:
    score = score_item(rubric(), ALL_MET, deductions_applied=["no_unit"])
    assert score.total == D(3)
    assert score.deductions_total == D(1)
    low = [dec("s1", "met"), dec("s2", "not_met"), dec("s3", "not_met"), dec("fa", "not_met")]
    floored = score_item(rubric(), low, deductions_applied=["no_unit", "sign"])
    assert floored.total == D(0)


def test_max_total_deduction_limits_deductions() -> None:
    score = score_item(
        rubric(max_total_deduction=1), ALL_MET, deductions_applied=["no_unit", "sign"]
    )
    assert score.deductions_total == D(1)
    assert score.total == D(3)


def test_unknown_or_repeated_deductions_are_errors() -> None:
    with pytest.raises(ScoringInputError, match="unknown deduction"):
        score_item(rubric(), ALL_MET, deductions_applied=["nope"])
    with pytest.raises(ScoringInputError, match="duplicate deduction"):
        score_item(rubric(), ALL_MET, deductions_applied=["sign", "sign"])


def test_caps_trigger_on_unmet_criteria() -> None:
    capped = rubric(caps=[{"id": "fa_wrong", "max_marks": 2, "when_not_met": ["fa"]}])
    decisions = [*ALL_MET[:3], dec("fa", "not_met")]
    score = score_item(capped, decisions)
    assert score.total == D(2)
    assert score.caps_applied == ("fa_wrong",)
    assert score_item(capped, ALL_MET).caps_applied == ()


def test_cap_not_triggered_when_ecf_credits_the_criterion() -> None:
    capped = rubric(caps=[{"id": "fa_wrong", "max_marks": 1, "when_not_met": ["fa"]}])
    decisions = [
        dec("s1", "not_met"),
        dec("s2", "met"),
        dec("s3", "met"),
        dec("fa", "not_met", ecf=True),
    ]
    score = score_item(capped, decisions)
    assert score.caps_applied == ()
    assert score.total == D(3)


def test_total_override_replaces_total_but_keeps_computed() -> None:
    override = TotalOverride(total=D(4), reason="alternative method accepted by HoD")
    score = score_item(rubric(), [dec("s1", "not_met"), *ALL_MET[1:]], total_override=override)
    assert score.computed_total == D(3)
    assert score.total == D(4)
    assert score.override == override


def test_total_override_bounds_and_grid() -> None:
    with pytest.raises(ScoringInputError, match="override"):
        score_item(rubric(), ALL_MET, total_override=TotalOverride(total=D(5), reason="x"))
    with pytest.raises(ScoringInputError, match="override"):
        score_item(rubric(), ALL_MET, total_override=TotalOverride(total=D("2.5"), reason="x"))
    ok = score_item(
        rubric(half_marks_allowed=True),
        ALL_MET,
        total_override=TotalOverride(total=D("2.5"), reason="x"),
    )
    assert ok.total == D("2.5")
    with pytest.raises(ValueError):
        TotalOverride(total=D(1), reason="   ")


def test_alternative_method_criteria() -> None:
    alt = rubric(
        alternatives=[
            {
                "id": "graph",
                "kind": "method",
                "text": "graphical method",
                "criteria": [
                    {"id": "g1", "text_en": "draws graph", "marks": 2, "type": "step"},
                    {"id": "g2", "text_en": "reads value", "marks": 2, "type": "final_answer"},
                ],
            }
        ]
    )
    score = score_item(alt, [dec("g1", "met"), dec("g2", "not_met")], method_id="graph")
    assert score.total == D(2)
    assert score.method_id == "graph"
    with pytest.raises(ScoringInputError, match="method"):
        score_item(alt, ALL_MET, method_id="nope")


def test_explicit_item_max_bounds_total() -> None:
    score = score_item(rubric(), ALL_MET, item_max=D(3))
    assert score.total == D(3)
    with pytest.raises(ScoringInputError, match="item_max"):
        score_item(rubric(), ALL_MET, item_max=D(0))


def test_decision_order_does_not_matter() -> None:
    forward = score_item(rubric(), [*ALL_MET[:2], dec("s3", "partly", "0.5"), ALL_MET[3]])
    backward = score_item(rubric(), [ALL_MET[3], dec("s3", "partly", "0.5"), *ALL_MET[:2][::-1]])
    assert forward == backward


# ---------------------------------------------------------------- properties

LEVELS = ["not_met", "partly", "met"]
decision_st = st.tuples(
    st.sampled_from(["not_met", "partly", "met", "cannot_determine"]),
    st.sampled_from(["0", "0.5", "1", "1.5", "-1", "3"]),
    st.booleans(),
)


def _build(raw: list[tuple[str, str, bool]]) -> list[CriterionDecision]:
    out = []
    for cid, (decision, marks, ecf) in zip(["s1", "s2", "s3", "fa"], raw, strict=True):
        out.append(dec(cid, decision, marks if decision == "partly" else None, ecf))
    return out


rubric_st = st.builds(
    lambda half, ecf, cap, mode: rubric(
        half_marks_allowed=half,
        ecf_policy={"enabled": ecf, "steps": ["s1", "s2", "s3", "fa"]},
        caps=[{"id": "c", "max_marks": 2, "when_not_met": ["fa"]}] if cap else [],
        rounding_mode=mode,
    ),
    st.booleans(),
    st.booleans(),
    st.booleans(),
    st.sampled_from(["half_up", "half_even", "down", "up"]),
)


@settings(max_examples=400)
@given(
    rubric_st,
    st.lists(decision_st, min_size=4, max_size=4),
    st.lists(st.sampled_from(["no_unit", "sign"]), unique=True),
)
def test_property_bounds_and_determinism(
    rb: Rubric, raw: list[tuple[str, str, bool]], deductions: list[str]
) -> None:
    decisions = _build(raw)
    first = score_item(rb, decisions, deductions_applied=deductions)
    second = score_item(rb, list(reversed(decisions)), deductions_applied=deductions)
    assert first == second
    assert D(0) <= first.total <= first.item_max
    assert (first.total / rb.mark_quantum) == int(first.total / rb.mark_quantum)
    for criterion in first.criteria:
        assert D(0) <= criterion.awarded <= criterion.max_marks


@settings(max_examples=400)
@given(rubric_st, st.lists(decision_st, min_size=4, max_size=4), st.integers(0, 3))
def test_property_upgrading_a_decision_never_lowers_the_mark(
    rb: Rubric, raw: list[tuple[str, str, bool]], index: int
) -> None:
    decision, marks, ecf = raw[index]
    if decision == "cannot_determine":
        decision = "not_met"
    rank = LEVELS.index(decision)
    if rank == len(LEVELS) - 1:
        return
    before_raw = list(raw)
    before_raw[index] = (decision, marks, ecf)
    after_raw = list(raw)
    after_raw[index] = (LEVELS[rank + 1], "1" if LEVELS[rank + 1] == "partly" else marks, ecf)
    if LEVELS[rank + 1] == "partly" and decision == "not_met":
        after_raw[index] = ("partly", "0.5", ecf)
    before = score_item(rb, _build(before_raw))
    after = score_item(rb, _build(after_raw))
    assert after.total >= before.total


@settings(max_examples=200)
@given(rubric_st, st.lists(decision_st, min_size=4, max_size=4), st.sampled_from(["0", "1", "4"]))
def test_property_override_takes_precedence(
    rb: Rubric, raw: list[tuple[str, str, bool]], value: str
) -> None:
    override = TotalOverride(total=D(value), reason="teacher judgement")
    plain = score_item(rb, _build(raw))
    overridden = score_item(rb, _build(raw), total_override=override)
    assert overridden.total == D(value)
    assert overridden.computed_total == plain.computed_total
