"""Tenant isolation: the property that must never regress.

Two layers are checked. First, that every table holding a ``tenant_id`` actually has
row-level security enabled *and* forced — a new table that forgets it fails here
rather than in production. Second, that the running API refuses cross-tenant reads
and writes even when the caller supplies a valid id from another tenant.
"""

from __future__ import annotations

import uuid
from collections.abc import Callable

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text

from khata.core.db import Database
from khata.core.roles import Role

pytestmark = pytest.mark.integration

# Tables with a tenant_id column that are deliberately not tenant-scoped.
RLS_EXEMPT: frozenset[str] = frozenset()


def _seed_tenant(database: Database, *, name: str, mobile: str) -> dict[str, uuid.UUID | str]:
    from khata.modules.identity.service import create_user
    from khata.modules.org.models import Organization, RoleAssignment, School

    password = "correct-horse-battery"
    tenant_id = uuid.uuid4()
    with database.session_scope(tenant_id) as session:
        session.add(Organization(id=tenant_id, name=name))
        session.flush()
        school = School(tenant_id=tenant_id, name_bn=name, name_en=name, board="dhaka")
        session.add(school)
        user = create_user(session, mobile=mobile, name=f"{name} staff", password=password)
        session.add(
            RoleAssignment(
                tenant_id=tenant_id,
                user_id=user.id,
                school_id=school.id,
                role=Role.EXAM_COORDINATOR.value,
            )
        )
        session.flush()
        return {
            "tenant_id": tenant_id,
            "school_id": school.id,
            "mobile": mobile,
            "password": password,
        }


