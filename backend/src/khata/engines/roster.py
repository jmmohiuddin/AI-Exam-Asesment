"""Roster import validation (FR-ORG-03, TR-BE-05).

Pure: rows in, a report out. Nothing is written anywhere, so the API can show the
admin exactly what a commit would do before it does it — which is the requirement
("nothing is committed until confirmed"), not a nicety.

Two rules shape everything here:

* **Never guess.** An unrecognised group or version is rejected, not mapped to the
  nearest match. A roster is identity data; a wrong guess attaches a script to the
  wrong student, and the school has no way to notice.
* **Report the whole file.** Validation never stops at the first bad row, because
  a school fixing a 500-row export one error per upload will give up.
"""

from __future__ import annotations

import re
from collections.abc import Iterable, Sequence
from enum import StrEnum

from khata.engines.bangla import to_latin_digits
from khata.engines.base import FrozenModel

MAX_ROLL_LENGTH = 32
MAX_NAME_LENGTH = 200
MAX_SECTION_LENGTH = 32
MAX_SUBJECT_CODE_LENGTH = 32
MAX_STUDENT_UID_LENGTH = 64
MIN_CLASS_LEVEL = 6
MAX_CLASS_LEVEL = 12

#: The four values `section.group_code` accepts. Kept here so the engine can never
#: produce a group the database will reject.
GROUP_CODES = ("science", "humanities", "business", "none")
VERSION_CODES = ("BM", "EV")
SHIFT_CODES = ("morning", "day", "evening")
DEFAULT_SHIFT = "day"

_GROUP_SYNONYMS = {
    "science": "science",
    "sc": "science",
    "বিজ্ঞান": "science",
    "humanities": "humanities",
    "arts": "humanities",
    "arts/humanities": "humanities",
    "মানবিক": "humanities",
    "business": "business",
    "business studies": "business",
    "commerce": "business",
    "ব্যবসায় শিক্ষা": "business",
    "ব্যবসায়": "business",
    "none": "none",
    "general": "none",
    "সাধারণ": "none",
    "": "none",
}

_VERSION_SYNONYMS = {
    "bm": "BM",
    "bn": "BM",
    "bangla": "BM",
    "bengali": "BM",
    "bangla medium": "BM",
    "বাংলা": "BM",
    "বাংলা মাধ্যম": "BM",
    "ev": "EV",
    "en": "EV",
    "english": "EV",
    "english version": "EV",
    "ইংরেজি": "EV",
    "ইংরেজি ভার্সন": "EV",
}

_SHIFT_SYNONYMS = {
    "": DEFAULT_SHIFT,
    "day": "day",
    "দিবা": "day",
    "morning": "morning",
    "প্রভাতি": "morning",
    "evening": "evening",
    "সান্ধ্য": "evening",
}

_WHITESPACE = re.compile(r"\s+")
_BANGLA_BLOCK = re.compile(r"[ঀ-৿]")
_BD_MOBILE = re.compile(r"^(?:\+?88)?(01[3-9]\d{8})$")

#: Characters Bijoy/ANSI text uses for kars, folas and conjuncts once it is read as
#: Latin-1. None of them is a letter in any Latin orthography, so their presence in
#: a field that carries no Bangla codepoint means the file was never converted.
_BIJOY_MARKERS = frozenset("‡†ˆ‰Š„¨ª«©¬­¯®¤¥¦§•”“›š™˜—°±²³µ¶·¸¹º»¼½¾×÷ŒœŽžŸ")
#: Bijoy encodes several vowel signs as bare ASCII letters, so a marker character is
#: not always present. What is always true is that the result does not read as text
#: in any Latin orthography: it is consonant-dense, because the Bangla vowels became
#: these letters rather than a, e, i, o, u.
_BIJOY_ASCII_HINTS = frozenset("wxyz")
_LATIN_VOWELS = frozenset("aeiou")
#: Below this share of vowels, a run of Latin letters is not a name anyone typed.
#: "Rahim Uddin" sits at 0.40; Bijoy's "ivwng DwÏb" at 0.11.
_MIN_VOWEL_RATIO = 0.20
_MIN_HINT_RATIO = 0.25
_MIN_LETTERS_TO_JUDGE = 4


class Severity(StrEnum):
    ERROR = "error"
    WARNING = "warning"


