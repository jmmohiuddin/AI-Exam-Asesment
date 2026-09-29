"""Organisation, school and role assignment (migration 0001)."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import Date, ForeignKey, SmallInteger, Text
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from khata.core.models import Base, created_at_column, uuid_pk


class Organization(Base):
    """The tenant root: ``organization.id`` is the ``tenant_id`` everywhere else."""

    __tablename__ = "organization"

    id: Mapped[uuid.UUID] = uuid_pk()
    name: Mapped[str] = mapped_column(Text, nullable=False)
    plan_id: Mapped[uuid.UUID | None] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(Text, nullable=False, default="active")
    created_at: Mapped[datetime] = created_at_column()
    updated_at: Mapped[datetime] = created_at_column()


class School(Base):
    __tablename__ = "school"

    id: Mapped[uuid.UUID] = uuid_pk()
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organization.id"), nullable=False)
    name_bn: Mapped[str] = mapped_column(Text, nullable=False)
    name_en: Mapped[str] = mapped_column(Text, nullable=False)
    eiin: Mapped[str | None] = mapped_column(Text, nullable=True)
    board: Mapped[str] = mapped_column(Text, nullable=False)
    versions: Mapped[list[str]] = mapped_column(ARRAY(Text), nullable=False, default=list)
    shifts: Mapped[list[str]] = mapped_column(ARRAY(Text), nullable=False, default=list)
    logo_ref: Mapped[str | None] = mapped_column(Text, nullable=True)
    booklet_profile: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False, default=dict)
    settings: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False, default=dict)
    created_at: Mapped[datetime] = created_at_column()
    updated_at: Mapped[datetime] = created_at_column()


class AcademicYear(Base):
    __tablename__ = "academic_year"

    id: Mapped[uuid.UUID] = uuid_pk()
    tenant_id: Mapped[uuid.UUID] = mapped_column(nullable=False)
    school_id: Mapped[uuid.UUID] = mapped_column(nullable=False)
    year: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    starts_on: Mapped[datetime] = mapped_column(Date, nullable=False)
    ends_on: Mapped[datetime] = mapped_column(Date, nullable=False)
    is_current: Mapped[bool] = mapped_column(nullable=False, default=False)
    created_at: Mapped[datetime] = created_at_column()


class Section(Base):
    """A teaching group: class, group, version and shift, named (A, B, ...).

    Identity is the whole tuple, not the name: "9 Science EV A" and "9 Humanities
    EV A" are different sections that a school writes down as the same letter.
    """

    __tablename__ = "section"

    id: Mapped[uuid.UUID] = uuid_pk()
    tenant_id: Mapped[uuid.UUID] = mapped_column(nullable=False)
    school_id: Mapped[uuid.UUID] = mapped_column(nullable=False)
    academic_year_id: Mapped[uuid.UUID] = mapped_column(nullable=False)
    class_level: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    group_code: Mapped[str] = mapped_column(Text, nullable=False)
    version: Mapped[str] = mapped_column(Text, nullable=False)
    shift: Mapped[str] = mapped_column(Text, nullable=False, default="day")
    name: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = created_at_column()


class RoleAssignment(Base):
    """A user's role in one tenant, optionally scoped to a school and subject (08 §5.3)."""

    __tablename__ = "role_assignment"

    id: Mapped[uuid.UUID] = uuid_pk()
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organization.id"), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("app_user.id"), nullable=False)
    school_id: Mapped[uuid.UUID | None] = mapped_column(nullable=True)
    role: Mapped[str] = mapped_column(Text, nullable=False)
    subject_code: Mapped[str | None] = mapped_column(Text, nullable=True)
    valid_from: Mapped[datetime] = created_at_column()
    valid_to: Mapped[datetime | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = created_at_column()
    created_by: Mapped[uuid.UUID | None] = mapped_column(nullable=True)
