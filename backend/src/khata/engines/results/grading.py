"""Grades, grade points and GPA (FR-RES-02/03, ASR-06; scale from VF-05).

The NCTB scale is the default, not a hard-coded rule: a school may supply its own
:class:`GradeScale`. Two rules carry the Bangladeshi semantics and are easy to get
wrong, so they are stated once, here:

* **Fourth subject.** Only the grade point *above* 2.00 counts, and it is added to
  the main-subject total before dividing by the number of **main** subjects. A weak
  optional subject therefore never drags the GPA down.
* **Any fail fails the result.** A single failed or absent main subject makes the
  whole result a fail with GPA 0.00, whatever the other subjects scored. A failed
  fourth subject does not.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from decimal import Decimal
from itertools import pairwise

from pydantic import Field, field_validator, model_validator

from khata.engines.base import FrozenModel, Percent
from khata.engines.errors import ResultInputError
from khata.engines.marks import RoundingMode, round_exact

ZERO = Decimal(0)
GPA_QUANTUM = Decimal("0.01")
GPA_CAP = Decimal("5.00")
FOURTH_SUBJECT_THRESHOLD = Decimal("2.00")


class GradeBand(FrozenModel):
    """One row of a grade scale: everything from ``min_percent`` up to the next band."""

    min_percent: Percent
    letter: str = Field(min_length=1, max_length=8)
    grade_point: Decimal = Field(ge=0, le=10, allow_inf_nan=False)


class GradeScale(FrozenModel):
    """Bands ordered high to low, covering 0–100 with no gaps or overlaps."""

    bands: tuple[GradeBand, ...] = Field(min_length=2)
    pass_percent: Percent

    @field_validator("bands")
    @classmethod
    def _ordered_and_complete(cls, bands: tuple[GradeBand, ...]) -> tuple[GradeBand, ...]:
        ordered = sorted(bands, key=lambda b: b.min_percent, reverse=True)
        if tuple(ordered) != bands:
            raise ResultInputError("grade bands must be ordered from highest to lowest")
        for higher, lower in pairwise(bands):
            if higher.min_percent == lower.min_percent:
                raise ResultInputError(
                    f"grade bands overlap at {higher.min_percent}%: "
                    f"{higher.letter!r} and {lower.letter!r}"
                )
        if bands[-1].min_percent != ZERO:
            raise ResultInputError("the lowest grade band must start at 0%")
        return bands

    @model_validator(mode="after")
    def _pass_percent_is_a_band_boundary(self) -> GradeScale:
        if self.pass_percent not in {band.min_percent for band in self.bands}:
            raise ResultInputError(
                f"pass_percent {self.pass_percent} is not the start of any grade band"
            )
        return self


class Grade(FrozenModel):
    letter: str
    grade_point: Decimal
    is_pass: bool


class SubjectGrade(FrozenModel):
    """A graded subject, as GPA sees it."""

    subject_id: str = Field(min_length=1)
    letter: str
    grade_point: Decimal = Field(ge=0, allow_inf_nan=False)
    is_pass: bool
    is_fourth_subject: bool = False
    is_absent: bool = False


class GpaResult(FrozenModel):
    gpa: Decimal
    is_pass: bool
    main_subject_count: int
    fourth_subject_bonus: Decimal
    failed_subjects: tuple[str, ...]
    absent_subjects: tuple[str, ...]


# NCTB secondary scale (VF-05). Pass mark 33%; GPA capped at 5.00.
NCTB_GRADE_SCALE = GradeScale(
    bands=(
        GradeBand(min_percent=Decimal(80), letter="A+", grade_point=Decimal("5.0")),
        GradeBand(min_percent=Decimal(70), letter="A", grade_point=Decimal("4.0")),
        GradeBand(min_percent=Decimal(60), letter="A-", grade_point=Decimal("3.5")),
        GradeBand(min_percent=Decimal(50), letter="B", grade_point=Decimal("3.0")),
        GradeBand(min_percent=Decimal(40), letter="C", grade_point=Decimal("2.0")),
        GradeBand(min_percent=Decimal(33), letter="D", grade_point=Decimal("1.0")),
        GradeBand(min_percent=ZERO, letter="F", grade_point=ZERO),
    ),
    pass_percent=Decimal(33),
)


def grade_for_percent(percent: Decimal, scale: GradeScale = NCTB_GRADE_SCALE) -> Grade:
    """The band a percentage falls in. ``percent`` must be within 0–100."""
    if percent < ZERO or percent > Decimal(100):
        raise ResultInputError(f"percent must be within 0–100 (got {percent})")
    for band in scale.bands:
        if percent >= band.min_percent:
            return Grade(
                letter=band.letter,
                grade_point=band.grade_point,
                is_pass=percent >= scale.pass_percent,
            )
    raise ResultInputError(f"no grade band matches {percent}%")  # pragma: no cover


def gpa(subjects: Iterable[SubjectGrade]) -> GpaResult:
    """GPA across the subjects of one student, applying the 4th-subject rule."""
    graded = tuple(subjects)
    _check_subjects(graded)
    mains = tuple(s for s in graded if not s.is_fourth_subject)
    fourth = next((s for s in graded if s.is_fourth_subject), None)

    failed = tuple(s.subject_id for s in mains if not s.is_pass and not s.is_absent)
    absent = tuple(s.subject_id for s in mains if s.is_absent)
    bonus = _fourth_subject_bonus(fourth)

    if failed or absent:
        return GpaResult(
            gpa=Decimal("0.00"),
            is_pass=False,
            main_subject_count=len(mains),
            fourth_subject_bonus=bonus,
            failed_subjects=failed,
            absent_subjects=absent,
        )

    total = sum((s.grade_point for s in mains), ZERO) + bonus
    value = min(_round_gpa(total / Decimal(len(mains))), GPA_CAP)
    return GpaResult(
        gpa=value,
        is_pass=True,
        main_subject_count=len(mains),
        fourth_subject_bonus=bonus,
        failed_subjects=(),
        absent_subjects=(),
    )


def _fourth_subject_bonus(fourth: SubjectGrade | None) -> Decimal:
    if fourth is None or fourth.is_absent:
        return ZERO
    return max(ZERO, fourth.grade_point - FOURTH_SUBJECT_THRESHOLD)


def _check_subjects(graded: Sequence[SubjectGrade]) -> None:
    ids = [s.subject_id for s in graded]
    duplicates = sorted({sid for sid in ids if ids.count(sid) > 1})
    if duplicates:
        raise ResultInputError(f"duplicate subject ids: {', '.join(duplicates)}")
    fourths = [s.subject_id for s in graded if s.is_fourth_subject]
    if len(fourths) > 1:
        raise ResultInputError(f"more than one fourth subject: {', '.join(sorted(fourths))}")
    if not any(not s.is_fourth_subject for s in graded):
        raise ResultInputError("a result needs at least one main subject")


def _round_gpa(value: Decimal) -> Decimal:
    return round_exact(value, GPA_QUANTUM, RoundingMode.HALF_UP)
