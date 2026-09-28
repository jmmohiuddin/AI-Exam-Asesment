"""Authentication endpoints: ``/v1/auth/*`` and ``/v1/me``."""

from __future__ import annotations

import uuid
from typing import Annotated, Literal

from fastapi import APIRouter, Header, Response, status
from pydantic import BaseModel, ConfigDict, Field

from khata.core.roles import Role
from khata.modules.authz.deps import DatabaseDep, PrincipalDep, SettingsDep
from khata.modules.identity.service import (
    CAPTURE_CLIENT,
    WEB_CLIENT,
    Membership,
    active_memberships,
    sign_in,
    sign_out,
)

router = APIRouter(tags=["auth"])

REFRESH_COOKIE = "khata_refresh"
REFRESH_COOKIE_PATH = "/v1/auth"


class LoginRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mobile: str = Field(pattern=r"^\+[1-9][0-9]{7,14}$")
    password: str = Field(min_length=1, max_length=256)
    tenant_id: uuid.UUID | None = None
    device_name: str = Field(default="browser", max_length=100)


class MembershipOut(BaseModel):
    tenant_id: uuid.UUID
    tenant_name: str
    role: Role
    school_id: uuid.UUID | None
    subject_code: str | None

    @classmethod
    def of(cls, membership: Membership) -> MembershipOut:
        return cls(
            tenant_id=membership.tenant_id,
            tenant_name=membership.tenant_name,
            role=membership.role,
            school_id=membership.school_id,
            subject_code=membership.subject_code,
        )


class UserOut(BaseModel):
    id: uuid.UUID
    mobile: str
    name: str
    locale: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: Literal["Bearer"] = "Bearer"  # noqa: S105 - the OAuth scheme name
    expires_in: int
    active_tenant_id: uuid.UUID | None
    user: UserOut
    memberships: list[MembershipOut]
    #: Only returned to the capture client; web receives it as an HttpOnly cookie.
    refresh_token: str | None = None


class MeResponse(BaseModel):
    user: UserOut
    active_tenant_id: uuid.UUID | None
    memberships: list[MembershipOut]
    roles: list[Role]


@router.post("/auth/login", response_model=LoginResponse)
def login(
    payload: LoginRequest,
    response: Response,
    database: DatabaseDep,
    settings: SettingsDep,
    x_client: Annotated[Literal["web", "capture"], Header(alias="X-Client")] = WEB_CLIENT,
) -> LoginResponse:
    with database.session_scope(None) as session:
        result = sign_in(
            session,
            settings,
            mobile=payload.mobile,
            password=payload.password,
            client=x_client,
            device_name=payload.device_name,
            tenant_id=payload.tenant_id,
        )
        body = LoginResponse(
            access_token=result.access_token,
            expires_in=result.expires_in,
            active_tenant_id=result.active_tenant_id,
            user=UserOut(
                id=result.user.id,
                mobile=result.user.mobile,
                name=result.user.name,
                locale=result.user.locale,
            ),
            memberships=[MembershipOut.of(m) for m in result.memberships],
            refresh_token=result.refresh_token if x_client == CAPTURE_CLIENT else None,
        )
        refresh = result.refresh_token
        idle = (
            settings.refresh_idle_web_seconds
            if x_client == WEB_CLIENT
            else settings.refresh_idle_capture_seconds
        )

    if x_client == WEB_CLIENT:
        # Not readable by JavaScript, so an XSS bug cannot exfiltrate the refresh token.
        response.set_cookie(
            REFRESH_COOKIE,
            refresh,
            max_age=idle,
            httponly=True,
            secure=settings.cookie_secure,
            samesite="strict",
            path=REFRESH_COOKIE_PATH,
        )
    return body


@router.post("/auth/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    response: Response, principal: PrincipalDep, database: DatabaseDep, settings: SettingsDep
) -> None:
    with database.session_scope(None, user_id=principal.user_id) as session:
        sign_out(session, principal.session_id)
    response.delete_cookie(
        REFRESH_COOKIE,
        path=REFRESH_COOKIE_PATH,
        httponly=True,
        secure=settings.cookie_secure,
        samesite="strict",
    )


@router.get("/me", response_model=MeResponse)
def me(principal: PrincipalDep, database: DatabaseDep) -> MeResponse:
    from khata.modules.identity.models import AppUser

    with database.session_scope(None, user_id=principal.user_id) as session:
        user = session.get(AppUser, principal.user_id)
        if user is None:  # pragma: no cover - the token proved the user exists
            from khata.core.errors import DomainError

            raise DomainError("UNAUTHENTICATED")
        memberships = active_memberships(session, principal.user_id)
        out = UserOut(id=user.id, mobile=user.mobile, name=user.name, locale=user.locale)

    return MeResponse(
        user=out,
        active_tenant_id=principal.tenant_id,
        memberships=[MembershipOut.of(m) for m in memberships],
        roles=sorted(principal.roles),
    )
