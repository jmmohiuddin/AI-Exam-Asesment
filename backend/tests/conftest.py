"""Shared fixtures.

Integration tests run against the real ``khata_test`` database, not a mock: RLS,
constraints and the migration chain are the things most worth testing, and none of
them exist in a fake. The schema is built once per session by running the real
migrations; each test starts from truncated tables.
"""

from __future__ import annotations

import os
import subprocess
import sys
import uuid
from collections.abc import Iterator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text

from khata.core.config import Environment, Settings
from khata.core.db import Database
from khata.core.roles import Role

BACKEND_DIR = Path(__file__).resolve().parents[1]
TEST_APP_URL_VAR = "KHATA_TEST_DATABASE_URL_APP"
TEST_OWNER_URL_VAR = "KHATA_TEST_DATABASE_URL_OWNER"

# Tables the migrations own and tests must not wipe.
PRESERVED_TABLES = frozenset({"alembic_version", "class_level"})


def _dotenv_value(name: str) -> str | None:
    """Read one key from ``backend/.env``.

    The test database URLs are deliberately not fields on ``Settings`` (core knows
    nothing about tests), so pydantic drops them as extras and they never reach
    ``os.environ``. Reading the file directly keeps them out of the app config.
    """
    env_file = BACKEND_DIR / ".env"
    if not env_file.is_file():
        return None
    for line in env_file.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, _, value = stripped.partition("=")
        if key.strip() == name:
            return value.split(" #")[0].strip().strip("'\"") or None
    return None


def _required_env(name: str) -> str:
    value = os.environ.get(name) or _dotenv_value(name)
    if not value:
        pytest.skip(f"{name} is not set; the integration database is unavailable")
    return value


@pytest.fixture(scope="session")
def test_settings() -> Settings:
    """Settings pointed at ``khata_test``, borrowing the dev secrets."""
    base = Settings()  # type: ignore[call-arg]  # from .env
    return base.model_copy(
        update={
            "env": Environment.TEST,
            "database_url_app": _required_env(TEST_APP_URL_VAR),
            "database_url_owner": _required_env(TEST_OWNER_URL_VAR),
        }
    )


@pytest.fixture(scope="session")
def migrated_database(test_settings: Settings) -> Iterator[Database]:
    """Run the real migration chain once, then hand back an app-role database."""
    environment = {
        **os.environ,
        "KHATA_ENV": "test",
        "KHATA_DATABASE_URL_APP": test_settings.database_url_app,
        "KHATA_DATABASE_URL_OWNER": test_settings.database_url_owner or "",
    }
    completed = subprocess.run(
        [sys.executable, "-m", "alembic", "upgrade", "head"],
        cwd=BACKEND_DIR,
        env=environment,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        pytest.fail(f"alembic upgrade failed:\n{completed.stdout}\n{completed.stderr}")

    database = Database.from_settings(test_settings)
    yield database
    database.dispose()


@pytest.fixture
def database(migrated_database: Database) -> Iterator[Database]:
    """Truncate every tenant table before each test, as the owner (RLS would hide rows)."""
    with migrated_database.owner_engine.begin() as connection:
        names = [
            row[0]
            for row in connection.execute(
                text(
                    "SELECT tablename FROM pg_tables"
                    " WHERE schemaname = 'public' AND tablename NOT LIKE 'procrastinate%'"
                )
            )
            if row[0] not in PRESERVED_TABLES
        ]
        if names:
            joined = ", ".join(names)
            # audit_event carries an append-only trigger that (correctly) refuses
            # deletes. The owner may disable it for the reset; production never does.
            for name in names:
                connection.execute(text(f"ALTER TABLE {name} DISABLE TRIGGER USER"))
            try:
                connection.execute(text(f"TRUNCATE {joined} RESTART IDENTITY CASCADE"))
            finally:
                for name in names:
                    connection.execute(text(f"ALTER TABLE {name} ENABLE TRIGGER USER"))
    yield migrated_database


@pytest.fixture
def client(database: Database, test_settings: Settings) -> Iterator[TestClient]:
    """A TestClient whose app reuses the already-migrated test database."""
    from khata.main import create_app

    app = create_app(test_settings)
    with TestClient(app) as running:
        # The lifespan built its own Database; swap in the truncated one so the
        # fixtures and the app observe exactly the same rows.
        running.app.state.db.dispose()
        running.app.state.db = database
        yield running


@pytest.fixture
def seed(database: Database) -> dict[str, object]:
    """One organisation, one school, and a teacher who can sign in.

    Written through the ordinary app role with the tenant context bound to the new
    organisation's id. Tables are ``FORCE``d RLS, so even the owner is subject to the
    policies: provisioning a tenant means choosing its id first and binding it, which
    is exactly what the real provisioning path has to do.
    """
    from khata.modules.identity.service import create_user
    from khata.modules.org.models import Organization, RoleAssignment, School

    password = "correct-horse-battery"
    tenant_id = uuid.uuid4()
    with database.session_scope(tenant_id) as session:
        org = Organization(id=tenant_id, name="Test Model School")
        session.add(org)
        session.flush()
        school = School(
            tenant_id=org.id,
            name_bn="পরীক্ষা বিদ্যালয়",
            name_en="Test Model School",
            board="dhaka",
        )
        session.add(school)
        teacher = create_user(
            session, mobile="+8801700000001", name="Rahim Teacher", password=password
        )
        other = create_user(
            session, mobile="+8801700000002", name="Other Tenant User", password=password
        )
        session.add(
            RoleAssignment(
                tenant_id=org.id,
                user_id=teacher.id,
                school_id=school.id,
                role=Role.EXAM_COORDINATOR.value,
            )
        )
        session.flush()
        result = {
            "tenant_id": org.id,
            "school_id": school.id,
            "teacher_id": teacher.id,
            "teacher_mobile": teacher.mobile,
            "outsider_mobile": other.mobile,
            "password": password,
        }
    return result


@pytest.fixture
def auth(client: TestClient, seed: dict[str, object]) -> dict[str, str]:
    """Authorization header for the seeded teacher."""
    response = client.post(
        "/v1/auth/login",
        json={"mobile": seed["teacher_mobile"], "password": seed["password"]},
        headers={"X-Client": "web"},
    )
    assert response.status_code == 200, response.text
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


def new_uuid() -> uuid.UUID:
    return uuid.uuid4()
