"""Build the result-engine fixture corpus (TR-RES-01: >=200 cases at 100%).

This is an **independent oracle**, not a wrapper around the engine. It re-derives
every expected value from the specification (VF-05 grade table; FR-RES-01/02/03)
using plain ``Fraction`` arithmetic and its own aggregation logic, so a fixture
that disagrees with ``khata.engines.results`` means one of the two is wrong — which
is the whole point of the corpus.

Run ``python tests/engines/results/fixtures/generate.py`` to rewrite
``result_cases.json``. The JSON is the committed artefact; the tests read it.
"""

from __future__ import annotations

import json
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
from typing import Any

OUT = Path(__file__).with_name("result_cases.json")

# VF-05, restated here rather than imported: (min percent, letter, grade point).
BANDS: list[tuple[int, str, str]] = [
    (80, "A+", "5.0"),
    (70, "A", "4.0"),
    (60, "A-", "3.5"),
    (50, "B", "3.0"),
    (40, "C", "2.0"),
    (33, "D", "1.0"),
    (0, "F", "0.0"),
]
PASS_PERCENT = Fraction(33)


def band(percent: Fraction) -> tuple[str, str]:
    for minimum, letter, point in BANDS:
        if percent >= minimum:
            return letter, point
    raise AssertionError("bands must cover 0")  # pragma: no cover


def half_up(value: Fraction) -> Fraction:
    """Round to a whole mark, ties away from zero."""
    floor = value.numerator // value.denominator
    remainder = value - floor
    return Fraction(floor + 1) if remainder >= Fraction(1, 2) else Fraction(floor)


def dec(value: Fraction) -> str:
    """Exact decimal string. Every value serialised here terminates in base 10."""
    remainder = value.denominator
    for factor in (2, 5):
        while remainder % factor == 0:
            remainder //= factor
    if remainder != 1:
        raise ValueError(f"{value} is not exactly representable in decimal")
    return str(Decimal(value.numerator) / Decimal(value.denominator))


# --------------------------------------------------------------------------- papers

SUB_PARTS = [("ka", 1), ("kha", 2), ("ga", 3), ("gha", 4)]


def cq_questions(count: int, prefix: str = "q") -> list[dict[str, Any]]:
    return [
        {
            "id": f"{prefix}{i}",
            "sub_parts": [
                {"id": f"{prefix}{i}.{part}", "max_marks": str(marks)} for part, marks in SUB_PARTS
            ],
        }
        for i in range(1, count + 1)
    ]


PAPERS: dict[str, dict[str, Any]] = {
    # One 100-mark component: isolates the grade table.
    "single100": {
        "subject_id": "single",
        "components": [
            {
                "code": "total",
                "kind": "other",
                "max_marks": "100",
                "questions": [{"id": "t1", "sub_parts": [{"id": "t1.a", "max_marks": "100"}]}],
            }
        ],
    },
    # Physics: CQ 50 marked here (5 x 10, no choice), MCQ 25 and practical 25 imported.
    "physics": {
        "subject_id": "physics",
        "components": [
            {"code": "cq", "kind": "cq", "max_marks": "50", "questions": cq_questions(5)},
            {"code": "mcq", "kind": "mcq", "max_marks": "25"},
            {"code": "practical", "kind": "practical", "max_marks": "25"},
        ],
    },
    # Maths: CQ answer 5 of 8 (each 10), MCQ 25 imported. Total 75.
    "maths_first": {
        "subject_id": "maths",
        "components": [
            {
                "code": "cq",
                "kind": "cq",
                "max_marks": "50",
                "questions": cq_questions(8),
                "choice": {"answer": 5, "policy": "first_attempted"},
            },
            {"code": "mcq", "kind": "mcq", "max_marks": "25"},
        ],
    },
    "maths_best": {
        "subject_id": "maths",
        "components": [
            {
                "code": "cq",
                "kind": "cq",
                "max_marks": "50",
                "questions": cq_questions(8),
                "choice": {"answer": 5, "policy": "best"},
            },
            {"code": "mcq", "kind": "mcq", "max_marks": "25"},
        ],
    },
}

COMPONENT_MAX = {
    "single100": {"total": Fraction(100)},
    "physics": {"cq": Fraction(50), "mcq": Fraction(25), "practical": Fraction(25)},
    "maths_first": {"cq": Fraction(50), "mcq": Fraction(25)},
    "maths_best": {"cq": Fraction(50), "mcq": Fraction(25)},
}


