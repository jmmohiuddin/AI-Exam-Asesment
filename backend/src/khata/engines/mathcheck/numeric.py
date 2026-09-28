"""Verification badges for one answer (FR-AI-05, TR-MATH-01).

Badges are evidence a teacher can read, not a score. Two rules keep them honest:

* **A badge is earned deterministically or not at all.** If the student's text, the
  key or either unit does not parse, the answer is ``cannot_verify`` — never
  ``value_differs``. An unreadable answer is not a wrong one, and the specification
  is explicit that "cannot verify" must not reduce a suggestion by itself.
* **A required unit is part of the answer.** A right number with no unit still
  matches on value, and the ``value_matches`` badge says so, but ``matches`` is
  false and the rubric's deduction applies. The teacher sees both facts.

Expressions and equations need a CAS in a sandbox (TR-MATH-02/03/05) and are not
implemented; they report ``cannot_verify`` rather than pretending.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from enum import StrEnum
from fractions import Fraction

from khata.engines.mathcheck.numbers import ParsedNumber, parse_number
from khata.engines.mathcheck.units import Unit, convert, parse_unit, same_dimension
from khata.engines.rubric import AnswerKind, AnswerSpec, SigFigMode

ZERO = Decimal(0)


class Badge(StrEnum):
    VALUE_MATCHES = "value_matches"
    VALUE_DIFFERS = "value_differs"
    UNIT_MISSING = "unit_missing"
    UNIT_WRONG = "unit_wrong"
    UNIT_CONVERTED = "unit_converted"
    SIG_FIGS_SHORT = "sig_figs_short"
    CANNOT_VERIFY = "cannot_verify"


@dataclass(frozen=True, slots=True)
class AnswerCheck:
    badges: tuple[Badge, ...]
    matches: bool
    unit_deduction: Decimal = ZERO
    #: The student's value converted into the key's unit, for the review card.
    normalized: Fraction | None = field(default=None)


_CANNOT_VERIFY = AnswerCheck(badges=(Badge.CANNOT_VERIFY,), matches=False)


def check_answer(spec: AnswerSpec, student_text: str) -> AnswerCheck:
    if spec.kind is AnswerKind.MCQ:
        return _check_mcq(spec, student_text)
    if spec.kind is not AnswerKind.NUMERIC:
        # TR-MATH-02/03: expression and equation checking need a sandboxed CAS.
        return _CANNOT_VERIFY
    return _check_numeric(spec, student_text)


def _check_mcq(spec: AnswerSpec, student_text: str) -> AnswerCheck:
    chosen = student_text.strip()
    if not chosen or (spec.options and chosen not in spec.options):
        return _CANNOT_VERIFY
    matches = chosen == spec.value.strip()
    return AnswerCheck(
        badges=(Badge.VALUE_MATCHES if matches else Badge.VALUE_DIFFERS,), matches=matches
    )


def _check_numeric(spec: AnswerSpec, student_text: str) -> AnswerCheck:
    key = parse_number(spec.value)
    if key is None:
        return _CANNOT_VERIFY
    key_unit = parse_unit(spec.unit) if spec.unit else None
    if spec.unit and key_unit is None:
        return _CANNOT_VERIFY

    value_text, unit_text = _split(student_text)
    student = parse_number(value_text)
    if student is None:
        return _CANNOT_VERIFY

    student_unit = parse_unit(unit_text) if unit_text else None
    if unit_text and student_unit is None:
        return _CANNOT_VERIFY

    badges: list[Badge] = []
    comparable, unit_ok, deduction = _reconcile_units(
        spec, student.value, key_unit, student_unit, badges
    )
    if comparable is None:
        return AnswerCheck(badges=tuple(badges), matches=False, unit_deduction=deduction)

    value_ok = _within_tolerance(comparable, key.value, spec)
    badges.append(Badge.VALUE_MATCHES if value_ok else Badge.VALUE_DIFFERS)
    if value_ok and not _sig_figs_ok(student, spec):
        badges.append(Badge.SIG_FIGS_SHORT)

    return AnswerCheck(
        badges=tuple(badges),
        matches=value_ok and unit_ok,
        unit_deduction=deduction,
        normalized=comparable,
    )


def _reconcile_units(
    spec: AnswerSpec,
    value: Fraction,
    key_unit: Unit | None,
    student_unit: Unit | None,
    badges: list[Badge],
) -> tuple[Fraction | None, bool, Decimal]:
    """Return the student's value in the key's unit, whether the unit is acceptable,
    and the deduction a missing unit earns."""
    if key_unit is None:
        return value, True, ZERO
    if student_unit is None:
        if not spec.unit_required:
            # The rubric already decided the unit does not matter here; saying
            # "unit missing" on the card would be noise the teacher must dismiss.
            return value, True, ZERO
        badges.append(Badge.UNIT_MISSING)
        # Still comparable: the teacher should see whether the number was right.
        return value, False, spec.missing_unit_deduction
    if not same_dimension(student_unit, key_unit):
        badges.append(Badge.UNIT_WRONG)
        return None, False, ZERO
    converted = convert(value, student_unit, key_unit)
    if converted is None:  # pragma: no cover - same_dimension already proved it
        return None, False, ZERO
    if student_unit.scale != key_unit.scale:
        badges.append(Badge.UNIT_CONVERTED)
    return converted, True, ZERO


def _split(text: str) -> tuple[str, str]:
    """Separate the number from the unit at the first character that cannot start
    a number. Splitting on whitespace alone would lose ``9.8m/s^2``."""
    stripped = text.strip()
    for index, char in enumerate(stripped):
        if index and char not in "0123456789.,/ \t^*x×eE+-" and not _is_digit_like(char):
            return stripped[:index].strip(), stripped[index:].strip()
    return stripped, ""


def _is_digit_like(char: str) -> bool:
    return char in "০১২৩৪৫৬৭৮৯⁰¹²³⁴⁵⁶⁷⁸⁹⁻" or char.isdigit()


def _within_tolerance(student: Fraction, key: Fraction, spec: AnswerSpec) -> bool:
    difference = abs(student - key)
    if spec.tolerance is None:
        return difference == 0
    if spec.tolerance.abs is not None and difference <= Fraction(spec.tolerance.abs):
        return True
    if spec.tolerance.rel is not None and key != 0:
        return difference / abs(key) <= Fraction(spec.tolerance.rel)
    return difference == 0


def _sig_figs_ok(student: ParsedNumber, spec: AnswerSpec) -> bool:
    policy = spec.sig_figs
    if policy.mode is SigFigMode.IGNORE or policy.count is None:
        return True
    if student.sig_figs is None:  # a fraction has no written precision to judge
        return True
    if policy.mode is SigFigMode.AT_LEAST:
        return student.sig_figs >= policy.count
    return student.sig_figs == policy.count
