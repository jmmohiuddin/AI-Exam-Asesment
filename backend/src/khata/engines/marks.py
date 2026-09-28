"""Exact mark arithmetic shared by the scoring and result engines.

Marks are :class:`~decimal.Decimal` at every interface. Divisions (percentages,
weighted combinations, averages) are carried out on :class:`fractions.Fraction`
so that no intermediate value is ever approximated; rounding happens once, at
the stage a policy names, via :func:`round_exact`. Floats are rejected.
"""

from __future__ import annotations

from decimal import Decimal
from enum import StrEnum
from fractions import Fraction

Number = Decimal | Fraction | int

HALF = Fraction(1, 2)


class RoundingMode(StrEnum):
    HALF_UP = "half_up"  # ties away from zero (school default)
    HALF_EVEN = "half_even"
    DOWN = "down"  # toward zero (truncate)
    UP = "up"  # away from zero
    NONE = "none"  # keep the exact value


def to_fraction(value: Number) -> Fraction:
    """Convert an exact number to a Fraction; floats and bools are refused."""
    if isinstance(value, bool | float):
        raise TypeError(f"inexact or boolean value not allowed in mark arithmetic: {value!r}")
    if isinstance(value, Decimal):
        if not value.is_finite():
            raise ValueError(f"non-finite decimal: {value!r}")
        return Fraction(value)
    return Fraction(value)


def _round_integer(scaled: Fraction, mode: RoundingMode) -> int:
    sign = -1 if scaled < 0 else 1
    magnitude = abs(scaled)
    floor_ = magnitude.numerator // magnitude.denominator
    remainder = magnitude - floor_
    if mode is RoundingMode.DOWN or remainder == 0:
        bump = 0
    elif mode is RoundingMode.UP:
        bump = 1
    elif mode is RoundingMode.HALF_UP:
        bump = 1 if remainder >= HALF else 0
    elif remainder != HALF:
        bump = 1 if remainder > HALF else 0
    else:  # HALF_EVEN tie
        bump = floor_ % 2
    return sign * (floor_ + bump)


def round_exact(value: Number, quantum: Decimal, mode: RoundingMode) -> Decimal:
    """Round ``value`` to a multiple of ``quantum`` using ``mode``, exactly.

    With :attr:`RoundingMode.NONE` the value must already be a finite decimal.
    """
    exact = to_fraction(value)
    if quantum <= 0:
        raise ValueError(f"rounding quantum must be positive: {quantum}")
    if mode is RoundingMode.NONE:
        return fraction_to_decimal(exact)
    units = _round_integer(exact / to_fraction(quantum), mode)
    return normalize_decimal(Decimal(units) * quantum)


def fraction_to_decimal(value: Fraction) -> Decimal:
    """Exact Decimal for a Fraction whose denominator has only factors 2 and 5."""
    denominator = value.denominator
    for prime in (2, 5):
        while denominator % prime == 0:
            denominator //= prime
    if denominator != 1:
        raise ValueError(f"{value} has no finite decimal representation; round it first")
    scale = 0
    while (value * 10**scale).denominator != 1:
        scale += 1
    return normalize_decimal(Decimal((value * 10**scale).numerator).scaleb(-scale))


def normalize_decimal(value: Decimal) -> Decimal:
    """Canonical Decimal without exponent noise: 17.0 -> 17, 1E+1 -> 10."""
    if value == value.to_integral_value():
        return Decimal(int(value))
    return value.normalize()


def is_multiple_of(value: Number, quantum: Decimal) -> bool:
    return (to_fraction(value) / to_fraction(quantum)).denominator == 1
