"""Item scoring function (TR-SCO-01/02, ASR-02..04).

``score_item`` is a pure function of the rubric and the criterion decisions; the
same function scores AI suggestions and teacher edits. Order of operations:

1. per criterion: met -> max, not_met / cannot_determine -> 0, partly -> the
   explicit proposed marks clamped to [0, criterion max];
2. ECF: a later step (in ``ecf_policy.steps`` order) that is wrong only because
   it correctly carries an earlier value (``ecf_consistent``) gets full credit,
   so the first erroneous step is penalised once;
3. subtract applied deductions (optionally limited by ``max_total_deduction``);
4. apply triggered caps (a cap triggers when a listed criterion is not fully
   awarded after ECF);
5. clamp to [0, item max], round to the mark grid (whole marks, or 0.5 when half
   marks are allowed) with the rubric's rounding mode, clamp again.

A teacher ``total_override`` (with reason) replaces the total; the computed
total is kept alongside it.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from decimal import Decimal
from enum import StrEnum

from pydantic import Field, field_validator

from khata.engines.base import FrozenModel
from khata.engines.errors import ScoringInputError
from khata.engines.marks import is_multiple_of, round_exact
from khata.engines.rubric import Criterion, Rubric

ZERO = Decimal(0)


class Decision(StrEnum):
    MET = "met"
    PARTLY = "partly"
    NOT_MET = "not_met"
    CANNOT_DETERMINE = "cannot_determine"


class CriterionDecision(FrozenModel):
    criterion_id: str
    decision: Decision
    marks: Decimal | None = Field(default=None, allow_inf_nan=False)
    ecf_consistent: bool = False


class TotalOverride(FrozenModel):
    total: Decimal = Field(allow_inf_nan=False)
    reason: str

    @field_validator("reason")
    @classmethod
    def _reason_required(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("a total override requires a reason")
        return value


class CriterionScore(FrozenModel):
    criterion_id: str
    decision: Decision
    max_marks: Decimal
    awarded: Decimal
    ecf_credit: bool = False


class ItemScore(FrozenModel):
    item_id: str
    rubric_version: int
    method_id: str | None
    item_max: Decimal
    criteria: tuple[CriterionScore, ...]
    criteria_total: Decimal
    deductions_applied: tuple[str, ...]
    deductions_total: Decimal
    caps_applied: tuple[str, ...]
    computed_total: Decimal
    override: TotalOverride | None
    total: Decimal
    needs_teacher: bool


def score_item(
    rubric: Rubric,
    criterion_decisions: Sequence[CriterionDecision],
    deductions_applied: Sequence[str] = (),
    total_override: TotalOverride | None = None,
    *,
    item_max: Decimal | None = None,
    method_id: str | None = None,
) -> ItemScore:
    criteria = _criteria(rubric, method_id)
    bound = sum((c.marks for c in criteria), ZERO) if item_max is None else item_max
    if bound <= 0:
        raise ScoringInputError(f"item_max must be > 0 (got {bound})")
    by_id = _decisions_by_id(criteria, criterion_decisions)
    scores = _criterion_scores(rubric, criteria, by_id)
    criteria_total = sum((s.awarded for s in scores), ZERO)
    deductions = tuple(deductions_applied)
    deductions_total = _deductions_total(rubric, deductions)
    caps = _triggered_caps(rubric, scores)
    raw = criteria_total - deductions_total
    for cap_max in (cap.max_marks for cap in rubric.caps if cap.id in caps):
        raw = min(raw, cap_max)
    computed = _bounded(round_exact(_bounded(raw, bound), rubric.mark_quantum, rubric.rounding_mode), bound)
    if total_override is not None:
        _check_override(total_override, bound, rubric.mark_quantum)
    return ItemScore(
        item_id=rubric.item_id,
        rubric_version=rubric.version,
        method_id=method_id,
        item_max=bound,
        criteria=scores,
        criteria_total=criteria_total,
        deductions_applied=deductions,
        deductions_total=deductions_total,
        caps_applied=caps,
        computed_total=computed,
        override=total_override,
        total=computed if total_override is None else total_override.total,
        needs_teacher=any(s.decision is Decision.CANNOT_DETERMINE for s in scores),
    )


def _criteria(rubric: Rubric, method_id: str | None) -> tuple[Criterion, ...]:
    try:
        return rubric.criteria_for(method_id)
    except KeyError as exc:
        raise ScoringInputError(f"unknown alternative method {method_id!r}") from exc


def _decisions_by_id(
    criteria: tuple[Criterion, ...], decisions: Iterable[CriterionDecision]
) -> dict[str, CriterionDecision]:
    known = {c.id for c in criteria}
    by_id: dict[str, CriterionDecision] = {}
    for decision in decisions:
        if decision.criterion_id not in known:
            raise ScoringInputError(f"unknown criterion {decision.criterion_id!r}")
        if decision.criterion_id in by_id:
            raise ScoringInputError(f"duplicate decision for {decision.criterion_id!r}")
        by_id[decision.criterion_id] = decision
    missing = [c.id for c in criteria if c.id not in by_id]
    if missing:
        raise ScoringInputError(f"missing decisions for criteria {missing}")
    return by_id


def _criterion_scores(
    rubric: Rubric, criteria: tuple[Criterion, ...], by_id: dict[str, CriterionDecision]
) -> tuple[CriterionScore, ...]:
    steps = rubric.ecf_policy.steps if rubric.ecf_policy.enabled else ()
    later_steps = set(steps[1:])
    scores = []
    for criterion in criteria:
        decision = by_id[criterion.id]
        awarded = _base_award(criterion, decision)
        credit = (
            criterion.id in later_steps
            and decision.ecf_consistent
            and decision.decision in (Decision.NOT_MET, Decision.PARTLY)
        )
        scores.append(
            CriterionScore(
                criterion_id=criterion.id,
                decision=decision.decision,
                max_marks=criterion.marks,
                awarded=criterion.marks if credit else awarded,
                ecf_credit=credit,
            )
        )
    return tuple(scores)


def _base_award(criterion: Criterion, decision: CriterionDecision) -> Decimal:
    kind, marks = decision.decision, decision.marks
    if kind is Decision.MET:
        if marks is not None and marks != criterion.marks:
            raise ScoringInputError(f"{criterion.id}: met implies {criterion.marks}, got {marks}")
        return criterion.marks
    if kind is Decision.PARTLY:
        if marks is None:
            raise ScoringInputError(f"{criterion.id}: partly requires explicit marks")
        return _bounded(marks, criterion.marks)
    if marks is not None and marks != 0:
        raise ScoringInputError(f"{criterion.id}: {kind.value} implies 0, got {marks}")
    return ZERO


def _deductions_total(rubric: Rubric, applied: tuple[str, ...]) -> Decimal:
    catalogue = {d.id: d.marks for d in rubric.deductions}
    seen: set[str] = set()
    for deduction_id in applied:
        if deduction_id not in catalogue:
            raise ScoringInputError(f"unknown deduction {deduction_id!r}")
        if deduction_id in seen:
            raise ScoringInputError(f"duplicate deduction {deduction_id!r}")
        seen.add(deduction_id)
    total = sum((max(catalogue[d], ZERO) for d in applied), ZERO)
    if rubric.max_total_deduction is not None:
        total = min(total, rubric.max_total_deduction)
    return total


def _triggered_caps(rubric: Rubric, scores: tuple[CriterionScore, ...]) -> tuple[str, ...]:
    short = {s.criterion_id for s in scores if s.awarded < s.max_marks}
    return tuple(cap.id for cap in rubric.caps if short.intersection(cap.when_not_met))


def _check_override(override: TotalOverride, bound: Decimal, quantum: Decimal) -> None:
    if not ZERO <= override.total <= bound:
        raise ScoringInputError(f"override {override.total} outside [0, {bound}]")
    if not is_multiple_of(override.total, quantum):
        raise ScoringInputError(f"override {override.total} not a multiple of {quantum}")


def _bounded(value: Decimal, upper: Decimal) -> Decimal:
    return min(max(value, ZERO), upper)
