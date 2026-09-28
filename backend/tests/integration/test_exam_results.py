"""Exam results: the deterministic engine reached through the API (FR-RES-01/02/03).

The slice already went sign-in -> review -> lock marks. This takes it one step
further, to the number the school actually publishes.
"""

from __future__ import annotations

from decimal import Decimal
from typing import Any

import pytest
from fastapi.testclient import TestClient

pytestmark = pytest.mark.integration

RUBRIC_TEMPLATE: dict[str, Any] = {
    "item_id": "q",
    "version": 1,
    "model_answer": "Chlorophyll captures sunlight to make glucose.",
    "half_marks_allowed": False,
    "criteria": [
        {
            "id": "c1",
            "text_en": "chlorophyll",
            "marks": "2",
            "type": "concept",
            "evidence_expectation": "chlorophyll",
        },
        {
            "id": "c2",
            "text_en": "sunlight",
            "marks": "2",
            "type": "concept",
            "evidence_expectation": "sunlight",
        },
        {
            "id": "c3",
            "text_en": "glucose",
            "marks": "1",
            "type": "final_answer",
            "evidence_expectation": "glucose",
        },
    ],
}


class ExamBuilder:
    """Drives the public API to get an exam into a state worth asking results of."""

    def __init__(self, client: TestClient, auth: dict[str, str], school_id: str) -> None:
        self.client = client
        self.auth = auth
        self.exam_id = self._create(school_id)
        self.item_ids: list[str] = []

    def _create(self, school_id: str) -> str:
        response = self.client.post(
            "/v1/exams",
            headers=self.auth,
            json={
                "school_id": school_id,
                "name": "Biology First Term",
                "subject_code": "BIO",
                "class_level": 9,
            },
        )
        assert response.status_code == 201, response.text
        return str(response.json()["id"])

    def add_item(self, item_no: int, max_marks: str = "5") -> str:
        response = self.client.post(
            f"/v1/exams/{self.exam_id}/items",
            headers=self.auth,
            json={"item_no": item_no, "max_marks": max_marks, "prompt_en": "?", "prompt_bn": "?"},
        )
        assert response.status_code == 201, response.text
        item_id = str(response.json()["id"])
        rubric = {**RUBRIC_TEMPLATE, "item_id": f"q{item_no}"}
        assert (
            self.client.put(
                f"/v1/exams/{self.exam_id}/items/{item_id}/rubric",
                headers=self.auth,
                json={"rubric": rubric},
            ).status_code
            == 200
        )
        self.item_ids.append(item_id)
        return item_id

    def lock_rubric(self) -> None:
        assert (
            self.client.post(f"/v1/exams/{self.exam_id}/lock-rubric", headers=self.auth).status_code
            == 200
        )

    def candidate(self, roll: str, name: str) -> str:
        response = self.client.post(
            f"/v1/exams/{self.exam_id}/candidates",
            headers=self.auth,
            json={"roll": roll, "name": name},
        )
        assert response.status_code == 201, response.text
        return str(response.json()["id"])

    def answer(self, candidate_id: str, item_id: str, text: str = "answer") -> str:
        response = self.client.post(
            f"/v1/exams/{self.exam_id}/answers",
            headers=self.auth,
            json={"candidate_id": candidate_id, "item_id": item_id, "answer_text": text},
        )
        assert response.status_code == 201, response.text
        return str(response.json()["id"])

    def decide(self, result_id: str, marks: list[str]) -> None:
        """Award c1 (2), c2 (2) and c3 (1) by naming which criteria are met."""
        response = self.client.post(
            f"/v1/item-results/{result_id}/review",
            headers=self.auth,
            json={
                "decisions": [
                    {"criterion_id": cid, "decision": "met" if cid in marks else "not_met"}
                    for cid in ("c1", "c2", "c3")
                ],
                "accepted_ai": False,
            },
        )
        assert response.status_code == 200, response.text

    def results(self) -> dict:
        response = self.client.get(f"/v1/exams/{self.exam_id}/results", headers=self.auth)
        assert response.status_code == 200, response.text
        return dict(response.json())


@pytest.fixture
def exam(client: TestClient, auth: dict[str, str], seed: dict[str, object]) -> ExamBuilder:
    builder = ExamBuilder(client, auth, str(seed["school_id"]))
    builder.add_item(1, "5")
    builder.add_item(2, "5")
    builder.lock_rubric()
    return builder


def only(results: dict) -> dict:
    assert len(results["candidates"]) == 1
    return dict(results["candidates"][0])


