"""AES-256-GCM envelope encryption with per-tenant data keys (ADR-005, ADR-014, TR-TEN-03).

Layout of a sealed value (all integers big-endian)::

    version (1 byte = 0x01) | key_version (4 bytes) | nonce (12 bytes) | ciphertext+tag

The AAD always binds the tenant ID, so a ciphertext moved to another tenant fails
authentication even before key lookup. DEKs are stored only wrapped by the KMS in
``tenant_key``; shredding removes the wrapped DEK, making the data unrecoverable.
"""

from __future__ import annotations

import os
import struct
import uuid
from dataclasses import dataclass
from typing import Protocol

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from sqlalchemy import select, update
from sqlalchemy.orm import Session

from khata.core.models import TenantKey, utcnow

ENVELOPE_VERSION = 1
NONCE_BYTES = 12
DEK_BYTES = 32
_HEADER = struct.Struct(">BI")
LOCAL_KMS_KEY_ID = "local-v1"


class CryptoError(Exception):
    """Decryption failed (wrong key, wrong tenant, tampering or shredded key)."""


class KeyShreddedError(CryptoError):
    pass


@dataclass(frozen=True, slots=True)
class WrappedKey:
    ciphertext: bytes
    key_id: str


class Kms(Protocol):
    def wrap(self, plaintext_key: bytes, *, context: bytes) -> WrappedKey: ...

    def unwrap(self, wrapped: WrappedKey, *, context: bytes) -> bytes: ...


class LocalKms:
    """Development/test KMS: wraps DEKs with a master key from the environment."""

    def __init__(self, master_key: bytes, key_id: str = LOCAL_KMS_KEY_ID) -> None:
        if len(master_key) != DEK_BYTES:
            raise ValueError("master key must be 32 bytes")
        self._aead = AESGCM(master_key)
        self._key_id = key_id

    def wrap(self, plaintext_key: bytes, *, context: bytes) -> WrappedKey:
        nonce = os.urandom(NONCE_BYTES)
        return WrappedKey(nonce + self._aead.encrypt(nonce, plaintext_key, context), self._key_id)

    def unwrap(self, wrapped: WrappedKey, *, context: bytes) -> bytes:
        if wrapped.key_id != self._key_id:
            raise CryptoError("unknown KMS key id")
        nonce, body = wrapped.ciphertext[:NONCE_BYTES], wrapped.ciphertext[NONCE_BYTES:]
        try:
            return self._aead.decrypt(nonce, body, context)
        except InvalidTag as exc:
            raise CryptoError("DEK unwrap failed") from exc


def _tenant_aad(tenant_id: uuid.UUID, aad: bytes) -> bytes:
    return b"khata:tenant:" + tenant_id.bytes + b":" + aad


def seal(dek: bytes, tenant_id: uuid.UUID, key_version: int, plaintext: bytes, aad: bytes) -> bytes:
    nonce = os.urandom(NONCE_BYTES)
    body = AESGCM(dek).encrypt(nonce, plaintext, _tenant_aad(tenant_id, aad))
    return _HEADER.pack(ENVELOPE_VERSION, key_version) + nonce + body


def parse_key_version(blob: bytes) -> int:
    if len(blob) < _HEADER.size + NONCE_BYTES:
        raise CryptoError("ciphertext too short")
    version, key_version = _HEADER.unpack_from(blob)
    if version != ENVELOPE_VERSION:
        raise CryptoError("unsupported envelope version")
    return int(key_version)


def open_sealed(dek: bytes, tenant_id: uuid.UUID, blob: bytes, aad: bytes) -> bytes:
    parse_key_version(blob)
    nonce = blob[_HEADER.size : _HEADER.size + NONCE_BYTES]
    body = blob[_HEADER.size + NONCE_BYTES :]
    try:
        return AESGCM(dek).decrypt(nonce, body, _tenant_aad(tenant_id, aad))
    except InvalidTag as exc:
        raise CryptoError("decryption failed") from exc


def _dek_context(tenant_id: uuid.UUID, key_version: int) -> bytes:
    return f"khata:dek:{tenant_id}:{key_version}".encode()


def _current_key(session: Session, tenant_id: uuid.UUID) -> TenantKey | None:
    stmt = (
        select(TenantKey)
        .where(TenantKey.tenant_id == tenant_id, TenantKey.shredded_at.is_(None))
        .order_by(TenantKey.key_version.desc())
        .limit(1)
    )
    return session.scalars(stmt).first()


def ensure_tenant_key(session: Session, kms: Kms, tenant_id: uuid.UUID) -> TenantKey:
    """Return the tenant's current key row, creating version 1 if none exists."""
    existing = _current_key(session, tenant_id)
    if existing is not None:
        return existing
    dek = AESGCM.generate_key(bit_length=DEK_BYTES * 8)
    wrapped = kms.wrap(dek, context=_dek_context(tenant_id, 1))
    row = TenantKey(
        tenant_id=tenant_id,
        key_version=1,
        wrapped_dek=wrapped.ciphertext,
        kms_key_id=wrapped.key_id,
    )
    session.add(row)
    session.flush()
    return row


def _unwrap(kms: Kms, row: TenantKey) -> bytes:
    if row.wrapped_dek is None or row.shredded_at is not None:
        raise KeyShreddedError("tenant key has been shredded")
    wrapped = WrappedKey(row.wrapped_dek, row.kms_key_id)
    return kms.unwrap(wrapped, context=_dek_context(row.tenant_id, row.key_version))


def encrypt_for_tenant(
    session: Session, kms: Kms, tenant_id: uuid.UUID, plaintext: bytes, aad: bytes = b""
) -> bytes:
    row = ensure_tenant_key(session, kms, tenant_id)
    return seal(_unwrap(kms, row), tenant_id, row.key_version, plaintext, aad)


def decrypt_for_tenant(
    session: Session, kms: Kms, tenant_id: uuid.UUID, blob: bytes, aad: bytes = b""
) -> bytes:
    key_version = parse_key_version(blob)
    row = session.get(TenantKey, (tenant_id, key_version))
    if row is None:
        raise CryptoError("no key for this tenant and version")
    return open_sealed(_unwrap(kms, row), tenant_id, blob, aad)


def shred_tenant_keys(session: Session, tenant_id: uuid.UUID) -> int:
    """Destroy every wrapped DEK of the tenant (crypto-erasure). Returns rows shredded."""
    result = session.execute(
        update(TenantKey)
        .where(TenantKey.tenant_id == tenant_id, TenantKey.shredded_at.is_(None))
        .values(wrapped_dek=None, shredded_at=utcnow())
    )
    return int(getattr(result, "rowcount", 0) or 0)
