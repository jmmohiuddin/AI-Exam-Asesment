"""Units: the Bangla/English lexicon, dimensions and conversion (TR-MATH-01)."""

from __future__ import annotations

from fractions import Fraction

import pytest

from khata.engines.mathcheck.units import (
    Dimension,
    convert,
    parse_unit,
    same_dimension,
)

F = Fraction


class TestLexicon:
    @pytest.mark.parametrize(
        ("text", "dimension"),
        [
            ("m", Dimension(length=1)),
            ("km", Dimension(length=1)),
            ("cm", Dimension(length=1)),
            ("s", Dimension(time=1)),
            ("kg", Dimension(mass=1)),
            ("g", Dimension(mass=1)),
            ("N", Dimension(mass=1, length=1, time=-2)),
            ("J", Dimension(mass=1, length=2, time=-2)),
            ("W", Dimension(mass=1, length=2, time=-3)),
            ("Pa", Dimension(mass=1, length=-1, time=-2)),
            ("A", Dimension(current=1)),
            ("K", Dimension(temperature=1)),
        ],
    )
    def test_base_and_derived_units(self, text: str, dimension: Dimension) -> None:
        unit = parse_unit(text)
        assert unit is not None
        assert unit.dimension == dimension

    @pytest.mark.parametrize(
        ("bangla", "english"),
        [("মিটার", "m"), ("সেকেন্ড", "s"), ("কিলোগ্রাম", "kg"), ("নিউটন", "N"), ("জুল", "J")],
    )
    def test_bangla_names_resolve_to_the_same_unit(self, bangla: str, english: str) -> None:
        left, right = parse_unit(bangla), parse_unit(english)
        assert left is not None and right is not None
        assert left.dimension == right.dimension
        assert left.scale == right.scale

    def test_an_unknown_unit_is_none_rather_than_dimensionless(self) -> None:
        assert parse_unit("bananas") is None


class TestCompoundUnits:
    @pytest.mark.parametrize(
        ("text", "dimension"),
        [
            ("m/s", Dimension(length=1, time=-1)),
            ("m/s^2", Dimension(length=1, time=-2)),
            ("m/s²", Dimension(length=1, time=-2)),
            ("m s^-2", Dimension(length=1, time=-2)),
            ("kg m/s^2", Dimension(mass=1, length=1, time=-2)),
            ("N m", Dimension(mass=1, length=2, time=-2)),
            ("kg/m^3", Dimension(mass=1, length=-3)),
        ],
    )
    def test_products_quotients_and_powers(self, text: str, dimension: Dimension) -> None:
        unit = parse_unit(text)
        assert unit is not None
        assert unit.dimension == dimension

    @pytest.mark.parametrize("text", ["ms^-1", "kgm/s^2", "Nm"])
    def test_run_together_symbols_are_refused_rather_than_guessed(self, text: str) -> None:
        """``ms`` is metre-second to a physicist and millisecond as a symbol.

        Splitting it silently would decide a mark on a coin flip, so a product
        needs a separator (``m s^-1``, ``m/s``) and anything else is unparseable —
        which the checker reports as "cannot verify", never as a wrong answer.
        """
        assert parse_unit(text) is None

    def test_a_derived_unit_matches_its_expansion(self) -> None:
        assert same_dimension(parse_unit("N"), parse_unit("kg m/s^2"))
        assert same_dimension(parse_unit("J"), parse_unit("N m"))
        assert same_dimension(parse_unit("W"), parse_unit("J/s"))

    def test_different_dimensions_do_not_match(self) -> None:
        assert not same_dimension(parse_unit("m"), parse_unit("s"))
        assert not same_dimension(parse_unit("m/s"), parse_unit("m/s^2"))

    def test_a_missing_unit_never_matches(self) -> None:
        assert not same_dimension(None, parse_unit("m"))
        assert not same_dimension(parse_unit("m"), None)


class TestConversion:
    @pytest.mark.parametrize(
        ("value", "source", "target", "expected"),
        [
            (1, "km", "m", F(1000)),
            (100, "cm", "m", F(1)),
            (1, "m", "cm", F(100)),
            (1000, "g", "kg", F(1)),
            (1, "kg", "g", F(1000)),
            (1, "h", "s", F(3600)),
            (1, "min", "s", F(60)),
            (72, "km/h", "m/s", F(20)),
            (1, "kN", "N", F(1000)),
            (5, "m", "m", F(5)),
        ],
    )
    def test_scaling_is_exact(
        self, value: int, source: str, target: str, expected: Fraction
    ) -> None:
        converted = convert(F(value), parse_unit(source), parse_unit(target))
        assert converted == expected

    def test_converting_across_dimensions_is_refused(self) -> None:
        assert convert(F(1), parse_unit("m"), parse_unit("s")) is None

    def test_converting_without_a_unit_is_refused(self) -> None:
        assert convert(F(1), None, parse_unit("m")) is None
        assert convert(F(1), parse_unit("m"), None) is None
