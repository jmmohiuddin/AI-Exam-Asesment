"""Units for Grade 9–10 Maths and Physics (TR-MATH-01).

A closed lexicon rather than a general unit library: the MVP's syllabus uses a few
dozen units, the Bangla names have to be curated by hand anyway, and a table that
fits on a screen is one a physics teacher can check. Adding SI prefixes to that
table is where a general library would earn its place; until then this stays
dependency-free and auditable.

Scales are :class:`~fractions.Fraction`, so km→m and km/h→m/s are exact.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from fractions import Fraction

from khata.engines.bangla.digits import to_latin_digits

SUPERSCRIPTS = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹⁻", "0123456789-")


@dataclass(frozen=True, slots=True)
class Dimension:
    """Exponents of the SI base quantities this lexicon needs."""

    length: int = 0
    mass: int = 0
    time: int = 0
    current: int = 0
    temperature: int = 0

    def __mul__(self, other: Dimension) -> Dimension:
        return Dimension(
            length=self.length + other.length,
            mass=self.mass + other.mass,
            time=self.time + other.time,
            current=self.current + other.current,
            temperature=self.temperature + other.temperature,
        )

    def power(self, exponent: int) -> Dimension:
        return Dimension(
            length=self.length * exponent,
            mass=self.mass * exponent,
            time=self.time * exponent,
            current=self.current * exponent,
            temperature=self.temperature * exponent,
        )

    @property
    def is_dimensionless(self) -> bool:
        return self == Dimension()


@dataclass(frozen=True, slots=True)
class Unit:
    """A dimension plus the factor that takes it to SI base units."""

    dimension: Dimension
    scale: Fraction

    def __mul__(self, other: Unit) -> Unit:
        return Unit(self.dimension * other.dimension, self.scale * other.scale)

    def power(self, exponent: int) -> Unit:
        return Unit(self.dimension.power(exponent), self.scale**exponent)


DIMENSIONLESS = Unit(Dimension(), Fraction(1))

_LENGTH = Dimension(length=1)
_MASS = Dimension(mass=1)
_TIME = Dimension(time=1)
_FORCE = Dimension(mass=1, length=1, time=-2)
_ENERGY = Dimension(mass=1, length=2, time=-2)
_POWER = Dimension(mass=1, length=2, time=-3)
_PRESSURE = Dimension(mass=1, length=-1, time=-2)

#: symbol or name -> (dimension, scale to SI base). Bangla names sit beside the
#: symbols deliberately: a Bangla-medium student writes মিটার, not m.
LEXICON: dict[str, tuple[Dimension, Fraction]] = {
    # length
    "m": (_LENGTH, Fraction(1)),
    "metre": (_LENGTH, Fraction(1)),
    "meter": (_LENGTH, Fraction(1)),
    "মিটার": (_LENGTH, Fraction(1)),
    "km": (_LENGTH, Fraction(1000)),
    "কিলোমিটার": (_LENGTH, Fraction(1000)),
    "cm": (_LENGTH, Fraction(1, 100)),
    "সেন্টিমিটার": (_LENGTH, Fraction(1, 100)),
    "mm": (_LENGTH, Fraction(1, 1000)),
    "মিলিমিটার": (_LENGTH, Fraction(1, 1000)),
    # mass
    "kg": (_MASS, Fraction(1)),
    "কিলোগ্রাম": (_MASS, Fraction(1)),
    "g": (_MASS, Fraction(1, 1000)),
    "gram": (_MASS, Fraction(1, 1000)),
    "গ্রাম": (_MASS, Fraction(1, 1000)),
    "mg": (_MASS, Fraction(1, 1_000_000)),
    "t": (_MASS, Fraction(1000)),
    # time
    "s": (_TIME, Fraction(1)),
    "sec": (_TIME, Fraction(1)),
    "second": (_TIME, Fraction(1)),
    "সেকেন্ড": (_TIME, Fraction(1)),
    "min": (_TIME, Fraction(60)),
    "মিনিট": (_TIME, Fraction(60)),
    "h": (_TIME, Fraction(3600)),
    "hr": (_TIME, Fraction(3600)),
    "ঘণ্টা": (_TIME, Fraction(3600)),
    # electrical and thermal
    "A": (Dimension(current=1), Fraction(1)),
    "অ্যাম্পিয়ার": (Dimension(current=1), Fraction(1)),
    "K": (Dimension(temperature=1), Fraction(1)),
    "কেলভিন": (Dimension(temperature=1), Fraction(1)),
    "V": (Dimension(mass=1, length=2, time=-3, current=-1), Fraction(1)),
    "ভোল্ট": (Dimension(mass=1, length=2, time=-3, current=-1), Fraction(1)),
    "ohm": (Dimension(mass=1, length=2, time=-3, current=-2), Fraction(1)),
    "Ω": (Dimension(mass=1, length=2, time=-3, current=-2), Fraction(1)),
    # derived mechanics
    "N": (_FORCE, Fraction(1)),
    "নিউটন": (_FORCE, Fraction(1)),
    "kN": (_FORCE, Fraction(1000)),
    "J": (_ENERGY, Fraction(1)),
    "জুল": (_ENERGY, Fraction(1)),
    "kJ": (_ENERGY, Fraction(1000)),
    "W": (_POWER, Fraction(1)),
    "ওয়াট": (_POWER, Fraction(1)),
    "kW": (_POWER, Fraction(1000)),
    "Pa": (_PRESSURE, Fraction(1)),
    "প্যাসকেল": (_PRESSURE, Fraction(1)),
    "kPa": (_PRESSURE, Fraction(1000)),
    "Hz": (Dimension(time=-1), Fraction(1)),
    "হার্জ": (Dimension(time=-1), Fraction(1)),
}

_FACTOR = re.compile(r"^(?P<symbol>[^\s^*/0-9-]+)(?:\s*(?:\^|\*\*)?\s*(?P<exponent>-?\d+))?$")


def parse_unit(text: str | None) -> Unit | None:
    """Parse ``m/s^2``, ``kg m/s²``, ``ms^-1``. Unknown symbols give ``None``."""
    if text is None:
        return None
    cleaned = text.strip().translate(SUPERSCRIPTS)
    if not cleaned:
        return None
    numerator, _, denominator = cleaned.partition("/")
    if "/" in denominator:  # a/b/c is ambiguous; refuse rather than guess
        return None
    top = _parse_product(numerator)
    if top is None:
        return None
    if not denominator:
        return top
    bottom = _parse_product(denominator)
    if bottom is None:
        return None
    return top * bottom.power(-1)


def _parse_product(text: str) -> Unit | None:
    factors = [part for part in re.split(r"[\s*·]+", text.strip()) if part]
    if not factors:
        return None
    result = DIMENSIONLESS
    for factor in factors:
        parsed = _parse_factor(factor)
        if parsed is None:
            return None
        result = result * parsed
    return result


def _parse_factor(text: str) -> Unit | None:
    match = _FACTOR.match(to_latin_digits(text))
    if match is None:
        return None
    entry = LEXICON.get(match["symbol"])
    if entry is None:
        return None
    dimension, scale = entry
    unit = Unit(dimension, scale)
    return unit if match["exponent"] is None else unit.power(int(match["exponent"]))


def same_dimension(left: Unit | None, right: Unit | None) -> bool:
    """A missing unit is not a wildcard: it never matches a required one."""
    if left is None or right is None:
        return False
    return left.dimension == right.dimension


def convert(value: Fraction, source: Unit | None, target: Unit | None) -> Fraction | None:
    """``value`` expressed in ``target``, or ``None`` if the dimensions differ."""
    if not same_dimension(source, target):
        return None
    assert source is not None and target is not None  # narrowed by same_dimension
    return value * source.scale / target.scale
