"""OTP sign-in on a new device (FR-ORG-04, SEC-04/TR-AUTH-02, 08 §5.2).

The policy: password alone is not enough from a device the account has never used.
The web client already codes for the ``otp_required`` discriminator
(``web/src/auth/types.ts``), so these tests pin that contract.
"""

from __future__ import annotations

import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text

from khata.core.config import Settings
from khata.core.db import Database
from khata.modules.identity.api import REFRESH_COOKIE

pytestmark = pytest.mark.integration


def start_login(
    client: TestClient, seed: dict[str, object], *, device_id: str | None = None
) -> dict:
    payload: dict[str, object] = {
        "mobile": seed["teacher_mobile"],
        "password": seed["password"],
    }
    if device_id is not None:
        payload["device_id"] = device_id
    response = client.post("/v1/auth/login", json=payload, headers={"X-Client": "web"})
    assert response.status_code == 200, response.text
    return response.json()


def last_code(client: TestClient) -> str:
    sender = client.app.state.otp_sender  # type: ignore[attr-defined]
    return sender.last_code()


def verify(client: TestClient, challenge_id: str, code: str, **extra: object) -> object:
    return client.post(
        "/v1/auth/otp/verify",
        json={"challenge_id": challenge_id, "code": code, "device_name": "browser", **extra},
        headers={"X-Client": "web"},
    )


class TestNewDevice:
    def test_password_alone_does_not_sign_in_from_an_unknown_device(
        self, client: TestClient, seed: dict[str, object]
    ) -> None:
        body = start_login(client, seed)
        assert body["status"] == "otp_required"
        assert uuid.UUID(body["challenge_id"])
        assert body["otp_expires_at"]
        assert "access_token" not in body
        assert REFRESH_COOKIE not in client.cookies

    def test_the_code_completes_the_sign_in_and_returns_the_device_id(
        self, client: TestClient, seed: dict[str, object]
    ) -> None:
        body = start_login(client, seed)
        response = verify(client, body["challenge_id"], last_code(client))
        assert response.status_code == 200, response.text
        verified = response.json()
        assert verified["status"] == "ok"
        assert verified["expires_in"] > 0
        assert uuid.UUID(verified["device_id"])
        assert set(verified["user"]) == {"id", "name", "locale"}
        assert REFRESH_COOKIE in client.cookies

    def test_a_known_device_skips_the_code(
        self, client: TestClient, seed: dict[str, object]
    ) -> None:
        first = start_login(client, seed)
        device_id = verify(client, first["challenge_id"], last_code(client)).json()["device_id"]  # type: ignore[union-attr]

        again = start_login(client, seed, device_id=device_id)
        assert again["status"] == "ok"
        assert again["access_token"]

    def test_another_users_device_id_does_not_skip_the_code(
        self, client: TestClient, seed: dict[str, object], database: Database
    ) -> None:
        first = start_login(client, seed)
        verify(client, first["challenge_id"], last_code(client))
        stranger_device = uuid.uuid4()
        body = start_login(client, seed, device_id=str(stranger_device))
        assert body["status"] == "otp_required"

    def test_a_revoked_device_does_not_skip_the_code(
        self, client: TestClient, seed: dict[str, object], database: Database
    ) -> None:
        first = start_login(client, seed)
        device_id = verify(client, first["challenge_id"], last_code(client)).json()["device_id"]  # type: ignore[union-attr]
        with database.session_scope(None) as session:
            session.execute(
                text("UPDATE device SET revoked_at = now() WHERE id = :id"),
                {"id": uuid.UUID(device_id)},
            )
        assert start_login(client, seed, device_id=device_id)["status"] == "otp_required"

    def test_the_capture_client_gets_its_refresh_token_in_the_body(
        self, client: TestClient, seed: dict[str, object]
    ) -> None:
        response = client.post(
            "/v1/auth/login",
            json={"mobile": seed["teacher_mobile"], "password": seed["password"]},
            headers={"X-Client": "capture"},
        )
        body = response.json()
        verified = client.post(
            "/v1/auth/otp/verify",
            json={
                "challenge_id": body["challenge_id"],
                "code": last_code(client),
                "device_name": "Pixel 6a",
            },
            headers={"X-Client": "capture"},
        ).json()
        assert verified["refresh_token"]


