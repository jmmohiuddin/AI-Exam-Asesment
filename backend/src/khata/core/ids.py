"""Identifier helpers: time-ordered UUIDv7 primary keys and human support codes."""

from __future__ import annotations

import secrets
import time
import uuid

# Nil UUID: tenant key of the platform-level audit chain (events with no tenant).
PLATFORM_TENANT_ID = uuid.UUID(int=0)

_SUPPORT_ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"  # no 0/O/1/I for phone support
SUPPORT_CODE_LENGTH = 8


def uuid7() -> uuid.UUID:
    """RFC 9562 UUIDv7: 48-bit Unix ms timestamp + 74 random bits (index-friendly)."""
    unix_ms = time.time_ns() // 1_000_000
    rand_a = secrets.randbits(12)
    rand_b = secrets.randbits(62)
    value = (unix_ms & ((1 << 48) - 1)) << 80
    value |= 0x7 << 76
    value |= rand_a << 64
    value |= 0b10 << 62
    value |= rand_b
    return uuid.UUID(int=value)


def support_code() -> str:
    """Short code shown to users on errors and logged with the full error server-side."""
    body = "".join(secrets.choice(_SUPPORT_ALPHABET) for _ in range(SUPPORT_CODE_LENGTH))
    return f"KH-{body}"
