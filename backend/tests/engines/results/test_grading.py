"""Grade, grade point and GPA rules (FR-RES-02/03, VF-05)."""

from __future__ import annotations

from decimal import Decimal

import pytest
from pydantic import ValidationError

from khata.engines.errors import ResultInputError
from khata.engines.results.grading import (
    NCTB_GRADE_SCALE,
    GradeBand,
    GradeScale,
    SubjectGrade,
    gpa,
    grade_for_percent,
)

D = Decimal


class TestNctbScale:
    @pytest.mark.parametrize(
        ("percent", "letter", "point"),
        [
            (100, "A+", "5.0"),
            (80, "A+", "5.0"),
            (79.99, "A", "4.0"),
            (70, "A", "4.0"),
            (69.5, "A-", "3.5"),
            (60, "A-", "3.5"),
            (59, "B", "3.0"),
            (50, "B", "3.0"),
            (49, "C", "2.0"),
            (40, "C", "2.0"),
            (39, "D", "1.0"),
            (33, "D", "1.0"),
            (32.99, "F", "0.0"),
            (0, "F", "0.0"),
        ],
    )
    def test_band_boundaries(self, percent: float, letter: str, point: str) -> None:
        band = grade_for_percent(D(str(percent)), NCTB_GRADE_SCALE)
        assert band.letter == letter
        assert band.grade_point == D(point)

    def test_pass_mark_is_33_percent(self) -> None:
        assert NCTB_GRADE_SCALE.pass_percent == D(33)
        assert grade_for_percent(D(33), NCTB_GRADE_SCALE).is_pass
        assert not grade_for_percent(D("32.999"), NCTB_GRADE_SCALE).is_pass

    def test_percent_outside_range_is_rejected(self) -> None:
        with pytest.raises(ResultInputError):
            grade_for_percent(D("100.01"), NCTB_GRADE_SCALE)
        with pytest.raises(ResultInputError):
            grade_for_percent(D(-1), NCTB_GRADE_SCALE)


class TestCustomScale:
    def test_scale_must_cover_zero_to_hundred(self) -> None:
        with pytest.raises(ValidationError):
            GradeScale(
                bands=(
                    GradeBand(min_percent=D(50), letter="P", grade_point=D(4)),
                    GradeBand(min_percent=D(10), letter="F", grade_point=D(0)),
                ),
                pass_percent=D(50),
            )

    def test_bands_may_not_overlap(self) -> None:
        with pytest.raises(ValidationError):
            GradeScale(
                bands=(
                    GradeBand(min_percent=D(50), letter="P", grade_point=D(4)),
                    GradeBand(min_percent=D(50), letter="Q", grade_point=D(3)),
                    GradeBand(min_percent=D(0), letter="F", grade_point=D(0)),
                ),
                pass_percent=D(50),
            )

    def test_a_school_may_set_its_own_bands(self) -> None:
        scale = GradeScale(
            bands=(
                GradeBand(min_percent=D(45), letter="P", grade_point=D(4)),
                GradeBand(min_percent=D(0), letter="F", grade_point=D(0)),
            ),
            pass_percent=D(45),
        )
        assert grade_for_percent(D(45), scale).letter == "P"
        assert grade_for_percent(D(44), scale).letter == "F"


def sg(point: str, *, fourth: bool = False, subject: str = "s") -> SubjectGrade:
    return SubjectGrade(
        subject_id=subject,
        letter="X",
        grade_point=D(point),
        is_fourth_subject=fourth,
        is_pass=D(point) > 0,
    )


class TestGpa:
    def test_mean_of_main_subjects(self) -> None:
        result = gpa([sg("5.0", subject="a"), sg("4.0", subject="b"), sg("3.0", subject="c")])
        assert result.gpa == D("4.00")
        assert result.is_pass

    def test_fourth_subject_contributes_only_above_two(self) -> None:
        mains = [sg("4.0", subject=f"m{i}") for i in range(4)]
        # 4th subject GP 5.0 -> +3.0 spread over 4 main subjects
        result = gpa([*mains, sg("5.0", subject="opt", fourth=True)])
        assert result.gpa == D("4.75")

    def test_fourth_subject_at_or_below_two_adds_nothing(self) -> None:
        mains = [sg("4.0", subject=f"m{i}") for i in range(4)]
        assert gpa([*mains, sg("2.0", subject="opt", fourth=True)]).gpa == D("4.00")
        assert gpa([*mains, sg("1.0", subject="opt", fourth=True)]).gpa == D("4.00")

    def test_fourth_subject_never_drags_the_gpa_down(self) -> None:
        mains = [sg("5.0", subject=f"m{i}") for i in range(4)]
        assert gpa([*mains, sg("0.0", subject="opt", fourth=True)]).gpa == D("5.00")

    def test_gpa_is_capped_at_five(self) -> None:
        mains = [sg("5.0", subject=f"m{i}") for i in range(4)]
        result = gpa([*mains, sg("5.0", subject="opt", fourth=True)])
        assert result.gpa == D("5.00")

    def test_a_single_fail_makes_the_whole_result_fail_with_zero_gpa(self) -> None:
        result = gpa([sg("5.0", subject="a"), sg("0.0", subject="b")])
        assert not result.is_pass
        assert result.gpa == D("0.00")
        assert result.failed_subjects == ("b",)

    def test_a_failed_fourth_subject_does_not_fail_the_student(self) -> None:
        result = gpa([sg("4.0", subject="a"), sg("0.0", subject="opt", fourth=True)])
        assert result.is_pass
        assert result.gpa == D("4.00")

    def test_gpa_rounds_half_up_to_two_places(self) -> None:
        # (5 + 4 + 4) / 3 = 4.333... -> 4.33
        assert gpa(
            [sg("5.0", subject="a"), sg("4.0", subject="b"), sg("4.0", subject="c")]
        ).gpa == D("4.33")
        # (5 + 5 + 4) / 3 = 4.666... -> 4.67
        assert gpa(
            [sg("5.0", subject="a"), sg("5.0", subject="b"), sg("4.0", subject="c")]
        ).gpa == D("4.67")

    def test_absent_subject_fails_the_result(self) -> None:
        absent = SubjectGrade(
            subject_id="b", letter="F", grade_point=D(0), is_absent=True, is_pass=False
        )
        result = gpa([sg("5.0", subject="a"), absent])
        assert not result.is_pass
        assert result.gpa == D("0.00")

    def test_at_least_one_main_subject_is_required(self) -> None:
        with pytest.raises(ResultInputError):
            gpa([sg("5.0", subject="opt", fourth=True)])

    def test_duplicate_subject_ids_are_rejected(self) -> None:
        with pytest.raises(ResultInputError):
            gpa([sg("5.0", subject="a"), sg("4.0", subject="a")])

    def test_more_than_one_fourth_subject_is_rejected(self) -> None:
        with pytest.raises(ResultInputError):
            gpa(
                [
                    sg("5.0", subject="a"),
                    sg("4.0", subject="x", fourth=True),
                    sg("4.0", subject="y", fourth=True),
                ]
            )
