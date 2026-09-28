"""Rubric schema (TR-RUB-01) and pre-lock validation (TR-RUB-02, FR-RUB-07).

An item is AI-eligible only if it has a model answer and criteria that sum to
the item marks (FR-RUB-01); otherwise it is marked at L0 with a visible reason.
"""

from __future__ import annotations

from collections.abc import Iterable, Iterator
from decimal import Decimal, InvalidOperation
from enum import StrEnum

from pydantic import Field

from khata.engines.bangla.digits import to_latin_digits
from khata.engines.base import FrozenModel
from khata.engines.marks import RoundingMode, is_multiple_of
from khata.engines.rubric_heuristics import is_unobservable


class CriterionType(StrEnum):
    CONCEPT = "concept"
    STEP = "step"
    FINAL_ANSWER = "final_answer"
    UNIT = "unit"
    FORMAT = "format"


class AnswerKind(StrEnum):
    NUMERIC = "numeric"
    EXPRESSION = "expression"
    EQUATION = "equation"
    MCQ = "mcq"


class SigFigMode(StrEnum):
    IGNORE = "ignore"
    EXACT = "exact"
    AT_LEAST = "at_least"


class Criterion(FrozenModel):
    id: str = Field(min_length=1)
    text_bn: str = ""
    text_en: str = ""
    marks: Decimal = Field(allow_inf_nan=False)
    type: CriterionType
    evidence_expectation: str = ""


class Deduction(FrozenModel):
    id: str = Field(min_length=1)
    text: str = ""
    marks: Decimal = Field(allow_inf_nan=False)


class EcfPolicy(FrozenModel):
    enabled: bool = False
    steps: tuple[str, ...] = ()


class Cap(FrozenModel):
    """Caps the item total at ``max_marks`` when any listed criterion is not fully met."""

    id: str = Field(min_length=1)
    text: str = ""
    max_marks: Decimal = Field(allow_inf_nan=False)
    when_not_met: tuple[str, ...] = ()


class Tolerance(FrozenModel):
    abs: Decimal | None = Field(default=None, allow_inf_nan=False)
    rel: Decimal | None = Field(default=None, allow_inf_nan=False)


class SigFigPolicy(FrozenModel):
    mode: SigFigMode = SigFigMode.IGNORE
    count: int | None = Field(default=None, ge=1, le=15)


class AnswerSpec(FrozenModel):
    kind: AnswerKind
    value: str
    tolerance: Tolerance | None = None
    unit: str | None = None
    unit_required: bool = True
    missing_unit_deduction: Decimal = Field(default=Decimal(0), ge=0, allow_inf_nan=False)
    sig_figs: SigFigPolicy = SigFigPolicy()
    latex: str | None = None
    options: tuple[str, ...] = ()


class AlternativeKind(StrEnum):
    ANSWER = "answer"
    METHOD = "method"


class Alternative(FrozenModel):
    id: str = Field(min_length=1)
    kind: AlternativeKind
    text: str = ""
    answer_spec: AnswerSpec | None = None
    criteria: tuple[Criterion, ...] = ()


class Rubric(FrozenModel):
    item_id: str = Field(min_length=1)
    version: int = Field(default=1, ge=1)
    criteria: tuple[Criterion, ...]
    model_answer: str | None = None
    alternatives: tuple[Alternative, ...] = ()
    deductions: tuple[Deduction, ...] = ()
    ecf_policy: EcfPolicy = EcfPolicy()
    caps: tuple[Cap, ...] = ()
    half_marks_allowed: bool = False
    rounding_mode: RoundingMode = RoundingMode.HALF_UP
    max_total_deduction: Decimal | None = Field(default=None, ge=0, allow_inf_nan=False)
    answer_spec: AnswerSpec | None = None

    @property
    def mark_quantum(self) -> Decimal:
        return Decimal("0.5") if self.half_marks_allowed else Decimal(1)

    def criteria_for(self, method_id: str | None) -> tuple[Criterion, ...]:
        """Criteria of the main method, or of the named alternative method."""
        if method_id is None:
            return self.criteria
        for alternative in self.alternatives:
            if alternative.id == method_id and alternative.kind is AlternativeKind.METHOD:
                return alternative.criteria
        raise KeyError(f"unknown alternative method: {method_id}")


class Issue(FrozenModel):
    code: str
    path: str
    message: str


class ValidationReport(FrozenModel):
    errors: tuple[Issue, ...]
    warnings: tuple[Issue, ...]
    ai_eligible: bool

    @property
    def lockable(self) -> bool:
        """Lock is blocked on errors; warnings are shown (FR-RUB-07)."""
        return not self.errors


