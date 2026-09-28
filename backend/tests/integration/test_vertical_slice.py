"""End-to-end vertical slice.

Sign in -> create exam -> add question -> set rubric -> lock rubric -> capture answer
-> AI evaluation -> teacher review -> lock marks.

This is the test that proves the product path holds together. It uses the real
database, the real RLS policies, the real deterministic engines and the real (Fake)
marking provider — no mocks anywhere in the path.
"""

from __future__ import annotations

from decimal import Decimal

import pytest
from fastapi.testclient import TestClient

pytestmark = pytest.mark.integration

MODEL_ANSWER = (
    "Photosynthesis is the process where a plant uses chlorophyll to capture "
    "sunlight and convert carbon dioxide and water into glucose and oxygen."
)

RUBRIC = {
    "item_id": "q1",
    "version": 1,
    "model_answer": MODEL_ANSWER,
    "half_marks_allowed": False,
    "criteria": [
        {
            "id": "c1",
            "text_en": "Identifies chlorophyll as the pigment",
            "marks": "2",
            "type": "concept",
            "evidence_expectation": "chlorophyll",
        },
        {
            "id": "c2",
            "text_en": "Identifies sunlight as the energy source",
            "marks": "2",
            "type": "concept",
            "evidence_expectation": "sunlight",
        },
        {
            "id": "c3",
            "text_en": "Names glucose as a product",
            "marks": "1",
            "type": "final_answer",
            "evidence_expectation": "glucose",
        },
    ],
}

GOOD_ANSWER = (
    "Plants use chlorophyll in their leaves to absorb sunlight, and they make "
    "glucose from carbon dioxide and water."
)


def _create_exam(client: TestClient, auth: dict[str, str], seed: dict[str, object]) -> str:
    response = client.post(
        "/v1/exams",
        headers=auth,
        json={
            "school_id": str(seed["school_id"]),
            "name": "Biology First Term",
            "subject_code": "BIO",
            "class_level": 9,
        },
    )
    assert response.status_code == 201, response.text
    body = response.json()
    assert body["state"] == "draft"
    return str(body["id"])


def _add_item(client: TestClient, auth: dict[str, str], exam_id: str) -> str:
    response = client.post(
        f"/v1/exams/{exam_id}/items",
        headers=auth,
        json={
            "item_no": 1,
            "max_marks": "5",
            "prompt_en": "What is photosynthesis?",
            "prompt_bn": "সালোকসংশ্লেষণ কাকে বলে?",
        },
    )
    assert response.status_code == 201, response.text
    return str(response.json()["id"])


def _put_rubric(client: TestClient, auth: dict[str, str], exam_id: str, item_id: str) -> dict:
    response = client.put(
        f"/v1/exams/{exam_id}/items/{item_id}/rubric",
        headers=auth,
        json={"rubric": RUBRIC},
    )
    assert response.status_code == 200, response.text
    return response.json()


def test_full_marking_path(
    client: TestClient, auth: dict[str, str], seed: dict[str, object]
) -> None:
    exam_id = _create_exam(client, auth, seed)
    item_id = _add_item(client, auth, exam_id)

    rubric = _put_rubric(client, auth, exam_id, item_id)
    assert rubric["version"] == 1
    assert rubric["ai_eligible"] is True, "a rubric with a model answer should be AI-eligible"

    locked = client.post(f"/v1/exams/{exam_id}/lock-rubric", headers=auth)
    assert locked.status_code == 200, locked.text
    assert locked.json()["state"] == "rubric_locked"
    assert Decimal(locked.json()["total_marks"]) == Decimal(5)

    candidate = client.post(
        f"/v1/exams/{exam_id}/candidates",
        headers=auth,
        json={"roll": "101", "name": "Karim Student"},
    )
    assert candidate.status_code == 201, candidate.text
    candidate_id = candidate.json()["id"]

    submitted = client.post(
        f"/v1/exams/{exam_id}/answers",
        headers=auth,
        json={"candidate_id": candidate_id, "item_id": item_id, "answer_text": GOOD_ANSWER},
    )
    assert submitted.status_code == 201, submitted.text
    assert submitted.json()["state"] == "pending"
    script_id = submitted.json()["script_id"]

    evaluated = client.post(f"/v1/scripts/{script_id}/evaluate", headers=auth)
    assert evaluated.status_code == 200, evaluated.text
    result = evaluated.json()[0]
    assert result["state"] == "suggested"
    assert result["total"] is None, "the AI must not write a final mark"

    queue = client.get(f"/v1/scripts/{script_id}/review", headers=auth)
    assert queue.status_code == 200, queue.text
    card = queue.json()["items"][0]
    assert card["student_answer"] == GOOD_ANSWER
    assert card["model_answer"] == MODEL_ANSWER
    assert card["ai_model"] == "fake-marker"
    assert card["ai_rationale"]
    assert card["ai_evidence"], "the teacher must be able to see why the AI decided this"
    assert card["suggested_score"] is not None
    assert card["teacher_score"] is None
    assert [d["criterion_id"] for d in card["ai_decisions"]] == ["c1", "c2", "c3"]

    # The teacher accepts the AI on the two it matched and overrides the third.
    decided = client.post(
        f"/v1/item-results/{card['result_id']}/review",
        headers=auth,
        json={
            "decisions": [
                {"criterion_id": "c1", "decision": "met"},
                {"criterion_id": "c2", "decision": "met"},
                {"criterion_id": "c3", "decision": "met"},
            ],
            "accepted_ai": False,
        },
    )
    assert decided.status_code == 200, decided.text
    assert decided.json()["state"] == "edited"
    assert Decimal(decided.json()["total"]) == Decimal(5)

    marks_locked = client.post(f"/v1/exams/{exam_id}/lock-marks", headers=auth)
    assert marks_locked.status_code == 200, marks_locked.text
    assert marks_locked.json()["state"] == "marks_locked"

    final = client.get(f"/v1/scripts/{script_id}/review", headers=auth)
    assert final.json()["items"][0]["state"] == "locked"
    assert Decimal(final.json()["script_total"]) == Decimal(5)


