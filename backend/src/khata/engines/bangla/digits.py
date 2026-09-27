"""Bangla digit normalisation (TR-BN-02): ০–৯ <-> 0–9."""

from __future__ import annotations

BANGLA_DIGITS = "০১২৩৪৫৬৭৮৯"
LATIN_DIGITS = "0123456789"

_TO_LATIN = str.maketrans(BANGLA_DIGITS, LATIN_DIGITS)
_TO_BANGLA = str.maketrans(LATIN_DIGITS, BANGLA_DIGITS)


def to_latin_digits(text: str) -> str:
    """Replace every Bangla digit with its Latin counterpart; other text is kept."""
    return text.translate(_TO_LATIN)


def to_bangla_digits(text: str) -> str:
    """Replace every Latin digit with its Bangla counterpart; other text is kept."""
    return text.translate(_TO_BANGLA)


def has_bangla_digits(text: str) -> bool:
    return any(ch in BANGLA_DIGITS for ch in text)
