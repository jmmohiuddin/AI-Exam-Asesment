"""Deterministic Fake marking provider for development and tests (ADR-006).

It never calls a network. For each criterion it looks for the criterion's expected
evidence in the answer text and decides ``met`` / ``not_met``; an empty answer is
``cannot_determine``, which makes :func:`score_item` set ``needs_teacher``.

Determinism is the point: the same answer and rubric always give the same
suggestion, so pipeline and review tests assert on real values rather than mocks.
"""

from __future__ import annotations

import re
import unicodedata
from decimal import Decimal

from khata.engines.bangla.digits import to_latin_digits
from khata.engines.scoring import CriterionDecision, Decision
from khata.modules.aigateway.provider import AnswerContext, Suggestion

MODEL_NAME = "fake-marker"
PROMPT_VERSION = "fake-v1"

# Tokens too common to be evidence of anything.
_STOPWORDS = frozenset(
    {
        "the", "a", "an", "of", "and", "or", "is", "are", "to", "in", "for",
        "that", "this", "it", "as", "be", "with", "on", "by", "from",
        "এবং", "বা", "এই", "সেই", "হয়", "করে", "থেকে", "জন্য",
    }
)
_MIN_TOKEN_LENGTH = 2
_TOKEN_RE = re.compile(r"[^\W_]+", re.UNICODE)

# Confidence is a flat function of agreement, deliberately never 1.0: an
# uncalibrated provider must not claim certainty (ADR-011).
_CONFIDENCE_FLOOR = Decimal("0.35")
_CONFIDENCE_CEILING = Decimal("0.90")


def _normalize(text: str) -> str:
    return to_latin_digits(unicodedata.normalize("NFC", text)).casefold()


def _tokens(text: str) -> frozenset[str]:
    return frozenset(
        token
        for token in _TOKEN_RE.findall(_normalize(text))
        if len(token) >= _MIN_TOKEN_LENGTH and token not in _STOPWORDS
    )


def _expected_tokens(evidence_expectation: str, *fallbacks: str) -> frozenset[str]:
    """What to look for in the answer.

    ``evidence_expectation`` says precisely what the marker should find, so when it is
    set it is used alone. Mixing in the criterion prose ("Identifies chlorophyll as the
    pigment") would add words no student needs to write and push the match below the
    threshold. Only when there is no expectation do we fall back to the prose.
    """
    expected = _tokens(evidence_expectation)
    if expected:
        return expected
    combined: frozenset[str] = frozenset()
    for source in fallbacks:
        combined |= _tokens(source)
    return combined


class FakeMarkingProvider:
    """Keyword-overlap marker. Dev/test only — never selected in production."""

    name = MODEL_NAME

    def suggest(self, context: AnswerContext) -> Suggestion:
        answer_tokens = _tokens(context.answer_text)
        criteria = context.rubric.criteria

        if not context.answer_text.strip():
            return Suggestion(
                decisions=tuple(
                    CriterionDecision(
                        criterion_id=criterion.id, decision=Decision.CANNOT_DETERMINE
                    )
                    for criterion in criteria
                ),
                confidence=_CONFIDENCE_FLOOR,
                rationale="The answer is blank, so no criterion could be judged.",
                model=MODEL_NAME,
                prompt_version=PROMPT_VERSION,
            )

        decisions: list[CriterionDecision] = []
        evidence: list[str] = []
        matched = 0
        for criterion in criteria:
            expected = _expected_tokens(
                criterion.evidence_expectation, criterion.text_en, criterion.text_bn
            )
            overlap = expected & answer_tokens
            met = bool(overlap) and len(overlap) * 2 >= len(expected)
            if met:
                matched += 1
                evidence.append(f"{criterion.id}: matched {', '.join(sorted(overlap))}")
            decisions.append(
                CriterionDecision(
                    criterion_id=criterion.id,
                    decision=Decision.MET if met else Decision.NOT_MET,
                )
            )

        return Suggestion(
            decisions=tuple(decisions),
            confidence=_confidence(matched, len(criteria)),
            rationale=f"Matched {matched} of {len(criteria)} criteria by expected keywords.",
            evidence=tuple(evidence),
            model=MODEL_NAME,
            prompt_version=PROMPT_VERSION,
        )


def _confidence(matched: int, total: int) -> Decimal:
    """Highest when the answer is clearly all-right or all-wrong, lowest when mixed."""
    if total == 0:
        return _CONFIDENCE_FLOOR
    ratio = Decimal(matched) / Decimal(total)
    decisiveness = abs(ratio - Decimal("0.5")) * 2  # 0 when half-matched, 1 at either end
    span = _CONFIDENCE_CEILING - _CONFIDENCE_FLOOR
    return (_CONFIDENCE_FLOOR + span * decisiveness).quantize(Decimal("0.001"))
