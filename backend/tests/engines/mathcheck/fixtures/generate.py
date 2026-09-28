"""Build the numeric-checker corpus (TR-MATH-01: a fixture suite of 500 cases).

An oracle independent of ``khata.engines.mathcheck``: it restates the unit scales
and the tolerance, unit and significant-figure rules from the specification and
computes every expectation with ``Fraction`` arithmetic of its own. A disagreement
means the engine and the specification have drifted apart.

Run ``python tests/engines/mathcheck/fixtures/generate.py`` to rewrite
``numeric_cases.json``; the JSON is the committed artefact.
"""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path
from typing import Any

OUT = Path(__file__).with_name("numeric_cases.json")

BANGLA = str.maketrans("0123456789", "০১২৩৪৫৬৭৮৯")

#: unit -> (dimension key, scale to SI). Restated, not imported.
UNITS: dict[str, tuple[str, Fraction]] = {
    "m": ("L", Fraction(1)),
    "cm": ("L", Fraction(1, 100)),
    "km": ("L", Fraction(1000)),
    "mm": ("L", Fraction(1, 1000)),
    "s": ("T", Fraction(1)),
    "min": ("T", Fraction(60)),
    "h": ("T", Fraction(3600)),
    "kg": ("M", Fraction(1)),
    "g": ("M", Fraction(1, 1000)),
    "N": ("F", Fraction(1)),
    "kN": ("F", Fraction(1000)),
    "J": ("E", Fraction(1)),
    "kJ": ("E", Fraction(1000)),
    "W": ("P", Fraction(1)),
    "kW": ("P", Fraction(1000)),
    "m/s": ("V", Fraction(1)),
    "km/h": ("V", Fraction(1, 36) * Fraction(10)),
}
# km/h = 1000 m / 3600 s = 5/18 m/s
UNITS["km/h"] = ("V", Fraction(5, 18))


def render_decimal(value: Fraction) -> str:
    """Exact decimal text for a value whose denominator divides a power of ten."""
    remainder = value.denominator
    for factor in (2, 5):
        while remainder % factor == 0:
            remainder //= factor
    if remainder != 1:
        raise ValueError(f"{value} does not terminate")
    digits = 0
    scaled = value
    while scaled.denominator != 1:
        scaled *= 10
        digits += 1
    text = str(abs(scaled.numerator)).rjust(digits + 1, "0")
    body = text if digits == 0 else f"{text[:-digits]}.{text[-digits:]}"
    return f"-{body}" if value < 0 else body


def sig_figs(text: str) -> int | None:
    """Significant figures as written; ``None`` for a form that has no count."""
    body = text.lstrip("+-")
    if "/" in body:
        return None
    if "." in body:
        stripped = body.replace(".", "").lstrip("0")
        return len(stripped) if stripped else 1
    stripped = body.lstrip("0")
    return len(stripped) if stripped else 1


