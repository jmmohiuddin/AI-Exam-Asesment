"""The result-engine fixture corpus (TR-RES-01: >=200 hand-checkable cases at 100%).

Every expectation in ``fixtures/result_cases.json`` was derived by
``fixtures/generate.py``, an oracle that re-implements FR-RES-01/02/03 from the
specification without importing the engine. A disagreement here means the engine
and the specification have drifted apart.
"""

from __future__ import annotations

import json
from decimal import Decimal
from pathlib import Path
from typing import Any

import pytest

from khata.engines.results.compute import (
    SubjectMarks,
    compute_overall_result,
    compute_subject_result,
)
from khata.engines.results.grading import SubjectGrade, gpa
from khata.engines.results.structure import PaperStructure

CORPUS = json.loads((Path(__file__).parent / "fixtures" / "result_cases.json").read_text())
PAPERS = {name: PaperStructure.model_validate(spec) for name, spec in CORPUS["papers"].items()}
SUBJECT_CASES: list[dict[str, Any]] = CORPUS["subject_cases"]
GPA_CASES: list[dict[str, Any]] = CORPUS["gpa_cases"]


def test_the_corpus_meets_the_required_size() -> None:
    assert len(SUBJECT_CASES) + len(GPA_CASES) >= 200


def test_case_ids_are_unique() -> None:
    ids = [case["id"] for case in SUBJECT_CASES] + [case["id"] for case in GPA_CASES]
    assert len(ids) == len(set(ids))


@pytest.mark.parametrize("case", SUBJECT_CASES, ids=lambda c: c["id"])
def test_subject_result_matches_the_oracle(case: dict[str, Any]) -> None:
    structure = PAPERS[case["paper"]]
    marks = SubjectMarks.model_validate(
        {"subject_id": case["subject_id"], "components": case["components"]}
    )
    result = compute_subject_result(structure, marks)
    expect = case["expect"]

    assert result.marks == Decimal(expect["marks"]), case["why"]
    assert result.max_marks == Decimal(expect["max_marks"]), case["why"]
    assert result.letter == expect["letter"], case["why"]
    assert result.grade_point == Decimal(expect["grade_point"]), case["why"]
    assert result.is_pass == expect["is_pass"], case["why"]
    assert result.absent == expect["absent"], case["why"]
    assert sorted(result.failed_components) == expect["failed_components"], case["why"]
    assert sorted(result.absent_components) == expect["absent_components"], case["why"]
    if "counted_cq" in expect:
        counted = next(c for c in result.components if c.code == "cq")
        assert list(counted.counted_question_ids) == expect["counted_cq"], case["why"]


@pytest.mark.parametrize("case", GPA_CASES, ids=lambda c: c["id"])
def test_gpa_matches_the_oracle(case: dict[str, Any]) -> None:
    subjects = [
        SubjectGrade(
            subject_id=s["subject_id"],
            letter="X",
            grade_point=Decimal(s["grade_point"]),
            is_pass=s["is_pass"],
            is_fourth_subject=s.get("is_fourth_subject", False),
        )
        for s in case["subjects"]
    ]
    result = gpa(subjects)
    assert result.gpa == Decimal(case["expect"]["gpa"]), case["why"]
    assert result.is_pass == case["expect"]["is_pass"], case["why"]
    assert sorted(result.failed_subjects) == case["expect"]["failed_subjects"], case["why"]


def test_overall_result_totals_the_subject_results() -> None:
    """A whole student: three subjects from the corpus, rolled up."""
    picks = ["grade-085", "grade-075", "grade-065"]
    results = []
    for index, case_id in enumerate(picks):
        case = next(c for c in SUBJECT_CASES if c["id"] == case_id)
        structure = PAPERS[case["paper"]].model_copy(update={"subject_id": f"s{index}"})
        marks = SubjectMarks.model_validate(
            {"subject_id": f"s{index}", "components": case["components"]}
        )
        results.append(compute_subject_result(structure, marks))
    overall = compute_overall_result(results)
    assert overall.marks == Decimal(225)
    assert overall.max_marks == Decimal(300)
    assert overall.gpa == Decimal("4.17")  # (5 + 4 + 3.5) / 3 = 4.1666… -> 4.17
    assert overall.is_pass
