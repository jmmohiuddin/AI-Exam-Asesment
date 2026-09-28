"""Vendor-neutral marking-provider interface (ADR-006, TRD §16).

The application depends on :class:`MarkingProvider`, never on a vendor SDK, so a
provider can be swapped by configuration. A provider only ever *suggests*: it
returns criterion decisions and a confidence, and the deterministic engine
(:func:`khata.engines.scoring.score_item`) turns those into marks. No provider
can write a final mark — that is a teacher decision (ADR-011, spec 07 §4.1).
"""

from __future__ import annotations

from decimal import Decimal
from typing import Protocol, runtime_checkable

from pydantic import Field

from khata.engines.base import FrozenModel
from khata.engines.rubric import Rubric
from khata.engines.scoring import CriterionDecision

# Below this the suggestion is shown without a pre-filled mark: the teacher decides
# from scratch. Provisional until calibrated against gold data (ADR-011).
LOW_CONFIDENCE_THRESHOLD = Decimal("0.60")


class AnswerContext(FrozenModel):
    """Everything a provider is allowed to see about one answer."""

    item_id: str
    prompt: str
    max_marks: Decimal
    answer_text: str
    rubric: Rubric


class Suggestion(FrozenModel):
    """A provider's proposed decisions. Never a final mark."""

    decisions: tuple[CriterionDecision, ...]
    confidence: Decimal = Field(ge=0, le=1, allow_inf_nan=False)
    rationale: str = ""
    evidence: tuple[str, ...] = ()
    model: str
    prompt_version: str

    @property
    def is_low_confidence(self) -> bool:
        return self.confidence < LOW_CONFIDENCE_THRESHOLD


class ProviderError(RuntimeError):
    """The provider could not produce a suggestion. The item falls back to manual."""


@runtime_checkable
class MarkingProvider(Protocol):
    """Implemented by the Fake provider and, later, by real vendor adapters."""

    name: str

    def suggest(self, context: AnswerContext) -> Suggestion:
        """Propose criterion decisions for one answer, or raise :class:`ProviderError`."""
        ...