# ------------------------------------------------------------------------- oracle


def select(attempts: list[tuple[str, Fraction, bool]], paper: str) -> list[str]:
    """Which questions count, by this paper's choice rule."""
    attempted = [(qid, marks) for qid, marks, ok in attempts if ok]
    if paper == "maths_first":
        return [qid for qid, _ in attempted[:5]]
    if paper == "maths_best":
        order = {qid: i for i, (qid, _, _) in enumerate(attempts)}
        best = sorted(attempted, key=lambda pair: (-pair[1], order[pair[0]]))[:5]
        keep = {qid for qid, _ in best}
        return [qid for qid, _, ok in attempts if ok and qid in keep]
    return [qid for qid, _ in attempted]


def subject_expectation(
    paper: str, component_marks: dict[str, Fraction | None], counted: Fraction | None = None
) -> dict[str, Any]:
    maxima = COMPONENT_MAX[paper]
    absent = sorted(code for code, value in component_marks.items() if value is None)
    failed = sorted(
        code
        for code, value in component_marks.items()
        if value is not None and value < maxima[code] * PASS_PERCENT / 100
    )
    raw = sum((value for value in component_marks.values() if value is not None), Fraction(0))
    total = half_up(raw)
    max_total = sum(maxima.values(), Fraction(0))
    percent = total * 100 / max_total
    letter, point = band(percent)
    passed = percent >= PASS_PERCENT and not failed and not absent
    if not passed:
        letter, point = band(Fraction(0))
    return {
        "marks": dec(total),
        "max_marks": dec(max_total),
        "letter": letter,
        "grade_point": point,
        "is_pass": passed,
        "absent": bool(absent),
        "failed_components": failed,
        "absent_components": absent,
        **({"counted_cq": counted} if counted is not None else {}),
    }


# -------------------------------------------------------------------------- cases


def imported(code: str, value: Fraction | None) -> dict[str, Any]:
    if value is None:
        return {"component_code": code, "absent": True}
    return {"component_code": code, "marks": dec(value)}


def flat_marked(code: str, part: str, value: Fraction | None) -> dict[str, Any]:
    if value is None:
        return {"component_code": code, "absent": True}
    return {
        "component_code": code,
        "sub_parts": [{"sub_part_id": part, "marks": dec(value), "attempted": value > 0}],
    }


def cq_marks(code: str, per_question: list[list[int] | None]) -> dict[str, Any]:
    """``None`` means the question was not attempted; otherwise marks per sub-part."""
    parts = []
    for index, awards in enumerate(per_question, start=1):
        for (name, _), award in zip(SUB_PARTS, awards or [0, 0, 0, 0], strict=True):
            parts.append(
                {
                    "sub_part_id": f"q{index}.{name}",
                    "marks": str(award),
                    "attempted": awards is not None,
                }
            )
    return {"component_code": code, "sub_parts": parts}


def grade_table_cases() -> list[dict[str, Any]]:
    """Every whole mark 0–100 on a single 100-mark component."""
    cases = []
    for total in range(101):
        value = Fraction(total)
        cases.append(
            {
                "id": f"grade-{total:03d}",
                "why": f"{total}/100 on one component",
                "paper": "single100",
                "subject_id": "single",
                "components": [flat_marked("total", "t1.a", value)],
                "expect": subject_expectation("single100", {"total": value}),
            }
        )
    return cases


def rounding_cases() -> list[dict[str, Any]]:
    """Halves at and around grade boundaries: the total rounds before it grades."""
    cases = []
    for whole in (32, 39, 49, 59, 69, 79, 0, 99):
        for offset in ("0.5", "0.25", "0.75"):
            value = Fraction(whole) + Fraction(offset)
            cases.append(
                {
                    "id": f"round-{whole}-{offset.replace('.', '')}",
                    "why": f"{value} rounds half-up before grading",
                    "paper": "single100",
                    "subject_id": "single",
                    "components": [flat_marked("total", "t1.a", value)],
                    "expect": subject_expectation("single100", {"total": value}),
                }
            )
    return cases


