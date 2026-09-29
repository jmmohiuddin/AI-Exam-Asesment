"""Roster import validation (FR-ORG-03, TR-BE-05).

The engine's job is to be the thing that stands between a spreadsheet a school
typed by hand and the database. Every rule here exists because getting it wrong
silently is worse than rejecting the file: a mis-parsed roll number attaches a
student's script to another student.
"""

from __future__ import annotations

import pytest

from khata.engines.roster import (
    GROUP_CODES,
    RawRow,
    Severity,
    validate_roster,
)

pytestmark = pytest.mark.unit


def row(**overrides: object) -> RawRow:
    """A row that passes every rule, so each test changes exactly one thing."""
    base: dict[str, object] = {
        "row_number": 1,
        "roll": "101",
        "name_bn": "রহিম উদ্দিন",
        "name_en": "Rahim Uddin",
        "class_level": "9",
        "group_code": "science",
        "version": "BM",
        "shift": "day",
        "section": "A",
    }
    return RawRow(**{**base, **overrides})


def codes(report: object, *, field: str | None = None) -> set[str]:
    problems = report.problems  # type: ignore[attr-defined]
    return {p.code for p in problems if field is None or p.field == field}


# --------------------------------------------------------------------------- happy path


def test_a_complete_row_is_accepted() -> None:
    report = validate_roster([row()])

    assert report.problems == ()
    assert report.is_committable
    assert len(report.accepted) == 1
    accepted = report.accepted[0]
    assert accepted.roll == "101"
    assert accepted.class_level == 9
    assert accepted.group_code == "science"
    assert accepted.version == "BM"
    assert accepted.section == "A"


def test_student_uid_defaults_to_the_enrolment_coordinates() -> None:
    """Rolls restart per section, so the roll alone cannot identify a student.

    9-A-101 and 9-B-101 are two people; a bare "101" would merge them.
    """
    report = validate_roster([row(student_uid="")])

    assert report.accepted[0].student_uid == "9-A-101"


def test_a_generated_student_uid_is_stable_across_re_imports() -> None:
    """Re-uploading the same file must update those students, not duplicate them."""
    first = validate_roster([row(student_uid="")])
    again = validate_roster([row(student_uid="")])

    assert first.accepted[0].student_uid == again.accepted[0].student_uid


def test_an_explicit_student_uid_is_kept() -> None:
    report = validate_roster([row(student_uid="S-2026-0042")])

    assert report.accepted[0].student_uid == "S-2026-0042"


def test_counts_describe_the_whole_file() -> None:
    report = validate_roster([row(), row(row_number=2, roll="102", section="A")])

    assert report.row_count == 2
    assert report.accepted_count == 2
    assert report.error_count == 0


# --------------------------------------------------------------------------- normalisation


def test_bangla_digits_in_the_roll_become_latin() -> None:
    """A roll typed in Bangla numerals is the same roll (TR-BN-02)."""
    report = validate_roster([row(roll="১০১")])

    assert report.accepted[0].roll == "101"


def test_bangla_digits_in_the_class_are_read_as_the_class() -> None:
    report = validate_roster([row(class_level="৯")])

    assert report.accepted[0].class_level == 9


def test_surrounding_and_repeated_whitespace_is_collapsed() -> None:
    report = validate_roster([row(name_en="  Rahim   Uddin  ")])

    assert report.accepted[0].name_en == "Rahim Uddin"


@pytest.mark.parametrize(
    ("written", "expected"),
    [
        ("science", "science"),
        ("Science", "science"),
        ("বিজ্ঞান", "science"),
        ("humanities", "humanities"),
        ("arts", "humanities"),
        ("মানবিক", "humanities"),
        ("business", "business"),
        ("commerce", "business"),
        ("ব্যবসায় শিক্ষা", "business"),
        ("", "none"),
        ("general", "none"),
    ],
)
def test_groups_are_recognised_in_either_language(written: str, expected: str) -> None:
    report = validate_roster([row(group_code=written)])

    assert report.problems == ()
    assert report.accepted[0].group_code == expected


@pytest.mark.parametrize(
    ("written", "expected"),
    [
        ("BM", "BM"),
        ("bm", "BM"),
        ("bangla", "BM"),
        ("বাংলা", "BM"),
        ("EV", "EV"),
        ("english", "EV"),
        ("english version", "EV"),
        ("ইংরেজি", "EV"),
    ],
)
def test_versions_are_recognised_in_either_language(written: str, expected: str) -> None:
    report = validate_roster([row(version=written)])

    assert report.problems == ()
    assert report.accepted[0].version == expected


def test_an_empty_shift_defaults_to_day() -> None:
    report = validate_roster([row(shift="")])

    assert report.accepted[0].shift == "day"


def test_every_group_code_the_section_table_allows_is_reachable() -> None:
    """The engine must not emit a group the `section` CHECK constraint rejects."""
    produced = {
        validate_roster([row(group_code=code)]).accepted[0].group_code for code in GROUP_CODES
    }

    assert produced == set(GROUP_CODES)


# --------------------------------------------------------------------------- required fields


@pytest.mark.parametrize("field", ["roll", "class_level", "section"])
def test_a_missing_required_field_rejects_the_row(field: str) -> None:
    report = validate_roster([row(**{field: ""})])

    assert report.accepted == ()
    assert not report.is_committable
    assert codes(report, field=field) == {"required"}


