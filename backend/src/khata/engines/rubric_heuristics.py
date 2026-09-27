"""Text heuristics for rubric authoring warnings (FR-RUB-07).

A criterion is *unobservable* when its wording relies on a vague quality word
("good explanation", "ভালো ব্যাখ্যা", "properly", "সঠিকভাবে") without naming
anything a marker could point at in the script (a formula, value, unit, number,
diagram, ...). This is a warning heuristic, never an error.
"""

from __future__ import annotations

import re
import unicodedata

VAGUE_EN = (
    "good",
    "well",
    "properly",
    "proper",
    "correctly",
    "appropriate",
    "appropriately",
    "adequate",
    "adequately",
    "sufficient",
    "sufficiently",
    "clear",
    "clearly",
    "nice",
    "nicely",
    "satisfactory",
    "reasonable",
    "meaningful",
    "understanding",
    "understands",
)

VAGUE_BN = (
    "ভালো",
    "ভাল",
    "সঠিকভাবে",
    "যথাযথ",
    "যথাযথভাবে",
    "সুন্দর",
    "সুন্দরভাবে",
    "স্পষ্ট",
    "স্পষ্টভাবে",
    "পর্যাপ্ত",
    "বোঝে",
    "বুঝেছে",
    "ধারণা",
)

OBSERVABLE_EN_STEMS = (
    "formula",
    "equation",
    "value",
    "unit",
    "diagram",
    "label",
    "graph",
    "definition",
    "example",
    "step",
    "substitut",
    "answer",
    "result",
    "law",
    "term",
    "symbol",
    "sign",
    "figure",
    "table",
    "calculation",
    "number",
    "name",
    "keyword",
)

OBSERVABLE_BN = (
    "সূত্র",
    "সমীকরণ",
    "মান",
    "একক",
    "চিত্র",
    "লেখচিত্র",
    "সংজ্ঞা",
    "উদাহরণ",
    "ধাপ",
    "উত্তর",
    "ফলাফল",
    "নাম",
    "প্রতীক",
    "হিসাব",
    "সংখ্যা",
    "নীতি",
)

_WORD = re.compile(r"[\wঀ-৿]+", re.UNICODE)
_MATHY = re.compile(r"[0-9০-৯=+\-×÷/^√∑π]")


def _words(text: str) -> list[str]:
    return [w.casefold() for w in _WORD.findall(unicodedata.normalize("NFC", text))]


def has_vague_term(text: str) -> bool:
    words = set(_words(text))
    return any(term in words for term in VAGUE_EN) or any(
        term in words for term in VAGUE_BN
    )


def names_observable_object(text: str) -> bool:
    normalized = unicodedata.normalize("NFC", text)
    if _MATHY.search(normalized):
        return True
    words = _words(normalized)
    if any(word.startswith(stem) for word in words for stem in OBSERVABLE_EN_STEMS):
        return True
    return any(term in normalized for term in OBSERVABLE_BN)


def is_unobservable(text: str) -> bool:
    """True when ``text`` uses a vague quality word and names nothing observable."""
    return has_vague_term(text) and not names_observable_object(text)
