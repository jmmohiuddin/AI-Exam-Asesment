"""Read the number a student wrote (TR-MATH-01, TR-BN-02).

Scripts are handwritten and transcribed, so the input is whatever the page said:
Bangla or Latin numerals, ``3/4`` or ``0.75``, ``1 1/2``, ``3 × 10⁸`` or ``3e8``,
and digit grouping that is 2-2-3 in Bangladesh rather than 3-3-3 — which is why
separators are stripped rather than validated.

Values are :class:`~fractions.Fraction`, so ``1/3`` stays exact and never drifts
the way a float would before a tolerance is applied. Anything that does not parse
cleanly returns ``None``; the caller then reports "cannot verify", which is the
honest answer and the one the specification asks for.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from fractions import Fraction

from khata.engines.bangla.digits import to_latin_digits

SUPERSCRIPTS = "⁰¹²³⁴⁵⁶⁷⁸⁹"
_SUPERSCRIPT_TO_DIGIT = str.maketrans(SUPERSCRIPTS, "0123456789")
_MINUS_SIGNS = {"−": "-", "–": "-", "—": "-", "⁻": "-"}

# 3 x 10^8, 3 × 10⁸, 3*10^8 — the forms a student writes for scientific notation.
_TIMES_POWER = re.compile(
    r"^(?P<mantissa>[^x×*]+?)\s*[x×*]\s*10\s*(?:\^|\*\*)?\s*(?P<exponent>[+-]?\d+)$",
    re.IGNORECASE,
)
_E_NOTATION = re.compile(r"^(?P<mantissa>[+-]?[\d.]+)[eE](?P<exponent>[+-]?\d+)$")
_MIXED = re.compile(r"^(?P<sign>[+-]?)\s*(?P<whole>\d+)\s+(?P<num>\d+)\s*/\s*(?P<den>\d+)$")
_RATIO = re.compile(r"^(?P<sign>[+-]?)\s*(?P<num>\d+)\s*/\s*(?P<den>\d+)$")
_DECIMAL = re.compile(r"^(?P<sign>[+-]?)(?P<int>\d*)(?:\.(?P<frac>\d*))?$")


@dataclass(frozen=True, slots=True)
class ParsedNumber:
    """An exact value, plus how precisely it was written.

    ``sig_figs`` is ``None`` when the question does not arise — a fraction has no
    written precision to count, so a significant-figure policy cannot judge it.
    """

    value: Fraction
    sig_figs: int | None


def parse_number(text: str) -> ParsedNumber | None:
    cleaned = _clean(text)
    if not cleaned:
        return None
    for parser in (_parse_power_of_ten, _parse_e_notation, _parse_mixed, _parse_ratio):
        parsed = parser(cleaned)
        if parsed is not None:
            return parsed
    return _parse_decimal(cleaned)


def _clean(text: str) -> str:
    cleaned = to_latin_digits(text).strip()
    for sign, replacement in _MINUS_SIGNS.items():
        cleaned = cleaned.replace(sign, replacement)
    cleaned = cleaned.translate(_SUPERSCRIPT_TO_DIGIT)
    # Grouping separators only: a comma or space *between digits*. A trailing or
    # leading one is noise and should fail the parse rather than be swallowed.
    cleaned = re.sub(r"(?<=\d)[,  ](?=\d)", "", cleaned)
    return re.sub(r"(?<=\d) +(?=\d\d\d(\D|$))", "", cleaned)


def _parse_power_of_ten(text: str) -> ParsedNumber | None:
    match = _TIMES_POWER.match(text)
    if match is None:
        return None
    mantissa = _parse_decimal(match["mantissa"].strip())
    if mantissa is None:
        return None
    return ParsedNumber(
        value=mantissa.value * Fraction(10) ** int(match["exponent"]),
        sig_figs=mantissa.sig_figs,
    )


def _parse_e_notation(text: str) -> ParsedNumber | None:
    match = _E_NOTATION.match(text)
    if match is None:
        return None
    mantissa = _parse_decimal(match["mantissa"])
    if mantissa is None:
        return None
    return ParsedNumber(
        value=mantissa.value * Fraction(10) ** int(match["exponent"]),
        sig_figs=mantissa.sig_figs,
    )


def _parse_mixed(text: str) -> ParsedNumber | None:
    match = _MIXED.match(text)
    if match is None:
        return None
    denominator = int(match["den"])
    if denominator == 0:
        return None
    magnitude = int(match["whole"]) + Fraction(int(match["num"]), denominator)
    return ParsedNumber(value=-magnitude if match["sign"] == "-" else magnitude, sig_figs=None)


def _parse_ratio(text: str) -> ParsedNumber | None:
    match = _RATIO.match(text)
    if match is None:
        return None
    denominator = int(match["den"])
    if denominator == 0:
        return None
    magnitude = Fraction(int(match["num"]), denominator)
    return ParsedNumber(value=-magnitude if match["sign"] == "-" else magnitude, sig_figs=None)


def _parse_decimal(text: str) -> ParsedNumber | None:
    match = _DECIMAL.match(text)
    if match is None:
        return None
    whole, frac = match["int"] or "", match["frac"]
    if not whole and not frac:
        return None
    digits = f"{whole}{frac or ''}"
    value = Fraction(int(digits), 10 ** len(frac or ""))
    if match["sign"] == "-":
        value = -value
    return ParsedNumber(value=value, sig_figs=_significant_figures(whole, frac))


def _significant_figures(whole: str, frac: str | None) -> int:
    """Count as written: leading zeros never count, trailing zeros count once a
    decimal point is present. ``100`` is read as 3 — schools write it that way, and
    a student who meant 1 significant figure would write ``1 × 10²``."""
    if frac is not None:
        digits = f"{whole}{frac}".lstrip("0")
        return len(digits) if digits else 1
    stripped = whole.lstrip("0")
    return len(stripped) if stripped else 1