class TestGrading:
    def test_a_full_score_is_an_a_plus(self, exam: ExamBuilder) -> None:
        candidate = exam.candidate("101", "Karim")
        for item_id in exam.item_ids:
            exam.decide(exam.answer(candidate, item_id), ["c1", "c2", "c3"])

        row = only(exam.results())
        assert Decimal(row["marks"]) == Decimal(10)
        assert Decimal(row["max_marks"]) == Decimal(10)
        assert row["letter"] == "A+"
        assert Decimal(row["grade_point"]) == Decimal("5.0")
        assert row["is_pass"] is True

    def test_a_middling_score_grades_in_the_middle_of_the_scale(self, exam: ExamBuilder) -> None:
        candidate = exam.candidate("102", "Mita")
        # c1 + c2 = 4 on one item, c1 + c3 = 3 on the other: 7 of 10 = 70% -> A
        exam.decide(exam.answer(candidate, exam.item_ids[0]), ["c1", "c2"])
        exam.decide(exam.answer(candidate, exam.item_ids[1]), ["c1", "c3"])

        row = only(exam.results())
        assert Decimal(row["marks"]) == Decimal(7)
        assert row["letter"] == "A"
        assert Decimal(row["grade_point"]) == Decimal("4.0")
        assert row["is_pass"] is True

    def test_below_the_pass_mark_fails(self, exam: ExamBuilder) -> None:
        candidate = exam.candidate("103", "Rana")
        exam.decide(exam.answer(candidate, exam.item_ids[0]), ["c3"])
        exam.decide(exam.answer(candidate, exam.item_ids[1]), [])

        row = only(exam.results())
        assert Decimal(row["marks"]) == Decimal(1)
        assert row["letter"] == "F"
        assert Decimal(row["grade_point"]) == Decimal(0)
        assert row["is_pass"] is False

    def test_every_candidate_appears_once_ordered_by_roll(self, exam: ExamBuilder) -> None:
        for roll, name in (("103", "C"), ("101", "A"), ("102", "B")):
            candidate = exam.candidate(roll, name)
            for item_id in exam.item_ids:
                exam.decide(exam.answer(candidate, item_id), ["c1", "c2", "c3"])

        rows = exam.results()["candidates"]
        assert [r["roll"] for r in rows] == ["101", "102", "103"]
        assert [r["name"] for r in rows] == ["A", "B", "C"]


class TestProvisionalResults:
    def test_results_are_provisional_until_marks_are_locked(self, exam: ExamBuilder) -> None:
        candidate = exam.candidate("101", "Karim")
        for item_id in exam.item_ids:
            exam.decide(exam.answer(candidate, item_id), ["c1", "c2", "c3"])

        assert exam.results()["provisional"] is True
        assert (
            exam.client.post(f"/v1/exams/{exam.exam_id}/lock-marks", headers=exam.auth).status_code
            == 200
        )
        assert exam.results()["provisional"] is False

    def test_an_undecided_item_is_counted_and_reported_not_hidden(self, exam: ExamBuilder) -> None:
        """A provisional total must say how much of it is still missing."""
        candidate = exam.candidate("101", "Karim")
        exam.decide(exam.answer(candidate, exam.item_ids[0]), ["c1", "c2", "c3"])
        exam.answer(candidate, exam.item_ids[1])  # captured, never decided

        row = only(exam.results())
        assert row["pending_items"] == 1
        assert Decimal(row["marks"]) == Decimal(5), "only decided marks count"
        assert exam.results()["provisional"] is True

    def test_a_candidate_with_no_script_is_still_listed(self, exam: ExamBuilder) -> None:
        exam.candidate("104", "Absent Ali")
        row = only(exam.results())
        assert Decimal(row["marks"]) == Decimal(0)
        assert row["pending_items"] == 2
        assert row["is_pass"] is False


class TestShape:
    def test_the_exam_header_carries_what_a_ledger_needs(self, exam: ExamBuilder) -> None:
        exam.candidate("101", "Karim")
        results = exam.results()
        assert results["exam_id"] == exam.exam_id
        assert results["subject_code"] == "BIO"
        assert Decimal(results["max_marks"]) == Decimal(10)
        assert results["state"] == "rubric_locked"

    def test_an_exam_with_no_items_has_no_results_to_give(
        self, client: TestClient, auth: dict[str, str], seed: dict[str, object]
    ) -> None:
        empty = ExamBuilder(client, auth, str(seed["school_id"]))
        response = client.get(f"/v1/exams/{empty.exam_id}/results", headers=auth)
        assert response.status_code == 409
        assert response.json()["code"] == "EXAM_HAS_NO_ITEMS"

    def test_another_tenant_cannot_read_these_results(
        self, client: TestClient, exam: ExamBuilder
    ) -> None:
        response = client.get(f"/v1/exams/{exam.exam_id}/results")
        assert response.status_code == 401