def component_rule_cases() -> list[dict[str, Any]]:
    """Physics: component pass rules against the subject total."""
    combinations = [
        (50, 25, 25),
        (40, 20, 20),
        (17, 9, 9),
        (16, 9, 9),
        (17, 8, 9),
        (17, 9, 8),
        (15, 25, 25),
        (50, 8, 25),
        (50, 25, 8),
        (0, 25, 25),
        (50, 0, 25),
        (50, 25, 0),
        (16, 25, 25),
        (17, 25, 25),
        (25, 13, 13),
        (33, 17, 17),
        (20, 10, 10),
        (45, 22, 22),
        (35, 18, 18),
        (30, 15, 15),
        (18, 9, 9),
        (49, 24, 24),
        (16, 8, 8),
        (17, 9, 25),
        (42, 21, 8),
        (10, 20, 20),
        (50, 24, 24),
        (19, 9, 9),
        (22, 11, 11),
        (28, 14, 14),
    ]
    cases = []
    for cq, mcq, practical in combinations:
        marks = {
            "cq": Fraction(cq),
            "mcq": Fraction(mcq),
            "practical": Fraction(practical),
        }
        cases.append(
            {
                "id": f"physics-{cq}-{mcq}-{practical}",
                "why": f"CQ {cq}/50, MCQ {mcq}/25, practical {practical}/25",
                "paper": "physics",
                "subject_id": "physics",
                "components": [
                    cq_marks("cq", _spread(cq, 5)),
                    imported("mcq", Fraction(mcq)),
                    imported("practical", Fraction(practical)),
                ],
                "expect": subject_expectation("physics", marks),
            }
        )
    return cases


def _spread(total: int, questions: int) -> list[list[int] | None]:
    """Spread a CQ total over whole questions: full 10s, then a partial, then blanks."""
    out: list[list[int] | None] = []
    left = total
    for _ in range(questions):
        if left >= 10:
            out.append([1, 2, 3, 4])
            left -= 10
        elif left > 0:
            awards = []
            for _, maximum in SUB_PARTS:
                take = min(maximum, left)
                awards.append(take)
                left -= take
            out.append(awards)
        else:
            out.append(None)
    assert left == 0, (total, left)
    return out


def absence_cases() -> list[dict[str, Any]]:
    cases = []
    for absent_code in ("cq", "mcq", "practical"):
        for cq, mcq, practical in ((40, 20, 20), (17, 9, 9), (50, 25, 25)):
            values: dict[str, Fraction | None] = {
                "cq": Fraction(cq),
                "mcq": Fraction(mcq),
                "practical": Fraction(practical),
            }
            values[absent_code] = None
            components = [
                cq_marks("cq", _spread(cq, 5))
                if values["cq"] is not None
                else {"component_code": "cq", "absent": True},
                imported("mcq", values["mcq"]),
                imported("practical", values["practical"]),
            ]
            cases.append(
                {
                    "id": f"absent-{absent_code}-{cq}-{mcq}-{practical}",
                    "why": f"{absent_code} absent; absence is not zero",
                    "paper": "physics",
                    "subject_id": "physics",
                    "components": components,
                    "expect": subject_expectation("physics", values),
                }
            )
    return cases


CQ_PATTERNS: list[list[list[int] | None]] = [
    # eight questions; None = not attempted
    [[1, 2, 3, 4]] * 5 + [None] * 3,
    [[1, 2, 3, 4]] * 6 + [None] * 2,
    [[1, 2, 3, 4]] * 8,
    [[0, 1, 1, 1]] * 5 + [[1, 2, 3, 4]] + [None] * 2,
    [[0, 0, 0, 0]] * 5 + [[1, 2, 3, 4]] * 3,
    [[1, 1, 1, 1]] * 4 + [None] * 4,
    [[1, 2, 3, 4]] * 3 + [None] * 5,
    [None] * 8,
    [[1, 0, 0, 0]] + [[1, 2, 3, 4]] * 5 + [None] * 2,
    [[1, 2, 3, 4]] * 2 + [None] * 2 + [[1, 2, 3, 4]] * 4,
    [[0, 2, 0, 4]] * 8,
    [[1, 2, 3, 0]] * 5 + [[1, 2, 3, 4]] * 3,
]


def choice_cases() -> list[dict[str, Any]]:
    cases = []
    for paper in ("maths_first", "maths_best"):
        for index, pattern in enumerate(CQ_PATTERNS):
            for mcq in (25, 20, 9, 8, 0):
                attempts = [
                    (f"q{i + 1}", Fraction(sum(awards or [])), awards is not None)
                    for i, awards in enumerate(pattern)
                ]
                counted = select(attempts, paper)
                cq_total = sum((marks for qid, marks, _ in attempts if qid in counted), Fraction(0))
                values = {"cq": cq_total, "mcq": Fraction(mcq)}
                cases.append(
                    {
                        "id": f"{paper}-p{index}-mcq{mcq}",
                        "why": f"{paper} pattern {index}, MCQ {mcq}/25",
                        "paper": paper,
                        "subject_id": "maths",
                        "components": [cq_marks("cq", pattern), imported("mcq", Fraction(mcq))],
                        "expect": subject_expectation(paper, values, counted=counted),
                    }
                )
    return cases


