"""Password hashing, access/step-up JWTs, opaque refresh tokens and OTP codes (ADR-001).

No hand-rolled crypto: argon2id via pwdlib, HS256 via PyJWT, HMAC/SHA-256 via hashlib.
"""

from __future__ import annotations

import hashlib
import hmac
import secrets
import uuid
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher

JWT_ALGORITHM = "HS256"
JWT_ISSUER = "khata"
JWT_AUDIENCE = "khata-api"
ACCESS_TOKEN_TYPE = "access"
STEP_UP_TOKEN_TYPE = "step_up"
REFRESH_TOKEN_BYTES = 32
OTP_DIGITS = 6
CLOCK_SKEW_SECONDS = 10

_password_hash = PasswordHash((Argon2Hasher(),))
# Verified against when the account does not exist, so timing does not reveal it.
_DUMMY_HASH = _password_hash.hash(secrets.token_urlsafe(16))


class TokenError(Exception):
    """Base class for token validation failures."""


class TokenExpiredError(TokenError):
    pass


class TokenInvalidError(TokenError):
    pass


def hash_password(password: str) -> str:
    return _password_hash.hash(password)


def verify_password(password: str, password_hash: str | None) -> tuple[bool, str | None]:
    """Return ``(ok, new_hash)``; ``new_hash`` is set when parameters need upgrading.

    Always performs one argon2 verification, even when there is no stored hash.
    """
    if password_hash is None:
        _password_hash.verify(password, _DUMMY_HASH)
        return False, None
    ok, updated = _password_hash.verify_and_update(password, password_hash)
    return ok, updated


@dataclass(frozen=True, slots=True)
class AccessClaims:
    user_id: uuid.UUID
    tenant_id: uuid.UUID | None
    session_id: uuid.UUID
    token_id: str
    issued_at: datetime
    expires_at: datetime


@dataclass(frozen=True, slots=True)
class StepUpClaims:
    user_id: uuid.UUID
    session_id: uuid.UUID
    purpose: str
    token_id: str
    expires_at: datetime


def _encode(secret: str, claims: dict[str, Any]) -> str:
    return jwt.encode(claims, secret, algorithm=JWT_ALGORITHM)


def _decode(secret: str, token: str, expected_type: str) -> dict[str, Any]:
    try:
        claims: dict[str, Any] = jwt.decode(
            token,
            secret,
            algorithms=[JWT_ALGORITHM],
            audience=JWT_AUDIENCE,
            issuer=JWT_ISSUER,
            leeway=CLOCK_SKEW_SECONDS,
            options={"require": ["exp", "iat", "sub", "jti", "typ"]},
        )
    except jwt.ExpiredSignatureError as exc:
        raise TokenExpiredError("token expired") from exc
    except jwt.PyJWTError as exc:
        raise TokenInvalidError("token invalid") from exc
    if claims.get("typ") != expected_type:
        raise TokenInvalidError("wrong token type")
    return claims


def _base_claims(
    user_id: uuid.UUID, token_type: str, now: datetime, ttl: timedelta
) -> dict[str, Any]:
    return {
        "iss": JWT_ISSUER,
        "aud": JWT_AUDIENCE,
        "typ": token_type,
        "sub": str(user_id),
        "jti": secrets.token_urlsafe(16),
        "iat": int(now.timestamp()),
        "exp": int((now + ttl).timestamp()),
    }


def create_access_token(
    secret: str,
    *,
    user_id: uuid.UUID,
    tenant_id: uuid.UUID | None,
    session_id: uuid.UUID,
    ttl_seconds: int,
    now: datetime | None = None,
) -> str:
    issued = now or datetime.now(UTC)
    claims = _base_claims(user_id, ACCESS_TOKEN_TYPE, issued, timedelta(seconds=ttl_seconds))
    claims["tid"] = str(tenant_id) if tenant_id else None
    claims["sid"] = str(session_id)
    return _encode(secret, claims)


def decode_access_token(secret: str, token: str) -> AccessClaims:
    claims = _decode(secret, token, ACCESS_TOKEN_TYPE)
    try:
        tenant = claims.get("tid")
        return AccessClaims(
            user_id=uuid.UUID(claims["sub"]),
            tenant_id=uuid.UUID(tenant) if tenant else None,
            session_id=uuid.UUID(claims["sid"]),
            token_id=str(claims["jti"]),
            issued_at=datetime.fromtimestamp(int(claims["iat"]), UTC),
            expires_at=datetime.fromtimestamp(int(claims["exp"]), UTC),
        )
    except (KeyError, TypeError, ValueError) as exc:
        raise TokenInvalidError("malformed claims") from exc


def create_step_up_token(
    secret: str,
    *,
    user_id: uuid.UUID,
    session_id: uuid.UUID,
    purpose: str,
    ttl_seconds: int,
    now: datetime | None = None,
) -> str:
    issued = now or datetime.now(UTC)
    claims = _base_claims(user_id, STEP_UP_TOKEN_TYPE, issued, timedelta(seconds=ttl_seconds))
    claims["sid"] = str(session_id)
    claims["purpose"] = purpose
    return _encode(secret, claims)


def decode_step_up_token(secret: str, token: str) -> StepUpClaims:
    claims = _decode(secret, token, STEP_UP_TOKEN_TYPE)
    try:
        return StepUpClaims(
            user_id=uuid.UUID(claims["sub"]),
            session_id=uuid.UUID(claims["sid"]),
            purpose=str(claims["purpose"]),
            token_id=str(claims["jti"]),
            expires_at=datetime.fromtimestamp(int(claims["exp"]), UTC),
        )
    except (KeyError, TypeError, ValueError) as exc:
        raise TokenInvalidError("malformed claims") from exc


def new_refresh_token() -> tuple[str, str]:
    """Return ``(opaque_token, sha256_hex)``. Only the hash is stored."""
    token = secrets.token_urlsafe(REFRESH_TOKEN_BYTES)
    return token, hash_refresh_token(token)


def hash_refresh_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


def generate_otp_code() -> str:
    return f"{secrets.randbelow(10**OTP_DIGITS):0{OTP_DIGITS}d}"


def otp_hmac(pepper: str, challenge_id: uuid.UUID, code: str) -> str:
    """Keyed hash of the OTP bound to its challenge (a 6-digit space is not safe unkeyed)."""
    message = f"{challenge_id}:{code}".encode()
    return hmac.new(pepper.encode(), message, hashlib.sha256).hexdigest()


def constant_time_equals(left: str, right: str) -> bool:
    return hmac.compare_digest(left.encode(), right.encode())
