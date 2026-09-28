"""The auth contract the web client codes against, plus refresh-token safety."""

from __future__ import annotations

from collections.abc import Callable

import pytest
from fastapi.testclient import TestClient

from khata.modules.identity.api import REFRESH_COOKIE
from khata.modules.identity.service import mask_mobile

pytestmark = pytest.mark.integration


def _login(sign_in: Callable[..., dict], seed: dict[str, object]) -> dict:
    return sign_in(str(seed["teacher_mobile"]), str(seed["password"]))


@pytest.mark.parametrize(
    ("mobile", "expected"),
    [
        ("+8801712345678", "+880****5678"),
        ("+880171234", "+880****1234"),
        ("+8801", "****"),
    ],
)
def test_mask_mobile_never_shows_the_whole_number(mobile: str, expected: str) -> None:
    masked = mask_mobile(mobile)
    assert masked == expected
    assert mobile not in masked, "the full number must never survive masking"


def test_mask_mobile_does_not_leak_the_length() -> None:
    """Two numbers of different lengths must not be distinguishable by the mask."""
    short = mask_mobile("+8801712345")
    long = mask_mobile("+880171234567890")
    assert len(short) == len(long)


def test_login_shape_matches_the_web_client(
    sign_in: Callable[..., dict], client: TestClient, seed: dict[str, object]
) -> None:
    body = _login(sign_in, seed)
    assert body["status"] == "ok"
    assert body["expires_in"] > 0
    assert set(body["user"]) == {"id", "name", "locale"}
    # The web client must never receive the refresh token in the body.
    assert body["refresh_token"] is None
    assert REFRESH_COOKIE in client.cookies


def test_capture_client_gets_the_refresh_token_in_the_body(
    sign_in: Callable[..., dict], seed: dict[str, object]
) -> None:
    body = sign_in(str(seed["teacher_mobile"]), str(seed["password"]), client_kind="capture")
    assert body["refresh_token"]


def test_me_shape_matches_the_web_client(
    sign_in: Callable[..., dict], client: TestClient, seed: dict[str, object]
) -> None:
    token = _login(sign_in, seed)["access_token"]
    response = client.get("/v1/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200, response.text
    body = response.json()
    assert set(body) == {
        "id",
        "name",
        "mobile_masked",
        "locale",
        "preferences",
        "platform_role",
        "memberships",
        "active_tenant_id",
    }
    assert body["mobile_masked"] == mask_mobile(str(seed["teacher_mobile"]))
    membership = body["memberships"][0]
    assert set(membership) == {
        "tenant_id",
        "org_name",
        "school_id",
        "school_name_bn",
        "school_name_en",
        "roles",
    }
    assert membership["roles"] == ["exam_coordinator"]
    assert body["active_tenant_id"] == str(seed["tenant_id"])


def test_refresh_rotates_the_cookie_and_returns_a_new_access_token(
    sign_in: Callable[..., dict], client: TestClient, seed: dict[str, object]
) -> None:
    first = _login(sign_in, seed)
    original_cookie = client.cookies[REFRESH_COOKIE]

    response = client.post("/v1/auth/refresh")
    assert response.status_code == 200, response.text
    assert response.json()["access_token"] != first["access_token"]
    assert client.cookies[REFRESH_COOKIE] != original_cookie, "the cookie must rotate"


def test_replaying_a_rotated_refresh_token_kills_the_session(
    sign_in: Callable[..., dict], client: TestClient, seed: dict[str, object]
) -> None:
    """A replayed refresh cookie means it leaked: revoke the family, do not serve it."""
    _login(sign_in, seed)
    stolen = client.cookies[REFRESH_COOKIE]

    assert client.post("/v1/auth/refresh").status_code == 200

    client.cookies.set(REFRESH_COOKIE, stolen, path="/v1/auth")
    replayed = client.post("/v1/auth/refresh")
    assert replayed.status_code == 401
    assert replayed.json()["code"] == "REFRESH_REUSED"

    # The whole family is gone, so the legitimate holder is locked out too.
    client.cookies.clear()
    assert client.post("/v1/auth/refresh").status_code == 401


def test_refresh_without_a_cookie_is_rejected(client: TestClient) -> None:
    client.cookies.clear()
    response = client.post("/v1/auth/refresh")
    assert response.status_code == 401
    assert response.json()["code"] == "REFRESH_INVALID"


def test_switching_to_a_tenant_you_do_not_belong_to_is_refused(
    sign_in: Callable[..., dict], client: TestClient, seed: dict[str, object]
) -> None:
    import uuid

    token = _login(sign_in, seed)["access_token"]
    response = client.post(
        "/v1/auth/switch-tenant",
        headers={"Authorization": f"Bearer {token}"},
        json={"tenant_id": str(uuid.uuid4())},
    )
    assert response.status_code == 403
    assert response.json()["code"] == "NOT_A_MEMBER"


def test_wrong_password_is_indistinguishable_from_an_unknown_account(
    client: TestClient, seed: dict[str, object]
) -> None:
    wrong = client.post(
        "/v1/auth/login",
        json={"mobile": seed["teacher_mobile"], "password": "not-the-password"},
    )
    unknown = client.post(
        "/v1/auth/login",
        json={"mobile": "+8809999999999", "password": "not-the-password"},
    )
    assert wrong.status_code == unknown.status_code == 401
    assert wrong.json()["code"] == unknown.json()["code"] == "INVALID_CREDENTIALS"
