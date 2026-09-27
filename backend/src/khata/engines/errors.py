"""Typed errors raised by the deterministic engines.

Every engine error derives from :class:`EngineError` so callers (the API layer)
can map them to HTTP responses without string matching.
"""

from __future__ import annotations

from enum import StrEnum


class EngineError(Exception):
    """Base class for all engine errors."""


class IllegalTransition(EngineError):
    """A workflow transition that is not an edge of the state machine (API: 409)."""

    def __init__(self, current: StrEnum, target: StrEnum, reason: str) -> None:
        self.current = current
        self.target = target
        self.reason = reason
        super().__init__(f"illegal transition {current.value} -> {target.value}: {reason}")


class MarksInputError(EngineError, ValueError):
    """Marks or decisions that violate bounds or reference unknown ids."""


class ScoringInputError(MarksInputError):
    """Criterion decisions that cannot be scored against the rubric."""


class ResultInputError(MarksInputError):
    """Result-engine input that is incomplete or inconsistent with the structure."""


class TemplateError(EngineError, ValueError):
    """A paper template whose structure or sums are invalid."""
