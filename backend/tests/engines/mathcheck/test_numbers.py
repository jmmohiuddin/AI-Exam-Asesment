"""Parsing what a student actually writes (TR-MATH-01, TR-BN-02)."""

from __future__ import annotations

from fractions import Fraction

import pytest

from khata.engines.mathcheck.numbers import ParsedNumber, parse_number

F = Fraction


class TestPlainNumbers:
    @pytest.mark.parametrize(
        ("text", "value"),
        [
            ("5", F(5)),
            ("-5", F(-5)),
            ("+5", F(5)),
            ("0", F(0)),
            ("9.8", F(49, 5)),
            ("0.5", F(1, 2)),
            (".5", F(1, 2)),
            ("5.", F(5)),
            ("-0.25", F(-1, 4)),
            ("  12  ", F(12)),
        ],
    )
    def test_decimals(self, text: str, value: Fraction) -> None:
        parsed = parse_number(text)
        assert parsed is not None
        assert parsed.value == value


class TestBanglaDigits:
    @pytest.mark.parametrize(
        ("text", "value"),
        [("৫", F(5)), ("৯.৮", F(49, 5)), ("-৩", F(-3)), ("১০০০", F(1000))],
    )
    def test_bangla_numerals_parse_like_latin(self, text: str, value: Fraction) -> None:
        parsed = parse_number(text)
        assert parsed is not None
        assert parsed.value == value

    def test_a_bangla_decimal_separator_is_the_same_full_stop(self) -> None:
        assert parse_number("৩.১৪") == parse_number("3.14")


class TestFractions:
    @pytest.mark.parametrize(
        ("text", "value"),
        [
            ("1/2", F(1, 2)),
            ("3/4", F(3, 4)),
            ("-1/2", F(-1, 2)),
            ("10/5", F(2)),
            ("1 1/2", F(3, 2)),
            ("2 3/4", F(11, 4)),
            ("-1 1/2", F(-3, 2)),
            ("০.৫", F(1, 2)),
            ("১/২", F(1, 2)),
        ],
    )
    def test_fractions_and_mixed_numbers(self, text: str, value: Fraction) -> None:
        parsed = parse_number(text)
        assert parsed is not None
        assert parsed.value == value

    def test_division_by_zero_does_not_parse(self) -> None:
        assert parse_number("1/0") is None


class TestScientificNotation:
    @pytest.mark.parametrize(
        ("text", "value"),
        [
            ("1e3", F(1000)),
            ("1E3", F(1000)),
            ("1.5e2", F(150)),
            ("2e-3", F(1, 500)),
            ("6.02e23", F(602) * F(10) ** 21),
            ("3 x 10^8", F(3) * F(10) ** 8),
            ("3 × 10^8", F(3) * F(10) ** 8),
            ("3×10⁸", F(3) * F(10) ** 8),
            ("1.6 x 10^-19", F(16, 10) * F(10) ** -19),
        ],
    )
    def test_exponent_forms(self, text: str, value: Fraction) -> None:
        parsed = parse_number(text)
        assert parsed is not None
        assert parsed.value == value


class TestSeparatorsAndNoise:
    @pytest.mark.parametrize(
        ("text", "value"),
        [("1,000", F(1000)), ("12,34,567", F(1234567)), ("1 000", F(1000))],
    )
    def test_thousands_separators_are_ignored(self, text: str, value: Fraction) -> None:
        """Bangladeshi grouping is 2-2-3, so grouping cannot be validated by width."""
        parsed = parse_number(text)
        assert parsed is not None
        assert parsed.value == value

    @pytest.mark.parametrize("text", ["", "   ", "abc", "5 apples and 3", "--5", "5/", "/5", "?"])
    def test_unparseable_text_is_none_not_a_guess(self, text: str) -> None:
        assert parse_number(text) is None


class TestSignificantFigures:
    @pytest.mark.parametrize(
        ("text", "digits"),
        [
            ("9.8", 2),
            ("9.80", 3),
            ("0.0098", 2),
            ("100", 3),
            ("100.", 3),
            ("100.0", 4),
            ("1.60e-19", 3),
            ("0.5", 1),
            ("-9.81", 3),
        ],
    )
    def test_counted_from_what_was_written(self, text: str, digits: int) -> None:
        parsed = parse_number(text)
        assert parsed is not None
        assert parsed.sig_figs == digits

    def test_a_fraction_has_no_meaningful_significant_figures(self) -> None:
        parsed = parse_number("1/3")
        assert parsed is not None
        assert parsed.sig_figs is None


def test_parsed_number_is_immutable() -> None:
    parsed = parse_number("5")
    assert isinstance(parsed, ParsedNumber)
    with pytest.raises(AttributeError):
        parsed.value = Fraction(6)  # type: ignore[misc]
