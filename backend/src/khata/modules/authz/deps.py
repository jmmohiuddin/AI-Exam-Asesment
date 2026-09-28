"""Request authentication and authorisation (08 §5.3).

Two layers, always both: this module decides in the application, and every tenant
table additionally enforces RLS in PostgreSQL against ``app.tenant_id`` (ADR-003).
A bug here therefore cannot by itself leak another tenant's rows.
"""

from __future__ import annotations

import uuid
from collections.abc import Iterator
from dataclasses import dataclass
from datetime import datetime
from typing import Annotated

from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from khata.core.config import Settings
from khata.core.db import Database
from khata.core.errors import DomainError
from khata.core.models import utcnow
from khata.core.roles import Role
from khata.core.security import (
    AccessClaims,
    TokenExpiredError,
    TokenInvalidError,
    decode_access_token,
)
from khata.modules.identity.models import AuthSession
from khata.modules.identity.service import Membership, active_memberships

_bearer = HTTPBearer(auto_error=False)


@dataclass(frozen=True, slots=True)
class Principal:
    """Who is making this request, and in which tenant."""

    user_id: uuid.UUID
    session_id: uuid.UUID
    tenant_id: uuid.UUID | None
    memberships: tuple[Membership, ...]

    @property
    def roles(self) -> frozenset[Role]:
        """Roles held in the active tenant (empty when no tenant is selected)."""
        if self.tenant_id is None:
            return frozenset()
        return frozenset(m.role for m in self.memberships if m.tenant_id == self.tenant_id)

    def require_tenant(self) -> uuid.UUID:
        if self.tenant_id is None:
            raise DomainError("NO_ACTIVE_TENANT")
        return self.tenant_id

    def has_any(self, *roles: Role) -> bool:
        return bool(self.roles & frozenset(roles))


def get_database(request: Request) -> Database:
    database: Database = request.app.state.db
    return database


def get_settings_dep(request: Request) -> Settings:
    settings: Settings = request.app.state.settings
    return settings


DatabaseDep = Annotated[Database, Depends(get_database)]
SettingsDep = Annotated[Settings, Depends(get_settings_dep)]


def _claims(settings: Settings, credentials: HTTPAuthorizationCredentials | None) -> AccessClaims:
    if credentials is None or not credentials.credentials:
        raise DomainError("UNAUTHENTICATED")
    try:
        return decode_access_token(settings.jwt_secret.get_secret_value(), credentials.credentials)
    except TokenExpiredError as exc:
        raise DomainError("TOKEN_EXPIRED") from exc
    except TokenInvalidError as exc:
        raise DomainError("UNAUTHENTICATED") from exc


def _assert_session_usable(auth_session: AuthSession | None, now: datetime) -> AuthSession:
    if auth_session is None:
        raise DomainError("UNAUTHENTICATED")
    if auth_session.revoked_at is not None:
        raise DomainError("SESSION_REVOKED")
    if auth_session.expires_at <= now:
        raise DomainError("TOKEN_EXPIRED")
    return auth_session


def current_principal(
    database: DatabaseDep,
    settings: SettingsDep,
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(_bearer)] = None,
) -> Principal:
    """Resolve the bearer token to a live session and the user's memberships.

    The token alone is not enough: the session must still exist and be unrevoked,
    so signing out takes effect before the access token expires.
    """
    claims = _claims(settings, credentials)
    now = utcnow()
    # No tenant bound: identity tables are global and the membership RLS policies
    # only expose the caller's own rows in this state.
    with database.session_scope(None, user_id=claims.user_id) as session:
        auth_session = _assert_session_usable(session.get(AuthSession, claims.session_id), now)
        if auth_session.user_id != claims.user_id:
            raise DomainError("UNAUTHENTICATED")
        memberships = active_memberships(session, claims.user_id)
        auth_session.last_seen_at = now
        tenant_id = claims.tenant_id

    if tenant_id is not None and tenant_id not in {m.tenant_id for m in memberships}:
        # The role was revoked after the token was issued.
        raise DomainError("NOT_A_MEMBER")
    return Principal(
        user_id=claims.user_id,
        session_id=claims.session_id,
        tenant_id=tenant_id,
        memberships=memberships,
    )


PrincipalDep = Annotated[Principal, Depends(current_principal)]


def tenant_session(principal: PrincipalDep, database: DatabaseDep) -> Iterator[Session]:
    """One transaction for the request, with the RLS tenant context bound."""
    tenant_id = principal.require_tenant()
    with database.session_scope(tenant_id, user_id=principal.user_id) as session:
        yield session


TenantSession = Annotated[Session, Depends(tenant_session)]


class RequireRoles:
    """Dependency factory: ``Depends(RequireRoles(Role.TEACHER))``."""

    def __init__(self, *roles: Role) -> None:
        if not roles:
            raise ValueError("at least one role is required")
        self.roles = frozenset(roles)

    def __call__(self, principal: PrincipalDep) -> Principal:
        principal.require_tenant()
        if not principal.has_any(*self.roles):
            raise DomainError("PERMISSION_DENIED")
        return principal


#: Roles that may build and lock an exam's rubric.
CAN_AUTHOR_EXAM = RequireRoles(
    Role.TEACHER, Role.EXAM_COORDINATOR, Role.HOD, Role.SCHOOL_ADMIN, Role.ORG_OWNER
)
#: Roles that may decide marks. Capture operators deliberately cannot.
CAN_MARK = RequireRoles(Role.TEACHER, Role.EXAM_COORDINATOR, Role.HOD)
#: Roles that may lock and publish results.
CAN_PUBLISH = RequireRoles(Role.EXAM_COORDINATOR, Role.SCHOOL_ADMIN, Role.ORG_OWNER)
