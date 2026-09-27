"""Shared Pydantic base for immutable engine data."""

from __future__ import annotations

from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

NonNegativeDecimal = Annotated[Decimal, Field(ge=0, allow_inf_nan=False)]
PositiveDecimal = Annotated[Decimal, Field(gt=0, allow_inf_nan=False)]
Percent = Annotated[Decimal, Field(ge=0, le=100, allow_inf_nan=False)]


class FrozenModel(BaseModel):
    """Immutable, strict-shape model: unknown keys are rejected."""

    model_config = ConfigDict(frozen=True, extra="forbid")
