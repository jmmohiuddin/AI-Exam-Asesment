"""Password sign-in, session creation and membership lookup (ADR-001).

Identity tables are not tenant-scoped (a user may hold roles in several
organisations), so these run with no tenant bound; the membership RLS policies in
migration 0001 make a user's own ``role_assignment`` rows readable in that state.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from khata.core.config import Settings
from khata.core.db import bind_context
from khata.core.errors import DomainError
from khata.core.models import utcnow
from khata.core.roles import Role
from khata.core.security import (
    create_access_token,
    hash_password,
    hash_refresh_token,
    new_refresh_token,
    verify_password,
)
from khata.modules.identity.models import AppUser, AuthSession, Device, RefreshToken
from khata.modules.org.models import Organization, RoleAssignment, School

WEB_CLIENT = "web"
CAPTURE_CLIENT = "capture"
MIN_PASSWORD_LENGTH = 10


@dataclass(frozen=True, slots=True)
class Membership:
    """One role assignment. The API groups these per school before sending them."""

    tenant_id: uuid.UUID
    tenant_name: str
    role: Role
    school_id: uuid.UUID | None
    school_name_bn: str
    school_name_en: str
    subject_code: str | None


@dataclass(frozen=True, slots=True)
class SignInResult:
    user: AppUser
    session: AuthSession
    access_token: str
    refresh_token: str
    expires_in: int
    memberships: tuple[Membership, ...]
    active_tenant_id: uuid.UUID | None


def active_memberships(session: Session, user_id: uuid.UUID) -> tuple[Membership, ...]:
    """The user's currently valid role assignments, with organisation names."""
    now = utcnow()
    rows = session.execute(
        select(RoleAssignment, Organization.name, School.name_bn, School.name_en)
        .join(Organization, Organization.id == RoleAssignment.tenant_id)
        .outerjoin(School, School.id == RoleAssignment.school_id)
        .where(
            RoleAssignment.user_id == user_id,
            RoleAssignment.valid_from <= now,
            (RoleAssignment.valid_to.is_(None)) | (RoleAssignment.valid_to > now),
        )
        .order_by(Organization.name, RoleAssignment.role)
    ).all()
    return tuple(
        Membership(
            tenant_id=assignment.tenant_id,
            tenant_name=tenant_name,
            role=Role(assignment.role),
            school_id=assignment.school_id,
            # An org-level role has no school; the organisation name stands in.
            school_name_bn=school_name_bn or tenant_name,
            school_name_en=school_name_en or tenant_name,
            subject_code=assignment.subject_code,
        )
        for assignment, tenant_name, school_name_bn, school_name_en in rows
    )


def _account_is_locked(user: AppUser, now: datetime) -> bool:
    return user.locked_until is not None and user.locked_until > now


def _register_failure(session: Session, user: AppUser, settings: Settings, now: datetime) -> None:
    window_start = now - timedelta(seconds=settings.lockout_window_seconds)
    within_window = (
        user.last_failed_login_at is not None and user.last_failed_login_at >= window_start
    )
    user.failed_login_count = user.failed_login_count + 1 if within_window else 1
    user.last_failed_login_at = now
    if user.failed_login_count >= settings.lockout_threshold:
        user.locked_until = now + timedelta(seconds=settings.lockout_duration_seconds)
    session.flush()