def validate_rubric(rubric: Rubric, item_max: Decimal) -> ValidationReport:
    errors = tuple(_errors(rubric, item_max))
    warnings = tuple(_warnings(rubric, item_max))
    has_model_answer = bool(rubric.model_answer and rubric.model_answer.strip())
    return ValidationReport(
        errors=errors, warnings=warnings, ai_eligible=not errors and has_model_answer
    )


def _errors(rubric: Rubric, item_max: Decimal) -> Iterator[Issue]:
    if item_max <= 0:
        yield Issue(code="invalid_item_max", path="item_max", message="item max must be > 0")
    if not rubric.criteria:
        yield Issue(code="no_criteria", path="criteria", message="rubric has no criteria")
    yield from _sum_error("criteria", rubric.criteria, item_max, "criteria_sum_mismatch")
    yield from _duplicate_ids(rubric)
    yield from _negative_marks(rubric)
    yield from _grid_errors(rubric)
    yield from _reference_errors(rubric)
    yield from _alternative_errors(rubric, item_max)
    if rubric.answer_spec is not None:
        yield from _answer_spec_errors(rubric.answer_spec, "answer_spec")


def _sum_error(
    path: str, criteria: tuple[Criterion, ...], item_max: Decimal, code: str
) -> Iterator[Issue]:
    total = sum((c.marks for c in criteria), Decimal(0))
    if criteria and total != item_max:
        yield Issue(code=code, path=path, message=f"criteria sum {total} != item max {item_max}")


def _duplicates(path: str, ids: Iterable[str]) -> Iterator[Issue]:
    seen: set[str] = set()
    for index, identifier in enumerate(ids):
        if identifier in seen:
            yield Issue(
                code="duplicate_id",
                path=f"{path}[{index}].id",
                message=f"duplicate id {identifier!r}",
            )
        seen.add(identifier)


def _duplicate_ids(rubric: Rubric) -> Iterator[Issue]:
    yield from _duplicates("criteria", (c.id for c in rubric.criteria))
    yield from _duplicates("deductions", (d.id for d in rubric.deductions))
    yield from _duplicates("caps", (c.id for c in rubric.caps))
    yield from _duplicates("alternatives", (a.id for a in rubric.alternatives))
    for index, alternative in enumerate(rubric.alternatives):
        ids = (c.id for c in alternative.criteria)
        yield from _duplicates(f"alternatives[{index}].criteria", ids)


def _negative_marks(rubric: Rubric) -> Iterator[Issue]:
    checks: list[tuple[str, Decimal]] = [
        (f"criteria[{i}].marks", c.marks) for i, c in enumerate(rubric.criteria)
    ]
    checks += [(f"deductions[{i}].marks", d.marks) for i, d in enumerate(rubric.deductions)]
    checks += [(f"caps[{i}].max_marks", c.max_marks) for i, c in enumerate(rubric.caps)]
    for a_index, alternative in enumerate(rubric.alternatives):
        checks += [
            (f"alternatives[{a_index}].criteria[{i}].marks", c.marks)
            for i, c in enumerate(alternative.criteria)
        ]
    for path, value in checks:
        if value < 0:
            yield Issue(code="negative_marks", path=path, message=f"negative marks {value}")


def _grid_errors(rubric: Rubric) -> Iterator[Issue]:
    quantum = rubric.mark_quantum
    for index, criterion in enumerate(rubric.criteria):
        if criterion.marks >= 0 and not is_multiple_of(criterion.marks, quantum):
            yield Issue(
                code="marks_not_on_grid",
                path=f"criteria[{index}].marks",
                message=f"{criterion.marks} is not a multiple of {quantum}",
            )


def _reference_errors(rubric: Rubric) -> Iterator[Issue]:
    known = {c.id for c in rubric.criteria}
    for index, step in enumerate(rubric.ecf_policy.steps):
        if step not in known:
            yield _unknown_ref(f"ecf_policy.steps[{index}]", step)
    for c_index, cap in enumerate(rubric.caps):
        for index, ref in enumerate(cap.when_not_met):
            if ref not in known:
                yield _unknown_ref(f"caps[{c_index}].when_not_met[{index}]", ref)


def _unknown_ref(path: str, ref: str) -> Issue:
    return Issue(code="unknown_criterion_ref", path=path, message=f"unknown criterion {ref!r}")


def _normalized(text: str) -> str:
    return " ".join(text.casefold().split())