class RawRow(FrozenModel):
    """One spreadsheet row, exactly as the file had it.

    Every field is a string because that is what a spreadsheet gives; turning them
    into the right types is this engine's job, and where it cannot, it says so.
    """

    row_number: int
    roll: str = ""
    student_uid: str = ""
    name_bn: str = ""
    name_en: str = ""
    class_level: str = ""
    group_code: str = ""
    version: str = ""
    shift: str = ""
    section: str = ""
    fourth_subject_code: str = ""
    guardian_mobile: str = ""


class AcceptedRow(FrozenModel):
    """A row that passed every rule, normalised to what the database stores."""

    row_number: int
    student_uid: str
    roll: str
    name_bn: str
    name_en: str
    class_level: int
    group_code: str
    version: str
    shift: str
    section: str
    fourth_subject_code: str | None = None
    guardian_mobile: str | None = None
    #: False when the id was derived from class, section and roll rather than given.
    #: A derived id can only collide where the roll already collides, which is
    #: reported against the roll instead.
    student_uid_supplied: bool = True


class RowProblem(FrozenModel):
    """One reason one row cannot be imported, in both languages."""

    row_number: int
    field: str
    code: str
    message_en: str
    message_bn: str
    severity: Severity = Severity.ERROR
    value: str = ""
    #: For duplicates: the other rows carrying the same value.
    conflicts_with: tuple[int, ...] = ()


class ImportReport(FrozenModel):
    """What a commit would do, and everything standing in its way."""

    row_count: int
    accepted: tuple[AcceptedRow, ...] = ()
    problems: tuple[RowProblem, ...] = ()

    @property
    def accepted_count(self) -> int:
        return len(self.accepted)

    @property
    def error_count(self) -> int:
        return len({p.row_number for p in self.problems if p.severity is Severity.ERROR})

    @property
    def is_committable(self) -> bool:
        """An empty file is not committable either: it is almost always a wrong upload."""
        return bool(self.accepted) and self.error_count == 0


def _clean(value: str) -> str:
    return _WHITESPACE.sub(" ", value).strip()


def _looks_like_legacy_encoding(value: str) -> bool:
    """Does this field carry Bijoy/ANSI bytes rather than Unicode Bangla?

    Anything holding a real Bangla codepoint is already Unicode and is never
    suspected, so a school that types Bangla properly is never bothered.
    """
    if not value or _BANGLA_BLOCK.search(value):
        return False
    if any(ch in _BIJOY_MARKERS for ch in value):
        return True
    letters = [ch for ch in value.lower() if ch.isalpha()]
    if len(letters) < _MIN_LETTERS_TO_JUDGE:
        return False
    vowel_ratio = sum(1 for ch in letters if ch in _LATIN_VOWELS) / len(letters)
    hint_ratio = sum(1 for ch in letters if ch in _BIJOY_ASCII_HINTS) / len(letters)
    return vowel_ratio < _MIN_VOWEL_RATIO or hint_ratio >= _MIN_HINT_RATIO


class _Problems:
    """Collects problems for one row so each check can stay a single expression."""

    def __init__(self, row_number: int) -> None:
        self._row_number = row_number
        self.items: list[RowProblem] = []

    def add(self, field: str, code: str, en: str, bn: str, value: str = "") -> None:
        self.items.append(
            RowProblem(
                row_number=self._row_number,
                field=field,
                code=code,
                message_en=en,
                message_bn=bn,
                value=value,
            )
        )

    @property
    def ok(self) -> bool:
        return not self.items


def _check_roll(raw: str, problems: _Problems) -> str:
    roll = to_latin_digits(_clean(raw))
    if not roll:
        problems.add("roll", "required", "Roll is required.", "রোল নম্বর দিতে হবে।")
    elif len(roll) > MAX_ROLL_LENGTH:
        problems.add(
            "roll",
            "too_long",
            f"Roll must be at most {MAX_ROLL_LENGTH} characters.",
            f"রোল নম্বর সর্বোচ্চ {MAX_ROLL_LENGTH} অক্ষরের হতে পারে।",
            roll,
        )
    return roll


def _check_name(field: str, raw: str, problems: _Problems) -> str:
    name = _clean(raw)
    if len(name) > MAX_NAME_LENGTH:
        problems.add(
            field,
            "too_long",
            f"Name must be at most {MAX_NAME_LENGTH} characters.",
            f"নাম সর্বোচ্চ {MAX_NAME_LENGTH} অক্ষরের হতে পারে।",
            name,
        )
    elif _looks_like_legacy_encoding(name):
        problems.add(
            field,
            "legacy_encoding",
            "This name looks like legacy Bijoy/ANSI text. Convert the file to Unicode first.",
            "নামটি বিজয়/ANSI ফরম্যাটে আছে বলে মনে হচ্ছে। ফাইলটি আগে ইউনিকোডে রূপান্তর করুন।",
            name,
        )
    return name