def sign_in(
    session: Session,
    settings: Settings,
    *,
    mobile: str,
    password: str,
    client: str = WEB_CLIENT,
    device_name: str = "browser",
    tenant_id: uuid.UUID | None = None,
) -> SignInResult:
    """Verify a password and open a session.

    Always performs one argon2 verification, so a missing account and a wrong
    password take the same time and return the same error.
    """
    now = utcnow()
    user = session.scalar(select(AppUser).where(AppUser.mobile == mobile))

    ok, upgraded_hash = verify_password(password, user.password_hash if user else None)
    if user is None or not ok:
        if user is not None:
            _register_failure(session, user, settings, now)
        raise DomainError("INVALID_CREDENTIALS")
    if _account_is_locked(user, now):
        raise DomainError("ACCOUNT_LOCKED")
    if not user.is_active:
        raise DomainError("INVALID_CREDENTIALS")

    if upgraded_hash is not None:
        user.password_hash = upgraded_hash
    user.failed_login_count = 0
    user.last_failed_login_at = None
    user.locked_until = None

    # The caller could not bind a user before the password was checked. The
    # membership_read policies key off app.user_id, so bind it now that we know who
    # this is; the tenant stays unset until one is selected below.
    bind_context(session, tenant_id=None, user_id=user.id)
    memberships = active_memberships(session, user.id)
    active_tenant = _resolve_active_tenant(user, memberships, tenant_id)
    user.last_active_tenant_id = active_tenant

    device = Device(user_id=user.id, name=device_name, kind=client)
    session.add(device)
    session.flush()

    idle_seconds = (
        settings.refresh_idle_web_seconds
        if client == WEB_CLIENT
        else settings.refresh_idle_capture_seconds
    )
    auth_session = AuthSession(
        user_id=user.id,
        device_id=device.id,
        client=client,
        active_tenant_id=active_tenant,
        expires_at=now + timedelta(seconds=settings.session_absolute_seconds),
    )
    session.add(auth_session)
    session.flush()

    raw_refresh, refresh_hash = new_refresh_token()
    session.add(
        RefreshToken(
            token_hash=refresh_hash,
            family_id=auth_session.id,
            user_id=user.id,
            device_id=device.id,
            expires_at=now + timedelta(seconds=settings.session_absolute_seconds),
            idle_expires_at=now + timedelta(seconds=idle_seconds),
        )
    )

    access = create_access_token(
        settings.jwt_secret.get_secret_value(),
        user_id=user.id,
        tenant_id=active_tenant,
        session_id=auth_session.id,
        ttl_seconds=settings.access_token_ttl_seconds,
        now=now,
    )
    return SignInResult(
        user=user,
        session=auth_session,
        access_token=access,
        refresh_token=raw_refresh,
        expires_in=settings.access_token_ttl_seconds,
        memberships=memberships,
        active_tenant_id=active_tenant,
    )


def _resolve_active_tenant(
    user: AppUser,
    memberships: tuple[Membership, ...],
    requested: uuid.UUID | None,
) -> uuid.UUID | None:
    """Pick the tenant this session acts in: the requested one, the last one, or the only one."""
    available = {membership.tenant_id for membership in memberships}
    if requested is not None:
        if requested not in available:
            raise DomainError("NOT_A_MEMBER")
        return requested
    if user.last_active_tenant_id in available:
        return user.last_active_tenant_id
    if len(available) == 1:
        return next(iter(available))
    return None


def sign_out(session: Session, session_id: uuid.UUID, reason: str = "user_logout") -> None:
    auth_session = session.get(AuthSession, session_id)
    if auth_session is None or auth_session.is_revoked:
        return
    now = utcnow()
    auth_session.revoked_at = now
    auth_session.revoke_reason = reason
    for token in session.scalars(
        select(RefreshToken).where(
            RefreshToken.family_id == session_id, RefreshToken.revoked_at.is_(None)
        )
    ):
        token.revoked_at = now


def create_user(
    session: Session,
    *,
    mobile: str,
    name: str,
    password: str,
    locale: str = "bn",
) -> AppUser:
    """Create an active user. Used by the dev seed and by tests."""
    if len(password) < MIN_PASSWORD_LENGTH:
        raise DomainError("PASSWORD_TOO_WEAK")
    user = AppUser(
        mobile=mobile,
        name=name,
        password_hash=hash_password(password),
        status="active",
        locale=locale,
        password_changed_at=datetime.now(UTC),
    )
    session.add(user)
    session.flush()
    return user


#: Digits kept at each end of a masked mobile number.
MASK_PREFIX = 4
MASK_SUFFIX = 4
#: Fixed-width mask, so the output does not leak how long the number is.
MASK_BODY = "****"