def _alternative_errors(rubric: Rubric, item_max: Decimal) -> Iterator[Issue]:
    mistakes = {_normalized(d.text) for d in rubric.deductions if d.text.strip()}
    main_kind = rubric.answer_spec.kind if rubric.answer_spec else None
    for index, alt in enumerate(rubric.alternatives):
        path = f"alternatives[{index}]"
        if alt.kind is AlternativeKind.METHOD:
            yield from _sum_error(
                f"{path}.criteria", alt.criteria, item_max, "alternative_sum_mismatch"
            )
            if not alt.criteria:
                yield Issue(
                    code="alternative_sum_mismatch", path=path, message="method has no criteria"
                )
        if alt.text.strip() and _normalized(alt.text) in mistakes:
            yield Issue(
                code="alternatives_conflict",
                path=path,
                message="alternative answer is also listed as a penalised mistake",
            )
        if alt.answer_spec is not None:
            if main_kind is not None and alt.answer_spec.kind is not main_kind:
                yield Issue(
                    code="alternatives_conflict",
                    path=f"{path}.answer_spec.kind",
                    message="alternative answer kind differs from the main answer spec",
                )
            yield from _answer_spec_errors(alt.answer_spec, f"{path}.answer_spec")


def _answer_spec_errors(spec: AnswerSpec, path: str) -> Iterator[Issue]:
    if spec.kind is AnswerKind.NUMERIC and not _is_decimal(spec.value):
        yield Issue(
            code="invalid_answer_value", path=f"{path}.value", message="not a decimal number"
        )
    if spec.kind is AnswerKind.MCQ and spec.options and spec.value not in spec.options:
        yield Issue(
            code="invalid_answer_value", path=f"{path}.value", message="key not among options"
        )
    tolerance = spec.tolerance
    if tolerance is not None:
        for name, value in (("abs", tolerance.abs), ("rel", tolerance.rel)):
            if value is not None and value < 0:
                yield Issue(
                    code="invalid_tolerance",
                    path=f"{path}.tolerance.{name}",
                    message="tolerance must be >= 0",
                )


def _is_decimal(text: str) -> bool:
    try:
        return Decimal(to_latin_digits(text.strip())).is_finite()
    except InvalidOperation:
        return False


def _warnings(rubric: Rubric, item_max: Decimal) -> Iterator[Issue]:
    if not (rubric.model_answer and rubric.model_answer.strip()):
        yield Issue(
            code="missing_model_answer",
            path="model_answer",
            message="no model answer: item is not AI-eligible (L0)",
        )
    yield from _criterion_text_warnings(rubric.criteria, "criteria")
    if rubric.ecf_policy.enabled and len(rubric.ecf_policy.steps) < 2:
        yield Issue(
            code="ecf_too_few_steps",
            path="ecf_policy.steps",
            message="ECF needs at least two ordered steps to have any effect",
        )
    for index, cap in enumerate(rubric.caps):
        if cap.max_marks >= item_max:
            yield Issue(code="cap_has_no_effect", path=f"caps[{index}]", message="cap >= item max")
    for index, deduction in enumerate(rubric.deductions):
        if deduction.marks > item_max:
            yield Issue(
                code="deduction_exceeds_item_max",
                path=f"deductions[{index}]",
                message="deduction larger than the item max",
            )
    yield from _duplicate_alternative_warnings(rubric)


def _criterion_text_warnings(criteria: tuple[Criterion, ...], path: str) -> Iterator[Issue]:
    for index, criterion in enumerate(criteria):
        texts = (criterion.text_en, criterion.text_bn)
        if not any(t.strip() for t in texts):
            yield Issue(
                code="criterion_text_missing",
                path=f"{path}[{index}]",
                message="criterion has no text in either language",
            )
            continue
        combined = " ".join((*texts, criterion.evidence_expectation))
        if any(is_unobservable(t) for t in texts if t.strip()) and is_unobservable(combined):
            yield Issue(
                code="unobservable_criterion",
                path=f"{path}[{index}]",
                message="criterion wording is vague and names no observable evidence",
            )


def _duplicate_alternative_warnings(rubric: Rubric) -> Iterator[Issue]:
    seen: dict[str, str] = {}
    for index, alt in enumerate(rubric.alternatives):
        key = _normalized(alt.text)
        if not key:
            continue
        if key in seen:
            yield Issue(
                code="duplicate_alternative",
                path=f"alternatives[{index}]",
                message=f"same text as alternative {seen[key]!r}",
            )
        else:
            seen[key] = alt.id