def gpa_cases() -> list[dict[str, Any]]:
    """GPA over grade points, including the 4th-subject rule and the 5.00 cap."""
    cases: list[dict[str, Any]] = []
    combos: list[tuple[list[str], str | None]] = [
        (["5.0", "5.0", "5.0", "5.0"], None),
        (["5.0", "4.0", "3.5", "3.0"], None),
        (["4.0", "4.0", "4.0", "4.0"], "5.0"),
        (["4.0", "4.0", "4.0", "4.0"], "2.0"),
        (["4.0", "4.0", "4.0", "4.0"], "1.0"),
        (["4.0", "4.0", "4.0", "4.0"], "0.0"),
        (["5.0", "5.0", "5.0", "5.0"], "5.0"),
        (["5.0", "5.0", "5.0", "5.0"], "3.0"),
        (["3.0", "3.0", "3.0"], "4.0"),
        (["1.0", "1.0", "1.0"], "5.0"),
        (["2.0", "3.0", "4.0", "5.0", "1.0"], None),
        (["5.0", "4.0"], "5.0"),
        (["3.5", "3.5", "3.5"], "3.5"),
        (["1.0"], "5.0"),
        (["5.0", "0.0"], None),
        (["0.0", "5.0", "5.0"], "5.0"),
        (["2.0", "2.0", "2.0", "2.0", "2.0"], "2.0"),
        (["4.0", "3.5", "3.0", "2.0", "1.0"], "4.0"),
        (["5.0", "5.0", "4.0"], None),
        (["5.0", "4.0", "4.0"], None),
    ]
    for index, (mains, fourth) in enumerate(combos):
        points = [Fraction(m.replace(".0", "")) if m.endswith(".0") else Fraction(m) for m in mains]
        failed = [f"m{i}" for i, value in enumerate(points) if value == 0]
        bonus = Fraction(0)
        if fourth is not None:
            fourth_gp = Fraction(fourth) if "." in fourth else Fraction(int(fourth))
            bonus = max(Fraction(0), fourth_gp - 2)
        if failed:
            value, passed = Fraction(0), False
        else:
            exact = (sum(points, Fraction(0)) + bonus) / len(points)
            value = min(_round2(exact), Fraction(5))
            passed = True
        subjects = [
            {"subject_id": f"m{i}", "grade_point": mains[i], "is_pass": points[i] > 0}
            for i in range(len(mains))
        ]
        if fourth is not None:
            subjects.append(
                {
                    "subject_id": "opt",
                    "grade_point": fourth,
                    "is_pass": Fraction(fourth) > 0,
                    "is_fourth_subject": True,
                }
            )
        cases.append(
            {
                "id": f"gpa-{index:02d}",
                "why": f"mains {mains}, fourth {fourth}",
                "subjects": subjects,
                "expect": {
                    "gpa": _two_places(value),
                    "is_pass": passed,
                    "failed_subjects": failed,
                },
            }
        )
    return cases


def _round2(value: Fraction) -> Fraction:
    scaled = value * 100
    floor = scaled.numerator // scaled.denominator
    remainder = scaled - floor
    whole = floor + 1 if remainder >= Fraction(1, 2) else floor
    return Fraction(whole, 100)


def _two_places(value: Fraction) -> str:
    hundredths = value * 100
    assert hundredths.denominator == 1, value
    digits = str(hundredths.numerator).rjust(3, "0")
    return f"{digits[:-2]}.{digits[-2:]}"


def main() -> None:
    subject_cases = (
        grade_table_cases()
        + rounding_cases()
        + component_rule_cases()
        + absence_cases()
        + choice_cases()
    )
    payload = {
        "note": "Generated by generate.py, an oracle independent of khata.engines.results.",
        "papers": PAPERS,
        "subject_cases": subject_cases,
        "gpa_cases": gpa_cases(),
    }
    OUT.write_text(json.dumps(payload, indent=1, ensure_ascii=False) + "\n")
    print(f"{len(subject_cases)} subject cases + {len(payload['gpa_cases'])} GPA cases")


if __name__ == "__main__":
    main()