def _check_class_level(raw: str, problems: _Problems) -> int:
    text = to_latin_digits(_clean(raw))
    if not text:
        problems.add("class_level", "required", "Class is required.", "শ্রেণি দিতে হবে।")
        return 0
    try:
        level = int(text)
    except ValueError:
        problems.add(
            "class_level",
            "not_a_number",
            "Class must be a number.",
            "শ্রেণি একটি সংখ্যা হতে হবে।",
            text,
        )
        return 0
    if not MIN_CLASS_LEVEL <= level <= MAX_CLASS_LEVEL:
        problems.add(
            "class_level",
            "out_of_range",
            f"Class must be between {MIN_CLASS_LEVEL} and {MAX_CLASS_LEVEL}.",
            f"শ্রেণি {MIN_CLASS_LEVEL} থেকে {MAX_CLASS_LEVEL} এর মধ্যে হতে হবে।",
            text,
        )
        return 0
    return level


def _check_choice(
    field: str,
    raw: str,
    synonyms: dict[str, str],
    problems: _Problems,
    *,
    en: str,
    bn: str,
) -> str:
    key = _clean(raw).casefold()
    resolved = synonyms.get(key)
    if resolved is None:
        problems.add(field, "unknown_value", en, bn, _clean(raw))
        return ""
    return resolved


def _check_section(raw: str, problems: _Problems) -> str:
    section = _clean(raw)
    if not section:
        problems.add("section", "required", "Section is required.", "শাখা দিতে হবে।")
    elif len(section) > MAX_SECTION_LENGTH:
        problems.add(
            "section",
            "too_long",
            f"Section must be at most {MAX_SECTION_LENGTH} characters.",
            f"শাখার নাম সর্বোচ্চ {MAX_SECTION_LENGTH} অক্ষরের হতে পারে।",
            section,
        )
    return section


def _check_guardian_mobile(raw: str, problems: _Problems) -> str | None:
    text = to_latin_digits(_clean(raw)).replace(" ", "").replace("-", "")
    if not text:
        return None
    match = _BD_MOBILE.match(text)
    if match is None:
        problems.add(
            "guardian_mobile",
            "invalid_mobile",
            "Guardian mobile must be a Bangladeshi number, e.g. 01712345678.",
            "অভিভাবকের মোবাইল নম্বরটি বাংলাদেশি হতে হবে, যেমন ০১৭১২৩৪৫৬৭৮।",
            text,
        )
        return None
    return f"+88{match.group(1)}"


def _check_optional_code(field: str, raw: str, problems: _Problems) -> str | None:
    code = _clean(raw)
    if not code:
        return None
    if len(code) > MAX_SUBJECT_CODE_LENGTH:
        problems.add(
            field,
            "too_long",
            f"Code must be at most {MAX_SUBJECT_CODE_LENGTH} characters.",
            f"কোড সর্বোচ্চ {MAX_SUBJECT_CODE_LENGTH} অক্ষরের হতে পারে।",
            code,
        )
        return None
    return code


def _generated_student_uid(class_level: int, section: str, roll: str) -> str:
    """The identity to use when the school supplies none.

    Built from the enrolment coordinates rather than the roll alone, because rolls
    restart in every section: two "101"s in 9-A and 9-B are two students. It is also
    stable, so re-importing the same file updates those students instead of
    duplicating them.
    """
    return f"{class_level}-{section}-{roll}"


def _check_student_uid(raw: str, roll: str, problems: _Problems) -> str:
    uid = _clean(raw) or roll
    if len(uid) > MAX_STUDENT_UID_LENGTH:
        problems.add(
            "student_uid",
            "too_long",
            f"Student id must be at most {MAX_STUDENT_UID_LENGTH} characters.",
            f"শিক্ষার্থী আইডি সর্বোচ্চ {MAX_STUDENT_UID_LENGTH} অক্ষরের হতে পারে।",
            uid,
        )
    return uid


