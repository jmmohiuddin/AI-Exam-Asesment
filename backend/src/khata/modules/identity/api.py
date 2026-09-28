"""Authentication endpoints: ``/v1/auth/*`` and ``/v1/me``.

The response shapes are the ones ``web/src/auth/types.ts`` already encodes, so the
two halves of the product agree without an adapter in between. ``status`` on the
login response is the discriminator: ``otp_required`` from a device the account
has never used, ``ok`` from one it has.
"""

from __future__ import annotations

import uuid
from collections import defaultdict
from datetime import datetime
from typing import Annotated, Literal

from fastapi import APIRouter, Cookie, Depends, Header, Request, Response, status
from pydantic import BaseModel, ConfigDict, Field

from khata.core.errors import DomainError
from khata.core.roles import Role
from khata.modules.authz.deps import DatabaseDep, PrincipalDep, SettingsDep
from khata.modules.identity.delivery import OtpSender
from khata.modules.identity.models import AppUser
from khata.modules.identity.otp import resend as resend_challenge
from khata.modules.identity.service import (
    CAPTURE_CLIENT,
    WEB_CLIENT,
    Membership,
    OtpRequired,
    SignInResult,
    active_memberships,
    complete_otp_login,
    mask_mobile,
    refresh_session,
    sign_in,
    sign_out,
    switch_tenant,
)

router = APIRouter(tags=["auth"])

REFRESH_COOKIE = "khata_refresh"
REFRESH_COOKIE_PATH = "/v1/auth"


class LoginRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mobile: str = Field(pattern=r"^\+[1-9][0-9]{7,14}$")
    password: str = Field(min_length=1, max_length=256)
    tenant_id: uuid.UUID | None = None
    #: A device id the client kept from an earlier OTP sign-in. Unknown, revoked
    #: or someone else's id simply means a code is required.
    device_id: uuid.UUID | None = None
    device_name: str = Field(default="browser", max_length=100)


class OtpVerifyRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    challenge_id: uuid.UUID
    code: str = Field(pattern=r"^[0-9]{6}$")
    device_name: str = Field(default="browser", max_length=100)
    tenant_id: uuid.UUID | None = None


class OtpResendRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    challenge_id: uuid.UUID


class SwitchTenantRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    tenant_id: uuid.UUID


class AuthUser(BaseModel):
    id: uuid.UUID
    name: str
    locale: str


class MembershipOut(BaseModel):
    """All roles a user holds at one school, grouped (the UI reasons per school)."""

    tenant_id: uuid.UUID
    org_name: str
    school_id: uuid.UUID | None
    school_name_bn: str
    school_name_en: str
    roles: list[Role]


class LoginResponse(BaseModel):
    status: Literal["ok"] = "ok"
    access_token: str
    expires_in: int
    user: AuthUser
    #: Returned to the capture client only; web receives it as an HttpOnly cookie.
    refresh_token: str | None = None


class LoginOtpRequired(BaseModel):
    """No token yet: the code proves the device, not the password."""

    status: Literal["otp_required"] = "otp_required"
    challenge_id: uuid.UUID
    otp_expires_at: datetime


class OtpVerifyResponse(BaseModel):
    status: Literal["ok"] = "ok"
    access_token: str
    expires_in: int
    #: The client stores this and sends it on later logins to skip the code.
    device_id: uuid.UUID
    user: AuthUser
    refresh_token: str | None = None


class OtpResendResponse(BaseModel):
    challenge_id: uuid.UUID
    otp_expires_at: datetime


class TokenResponse(BaseModel):
    access_token: str
    expires_in: int


class MeResponse(BaseModel):
    id: uuid.UUID
    name: str
    mobile_masked: str
    locale: str
    preferences: dict[str, object] | None
    platform_role: str | None
    memberships: list[MembershipOut]
    active_tenant_id: uuid.UUID | None


def _group_memberships(memberships: tuple[Membership, ...]) -> list[MembershipOut]:
    grouped: dict[tuple[uuid.UUID, uuid.UUID | None], list[Membership]] = defaultdict(list)
    for membership in memberships:
        grouped[(membership.tenant_id, membership.school_id)].append(membership)
    return [
        MembershipOut(
            tenant_id=tenant_id,
            org_name=items[0].tenant_name,
            school_id=school_id,
            school_name_bn=items[0].school_name_bn,
            school_name_en=items[0].school_name_en,
            roles=sorted({item.role for item in items}),
        )
        for (tenant_id, school_id), items in grouped.items()
    ]


def get_otp_sender(request: Request) -> OtpSender:
    sender: OtpSender = request.app.state.otp_sender
    return sender


OtpSenderDep = Annotated[OtpSender, Depends(get_otp_sender)]


def _set_refresh_cookie(response: Response, token: str, *, max_age: int, secure: bool) -> None:
    # Not readable by JavaScript, so an XSS bug cannot exfiltrate the refresh token.
    response.set_cookie(
        REFRESH_COOKIE,
        token,
        max_age=max_age,
        httponly=True,
        secure=secure,
        samesite="strict",
        path=REFRESH_COOKIE_PATH,
    )


