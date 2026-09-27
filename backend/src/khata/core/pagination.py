"""Opaque cursor pagination (TR-API-01).

A cursor is base64url(JSON) of the sort key of the last item returned. It is opaque
to clients; tampering produces ``400 INVALID_CURSOR``, never a server error.
"""

from __future__ import annotations

import base64
import binascii
import json
from collections.abc import Callable, Sequence
from typing import Any, Generic, TypeVar

from pydantic import BaseModel

from khata.core.errors import DomainError

DEFAULT_LIMIT = 50
MAX_LIMIT = 200
MAX_CURSOR_LENGTH = 512

T = TypeVar("T")
M = TypeVar("M")


class CursorPage(BaseModel, Generic[T]):
    items: list[T]
    next_cursor: str | None = None


def clamp_limit(limit: int | None) -> int:
    if limit is None:
        return DEFAULT_LIMIT
    return max(1, min(limit, MAX_LIMIT))


def encode_cursor(position: dict[str, Any]) -> str:
    raw = json.dumps(position, separators=(",", ":"), sort_keys=True, default=str)
    return base64.urlsafe_b64encode(raw.encode()).decode().rstrip("=")


def decode_cursor(cursor: str | None) -> dict[str, Any] | None:
    if cursor is None or cursor == "":
        return None
    if len(cursor) > MAX_CURSOR_LENGTH:
        raise DomainError("INVALID_CURSOR")
    try:
        padded = cursor + "=" * (-len(cursor) % 4)
        decoded = json.loads(base64.urlsafe_b64decode(padded.encode()))
    except (binascii.Error, ValueError, UnicodeDecodeError) as exc:
        raise DomainError("INVALID_CURSOR") from exc
    if not isinstance(decoded, dict):
        raise DomainError("INVALID_CURSOR")
    return decoded


def page_from_rows(
    rows: Sequence[M], limit: int, position_of: Callable[[M], dict[str, Any]]
) -> tuple[list[M], str | None]:
    """Given up to ``limit + 1`` rows, return the page and the cursor for the next one."""
    if len(rows) <= limit:
        return list(rows), None
    page = list(rows[:limit])
    return page, encode_cursor(position_of(page[-1]))
