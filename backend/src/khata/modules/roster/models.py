"""Students, enrolments, consent and staged imports (migration 0003)."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import Boolean, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from khata.core.models import Base, created_at_column, uuid_pk


class Student(Base):
    """A person on the school's roll.

    ``student_uid`` is the school's own identifier and the natural key inside a
    school, so re-importing a roster updates these rows rather than duplicating them.
    """

    __tablename__ = "student"

    id: Mapped[uuid.UUID] = uuid_pk()
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organization.id"), nullable=False)
    school_id: Mapped[uuid.UUID] = mapped_column(nullable=False)
    student_uid: Mapped[str] = mapped_column(Text, nullable=False)
    name_bn: Mapped[str] = mapped_column(Text, nullable=False, default="")
    name_en: Mapped[str] = mapped_column(Text, nullable=False, default="")
    guardian_mobile: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(Text, nullable=False, default="active")
    created_at: Mapped[datetime] = created_at_column()
    updated_at: Mapped[datetime] = created_at_column()
    created_by: Mapped[uuid.UUID | None] = mapped_column(nullable=True)

    @property
    def display_name(self) -> str:
        """Bangla first: it is what the school typed and what the report card shows."""
        return self.name_bn or self.name_en


class Enrolment(Base):
    """Which section a student sits in for one academic year, and their roll."""

    __tablename__ = "enrolment"

    id: Mapped[uuid.UUID] = uuid_pk()
    tenant_id: Mapped[uuid.UUID] = mapped_column(nullable=False)
    student_id: Mapped[uuid.UUID] = mapped_column(nullable=False)
    academic_year_id: Mapped[uuid.UUID] = mapped_column(nullable=False)
    section_id: Mapped[uuid.UUID] = mapped_column(nullable=False)
    roll: Mapped[str] = mapped_column(Text, nullable=False)
    fourth_subject_code: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = created_at_column()
    updated_at: Mapped[datetime] = created_at_column()


class StudentConsent(Base):
    """One recorded guardian decision (08 §6.1).

    Append-only: a change inserts a new row and supersedes the previous one, so the
    question "was AI allowed when this script was marked?" stays answerable later.
    """

    __tablename__ = "student_consent"

    id: Mapped[uuid.UUID] = uuid_pk()
    tenant_id: Mapped[uuid.UUID] = mapped_column(nullable=False)
    student_id: Mapped[uuid.UUID] = mapped_column(nullable=False)
    consent_type: Mapped[str] = mapped_column(Text, nullable=False)
    granted: Mapped[bool] = mapped_column(Boolean, nullable=False)
    method: Mapped[str] = mapped_column(Text, nullable=False)
    evidence_ref: Mapped[str | None] = mapped_column(Text, nullable=True)
    note: Mapped[str | None] = mapped_column(Text, nullable=True)
    recorded_by: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("app_user.id"), nullable=True)
    recorded_at: Mapped[datetime] = created_at_column()
    superseded_at: Mapped[datetime | None] = mapped_column(nullable=True)


class RosterImport(Base):
    """A validated import waiting for the admin to confirm it.

    ``rows`` is what the commit applies: the rows the engine accepted at validation
    time, so committing can never do something the admin was not shown.
    """

    __tablename__ = "roster_import"

    id: Mapped[uuid.UUID] = uuid_pk()
    tenant_id: Mapped[uuid.UUID] = mapped_column(nullable=False)
    school_id: Mapped[uuid.UUID] = mapped_column(nullable=False)
    academic_year_id: Mapped[uuid.UUID] = mapped_column(nullable=False)
    filename: Mapped[str] = mapped_column(Text, nullable=False)
    state: Mapped[str] = mapped_column(Text, nullable=False, default="validated")
    row_count: Mapped[int] = mapped_column(Integer, nullable=False)
    accepted_count: Mapped[int] = mapped_column(Integer, nullable=False)
    error_count: Mapped[int] = mapped_column(Integer, nullable=False)
    report: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False, default=dict)
    rows: Mapped[list[dict[str, Any]]] = mapped_column(JSONB, nullable=False, default=list)
    students_created: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    students_updated: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    sections_created: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_by: Mapped[uuid.UUID | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = created_at_column()
    committed_at: Mapped[datetime | None] = mapped_column(nullable=True)
