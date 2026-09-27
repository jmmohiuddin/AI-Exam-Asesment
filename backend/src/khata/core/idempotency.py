"""``Idempotency-Key`` support for POSTs that create content (TR-API-01).

Protocol, all inside the caller's business transaction:

1. ``INSERT … ON CONFLICT DO NOTHING`` a *pending* record for (tenant, user, key).
   A concurrent duplicate blocks on the unique index until the first commits.
2. Inserted → run the handler, store status + body on the record, return it.
3. Conflict → the committed record is read: same request hash ⇒ replay the stored
   response; different hash ⇒ ``409 IDEMPOTENCY_KEY_CONFLICT``.

If the handler fails, the transaction (including the pending row) rolls back, so the
client can retry with the same key.
"""

from __future__ import annotations

import hashlib
import json
import re
import uuid
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from khata.core.errors import DomainError
from khata.core.ids import uuid7
from khata.core.models import IdempotencyRecord, utcnow

IDEMPOTENCY_HEADER = "Idempotency-Key"
REPLAY_HEADER = "Idempotency-Replayed"
_VALID_KEY = re.compile(r"^[A-Za-z0-9._:-]{8,128}$")
STATE_PENDING = "pending"
STATE_COMPLETED = "completed"


@dataclass(frozen=True, slots=True)
class IdempotentResult:
    status_code: int
    body: Any
    replayed: bool


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), default=str, ensure_ascii=False)


def request_fingerprint(method: str, path: str, payload: Any) -> str:
    return hashlib.sha256(canonical_json([method.upper(), path, payload]).encode()).hexdigest()


def validate_key(key: str) -> str:
    if not _VALID_KEY.match(key):
        raise DomainError("IDEMPOTENCY_KEY_INVALID", "Use 8–128 characters: letters, digits, . _ : -")
    return key


def run_idempotent(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    user_id: uuid.UUID,
    key: str | None,
    fingerprint: str,
    handler: Callable[[], tuple[int, Any]],
) -> IdempotentResult:
    """Run ``handler`` at most once per key; ``handler`` returns ``(status, json_body)``."""
    if key is None:
        status, body = handler()
        return IdempotentResult(status, body, replayed=False)
    validate_key(key)
    inserted = session.execute(
        insert(IdempotencyRecord)
        .values(
            id=uuid7(),
            tenant_id=tenant_id,
            user_id=user_id,
            key=key,
            request_hash=fingerprint,
            state=STATE_PENDING,
            created_at=utcnow(),
        )
        .on_conflict_do_nothing(index_elements=["tenant_id", "user_id", "key"])
        .returning(IdempotencyRecord.id)
    ).scalar_one_or_none()
    if inserted is None:
        return _replay(session, tenant_id, user_id, key, fingerprint)
    status, body = handler()
    record = session.get(IdempotencyRecord, inserted)
    if record is None:  # pragma: no cover - the row was inserted in this transaction
        raise RuntimeError("idempotency record vanished")
    record.state = STATE_COMPLETED
    record.status_code = status
    record.response_body = body
    record.response_hash = hashlib.sha256(canonical_json(body).encode()).hexdigest()
    record.completed_at = utcnow()
    session.flush()
    return IdempotentResult(status, body, replayed=False)


def _replay(
    session: Session, tenant_id: uuid.UUID, user_id: uuid.UUID, key: str, fingerprint: str
) -> IdempotentResult:
    record = session.scalars(
        select(IdempotencyRecord).where(
            IdempotencyRecord.tenant_id == tenant_id,
            IdempotencyRecord.user_id == user_id,
            IdempotencyRecord.key == key,
        )
    ).one()
    if record.request_hash != fingerprint:
        raise DomainError("IDEMPOTENCY_KEY_CONFLICT")
    if record.state != STATE_COMPLETED or record.status_code is None:
        raise DomainError("CONFLICT", "The original request is still being processed")
    return IdempotentResult(record.status_code, record.response_body, replayed=True)
