"""Declarative base, shared column helpers and the core-owned infrastructure tables.

Schema changes are made in Alembic migrations (hand-written SQL); these ORM models
must match them — ``tests/integration/test_schema_drift.py`` compares the two.
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import (
    DateTime,
    Integer,
    LargeBinary,
    MetaData,
    SmallInteger,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from khata.core.ids import uuid7

NAMING_CONVENTION = {
    "ix": "ix_%(table_name)s_%(column_0_N_name)s",
    "uq": "uq_%(table_name)s_%(column_0_N_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_N_name)s",
    "pk": "pk_%(table_name)s",
}


def utcnow() -> datetime:
    return datetime.now(UTC)


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=NAMING_CONVENTION)
    type_annotation_map = {  # noqa: RUF012 - SQLAlchemy's declarative API expects a plain dict
        uuid.UUID: UUID(as_uuid=True),
        datetime: DateTime(timezone=True),
        dict[str, Any]: JSONB,
    }


def uuid_pk() -> Mapped[uuid.UUID]:
    return mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid7)


def created_at_column() -> Mapped[datetime]:
    return mapped_column(DateTime(timezone=True), nullable=False, default=utcnow)


class TenantKey(Base):
    """Per-tenant data-encryption key, wrapped by the KMS (ADR-005). RLS-protected."""

    __tablename__ = "tenant_key"

    tenant_id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    key_version: Mapped[int] = mapped_column(Integer, primary_key=True)
    wrapped_dek: Mapped[bytes | None] = mapped_column(LargeBinary, nullable=True)
    kms_key_id: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = created_at_column()
    shredded_at: Mapped[datetime | None] = mapped_column(nullable=True)


class IdempotencyRecord(Base):
    """Stored outcome of a POST carrying ``Idempotency-Key`` (TR-API-01). RLS-protected."""

    __tablename__ = "idempotency_record"
    __table_args__ = (UniqueConstraint("tenant_id", "user_id", "key"),)

    id: Mapped[uuid.UUID] = uuid_pk()
    tenant_id: Mapped[uuid.UUID] = mapped_column(nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(nullable=False)
    key: Mapped[str] = mapped_column(Text, nullable=False)
    request_hash: Mapped[str] = mapped_column(Text, nullable=False)
    state: Mapped[str] = mapped_column(Text, nullable=False)
    status_code: Mapped[int | None] = mapped_column(SmallInteger, nullable=True)
    response_body: Mapped[Any | None] = mapped_column(JSONB, nullable=True)
    response_hash: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = created_at_column()
    completed_at: Mapped[datetime | None] = mapped_column(nullable=True)