def mask_mobile(mobile: str) -> str:
    """``+8801712345678`` -> ``+880****5678``. Never show a full number in a UI.

    The mask is a fixed width rather than one star per hidden digit: a
    variable-width mask would disclose the length of the number.
    """
    if len(mobile) <= MASK_PREFIX + MASK_SUFFIX:
        return MASK_BODY
    return f"{mobile[:MASK_PREFIX]}{MASK_BODY}{mobile[-MASK_SUFFIX:]}"


def _revoke_family(session: Session, family_id: uuid.UUID, reason: str) -> None:
    now = utcnow()
    auth_session = session.get(AuthSession, family_id)
    if auth_session is not None and not auth_session.is_revoked:
        auth_session.revoked_at = now
        auth_session.revoke_reason = reason
    for token in session.scalars(
        select(RefreshToken).where(
            RefreshToken.family_id == family_id, RefreshToken.revoked_at.is_(None)
        )
    ):
        token.revoked_at = now


@dataclass(frozen=True, slots=True)
class RefreshResult:
    access_token: str
    refresh_token: str
    expires_in: int
    idle_seconds: int


def refresh_session(session: Session, settings: Settings, *, raw_token: str) -> RefreshResult:
    """Exchange a refresh token for a new access token, rotating the refresh token.

    Presenting an already-rotated token means the cookie leaked and is being replayed,
    so the whole family is revoked rather than served (ADR-001).
    """
    now = utcnow()
    stored = session.scalar(
        select(RefreshToken).where(RefreshToken.token_hash == hash_refresh_token(raw_token))
    )
    if stored is None:
        raise DomainError("REFRESH_INVALID")
    if stored.rotated_at is not None or stored.revoked_at is not None:
        _revoke_family(session, stored.family_id, "refresh_token_reuse")
        raise DomainError("REFRESH_REUSED")
    if stored.expires_at <= now or stored.idle_expires_at <= now:
        raise DomainError("REFRESH_INVALID")

    auth_session = session.get(AuthSession, stored.family_id)
    if auth_session is None or auth_session.is_revoked or auth_session.expires_at <= now:
        raise DomainError("REFRESH_INVALID")

    idle_seconds = (
        settings.refresh_idle_web_seconds
        if auth_session.client == WEB_CLIENT
        else settings.refresh_idle_capture_seconds
    )
    stored.rotated_at = now
    raw_next, next_hash = new_refresh_token()
    session.add(
        RefreshToken(
            token_hash=next_hash,
            family_id=auth_session.id,
            user_id=stored.user_id,
            device_id=stored.device_id,
            expires_at=auth_session.expires_at,
            idle_expires_at=now + timedelta(seconds=idle_seconds),
        )
    )
    auth_session.last_seen_at = now

    access = create_access_token(
        settings.jwt_secret.get_secret_value(),
        user_id=stored.user_id,
        tenant_id=auth_session.active_tenant_id,
        session_id=auth_session.id,
        ttl_seconds=settings.access_token_ttl_seconds,
        now=now,
    )
    return RefreshResult(
        access_token=access,
        refresh_token=raw_next,
        expires_in=settings.access_token_ttl_seconds,
        idle_seconds=idle_seconds,
    )


def switch_tenant(
    session: Session,
    settings: Settings,
    *,
    user_id: uuid.UUID,
    session_id: uuid.UUID,
    tenant_id: uuid.UUID,
) -> tuple[str, int]:
    """Re-issue the access token for another organisation the user belongs to."""
    bind_context(session, tenant_id=None, user_id=user_id)
    if tenant_id not in {m.tenant_id for m in active_memberships(session, user_id)}:
        raise DomainError("NOT_A_MEMBER")

    auth_session = session.get(AuthSession, session_id)
    if auth_session is None or auth_session.is_revoked:
        raise DomainError("SESSION_REVOKED")
    auth_session.active_tenant_id = tenant_id

    user = session.get(AppUser, user_id)
    if user is not None:
        user.last_active_tenant_id = tenant_id

    access = create_access_token(
        settings.jwt_secret.get_secret_value(),
        user_id=user_id,
        tenant_id=tenant_id,
        session_id=session_id,
        ttl_seconds=settings.access_token_ttl_seconds,
    )
    return access, settings.access_token_ttl_seconds