def expect(
    *,
    key_value: Fraction,
    key_unit: str | None,
    unit_required: bool,
    tolerance_abs: Fraction | None,
    tolerance_rel: Fraction | None,
    student_value: Fraction | None,
    student_unit: str | None,
    student_sig_figs: int | None,
    sig_mode: str,
    sig_count: int | None,
    missing_unit_deduction: Fraction,
) -> dict[str, Any]:
    """The badges and verdict the specification requires for one case."""
    if student_value is None:
        return {"badges": ["cannot_verify"], "matches": False, "unit_deduction": "0"}

    badges: list[str] = []
    deduction = Fraction(0)
    comparable = student_value
    unit_ok = True

    if key_unit is not None:
        if student_unit is None:
            if unit_required:
                badges.append("unit_missing")
                unit_ok = False
                deduction = missing_unit_deduction
        elif UNITS[student_unit][0] != UNITS[key_unit][0]:
            return {"badges": ["unit_wrong"], "matches": False, "unit_deduction": "0"}
        else:
            comparable = student_value * UNITS[student_unit][1] / UNITS[key_unit][1]
            if UNITS[student_unit][1] != UNITS[key_unit][1]:
                badges.append("unit_converted")

    difference = abs(comparable - key_value)
    if tolerance_abs is None and tolerance_rel is None:
        value_ok = difference == 0
    else:
        value_ok = (tolerance_abs is not None and difference <= tolerance_abs) or (
            tolerance_rel is not None
            and key_value != 0
            and difference / abs(key_value) <= tolerance_rel
        )
    badges.append("value_matches" if value_ok else "value_differs")

    judge_sig_figs = (
        value_ok and sig_mode != "ignore" and sig_count is not None and student_sig_figs is not None
    )
    if judge_sig_figs:
        assert student_sig_figs is not None and sig_count is not None
        enough = (
            student_sig_figs >= sig_count
            if sig_mode == "at_least"
            else student_sig_figs == sig_count
        )
        if not enough:
            badges.append("sig_figs_short")

    return {
        "badges": badges,
        "matches": value_ok and unit_ok,
        "unit_deduction": render_decimal(deduction),
    }


def case(
    case_id: str,
    why: str,
    *,
    key_value: str,
    key_unit: str | None = None,
    unit_required: bool = True,
    tol_abs: str | None = None,
    tol_rel: str | None = None,
    student_text: str,
    student_value: Fraction | None,
    student_unit: str | None = None,
    student_sig_figs: int | None = None,
    sig_mode: str = "ignore",
    sig_count: int | None = None,
    deduction: str = "0",
) -> dict[str, Any]:
    spec: dict[str, Any] = {"kind": "numeric", "value": key_value, "unit_required": unit_required}
    if key_unit is not None:
        spec["unit"] = key_unit
    if tol_abs is not None or tol_rel is not None:
        tolerance: dict[str, str] = {}
        if tol_abs is not None:
            tolerance["abs"] = tol_abs
        if tol_rel is not None:
            tolerance["rel"] = tol_rel
        spec["tolerance"] = tolerance
    if sig_mode != "ignore":
        spec["sig_figs"] = {"mode": sig_mode, "count": sig_count}
    if deduction != "0":
        spec["missing_unit_deduction"] = deduction
    return {
        "id": case_id,
        "why": why,
        "spec": spec,
        "student": student_text,
        "expect": expect(
            key_value=Fraction(key_value),
            key_unit=key_unit,
            unit_required=unit_required,
            tolerance_abs=Fraction(tol_abs) if tol_abs else None,
            tolerance_rel=Fraction(tol_rel) if tol_rel else None,
            student_value=student_value,
            student_unit=student_unit,
            student_sig_figs=student_sig_figs,
            sig_mode=sig_mode,
            sig_count=sig_count,
            missing_unit_deduction=Fraction(deduction),
        ),
    }


def tolerance_sweep() -> list[dict[str, Any]]:
    """A key of 9.8 with every student value from 9.0 to 10.6, at three tolerances."""
    cases = []
    for tol in (None, "0.1", "0.25", "0.5", "1"):
        for step in range(21):
            value = Fraction(90 + step, 10)
            text = render_decimal(value)
            cases.append(
                case(
                    f"tol-{tol or 'exact'}-{step:02d}",
                    f"key 9.8 m/s^2, student {text}, tolerance {tol or 'exact'}",
                    key_value="9.8",
                    key_unit="m/s",
                    tol_abs=tol,
                    student_text=f"{text} m/s",
                    student_value=value,
                    student_unit="m/s",
                    student_sig_figs=sig_figs(text),
                )
            )
    return cases


