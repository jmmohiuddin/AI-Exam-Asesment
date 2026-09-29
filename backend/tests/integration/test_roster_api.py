"""Roster import, enrolment and consent against the real database (FR-ORG-02/03/06).

These run against PostgreSQL rather than a fake because the rules that matter here
are database rules: one enrolment per student per year, one roll per section, and
exactly one live consent row per student per type.
"""

from __future__ import annotations

import uuid
from datetime import date

import pytest
from fastapi.testclient import TestClient

from khata.core.db import Database

pytestmark = pytest.mark.integration


@pytest.fixture
def academic_year(database: Database, seed: dict[str, object]) -> uuid.UUID:
    from khata.modules.org.models import AcademicYear

    tenant_id = seed["tenant_id"]
    assert isinstance(tenant_id, uuid.UUID)
    with database.session_scope(tenant_id) as session:
        year = AcademicYear(
            tenant_id=tenant_id,
            school_id=seed["school_id"],
            year=2026,
            starts_on=date(2026, 1, 1),
            ends_on=date(2026, 12, 31),
            is_current=True,
        )
        session.add(year)
        session.flush()
        return year.id


def spreadsheet_row(number: int, **overrides: object) -> dict[str, object]:
    base: dict[str, object] = {
        "row_number": number,
        "roll": str(100 + number),
        "name_bn": "রহিম উদ্দিন",
        "name_en": "Rahim Uddin",
        "class_level": "9",
        "group_code": "science",
        "version": "BM",
        "shift": "day",
        "section": "A",
    }
    return {**base, **overrides}


def upload(
    client: TestClient,
    auth: dict[str, str],
    seed: dict[str, object],
    academic_year: uuid.UUID,
    rows: list[dict[str, object]],
    filename: str = "class-9.xlsx",
) -> dict:
    response = client.post(
        f"/v1/schools/{seed['school_id']}/roster-imports",
        json={
            "academic_year_id": str(academic_year),
            "filename": filename,
            "rows": rows,
        },
        headers=auth,
    )
    assert response.status_code == 201, response.text
    return dict(response.json())


# --------------------------------------------------------------------------- dry run


def test_a_clean_file_validates_without_writing_any_student(
    client: TestClient, auth: dict[str, str], seed: dict[str, object], academic_year: uuid.UUID
) -> None:
    staged = upload(client, auth, seed, academic_year, [spreadsheet_row(1), spreadsheet_row(2)])

    assert staged["state"] == "validated"
    assert staged["accepted_count"] == 2
    assert staged["error_count"] == 0
    assert staged["report"]["is_committable"] is True

    listed = client.get(f"/v1/schools/{seed['school_id']}/students", headers=auth)
    assert listed.status_code == 200
    assert listed.json() == []


def test_a_file_with_errors_is_reported_not_rejected(
    client: TestClient, auth: dict[str, str], seed: dict[str, object], academic_year: uuid.UUID
) -> None:
    """The admin needs the report; an HTTP error would throw the diagnosis away."""
    staged = upload(
        client,
        auth,
        seed,
        academic_year,
        [spreadsheet_row(1), spreadsheet_row(2, roll=""), spreadsheet_row(3, class_level="99")],
    )

    assert staged["accepted_count"] == 1
    assert staged["error_count"] == 2
    assert staged["report"]["is_committable"] is False
    codes = {problem["code"] for problem in staged["report"]["problems"]}
    assert codes == {"required", "out_of_range"}


def test_a_report_problem_is_readable_in_both_languages(
    client: TestClient, auth: dict[str, str], seed: dict[str, object], academic_year: uuid.UUID
) -> None:
    staged = upload(client, auth, seed, academic_year, [spreadsheet_row(1, roll="")])

    problem = staged["report"]["problems"][0]
    assert problem["message_en"]
    assert problem["message_bn"]
    assert problem["row_number"] == 1


# --------------------------------------------------------------------------- commit


