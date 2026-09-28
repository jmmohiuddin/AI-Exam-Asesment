"""Numeric verification badges (FR-AI-05, TR-MATH-01)."""

from __future__ import annotations

from decimal import Decimal
from typing import Any

import pytest

from khata.engines.mathcheck.numeric import Badge, check_answer
from khata.engines.rubric import AnswerKind, AnswerSpec

D = Decimal


def spec(**overrides: Any) -> AnswerSpec:
    data: dict[str, Any] = {
        "kind": AnswerKind.NUMERIC,
        "value": "9.8",
        "unit": "m/s^2",
        "tolerance": {"abs": "0.1"},
    }
    data.update(overrides)
    return AnswerSpec.model_validate(data)


class TestValueMatching:
    def test_the_exact_value_with_the_right_unit_matches(self) -> None:
        result = check_answer(spec(), "9.8 m/s^2")
        assert Badge.VALUE_MATCHES in result.badges
        assert result.matches

    def test_a_value_inside_the_absolute_tolerance_matches(self) -> None:
        assert check_answer(spec(), "9.9 m/s^2").matches
        assert check_answer(spec(), "9.7 m/s^2").matches

    def test_a_value_outside_the_tolerance_differs(self) -> None:
        result = check_answer(spec(), "9.5 m/s^2")
        assert Badge.VALUE_DIFFERS in result.badges
        assert not result.matches

    def test_relative_tolerance(self) -> None:
        relative = spec(tolerance={"rel": "0.01"}, value="100", unit="m")
        assert check_answer(relative, "100.5 m").matches
        assert not check_answer(relative, "102 m").matches

    def test_either_tolerance_passing_is_enough(self) -> None:
        both = spec(tolerance={"abs": "0.1", "rel": "0.05"}, value="100", unit="m")
        assert check_answer(both, "104 m").matches  # inside 5% though far outside 0.1

    def test_without_a_tolerance_the_value_must_be_exact(self) -> None:
        exact = spec(tolerance=None, value="5", unit="m")
        assert check_answer(exact, "5 m").matches
        assert not check_answer(exact, "5.01 m").matches

    def test_a_fraction_answer_equals_its_decimal(self) -> None:
        half = spec(tolerance=None, value="0.5", unit=None, unit_required=False)
        assert check_answer(half, "1/2").matches
        assert check_answer(half, "50/100").matches

    def test_scientific_notation_matches_the_plain_form(self) -> None:
        big = spec(tolerance=None, value="300000000", unit="m/s")
        assert check_answer(big, "3 x 10^8 m/s").matches

    def test_bangla_numerals_match(self) -> None:
        assert check_answer(spec(), "৯.৮ m/s^2").matches


class TestUnits:
    def test_a_correct_unit_in_a_different_scale_is_converted_and_flagged(self) -> None:
        speed = spec(tolerance=None, value="20", unit="m/s")
        result = check_answer(speed, "72 km/h")
        assert result.matches
        assert Badge.UNIT_CONVERTED in result.badges

    def test_a_missing_unit_is_flagged_but_the_value_is_still_checked(self) -> None:
        result = check_answer(spec(), "9.8")
        assert Badge.UNIT_MISSING in result.badges
        assert Badge.VALUE_MATCHES in result.badges
        assert not result.matches, "a required unit is part of the answer"

    def test_a_missing_unit_carries_the_rubric_deduction(self) -> None:
        result = check_answer(spec(missing_unit_deduction="1"), "9.8")
        assert result.unit_deduction == D(1)

    def test_no_deduction_when_the_unit_is_there(self) -> None:
        result = check_answer(spec(missing_unit_deduction="1"), "9.8 m/s^2")
        assert result.unit_deduction == D(0)

    def test_a_unit_of_the_wrong_dimension_is_wrong_not_missing(self) -> None:
        result = check_answer(spec(), "9.8 m/s")
        assert Badge.UNIT_WRONG in result.badges
        assert Badge.UNIT_MISSING not in result.badges
        assert not result.matches

    def test_an_optional_unit_may_be_omitted(self) -> None:
        optional = spec(unit_required=False)
        result = check_answer(optional, "9.8")
        assert result.matches
        assert Badge.UNIT_MISSING not in result.badges

    def test_an_unknown_unit_cannot_be_verified(self) -> None:
        result = check_answer(spec(), "9.8 bananas")
        assert Badge.CANNOT_VERIFY in result.badges
        assert not result.matches