def relative_sweep() -> list[dict[str, Any]]:
    cases = []
    for rel in ("0.01", "0.05", "0.1"):
        for step in range(0, 25):
            value = Fraction(1000 + step * 10, 10)
            text = render_decimal(value)
            cases.append(
                case(
                    f"rel-{rel.replace('.', '')}-{step:02d}",
                    f"key 100 m, student {text}, relative tolerance {rel}",
                    key_value="100",
                    key_unit="m",
                    tol_rel=rel,
                    student_text=f"{text} m",
                    student_value=value,
                    student_unit="m",
                    student_sig_figs=sig_figs(text),
                )
            )
    return cases


CONVERSIONS = [
    ("1000", "m", "1", "km"),
    ("1", "km", "1000", "m"),
    ("100", "cm", "1", "m"),
    ("1", "m", "100", "cm"),
    ("1", "m", "1000", "mm"),
    ("1000", "g", "1", "kg"),
    ("1", "kg", "1000", "g"),
    ("60", "s", "1", "min"),
    ("3600", "s", "1", "h"),
    ("20", "m/s", "72", "km/h"),
    ("72", "km/h", "20", "m/s"),
    ("1000", "N", "1", "kN"),
    ("1", "kN", "1000", "N"),
    ("1000", "J", "1", "kJ"),
    ("1000", "W", "1", "kW"),
]


def conversion_cases() -> list[dict[str, Any]]:
    cases = []
    for index, (key_value, key_unit, student_value, student_unit) in enumerate(CONVERSIONS):
        for scale in (1, 2, 5, 10):
            key = Fraction(key_value) * scale
            student = Fraction(student_value) * scale
            cases.append(
                case(
                    f"conv-{index:02d}-x{scale}",
                    f"{student} {student_unit} expressed against {key} {key_unit}",
                    key_value=render_decimal(key),
                    key_unit=key_unit,
                    student_text=f"{render_decimal(student)} {student_unit}",
                    student_value=student,
                    student_unit=student_unit,
                    student_sig_figs=sig_figs(render_decimal(student)),
                )
            )
    return cases


WRONG_DIMENSIONS = [
    ("m", "s"),
    ("m", "kg"),
    ("m/s", "m"),
    ("N", "J"),
    ("J", "W"),
    ("kg", "N"),
    ("s", "m"),
    ("km/h", "kg"),
    ("W", "J"),
    ("m", "m/s"),
]


def wrong_unit_cases() -> list[dict[str, Any]]:
    cases = []
    for index, (key_unit, student_unit) in enumerate(WRONG_DIMENSIONS):
        for value in ("5", "12.5", "100"):
            cases.append(
                case(
                    f"dim-{index:02d}-{value.replace('.', '')}",
                    f"{value} {student_unit} against a key in {key_unit}",
                    key_value=value,
                    key_unit=key_unit,
                    student_text=f"{value} {student_unit}",
                    student_value=Fraction(value),
                    student_unit=student_unit,
                    student_sig_figs=sig_figs(value),
                )
            )
    return cases


def missing_unit_cases() -> list[dict[str, Any]]:
    cases = []
    for index, (required, deduction) in enumerate(
        [(True, "0"), (True, "1"), (True, "0.5"), (False, "0")]
    ):
        for value, key in [("9.8", "9.8"), ("9.9", "9.8"), ("5", "5"), ("4", "5")]:
            cases.append(
                case(
                    f"nounit-{index}-{value.replace('.', '')}-{key.replace('.', '')}",
                    f"student wrote {value} with no unit; required={required}",
                    key_value=key,
                    key_unit="m/s",
                    unit_required=required,
                    tol_abs="0.1",
                    student_text=value,
                    student_value=Fraction(value),
                    student_unit=None,
                    student_sig_figs=sig_figs(value),
                    deduction=deduction,
                )
            )
    return cases