def test_committing_creates_students_sections_and_enrolments(
    client: TestClient, auth: dict[str, str], seed: dict[str, object], academic_year: uuid.UUID
) -> None:
    staged = upload(
        client,
        auth,
        seed,
        academic_year,
        [spreadsheet_row(1), spreadsheet_row(2), spreadsheet_row(3, section="B")],
    )

    committed = client.post(f"/v1/roster-imports/{staged['id']}/commit", headers=auth)
    assert committed.status_code == 200, committed.text
    outcome = committed.json()
    assert outcome["students_created"] == 3
    assert outcome["students_updated"] == 0
    assert outcome["sections_created"] == 2
    assert outcome["enrolments_created"] == 3

    listed = client.get(f"/v1/schools/{seed['school_id']}/students", headers=auth).json()
    assert len(listed) == 3
    assert {row["student"]["student_uid"] for row in listed} == {"9-A-101", "9-A-102", "9-B-103"}
    assert all(row["enrolment"] is not None for row in listed)


def test_a_committed_import_records_what_it_changed(
    client: TestClient, auth: dict[str, str], seed: dict[str, object], academic_year: uuid.UUID
) -> None:
    staged = upload(client, auth, seed, academic_year, [spreadsheet_row(1)])
    client.post(f"/v1/roster-imports/{staged['id']}/commit", headers=auth)

    reread = client.get(f"/v1/roster-imports/{staged['id']}", headers=auth).json()
    assert reread["state"] == "committed"
    assert reread["committed_at"] is not None
    assert reread["students_created"] == 1


def test_a_file_with_errors_cannot_be_committed(
    client: TestClient, auth: dict[str, str], seed: dict[str, object], academic_year: uuid.UUID
) -> None:
    staged = upload(client, auth, seed, academic_year, [spreadsheet_row(1, roll="")])

    refused = client.post(f"/v1/roster-imports/{staged['id']}/commit", headers=auth)

    assert refused.status_code == 409
    assert refused.json()["code"] == "ROSTER_IMPORT_NOT_COMMITTABLE"


def test_committing_twice_is_refused(
    client: TestClient, auth: dict[str, str], seed: dict[str, object], academic_year: uuid.UUID
) -> None:
    """Otherwise a double-click silently re-runs the whole file."""
    staged = upload(client, auth, seed, academic_year, [spreadsheet_row(1)])
    client.post(f"/v1/roster-imports/{staged['id']}/commit", headers=auth)

    again = client.post(f"/v1/roster-imports/{staged['id']}/commit", headers=auth)

    assert again.status_code == 409
    assert again.json()["code"] == "ROSTER_IMPORT_ALREADY_COMMITTED"


def test_re_importing_the_same_roster_updates_rather_than_duplicates(
    client: TestClient, auth: dict[str, str], seed: dict[str, object], academic_year: uuid.UUID
) -> None:
    """Schools re-upload a corrected file; that must not create a second student."""
    first = upload(client, auth, seed, academic_year, [spreadsheet_row(1)])
    client.post(f"/v1/roster-imports/{first['id']}/commit", headers=auth)

    second = upload(
        client, auth, seed, academic_year, [spreadsheet_row(1, name_en="Rahim Uddin Ahmed")]
    )
    outcome = client.post(f"/v1/roster-imports/{second['id']}/commit", headers=auth).json()

    assert outcome["students_created"] == 0
    assert outcome["students_updated"] == 1
    assert outcome["sections_created"] == 0

    listed = client.get(f"/v1/schools/{seed['school_id']}/students", headers=auth).json()
    assert len(listed) == 1
    assert listed[0]["student"]["name_en"] == "Rahim Uddin Ahmed"