def _validate_row(raw: RawRow) -> tuple[AcceptedRow | None, list[RowProblem]]:
    problems = _Problems(raw.row_number)

    roll = _check_roll(raw.roll, problems)
    name_bn = _check_name("name_bn", raw.name_bn, problems)
    name_en = _check_name("name_en", raw.name_en, problems)
    if not name_bn and not name_en:
        problems.add(
            "name",
            "required",
            "A name in Bangla or English is required.",
            "বাংলা বা ইংরেজি — অন্তত একটি নাম দিতে হবে।",
        )
    class_level = _check_class_level(raw.class_level, problems)
    group_code = _check_choice(
        "group_code",
        raw.group_code,
        _GROUP_SYNONYMS,
        problems,
        en=f"Group must be one of: {', '.join(GROUP_CODES)}.",
        bn="বিভাগ হতে হবে: বিজ্ঞান, মানবিক, ব্যবসায় শিক্ষা বা সাধারণ।",
    )
    version = _check_choice(
        "version",
        raw.version,
        _VERSION_SYNONYMS,
        problems,
        en="Version must be Bangla (BM) or English (EV).",
        bn="ভার্সন হতে হবে বাংলা (BM) বা ইংরেজি (EV)।",
    )
    shift = _check_choice(
        "shift",
        raw.shift,
        _SHIFT_SYNONYMS,
        problems,
        en=f"Shift must be one of: {', '.join(SHIFT_CODES)}.",
        bn="শিফট হতে হবে: প্রভাতি, দিবা বা সান্ধ্য।",
    )
    section = _check_section(raw.section, problems)
    guardian_mobile = _check_guardian_mobile(raw.guardian_mobile, problems)
    fourth_subject = _check_optional_code("fourth_subject_code", raw.fourth_subject_code, problems)
    supplied_uid = _clean(raw.student_uid)
    student_uid = _check_student_uid(
        raw.student_uid,
        _generated_student_uid(class_level, section, roll),
        problems,
    )

    if not problems.ok:
        return None, problems.items
    return (
        AcceptedRow(
            row_number=raw.row_number,
            student_uid=student_uid,
            roll=roll,
            name_bn=name_bn,
            name_en=name_en,
            class_level=class_level,
            group_code=group_code,
            version=version,
            shift=shift,
            section=section,
            fourth_subject_code=fourth_subject,
            guardian_mobile=guardian_mobile,
            student_uid_supplied=bool(supplied_uid),
        ),
        [],
    )


def _duplicate_problems(
    rows: Sequence[AcceptedRow],
    *,
    key: object,
    field: str,
    code: str,
    en: str,
    bn: str,
) -> list[RowProblem]:
    """Flag every row sharing a key, not just the later ones.

    Which of two rows with the same roll is the real one is not something the file
    says, so neither is imported and both are reported.
    """
    grouped: dict[object, list[AcceptedRow]] = {}
    for row in rows:
        grouped.setdefault(key(row), []).append(row)  # type: ignore[operator]

    problems: list[RowProblem] = []
    for members in grouped.values():
        if len(members) < 2:
            continue
        numbers = tuple(member.row_number for member in members)
        for member in members:
            problems.append(
                RowProblem(
                    row_number=member.row_number,
                    field=field,
                    code=code,
                    message_en=en,
                    message_bn=bn,
                    conflicts_with=tuple(n for n in numbers if n != member.row_number),
                )
            )
    return problems


def validate_roster(rows: Iterable[RawRow]) -> ImportReport:
    """Validate a whole roster file and report what a commit would do.

    Rows are checked on their own first, then against each other: a row that is
    already invalid cannot meaningfully collide with anything.
    """
    raw_rows = list(rows)
    accepted: list[AcceptedRow] = []
    problems: list[RowProblem] = []

    for raw in raw_rows:
        row, row_problems = _validate_row(raw)
        if row is None:
            problems.extend(row_problems)
        else:
            accepted.append(row)

    collisions = _duplicate_problems(
        accepted,
        key=lambda row: (row.class_level, row.section, row.shift, row.version, row.roll),
        field="roll",
        code="duplicate_roll",
        en="This roll is used by another row in the same section.",
        bn="একই শাখায় অন্য একটি সারিতেও এই রোল নম্বর ব্যবহার করা হয়েছে।",
    ) + _duplicate_problems(
        [row for row in accepted if row.student_uid_supplied],
        key=lambda row: row.student_uid,
        field="student_uid",
        code="duplicate_student_uid",
        en="This student id is used by another row.",
        bn="অন্য একটি সারিতেও এই শিক্ষার্থী আইডি ব্যবহার করা হয়েছে।",
    )

    if collisions:
        colliding = {problem.row_number for problem in collisions}
        accepted = [row for row in accepted if row.row_number not in colliding]
        problems.extend(collisions)

    return ImportReport(
        row_count=len(raw_rows),
        accepted=tuple(sorted(accepted, key=lambda row: row.row_number)),
        problems=tuple(sorted(problems, key=lambda problem: (problem.row_number, problem.field))),
    )