def _login(sign_in: Callable[..., dict], mobile: str, password: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {sign_in(mobile, password)['access_token']}"}


def _create_exam(client: TestClient, auth: dict[str, str], school_id: uuid.UUID) -> str:
    response = client.post(
        "/v1/exams",
        headers=auth,
        json={
            "school_id": str(school_id),
            "name": "Isolated Exam",
            "subject_code": "BIO",
            "class_level": 9,
        },
    )
    assert response.status_code == 201, response.text
    return str(response.json()["id"])


def test_every_tenant_table_has_rls_enabled_and_forced(database: Database) -> None:
    """A table with a tenant_id and no forced RLS is a data leak waiting to happen."""
    with database.owner_engine.connect() as connection:
        rows = connection.execute(
            text(
                """
                SELECT c.relname, c.relrowsecurity, c.relforcerowsecurity
                FROM pg_class c
                JOIN pg_namespace n ON n.oid = c.relnamespace
                JOIN information_schema.columns col
                  ON col.table_name = c.relname AND col.table_schema = n.nspname
                WHERE n.nspname = 'public'
                  AND c.relkind = 'r'
                  AND col.column_name = 'tenant_id'
                  AND c.relname NOT LIKE 'procrastinate%'
                """
            )
        ).all()

    assert rows, "expected tenant-scoped tables to exist"
    unprotected = [
        name
        for name, enabled, forced in rows
        if name not in RLS_EXEMPT and not (enabled and forced)
    ]
    assert unprotected == [], f"tables without forced RLS: {unprotected}"


def test_organization_itself_is_tenant_scoped(database: Database) -> None:
    """``organization`` keys on ``id``, not ``tenant_id``, so it needs its own check."""
    with database.owner_engine.connect() as connection:
        enabled, forced = connection.execute(
            text(
                "SELECT relrowsecurity, relforcerowsecurity FROM pg_class"
                " WHERE relname = 'organization'"
            )
        ).one()
    assert enabled and forced


def test_a_tenant_cannot_read_another_tenants_exam(
    sign_in: Callable[..., dict], client: TestClient, database: Database
) -> None:
    first = _seed_tenant(database, name="First School", mobile="+8801710000001")
    second = _seed_tenant(database, name="Second School", mobile="+8801710000002")

    auth_first = _login(sign_in, str(first["mobile"]), str(first["password"]))
    auth_second = _login(sign_in, str(second["mobile"]), str(second["password"]))

    exam_id = _create_exam(client, auth_first, first["school_id"])  # type: ignore[arg-type]

    # The owner can read it.
    assert client.get(f"/v1/exams/{exam_id}", headers=auth_first).status_code == 200

    # The other tenant, holding a valid id and a valid token, cannot.
    response = client.get(f"/v1/exams/{exam_id}", headers=auth_second)
    assert response.status_code == 404, response.text
    assert response.json()["code"] == "NOT_FOUND"


def test_a_tenant_cannot_add_an_item_to_another_tenants_exam(
    sign_in: Callable[..., dict], client: TestClient, database: Database
) -> None:
    first = _seed_tenant(database, name="Third School", mobile="+8801710000003")
    second = _seed_tenant(database, name="Fourth School", mobile="+8801710000004")
    auth_first = _login(sign_in, str(first["mobile"]), str(first["password"]))
    auth_second = _login(sign_in, str(second["mobile"]), str(second["password"]))

    exam_id = _create_exam(client, auth_first, first["school_id"])  # type: ignore[arg-type]

    response = client.post(
        f"/v1/exams/{exam_id}/items",
        headers=auth_second,
        json={"item_no": 1, "max_marks": "5", "prompt_en": "Injected"},
    )
    assert response.status_code == 404, response.text

    # And the exam is untouched for its real owner.
    owner_view = client.get(f"/v1/exams/{exam_id}", headers=auth_first).json()
    assert owner_view["total_marks"] == "0.00"


def test_requests_without_a_token_are_rejected(client: TestClient) -> None:
    response = client.get(f"/v1/exams/{uuid.uuid4()}")
    assert response.status_code == 401
    assert response.json()["code"] == "UNAUTHENTICATED"


def test_a_signed_out_session_stops_working(
    sign_in: Callable[..., dict], client: TestClient, database: Database
) -> None:
    """Signing out must take effect immediately, not when the access token expires."""
    tenant = _seed_tenant(database, name="Fifth School", mobile="+8801710000005")
    auth = _login(sign_in, str(tenant["mobile"]), str(tenant["password"]))
    exam_id = _create_exam(client, auth, tenant["school_id"])  # type: ignore[arg-type]

    assert client.get(f"/v1/exams/{exam_id}", headers=auth).status_code == 200
    assert client.post("/v1/auth/logout", headers=auth).status_code == 204

    after = client.get(f"/v1/exams/{exam_id}", headers=auth)
    assert after.status_code == 401
    assert after.json()["code"] == "SESSION_REVOKED"


def test_a_capture_operator_cannot_decide_marks(
    sign_in: Callable[..., dict], client: TestClient, database: Database
) -> None:
    """Role separation: capture is not marking (08 §5.3)."""
    from khata.modules.identity.service import create_user
    from khata.modules.org.models import Organization, RoleAssignment, School

    tenant_id = uuid.uuid4()
    password = "correct-horse-battery"
    with database.session_scope(tenant_id) as session:
        session.add(Organization(id=tenant_id, name="Sixth School"))
        session.flush()
        school = School(tenant_id=tenant_id, name_bn="ছয়", name_en="Sixth School", board="dhaka")
        session.add(school)
        operator = create_user(
            session, mobile="+8801710000006", name="Capture Operator", password=password
        )
        session.add(
            RoleAssignment(
                tenant_id=tenant_id,
                user_id=operator.id,
                school_id=school.id,
                role=Role.CAPTURE_OPERATOR.value,
            )
        )
        session.flush()
        school_id = school.id

    auth = _login(sign_in, "+8801710000006", password)

    # A capture operator may not author an exam...
    created = client.post(
        "/v1/exams",
        headers=auth,
        json={
            "school_id": str(school_id),
            "name": "Not allowed",
            "subject_code": "BIO",
            "class_level": 9,
        },
    )
    assert created.status_code == 403
    assert created.json()["code"] == "PERMISSION_DENIED"

    # ...nor decide a mark.
    decided = client.post(
        f"/v1/item-results/{uuid.uuid4()}/review",
        headers=auth,
        json={"decisions": [], "accepted_ai": True},
    )
    assert decided.status_code == 403