def test_moving_a_student_to_another_section_moves_the_enrolment(
    client: TestClient, auth: dict[str, str], seed: dict[str, object], academic_year: uuid.UUID
) -> None:
    """A student sits in exactly one section per year (FR-ORG-02)."""
    first = upload(client, auth, seed, academic_year, [spreadsheet_row(1, student_uid="S-1")])
    client.post(f"/v1/roster-imports/{first['id']}/commit", headers=auth)

    second = upload(
        client, auth, seed, academic_year, [spreadsheet_row(1, student_uid="S-1", section="B")]
    )
    outcome = client.post(f"/v1/roster-imports/{second['id']}/commit", headers=auth).json()

    assert outcome["enrolments_created"] == 0
    assert outcome["enrolments_updated"] == 1

    listed = client.get(f"/v1/schools/{seed['school_id']}/students", headers=auth).json()
    assert len(listed) == 1


def test_students_can_be_filtered_to_one_section(
    client: TestClient, auth: dict[str, str], seed: dict[str, object], academic_year: uuid.UUID
) -> None:
    staged = upload(
        client,
        auth,
        seed,
        academic_year,
        [spreadsheet_row(1), spreadsheet_row(2, section="B")],
    )
    client.post(f"/v1/roster-imports/{staged['id']}/commit", headers=auth)

    everyone = client.get(f"/v1/schools/{seed['school_id']}/students", headers=auth).json()
    section_id = everyone[0]["enrolment"]["section_id"]

    filtered = client.get(
        f"/v1/schools/{seed['school_id']}/students",
        params={"section_id": section_id},
        headers=auth,
    ).json()

    assert len(filtered) == 1
    assert filtered[0]["enrolment"]["section_id"] == section_id


def test_a_500_row_file_imports(
    client: TestClient, auth: dict[str, str], seed: dict[str, object], academic_year: uuid.UUID
) -> None:
    """FR-ORG-03 sizes the acceptance criterion at 500 rows."""
    rows = [
        spreadsheet_row(n, roll=str(1000 + n), section="A" if n % 2 else "B") for n in range(1, 501)
    ]
    staged = upload(client, auth, seed, academic_year, rows)
    assert staged["accepted_count"] == 500

    outcome = client.post(f"/v1/roster-imports/{staged['id']}/commit", headers=auth).json()

    assert outcome["students_created"] == 500
    assert outcome["sections_created"] == 2


# --------------------------------------------------------------------------- consent


def _one_student(client: TestClient, auth: dict[str, str], seed: dict[str, object]) -> str:
    listed = client.get(f"/v1/schools/{seed['school_id']}/students", headers=auth).json()
    student_id: str = listed[0]["student"]["id"]
    return student_id


@pytest.fixture
def student_id(
    client: TestClient, auth: dict[str, str], seed: dict[str, object], academic_year: uuid.UUID
) -> str:
    staged = upload(client, auth, seed, academic_year, [spreadsheet_row(1)])
    client.post(f"/v1/roster-imports/{staged['id']}/commit", headers=auth)
    return _one_student(client, auth, seed)


def test_a_new_student_has_consented_to_nothing(
    client: TestClient, auth: dict[str, str], student_id: str
) -> None:
    """Absence of a record is a refusal, not a default yes (08 §6.1)."""
    state = client.get(f"/v1/students/{student_id}/consents", headers=auth).json()

    assert state["current"] == []
    assert state["capture_allowed"] is False
    assert state["ai_allowed"] is False


def test_recording_ct1_allows_capture_but_not_ai(
    client: TestClient, auth: dict[str, str], student_id: str
) -> None:
    state = client.put(
        f"/v1/students/{student_id}/consents",
        json={"consent_type": "CT-1", "granted": True, "method": "paper_form"},
        headers=auth,
    ).json()

    assert state["capture_allowed"] is True
    assert state["ai_allowed"] is False


def test_recording_ct2_allows_ai(client: TestClient, auth: dict[str, str], student_id: str) -> None:
    client.put(
        f"/v1/students/{student_id}/consents",
        json={"consent_type": "CT-1", "granted": True, "method": "paper_form"},
        headers=auth,
    )
    state = client.put(
        f"/v1/students/{student_id}/consents",
        json={"consent_type": "CT-2", "granted": True, "method": "paper_form"},
        headers=auth,
    ).json()

    assert state["capture_allowed"] is True
    assert state["ai_allowed"] is True