def test_blank_answer_is_flagged_for_the_teacher(
    client: TestClient, auth: dict[str, str], seed: dict[str, object]
) -> None:
    """A blank answer must reach a human, not be silently scored zero."""
    exam_id = _create_exam(client, auth, seed)
    item_id = _add_item(client, auth, exam_id)
    _put_rubric(client, auth, exam_id, item_id)
    client.post(f"/v1/exams/{exam_id}/lock-rubric", headers=auth)

    candidate = client.post(
        f"/v1/exams/{exam_id}/candidates",
        headers=auth,
        json={"roll": "102", "name": "Blank Script"},
    ).json()
    submitted = client.post(
        f"/v1/exams/{exam_id}/answers",
        headers=auth,
        json={"candidate_id": candidate["id"], "item_id": item_id, "answer_text": "   "},
    ).json()

    client.post(f"/v1/scripts/{submitted['script_id']}/evaluate", headers=auth)
    card = client.get(f"/v1/scripts/{submitted['script_id']}/review", headers=auth).json()["items"][
        0
    ]

    assert card["ai_low_confidence"] is True
    assert card["total"] is None
    assert all(d["decision"] == "cannot_determine" for d in card["ai_decisions"])
    assert card["suggested_score"]["needs_teacher"] is True


def test_rubric_that_does_not_sum_is_rejected(
    client: TestClient, auth: dict[str, str], seed: dict[str, object]
) -> None:
    exam_id = _create_exam(client, auth, seed)
    item_id = _add_item(client, auth, exam_id)

    broken = {**RUBRIC, "criteria": [{**RUBRIC["criteria"][0], "marks": "3"}]}
    response = client.put(
        f"/v1/exams/{exam_id}/items/{item_id}/rubric", headers=auth, json={"rubric": broken}
    )
    assert response.status_code == 422, response.text
    body = response.json()
    assert body["code"] == "VALIDATION_FAILED"
    assert any(issue["code"] == "criteria_sum_mismatch" for issue in body["errors"])
    assert body["message_bn"], "every error carries a Bangla message"


def test_marks_cannot_be_locked_while_an_answer_is_undecided(
    client: TestClient, auth: dict[str, str], seed: dict[str, object]
) -> None:
    exam_id = _create_exam(client, auth, seed)
    item_id = _add_item(client, auth, exam_id)
    _put_rubric(client, auth, exam_id, item_id)
    client.post(f"/v1/exams/{exam_id}/lock-rubric", headers=auth)

    candidate = client.post(
        f"/v1/exams/{exam_id}/candidates",
        headers=auth,
        json={"roll": "103", "name": "Undecided"},
    ).json()
    submitted = client.post(
        f"/v1/exams/{exam_id}/answers",
        headers=auth,
        json={"candidate_id": candidate["id"], "item_id": item_id, "answer_text": GOOD_ANSWER},
    ).json()
    client.post(f"/v1/scripts/{submitted['script_id']}/evaluate", headers=auth)

    response = client.post(f"/v1/exams/{exam_id}/lock-marks", headers=auth)
    assert response.status_code == 409, response.text
    assert response.json()["undecided_items"] == 1


def test_answers_are_refused_before_the_rubric_is_locked(
    client: TestClient, auth: dict[str, str], seed: dict[str, object]
) -> None:
    exam_id = _create_exam(client, auth, seed)
    item_id = _add_item(client, auth, exam_id)
    _put_rubric(client, auth, exam_id, item_id)

    candidate = client.post(
        f"/v1/exams/{exam_id}/candidates",
        headers=auth,
        json={"roll": "104", "name": "Too Early"},
    ).json()
    response = client.post(
        f"/v1/exams/{exam_id}/answers",
        headers=auth,
        json={"candidate_id": candidate["id"], "item_id": item_id, "answer_text": GOOD_ANSWER},
    )
    assert response.status_code == 409, response.text
    assert response.json()["from_state"] == "draft"