class TestSignificantFigures:
    def test_ignored_by_default(self) -> None:
        loose = spec(tolerance={"abs": "0.5"})
        assert check_answer(loose, "10 m/s^2").matches

    def test_at_least_flags_too_few_digits(self) -> None:
        policy = spec(sig_figs={"mode": "at_least", "count": 3}, tolerance={"abs": "0.5"})
        short = check_answer(policy, "9.8 m/s^2")
        assert Badge.SIG_FIGS_SHORT in short.badges
        assert check_answer(policy, "9.81 m/s^2").badges.count(Badge.SIG_FIGS_SHORT) == 0

    def test_exact_flags_any_other_count(self) -> None:
        policy = spec(sig_figs={"mode": "exact", "count": 2}, tolerance={"abs": "0.5"})
        assert Badge.SIG_FIGS_SHORT in check_answer(policy, "9.812 m/s^2").badges
        assert Badge.SIG_FIGS_SHORT not in check_answer(policy, "9.8 m/s^2").badges

    def test_a_fraction_is_never_judged_on_significant_figures(self) -> None:
        policy = spec(
            sig_figs={"mode": "at_least", "count": 3},
            tolerance=None,
            value="0.5",
            unit=None,
            unit_required=False,
        )
        assert Badge.SIG_FIGS_SHORT not in check_answer(policy, "1/2").badges


class TestCannotVerify:
    @pytest.mark.parametrize("text", ["", "   ", "about ten", "?", "I don't know"])
    def test_unreadable_answers_are_never_marked_wrong(self, text: str) -> None:
        result = check_answer(spec(), text)
        assert result.badges == (Badge.CANNOT_VERIFY,)
        assert not result.matches
        assert Badge.VALUE_DIFFERS not in result.badges

    def test_a_key_that_does_not_parse_cannot_verify_anything(self) -> None:
        broken = spec(value="roughly ten")
        assert check_answer(broken, "9.8 m/s^2").badges == (Badge.CANNOT_VERIFY,)

    def test_a_key_with_an_unknown_unit_cannot_verify(self) -> None:
        broken = spec(unit="bananas")
        assert Badge.CANNOT_VERIFY in check_answer(broken, "9.8 m/s^2").badges

    @pytest.mark.parametrize("kind", [AnswerKind.EXPRESSION, AnswerKind.EQUATION])
    def test_expressions_and_equations_are_not_claimed_as_checked(self, kind: AnswerKind) -> None:
        """TR-MATH-02/03 need a CAS in a sandbox; until then, say so."""
        result = check_answer(spec(kind=kind, value="x+x"), "2x")
        assert result.badges == (Badge.CANNOT_VERIFY,)
        assert not result.matches


class TestMcq:
    def test_the_chosen_option_matches_the_key(self) -> None:
        mcq = spec(
            kind=AnswerKind.MCQ,
            value="ka",
            unit=None,
            tolerance=None,
            options=("ka", "kha", "ga", "gha"),
        )
        assert check_answer(mcq, "ka").matches
        assert not check_answer(mcq, "kha").matches

    def test_bangla_option_letters(self) -> None:
        mcq = spec(
            kind=AnswerKind.MCQ, value="ক", unit=None, tolerance=None, options=("ক", "খ", "গ", "ঘ")
        )
        assert check_answer(mcq, "ক").matches
        assert check_answer(mcq, " ক ").matches

    def test_an_answer_outside_the_options_cannot_be_verified(self) -> None:
        mcq = spec(
            kind=AnswerKind.MCQ, value="ka", unit=None, tolerance=None, options=("ka", "kha")
        )
        assert Badge.CANNOT_VERIFY in check_answer(mcq, "zz").badges
