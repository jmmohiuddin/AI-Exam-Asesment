"""The numeric-checker corpus (TR-MATH-01: a fixture suite of 500 numeric cases).

Expectations come from ``fixtures/generate.py``, an oracle that restates the
tolerance, unit and significant-figure rules from the specification and never
imports the engine.
"""

from __future__ import annotations

import json
from decimal import Decimal
from pathlib import Path
from typing import Any

import pytest

from khata.engines.mathcheck.numeric import check_answer
from khata.engines.rubric import AnswerSpec

CORPUS = json.loads((Path(__file__).parent / "fixtures" / "numeric_cases.json").read_text())
CASES: list[dict[str, Any]] = CORPUS["cases"]


def test_the_corpus_meets_the_required_size() -> None:
    assert len(CASES) >= 500


def test_case_ids_are_unique() -> None:
    ids = [case["id"] for case in CASES]
    assert len(ids) == len(set(ids))


@pytest.mark.parametrize("case", CASES, ids=lambda c: c["id"])
def test_numeric_check_matches_the_oracle(case: dict[str, Any]) -> None:
    spec = AnswerSpec.model_validate(case["spec"])
    result = check_answer(spec, case["student"])
    expect = case["expect"]

    assert sorted(b.value for b in result.badges) == sorted(expect["badges"]), case["why"]
    assert result.matches == expect["matches"], case["why"]
    assert result.unit_deduction == Decimal(expect["unit_deduction"]), case["why"]