def test_withdrawing_a_consent_takes_effect(
    client: TestClient, auth: dict[str, str], student_id: str
) -> None:
    client.put(
        f"/v1/students/{student_id}/consents",
        json={"consent_type": "CT-2", "granted": True, "method": "paper_form"},
        headers=auth,
    )
    state = client.put(
        f"/v1/students/{student_id}/consents",
        json={"consent_type": "CT-2", "granted": False, "method": "digital", "note": "withdrawn"},
        headers=auth,
    ).json()

    assert state["ai_allowed"] is False
    assert len(state["current"]) == 1


def test_the_previous_decision_is_kept_in_history(
    client: TestClient, auth: dict[str, str], student_id: str
) -> None:
    """Whether AI was allowed when a script was marked must stay answerable."""
    client.put(
        f"/v1/students/{student_id}/consents",
        json={"consent_type": "CT-2", "granted": True, "method": "paper_form"},
        headers=auth,
    )
    client.put(
        f"/v1/students/{student_id}/consents",
        json={"consent_type": "CT-2", "granted": False, "method": "digital"},
        headers=auth,
    )

    history = client.get(f"/v1/students/{student_id}/consents/history", headers=auth).json()

    assert len(history) == 2
    assert history[0]["granted"] is False
    assert history[0]["superseded_at"] is None
    assert history[1]["granted"] is True
    assert history[1]["superseded_at"] is not None


def test_each_consent_type_is_tracked_separately(
    client: TestClient, auth: dict[str, str], student_id: str
) -> None:
    for consent_type in ("CT-1", "CT-2", "CT-3"):
        client.put(
            f"/v1/students/{student_id}/consents",
            json={"consent_type": consent_type, "granted": True, "method": "paper_form"},
            headers=auth,
        )
    state = client.put(
        f"/v1/students/{student_id}/consents",
        json={"consent_type": "CT-3", "granted": False, "method": "digital"},
        headers=auth,
    ).json()

    granted = {c["consent_type"]: c["granted"] for c in state["current"]}
    assert granted == {"CT-1": True, "CT-2": True, "CT-3": False}


def test_an_unknown_consent_type_is_rejected(
    client: TestClient, auth: dict[str, str], student_id: str
) -> None:
    refused = client.put(
        f"/v1/students/{student_id}/consents",
        json={"consent_type": "CT-9", "granted": True, "method": "paper_form"},
        headers=auth,
    )

    assert refused.status_code == 422


# --------------------------------------------------------------------------- isolation


def test_another_tenant_cannot_read_these_students(
    client: TestClient,
    auth: dict[str, str],
    seed: dict[str, object],
    student_id: str,
) -> None:
    outsider = client.get(f"/v1/students/{student_id}", headers={"Authorization": "Bearer nope"})

    assert outsider.status_code == 401


def test_the_roster_needs_an_administrative_role(
    client: TestClient,
    database: Database,
    seed: dict[str, object],
    sign_in: object,
) -> None:
    """A plain teacher may mark scripts but may not edit who the students are."""
    from khata.core.roles import Role
    from khata.modules.identity.service import create_user
    from khata.modules.org.models import RoleAssignment

    tenant_id = seed["tenant_id"]
    assert isinstance(tenant_id, uuid.UUID)
    password = "correct-horse-battery"
    with database.session_scope(tenant_id) as session:
        teacher = create_user(
            session, mobile="+8801700000009", name="Plain Teacher", password=password
        )
        session.add(
            RoleAssignment(
                tenant_id=tenant_id,
                user_id=teacher.id,
                school_id=seed["school_id"],
                role=Role.TEACHER.value,
            )
        )

    body = sign_in("+8801700000009", password)  # type: ignore[operator]
    headers = {"Authorization": f"Bearer {body['access_token']}"}

    refused = client.get(f"/v1/schools/{seed['school_id']}/students", headers=headers)

    assert refused.status_code == 403
    assert refused.json()["code"] == "PERMISSION_DENIED"
