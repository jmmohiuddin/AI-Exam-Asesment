"""Guardian consent decides whether a script reaches an AI provider (FR-ORG-06).

08 §6.1: without CT-2 the items are processed at L0 — no AI call, the teacher marks
from the answer itself. This is the mechanism behind the product's claim that it
works with AI switched off, so it is tested against the real marking path rather
than asserted in a unit test of the predicate.
"""

from __future__ import annotations

import uuid
from datetime import date

import pytest
from fastapi.testclient import TestClient

from khata.core.db import Database

pytestmark = pytest.mark.integration

RUBRIC = {
    "item_id": "q1",
    "version": 1,
    "model_answer": "Chlorophyll captures sunlight to make glucose.",
    "half_marks_allowed": False,
    "criteria": [
        {
            "id": "c1",
            "text_en": "Identifies chlorophyll",
            "marks": "2",
            "type": "concept",
            "evidence_expectation": "chlorophyll",
        },
    ],
}
ANSWER = "Plants use chlorophyll to absorb sunlight and make glucose."


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


@pytest.fixture
def student_id(
    client: TestClient, auth: dict[str, str], seed: dict[str, object], academic_year: uuid.UUID
) -> str:
    staged = client.post(
        f"/v1/schools/{seed['school_id']}/roster-imports",
        headers=auth,
        json={
            "academic_year_id": str(academic_year),
            "filename": "class-9.xlsx",
            "rows": [
                {
                    "row_number": 1,
                    "roll": "101",
                    "name_bn": "করিম উদ্দিন",
                    "name_en": "Karim Uddin",
                    "class_level": "9",
                    "group_code": "science",
                    "version": "BM",
                    "shift": "day",
                    "section": "A",
                }
            ],
        },
    ).json()
    client.post(f"/v1/roster-imports/{staged['id']}/commit", headers=auth)
    listed = client.get(f"/v1/schools/{seed['school_id']}/students", headers=auth).json()
    return str(listed[0]["student"]["id"])


def _exam_ready_for_capture(
    client: TestClient, auth: dict[str, str], seed: dict[str, object]
) -> tuple[str, str]:
    exam_id = str(
        client.post(
            "/v1/exams",
            headers=auth,
            json={
                "school_id": str(seed["school_id"]),
                "name": "Biology First Term",
                "subject_code": "BIO",
                "class_level": 9,
            },
        ).json()["id"]
    )
    item_id = str(
        client.post(
            f"/v1/exams/{exam_id}/items",
            headers=auth,
            json={"item_no": 1, "max_marks": "2", "prompt_en": "What is photosynthesis?"},
        ).json()["id"]
    )
    rubric = client.put(
        f"/v1/exams/{exam_id}/items/{item_id}/rubric", headers=auth, json={"rubric": RUBRIC}
    ).json()
    assert rubric["ai_eligible"] is True
    client.post(f"/v1/exams/{exam_id}/lock-rubric", headers=auth)
    return exam_id, item_id


def _mark(
    client: TestClient,
    auth: dict[str, str],
    exam_id: str,
    item_id: str,
    student_id: str | None,
) -> dict:
    candidate = client.post(
        f"/v1/exams/{exam_id}/candidates",
        headers=auth,
        json={"roll": "101", "name": "Karim Uddin", "student_id": student_id},
    )
    assert candidate.status_code == 201, candidate.text
    submitted = client.post(
        f"/v1/exams/{exam_id}/answers",
        headers=auth,
        json={
            "candidate_id": candidate.json()["id"],
            "item_id": item_id,
            "answer_text": ANSWER,
        },
    ).json()
    evaluated = client.post(f"/v1/scripts/{submitted['script_id']}/evaluate", headers=auth)
    assert evaluated.status_code == 200, evaluated.text
    result: dict = evaluated.json()[0]
    return result


def _grant(client: TestClient, auth: dict[str, str], student_id: str, granted: bool) -> None:
    response = client.put(
        f"/v1/students/{student_id}/consents",
        headers=auth,
        json={"consent_type": "CT-2", "granted": granted, "method": "paper_form"},
    )
    assert response.status_code == 200, response.text


def test_a_linked_student_without_ct2_is_marked_without_ai(
    client: TestClient, auth: dict[str, str], seed: dict[str, object], student_id: str
) -> None:
    exam_id, item_id = _exam_ready_for_capture(client, auth, seed)

    result = _mark(client, auth, exam_id, item_id, student_id)

    assert result["state"] == "manual_ready"
    assert result["ai_confidence"] is None


def test_the_review_card_for_such_a_student_carries_no_suggestion(
    client: TestClient, auth: dict[str, str], seed: dict[str, object], student_id: str
) -> None:
    """The teacher must not see a suggestion that was never allowed to be produced."""
    exam_id, item_id = _exam_ready_for_capture(client, auth, seed)
    result = _mark(client, auth, exam_id, item_id, student_id)

    card = client.get(f"/v1/scripts/{result['script_id']}/review", headers=auth).json()["items"][0]

    assert card["ai_model"] is None
    assert card["suggested_score"] is None
    assert card["ai_decisions"] == []
    assert card["student_answer"] == ANSWER


def test_granting_ct2_lets_the_ai_run(
    client: TestClient, auth: dict[str, str], seed: dict[str, object], student_id: str
) -> None:
    _grant(client, auth, student_id, True)
    exam_id, item_id = _exam_ready_for_capture(client, auth, seed)

    result = _mark(client, auth, exam_id, item_id, student_id)

    assert result["state"] == "suggested"
    assert result["total"] is None, "the AI still must not write a final mark"


def test_withdrawing_ct2_stops_the_ai_on_the_next_script(
    client: TestClient, auth: dict[str, str], seed: dict[str, object], student_id: str
) -> None:
    _grant(client, auth, student_id, True)
    _grant(client, auth, student_id, False)
    exam_id, item_id = _exam_ready_for_capture(client, auth, seed)

    result = _mark(client, auth, exam_id, item_id, student_id)

    assert result["state"] == "manual_ready"


def test_a_teacher_can_still_finish_a_script_marked_without_ai(
    client: TestClient, auth: dict[str, str], seed: dict[str, object], student_id: str
) -> None:
    """The point of L0 is that the exam completes, not that it stalls (FR-REV-10)."""
    exam_id, item_id = _exam_ready_for_capture(client, auth, seed)
    result = _mark(client, auth, exam_id, item_id, student_id)

    decided = client.post(
        f"/v1/item-results/{result['id']}/review",
        headers=auth,
        json={"decisions": [{"criterion_id": "c1", "decision": "met"}], "accepted_ai": False},
    )
    assert decided.status_code == 200, decided.text
    assert decided.json()["state"] == "edited"

    locked = client.post(f"/v1/exams/{exam_id}/lock-marks", headers=auth)
    assert locked.status_code == 200, locked.text
    assert locked.json()["state"] == "marks_locked"


def test_an_unlinked_candidate_keeps_the_pre_roster_behaviour(
    client: TestClient, auth: dict[str, str], seed: dict[str, object]
) -> None:
    """Consent attaches to students; a candidate with no student has no record to read."""
    exam_id, item_id = _exam_ready_for_capture(client, auth, seed)

    result = _mark(client, auth, exam_id, item_id, None)

    assert result["state"] == "suggested"