def test_a_row_with_neither_name_is_rejected() -> None:
    report = validate_roster([row(name_bn="", name_en="")])

    assert report.accepted == ()
    assert codes(report, field="name") == {"required"}


def test_one_name_is_enough() -> None:
    """Many rosters carry only the Bangla name; that is a complete row."""
    report = validate_roster([row(name_en="")])

    assert report.problems == ()
    assert report.accepted[0].name_en == ""


# --------------------------------------------------------------------------- bounds


@pytest.mark.parametrize("value", ["5", "13", "0", "-1"])
def test_a_class_outside_6_to_12_is_rejected(value: str) -> None:
    report = validate_roster([row(class_level=value)])

    assert codes(report, field="class_level") == {"out_of_range"}


def test_a_class_that_is_not_a_number_is_rejected() -> None:
    report = validate_roster([row(class_level="nine")])

    assert codes(report, field="class_level") == {"not_a_number"}


def test_an_over_long_roll_is_rejected() -> None:
    report = validate_roster([row(roll="1" * 33)])

    assert codes(report, field="roll") == {"too_long"}


def test_an_over_long_name_is_rejected() -> None:
    report = validate_roster([row(name_en="x" * 201)])

    assert codes(report, field="name_en") == {"too_long"}


def test_an_unknown_group_is_rejected_rather_than_guessed() -> None:
    report = validate_roster([row(group_code="astrology")])

    assert codes(report, field="group_code") == {"unknown_value"}


def test_an_unknown_version_is_rejected_rather_than_guessed() -> None:
    report = validate_roster([row(version="french")])

    assert codes(report, field="version") == {"unknown_value"}


def test_a_malformed_guardian_mobile_is_rejected() -> None:
    report = validate_roster([row(guardian_mobile="12345")])

    assert codes(report, field="guardian_mobile") == {"invalid_mobile"}


def test_a_valid_guardian_mobile_is_normalised_to_e164() -> None:
    report = validate_roster([row(guardian_mobile="01712345678")])

    assert report.problems == ()
    assert report.accepted[0].guardian_mobile == "+8801712345678"


# --------------------------------------------------------------------------- duplicates


def test_the_same_roll_twice_in_one_section_rejects_both_rows() -> None:
    """Neither row can be trusted: the file itself does not say which is which."""
    report = validate_roster([row(), row(row_number=2)])

    assert report.accepted == ()
    assert codes(report, field="roll") == {"duplicate_roll"}
    assert {p.row_number for p in report.problems} == {1, 2}


def test_the_same_roll_in_a_different_section_is_fine() -> None:
    report = validate_roster([row(), row(row_number=2, section="B")])

    assert report.problems == ()
    assert len(report.accepted) == 2


def test_the_same_roll_in_a_different_class_is_fine() -> None:
    report = validate_roster([row(), row(row_number=2, class_level="10")])

    assert report.problems == ()
    assert len(report.accepted) == 2


def test_a_repeated_student_uid_rejects_both_rows() -> None:
    report = validate_roster(
        [
            row(student_uid="S-1"),
            row(row_number=2, roll="102", student_uid="S-1"),
        ]
    )

    assert report.accepted == ()
    assert codes(report, field="student_uid") == {"duplicate_student_uid"}


def test_a_duplicate_reports_the_row_it_collides_with() -> None:
    report = validate_roster([row(), row(row_number=2)])

    assert all(p.conflicts_with for p in report.problems)
    by_row = {p.row_number: p.conflicts_with for p in report.problems}
    assert by_row[2] == (1,)


# --------------------------------------------------------------------------- legacy encoding


def test_legacy_bijoy_text_is_flagged_and_not_imported() -> None:
    """Importing mojibake would put an unreadable name on a report card."""
    report = validate_roster([row(name_bn="ivwng DwÏb")])

    assert report.accepted == ()
    assert codes(report, field="name_bn") == {"legacy_encoding"}


def test_unicode_bangla_is_not_mistaken_for_legacy_text() -> None:
    report = validate_roster([row(name_bn="রহিম উদ্দিন")])

    assert report.problems == ()


def test_plain_english_is_not_mistaken_for_legacy_text() -> None:
    report = validate_roster([row(name_bn="", name_en="Rahim Uddin")])

    assert report.problems == ()


# --------------------------------------------------------------------------- report shape


def test_a_rejected_row_does_not_stop_the_rest_of_the_file() -> None:
    """The admin should see every problem at once, not one per upload."""
    report = validate_roster(
        [
            row(),
            row(row_number=2, roll="", section="B"),
            row(row_number=3, roll="103", section="B"),
        ]
    )

    assert [a.row_number for a in report.accepted] == [1, 3]
    assert report.accepted_count == 2
    assert report.error_count == 1


def test_problems_are_ordered_by_row() -> None:
    report = validate_roster(
        [
            row(row_number=3, roll="", section="C"),
            row(row_number=1, roll="", section="A"),
            row(row_number=2, roll="", section="B"),
        ]
    )

    assert [p.row_number for p in report.problems] == [1, 2, 3]


def test_every_problem_is_readable_in_both_languages() -> None:
    report = validate_roster([row(roll="", class_level="99", group_code="astrology")])

    assert report.problems
    for problem in report.problems:
        assert problem.message_en.strip()
        assert problem.message_bn.strip()
        assert problem.severity is Severity.ERROR


def test_an_empty_file_is_reported_rather_than_committed() -> None:
    report = validate_roster([])

    assert report.row_count == 0
    assert not report.is_committable
