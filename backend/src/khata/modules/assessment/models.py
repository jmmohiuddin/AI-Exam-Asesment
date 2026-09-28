"""Assessment tables (migration 0002): exam, items, rubrics, candidates, scripts, results."""

from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import ForeignKey, Integer, Numeric, SmallInteger, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from khata.core.models import Base, created_at_column, uuid_pk

# Marks never use binary floats: the grid is whole or half marks.
MARKS = Numeric(6, 2)
CONFIDENCE = Numeric(4, 3)


class Exam(Base):
    __tablename__ = "exam"

    id: Mapped[uuid.UUID] = uuid_pk()
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organization.id"), nullable=False)
    school_id: Mapped[uuid.UUID] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    subject_code: Mapped[str] = mapped_column(Text, nullable=False)
    class_level: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    state: Mapped[str] = mapped_column(Text, nullable=False, default="draft")
    total_marks: Mapped[Decimal] = mapped_column(MARKS, nullable=False, default=Decimal(0))
    rubric_locked_at: Mapped[datetime | None] = mapped_column(nullable=True)
    marks_locked_at: Mapped[datetime | None] = mapped_column(nullable=True)
    published_at: Mapped[datetime | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = created_at_column()
    updated_at: Mapped[datetime] = created_at_column()
    created_by: Mapped[uuid.UUID | None] = mapped_column(nullable=True)


class ExamItem(Base):
    __tablename__ = "exam_item"

    id: Mapped[uuid.UUID] = uuid_pk()
    tenant_id: Mapped[uuid.UUID] = mapped_column(nullable=False)
    exam_id: Mapped[uuid.UUID] = mapped_column(nullable=False)
    item_no: Mapped[int] = mapped_column(Integer, nullable=False)
    prompt_bn: Mapped[str] = mapped_column(Text, nullable=False, default="")
    prompt_en: Mapped[str] = mapped_column(Text, nullable=False, default="")
    max_marks: Mapped[Decimal] = mapped_column(MARKS, nullable=False)
    created_at: Mapped[datetime] = created_at_column()


class ItemRubric(Base):
    """One rubric version. ``payload`` is a serialised :class:`khata.engines.rubric.Rubric`."""

    __tablename__ = "item_rubric"

    id: Mapped[uuid.UUID] = uuid_pk()
    tenant_id: Mapped[uuid.UUID] = mapped_column(nullable=False)
    exam_id: Mapped[uuid.UUID] = mapped_column(nullable=False)
    item_id: Mapped[uuid.UUID] = mapped_column(nullable=False)
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    payload: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    ai_eligible: Mapped[bool] = mapped_column(nullable=False, default=False)
    locked_at: Mapped[datetime | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = created_at_column()
    created_by: Mapped[uuid.UUID | None] = mapped_column(nullable=True)

    @property
    def is_locked(self) -> bool:
        return self.locked_at is not None


class ExamCandidate(Base):
    __tablename__ = "exam_candidate"

    id: Mapped[uuid.UUID] = uuid_pk()
    tenant_id: Mapped[uuid.UUID] = mapped_column(nullable=False)
    exam_id: Mapped[uuid.UUID] = mapped_column(nullable=False)
    roll: Mapped[str] = mapped_column(Text, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = created_at_column()


class Script(Base):
    """One candidate's answer script for one exam."""

    __tablename__ = "script"

    id: Mapped[uuid.UUID] = uuid_pk()
    tenant_id: Mapped[uuid.UUID] = mapped_column(nullable=False)
    exam_id: Mapped[uuid.UUID] = mapped_column(nullable=False)
    candidate_id: Mapped[uuid.UUID] = mapped_column(nullable=False)
    total_marks: Mapped[Decimal | None] = mapped_column(MARKS, nullable=True)
    created_at: Mapped[datetime] = created_at_column()
    updated_at: Mapped[datetime] = created_at_column()


class ItemResult(Base):
    """The captured answer, the AI suggestion and the teacher's decision for one item.

    ``score`` is a serialised :class:`khata.engines.scoring.ItemScore`; ``total`` is
    denormalised from it so results can be summed without parsing JSON.
    """

    __tablename__ = "item_result"

    id: Mapped[uuid.UUID] = uuid_pk()
    tenant_id: Mapped[uuid.UUID] = mapped_column(nullable=False)
    script_id: Mapped[uuid.UUID] = mapped_column(nullable=False)
    item_id: Mapped[uuid.UUID] = mapped_column(nullable=False)
    state: Mapped[str] = mapped_column(Text, nullable=False, default="pending")
    answer_text: Mapped[str] = mapped_column(Text, nullable=False, default="")
    rubric_version: Mapped[int | None] = mapped_column(Integer, nullable=True)
    ai_suggestion: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)
    ai_confidence: Mapped[Decimal | None] = mapped_column(CONFIDENCE, nullable=True)
    ai_model: Mapped[str | None] = mapped_column(Text, nullable=True)
    score: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)
    total: Mapped[Decimal | None] = mapped_column(MARKS, nullable=True)
    decided_by: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("app_user.id"), nullable=True
    )
    decided_at: Mapped[datetime | None] = mapped_column(nullable=True)
    locked_at: Mapped[datetime | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = created_at_column()
    updated_at: Mapped[datetime] = created_at_column()