NUMBER_FORMS = [
    ("1/2", Fraction(1, 2), None),
    ("0.5", Fraction(1, 2), 1),
    ("2/4", Fraction(1, 2), None),
    ("1 1/2", Fraction(3, 2), None),
    ("1.5", Fraction(3, 2), 2),
    ("3/2", Fraction(3, 2), None),
    ("0.25", Fraction(1, 4), 2),
    ("1/4", Fraction(1, 4), None),
    ("100", Fraction(100), 3),
    ("1e2", Fraction(100), 1),
    ("1 x 10^2", Fraction(100), 1),
    ("0.001", Fraction(1, 1000), 1),
    ("1e-3", Fraction(1, 1000), 1),
    ("1,000", Fraction(1000), 4),
    ("1000", Fraction(1000), 4),
    ("2.50", Fraction(5, 2), 3),
    ("2.5", Fraction(5, 2), 2),
]


def number_form_cases() -> list[dict[str, Any]]:
    """Every written form against every key value: the same number must read the same."""
    cases = []
    for index, (text, value, figures) in enumerate(NUMBER_FORMS):
        for key in ("0.5", "1.5", "100", "0.001", "2.5", "1000", "0.25", "0.75", "2"):
            cases.append(
                case(
                    f"form-{index:02d}-{key.replace('.', '')}",
                    f"student wrote {text!r} against a key of {key}",
                    key_value=key,
                    unit_required=False,
                    student_text=text,
                    student_value=value,
                    student_sig_figs=figures,
                )
            )
        bangla = text.translate(BANGLA)
        if bangla != text:
            cases.append(
                case(
                    f"form-{index:02d}-bn",
                    f"Bangla numerals {bangla!r} read like {text!r}",
                    key_value="0.5" if value == Fraction(1, 2) else render_decimal(value),
                    unit_required=False,
                    student_text=bangla,
                    student_value=value,
                    student_sig_figs=figures,
                )
            )
    return cases


def sig_fig_cases() -> list[dict[str, Any]]:
    cases = []
    written = [("9.8", 2), ("9.80", 3), ("9.812", 4), ("10", 2), ("9.8000", 5)]
    for mode in ("at_least", "exact"):
        for count in (2, 3, 4):
            for text, figures in written:
                cases.append(
                    case(
                        f"sig-{mode}-{count}-{text.replace('.', '')}",
                        f"{text} under {mode} {count} significant figures",
                        key_value="9.8",
                        unit_required=False,
                        tol_abs="0.5",
                        student_text=text,
                        student_value=Fraction(text),
                        student_sig_figs=figures,
                        sig_mode=mode,
                        sig_count=count,
                    )
                )
    return cases


UNREADABLE = [
    "",
    "   ",
    "abc",
    "about ten",
    "?",
    "-",
    "n/a",
    "I don't know",
    "5 apples and 3",
    "ten",
    "১০ টা মতো",
    "--5",
    "/5",
    "5/",
    "১/০",
    "1/0",
]


def unreadable_cases() -> list[dict[str, Any]]:
    return [
        case(
            f"unreadable-{index:02d}",
            f"{text!r} is unreadable, so the answer cannot be verified",
            key_value="9.8",
            key_unit="m/s",
            tol_abs="0.1",
            student_text=text,
            student_value=None,
        )
        for index, text in enumerate(UNREADABLE)
    ]


def main() -> None:
    groups = [
        tolerance_sweep(),
        relative_sweep(),
        conversion_cases(),
        wrong_unit_cases(),
        missing_unit_cases(),
        number_form_cases(),
        sig_fig_cases(),
        unreadable_cases(),
    ]
    cases = [c for group in groups for c in group]
    seen: dict[str, int] = {}
    for item in cases:
        seen[item["id"]] = seen.get(item["id"], 0) + 1
        if seen[item["id"]] > 1:
            item["id"] = f"{item['id']}#{seen[item['id']]}"
    payload = {
        "note": "Generated by generate.py, an oracle independent of khata.engines.mathcheck.",
        "cases": cases,
    }
    OUT.write_text(json.dumps(payload, indent=1, ensure_ascii=False) + "\n")
    print(f"{len(cases)} numeric cases")


if __name__ == "__main__":
    main()