class TestWrongCodes:
    def test_a_wrong_code_is_rejected(self, client: TestClient, seed: dict[str, object]) -> None:
        body = start_login(client, seed)
        wrong = "000000" if last_code(client) != "000000" else "111111"
        response = verify(client, body["challenge_id"], wrong)
        assert response.status_code == 400
        assert response.json()["code"] == "OTP_INVALID"

    def test_the_challenge_dies_after_the_attempt_limit(
        self, client: TestClient, seed: dict[str, object], test_settings: Settings
    ) -> None:
        body = start_login(client, seed)
        code = last_code(client)
        wrong = "000000" if code != "000000" else "111111"
        for _ in range(test_settings.otp_max_attempts):
            assert verify(client, body["challenge_id"], wrong).status_code == 400  # type: ignore[union-attr]
        blocked = verify(client, body["challenge_id"], code)
        assert blocked.status_code == 400  # type: ignore[union-attr]
        assert blocked.json()["code"] == "OTP_ATTEMPTS_EXCEEDED"  # type: ignore[union-attr]

    def test_an_expired_challenge_is_rejected(
        self, client: TestClient, seed: dict[str, object], database: Database
    ) -> None:
        body = start_login(client, seed)
        with database.session_scope(None) as session:
            session.execute(
                text(
                    "UPDATE otp_challenge SET expires_at = now() - interval '1 second'"
                    " WHERE id = :id"
                ),
                {"id": uuid.UUID(body["challenge_id"])},
            )
        response = verify(client, body["challenge_id"], last_code(client))
        assert response.status_code == 400  # type: ignore[union-attr]
        assert response.json()["code"] == "OTP_EXPIRED"  # type: ignore[union-attr]

    def test_a_code_works_once(self, client: TestClient, seed: dict[str, object]) -> None:
        body = start_login(client, seed)
        code = last_code(client)
        assert verify(client, body["challenge_id"], code).status_code == 200  # type: ignore[union-attr]
        replayed = verify(client, body["challenge_id"], code)
        assert replayed.status_code == 400  # type: ignore[union-attr]
        assert replayed.json()["code"] == "OTP_INVALID"  # type: ignore[union-attr]

    def test_an_unknown_challenge_is_rejected(self, client: TestClient) -> None:
        response = verify(client, str(uuid.uuid4()), "123456")
        assert response.status_code == 400  # type: ignore[union-attr]
        assert response.json()["code"] == "OTP_INVALID"  # type: ignore[union-attr]

    def test_a_non_numeric_code_is_rejected_by_the_schema(self, client: TestClient) -> None:
        response = verify(client, str(uuid.uuid4()), "abcdef")
        assert response.status_code == 422  # type: ignore[union-attr]


class TestSendLimits:
    def test_resend_delivers_a_fresh_code_for_the_same_challenge(
        self, client: TestClient, seed: dict[str, object]
    ) -> None:
        body = start_login(client, seed)
        first = last_code(client)
        response = client.post("/v1/auth/otp/resend", json={"challenge_id": body["challenge_id"]})
        assert response.status_code == 200, response.text
        assert response.json()["challenge_id"] == body["challenge_id"]
        second = last_code(client)
        assert second != first
        assert verify(client, body["challenge_id"], second).status_code == 200  # type: ignore[union-attr]

    def test_the_old_code_stops_working_after_a_resend(
        self, client: TestClient, seed: dict[str, object]
    ) -> None:
        body = start_login(client, seed)
        first = last_code(client)
        client.post("/v1/auth/otp/resend", json={"challenge_id": body["challenge_id"]})
        response = verify(client, body["challenge_id"], first)
        assert response.status_code == 400  # type: ignore[union-attr]
        assert response.json()["code"] == "OTP_INVALID"  # type: ignore[union-attr]

    def test_sends_are_capped_per_hour(
        self, client: TestClient, seed: dict[str, object], test_settings: Settings
    ) -> None:
        body = start_login(client, seed)  # send 1
        for _ in range(test_settings.otp_sends_per_hour - 1):
            assert (
                client.post(
                    "/v1/auth/otp/resend", json={"challenge_id": body["challenge_id"]}
                ).status_code
                == 200
            )
        limited = client.post("/v1/auth/otp/resend", json={"challenge_id": body["challenge_id"]})
        assert limited.status_code == 429
        assert limited.json()["code"] == "OTP_RATE_LIMITED"

    def test_an_older_send_does_not_count_against_the_hourly_cap(
        self, client: TestClient, seed: dict[str, object], database: Database
    ) -> None:
        body = start_login(client, seed)
        # otp_send is insert-only for the app role, so age the rows as the owner.
        with database.owner_engine.begin() as connection:
            connection.execute(text("UPDATE otp_send SET sent_at = now() - interval '2 hours'"))
        response = client.post("/v1/auth/otp/resend", json={"challenge_id": body["challenge_id"]})
        assert response.status_code == 200, response.text


class TestNoLeaks:
    def test_the_challenge_never_carries_the_code(
        self, client: TestClient, seed: dict[str, object]
    ) -> None:
        body = start_login(client, seed)
        assert last_code(client) not in str(body)

    def test_the_stored_challenge_holds_a_hash_not_the_code(
        self, client: TestClient, seed: dict[str, object], database: Database
    ) -> None:
        body = start_login(client, seed)
        code = last_code(client)
        with database.session_scope(None) as session:
            stored = session.execute(
                text("SELECT code_hmac FROM otp_challenge WHERE id = :id"),
                {"id": uuid.UUID(body["challenge_id"])},
            ).scalar_one()
        assert code not in stored
        assert len(stored) == 64  # sha256 hex

    def test_a_wrong_password_never_starts_a_challenge(
        self, client: TestClient, seed: dict[str, object], database: Database
    ) -> None:
        response = client.post(
            "/v1/auth/login",
            json={"mobile": seed["teacher_mobile"], "password": "not-the-password"},
        )
        assert response.status_code == 401
        with database.session_scope(None) as session:
            count = session.execute(text("SELECT count(*) FROM otp_challenge")).scalar_one()
        assert count == 0

    def test_an_unknown_mobile_never_starts_a_challenge(
        self, client: TestClient, database: Database
    ) -> None:
        response = client.post(
            "/v1/auth/login",
            json={"mobile": "+8801999999999", "password": "whatever-it-is"},
        )
        assert response.status_code == 401
        with database.session_scope(None) as session:
            count = session.execute(text("SELECT count(*) FROM otp_challenge")).scalar_one()
        assert count == 0