def _signed_in_body(result: SignInResult, client: str) -> LoginResponse:
    return LoginResponse(
        access_token=result.access_token,
        expires_in=result.expires_in,
        user=AuthUser(id=result.user.id, name=result.user.name, locale=result.user.locale),
        refresh_token=result.refresh_token if client == CAPTURE_CLIENT else None,
    )


@router.post("/auth/login", response_model=LoginResponse | LoginOtpRequired)
def login(
    payload: LoginRequest,
    response: Response,
    database: DatabaseDep,
    settings: SettingsDep,
    sender: OtpSenderDep,
    x_client: Annotated[Literal["web", "capture"], Header(alias="X-Client")] = WEB_CLIENT,
) -> LoginResponse | LoginOtpRequired:
    with database.session_scope(None) as session:
        result = sign_in(
            session,
            settings,
            sender,
            mobile=payload.mobile,
            password=payload.password,
            client=x_client,
            device_name=payload.device_name,
            device_id=payload.device_id,
            tenant_id=payload.tenant_id,
        )
        if isinstance(result, OtpRequired):
            return LoginOtpRequired(
                challenge_id=result.challenge.id, otp_expires_at=result.challenge.expires_at
            )
        body = _signed_in_body(result, x_client)
        refresh = result.refresh_token

    if x_client == WEB_CLIENT:
        _set_refresh_cookie(
            response,
            refresh,
            max_age=settings.refresh_idle_web_seconds,
            secure=settings.cookie_secure,
        )
    return body


@router.post("/auth/otp/verify", response_model=OtpVerifyResponse)
def verify_otp(
    payload: OtpVerifyRequest,
    response: Response,
    database: DatabaseDep,
    settings: SettingsDep,
    x_client: Annotated[Literal["web", "capture"], Header(alias="X-Client")] = WEB_CLIENT,
) -> OtpVerifyResponse:
    with database.session_scope(None) as session:
        result = complete_otp_login(
            session,
            settings,
            database,
            challenge_id=payload.challenge_id,
            code=payload.code,
            client=x_client,
            device_name=payload.device_name,
            tenant_id=payload.tenant_id,
        )
        body = OtpVerifyResponse(
            access_token=result.access_token,
            expires_in=result.expires_in,
            device_id=result.session.device_id,
            user=AuthUser(id=result.user.id, name=result.user.name, locale=result.user.locale),
            refresh_token=result.refresh_token if x_client == CAPTURE_CLIENT else None,
        )
        refresh = result.refresh_token

    if x_client == WEB_CLIENT:
        _set_refresh_cookie(
            response,
            refresh,
            max_age=settings.refresh_idle_web_seconds,
            secure=settings.cookie_secure,
        )
    return body


@router.post("/auth/otp/resend", response_model=OtpResendResponse)
def resend_otp(
    payload: OtpResendRequest,
    database: DatabaseDep,
    settings: SettingsDep,
    sender: OtpSenderDep,
) -> OtpResendResponse:
    """Re-issue the code for a live challenge. The previous code stops working."""
    with database.session_scope(None) as session:
        challenge = resend_challenge(session, settings, sender, challenge_id=payload.challenge_id)
    return OtpResendResponse(challenge_id=challenge.id, otp_expires_at=challenge.expires_at)


@router.post("/auth/refresh", response_model=TokenResponse)
def refresh(
    response: Response,
    database: DatabaseDep,
    settings: SettingsDep,
    khata_refresh: Annotated[str | None, Cookie(alias=REFRESH_COOKIE)] = None,
) -> TokenResponse:
    """Rotate the refresh cookie and mint a new access token."""
    if not khata_refresh:
        raise DomainError("REFRESH_INVALID")
    with database.session_scope(None) as session:
        result = refresh_session(session, settings, raw_token=khata_refresh)
    _set_refresh_cookie(
        response,
        result.refresh_token,
        max_age=result.idle_seconds,
        secure=settings.cookie_secure,
    )
    return TokenResponse(access_token=result.access_token, expires_in=result.expires_in)


@router.post("/auth/switch-tenant", response_model=TokenResponse)
def switch(
    payload: SwitchTenantRequest,
    principal: PrincipalDep,
    database: DatabaseDep,
    settings: SettingsDep,
) -> TokenResponse:
    with database.session_scope(None, user_id=principal.user_id) as session:
        access, expires_in = switch_tenant(
            session,
            settings,
            user_id=principal.user_id,
            session_id=principal.session_id,
            tenant_id=payload.tenant_id,
        )
    return TokenResponse(access_token=access, expires_in=expires_in)


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
    with database.session_scope(None, user_id=principal.user_id) as session:
        user = session.get(AppUser, principal.user_id)
        if user is None:  # pragma: no cover - the token proved the user exists
            raise DomainError("UNAUTHENTICATED")
        memberships = active_memberships(session, principal.user_id)
        return MeResponse(
            id=user.id,
            name=user.name,
            mobile_masked=mask_mobile(user.mobile),
            locale=user.locale,
            preferences=dict(user.preferences or {}),
            platform_role=user.platform_role,
            memberships=_group_memberships(memberships),
            active_tenant_id=principal.tenant_id,
        )
