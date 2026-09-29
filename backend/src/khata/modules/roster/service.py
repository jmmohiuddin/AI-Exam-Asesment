"""Roster rules: staged imports, enrolment and consent (FR-ORG-02, -03, -06).

The import is deliberately two steps. Validation runs the pure engine and stores
what it accepted; the commit replays exactly those rows. Re-parsing at commit time
would let the file change between what the admin approved and what was written,
which is the failure the requirement's "nothing is committed until confirmed" is
guarding against.
"""

from __future__ import annotations

import uuid
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from khata.core.errors import DomainError
from khata.core.models import utcnow
from khata.engines.roster import AcceptedRow, ImportReport, RawRow, validate_roster
from khata.modules.org.models import AcademicYear, School, Section
from khata.modules.roster.models import Enrolment, RosterImport, Student, StudentConsent

#: 08 §6.1. Absence of a record is a "no": nothing is assumed to be consented.
CONSENT_TYPES = ("CT-1", "CT-2", "CT-3")
#: The consent that has to be present before any AI call is made for a student.
AI_CONSENT = "CT-2"
#: The consent that has to be present before a script may be captured at all.
CAPTURE_CONSENT = "CT-1"

IMPORT_VALIDATED = "validated"
IMPORT_COMMITTED = "committed"
IMPORT_DISCARDED = "discarded"


@dataclass(frozen=True, slots=True)
class CommitOutcome:
    """What a commit actually changed, for the confirmation screen and the audit."""

    students_created: int
    students_updated: int
    sections_created: int
    enrolments_created: int
    enrolments_updated: int


# --------------------------------------------------------------------------- lookups


def get_school(session: Session, school_id: uuid.UUID) -> School:
    school = session.get(School, school_id)
    if school is None:
        raise DomainError("NOT_FOUND", detail="School not found.")
    return school


def get_academic_year(session: Session, academic_year_id: uuid.UUID) -> AcademicYear:
    year = session.get(AcademicYear, academic_year_id)
    if year is None:
        raise DomainError("NOT_FOUND", detail="Academic year not found.")
    return year


def get_student(session: Session, student_id: uuid.UUID) -> Student:
    student = session.get(Student, student_id)
    if student is None:
        raise DomainError("NOT_FOUND", detail="Student not found.")
    return student


def get_import(session: Session, import_id: uuid.UUID) -> RosterImport:
    staged = session.get(RosterImport, import_id)
    if staged is None:
        raise DomainError("NOT_FOUND", detail="Roster import not found.")
    return staged


def list_students(
    session: Session,
    *,
    school_id: uuid.UUID,
    section_id: uuid.UUID | None = None,
    limit: int = 500,
) -> list[tuple[Student, Enrolment | None]]:
    """Students of one school, with the enrolment that matches the filter."""
    query = (
        select(Student, Enrolment)
        .join(Enrolment, Enrolment.student_id == Student.id, isouter=section_id is None)
        .where(Student.school_id == school_id)
    )
    if section_id is not None:
        query = query.where(Enrolment.section_id == section_id)
    query = query.order_by(Student.student_uid).limit(limit)
    return [(student, enrolment) for student, enrolment in session.execute(query)]


# --------------------------------------------------------------------------- import


def validate_import(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    school: School,
    academic_year: AcademicYear,
    filename: str,
    rows: Sequence[RawRow],
    created_by: uuid.UUID | None,
) -> RosterImport:
    """Run the file through the engine and stage the result. Writes no students."""
    if academic_year.school_id != school.id:
        raise DomainError("BAD_REQUEST", detail="That academic year belongs to another school.")

    report = validate_roster(rows)
    staged = RosterImport(
        tenant_id=tenant_id,
        school_id=school.id,
        academic_year_id=academic_year.id,
        filename=filename,
        state=IMPORT_VALIDATED,
        row_count=report.row_count,
        accepted_count=report.accepted_count,
        error_count=report.error_count,
        report=_report_payload(report),
        rows=[row.model_dump(mode="json") for row in report.accepted],
        created_by=created_by,
    )
    session.add(staged)
    session.flush()
    return staged


def _report_payload(report: ImportReport) -> dict[str, Any]:
    return {
        "row_count": report.row_count,
        "accepted_count": report.accepted_count,
        "error_count": report.error_count,
        "is_committable": report.is_committable,
        "problems": [problem.model_dump(mode="json") for problem in report.problems],
    }


def commit_import(
    session: Session,
    *,
    staged: RosterImport,
    actor_id: uuid.UUID | None,
) -> CommitOutcome:
    """Apply a validated import. Idempotent per student: a re-import updates."""
    if staged.state == IMPORT_COMMITTED:
        raise DomainError(
            "ROSTER_IMPORT_ALREADY_COMMITTED",
            detail="This import was already committed.",
        )
    if staged.state == IMPORT_DISCARDED:
        raise DomainError("CONFLICT", detail="This import was discarded.")
    if staged.error_count or not staged.rows:
        raise DomainError(
            "ROSTER_IMPORT_NOT_COMMITTABLE",
            detail="Fix the reported rows and upload the file again.",
        )

    rows = [AcceptedRow.model_validate(row) for row in staged.rows]
    outcome = _apply_rows(
        session,
        tenant_id=staged.tenant_id,
        school_id=staged.school_id,
        academic_year_id=staged.academic_year_id,
        rows=rows,
        actor_id=actor_id,
    )

    staged.state = IMPORT_COMMITTED
    staged.committed_at = utcnow()
    staged.students_created = outcome.students_created
    staged.students_updated = outcome.students_updated
    staged.sections_created = outcome.sections_created
    session.flush()
    return outcome


def _apply_rows(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    school_id: uuid.UUID,
    academic_year_id: uuid.UUID,
    rows: Sequence[AcceptedRow],
    actor_id: uuid.UUID | None,
) -> CommitOutcome:
    sections_created = 0
    students_created = 0
    students_updated = 0
    enrolments_created = 0
    enrolments_updated = 0

    for row in rows:
        section, created = _section_for(
            session,
            tenant_id=tenant_id,
            school_id=school_id,
            academic_year_id=academic_year_id,
            row=row,
        )
        sections_created += int(created)

        student, created = _student_for(
            session,
            tenant_id=tenant_id,
            school_id=school_id,
            row=row,
            actor_id=actor_id,
        )
        students_created += int(created)
        students_updated += int(not created)

        created = _enrol(
            session,
            tenant_id=tenant_id,
            student=student,
            academic_year_id=academic_year_id,
            section=section,
            row=row,
        )
        enrolments_created += int(created)
        enrolments_updated += int(not created)

    session.flush()
    return CommitOutcome(
        students_created=students_created,
        students_updated=students_updated,
        sections_created=sections_created,
        enrolments_created=enrolments_created,
        enrolments_updated=enrolments_updated,
    )


def _section_for(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    school_id: uuid.UUID,
    academic_year_id: uuid.UUID,
    row: AcceptedRow,
) -> tuple[Section, bool]:
    """Find the section the row names, creating it when the school has not yet.

    Sections are created rather than demanded up front because the roster file is
    where a school first says which sections exist.
    """
    existing = session.scalars(
        select(Section).where(
            Section.academic_year_id == academic_year_id,
            Section.class_level == row.class_level,
            Section.group_code == row.group_code,
            Section.version == row.version,
            Section.shift == row.shift,
            Section.name == row.section,
        )
    ).first()
    if existing is not None:
        return existing, False

    section = Section(
        tenant_id=tenant_id,
        school_id=school_id,
        academic_year_id=academic_year_id,
        class_level=row.class_level,
        group_code=row.group_code,
        version=row.version,
        shift=row.shift,
        name=row.section,
    )
    session.add(section)
    session.flush()
    return section, True


def _student_for(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    school_id: uuid.UUID,
    row: AcceptedRow,
    actor_id: uuid.UUID | None,
) -> tuple[Student, bool]:
    existing = session.scalars(
        select(Student).where(
            Student.school_id == school_id,
            Student.student_uid == row.student_uid,
        )
    ).first()
    if existing is not None:
        existing.name_bn = row.name_bn
        existing.name_en = row.name_en
        existing.guardian_mobile = row.guardian_mobile
        existing.updated_at = utcnow()
        return existing, False

    student = Student(
        tenant_id=tenant_id,
        school_id=school_id,
        student_uid=row.student_uid,
        name_bn=row.name_bn,
        name_en=row.name_en,
        guardian_mobile=row.guardian_mobile,
        created_by=actor_id,
    )
    session.add(student)
    session.flush()
    return student, True


def _enrol(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    student: Student,
    academic_year_id: uuid.UUID,
    section: Section,
    row: AcceptedRow,
) -> bool:
    """One enrolment per student per year (FR-ORG-02); moving section updates it."""
    existing = session.scalars(
        select(Enrolment).where(
            Enrolment.student_id == student.id,
            Enrolment.academic_year_id == academic_year_id,
        )
    ).first()
    if existing is not None:
        existing.section_id = section.id
        existing.roll = row.roll
        existing.fourth_subject_code = row.fourth_subject_code
        existing.updated_at = utcnow()
        return False

    session.add(
        Enrolment(
            tenant_id=tenant_id,
            student_id=student.id,
            academic_year_id=academic_year_id,
            section_id=section.id,
            roll=row.roll,
            fourth_subject_code=row.fourth_subject_code,
        )
    )
    session.flush()
    return True


# --------------------------------------------------------------------------- consent


def record_consent(
    session: Session,
    *,
    tenant_id: uuid.UUID,
    student: Student,
    consent_type: str,
    granted: bool,
    method: str,
    evidence_ref: str | None,
    note: str | None,
    actor_id: uuid.UUID | None,
) -> StudentConsent:
    """Record a guardian's decision, superseding any previous one.

    Withdrawal is the same operation with ``granted=False``: the old row stays,
    stamped, so the record of what was permitted at marking time survives.
    """
    if consent_type not in CONSENT_TYPES:
        raise DomainError("BAD_REQUEST", detail=f"Unknown consent type {consent_type}.")

    now = utcnow()
    current = _current_consent(session, student.id, consent_type)
    if current is not None:
        current.superseded_at = now
        session.flush()

    consent = StudentConsent(
        tenant_id=tenant_id,
        student_id=student.id,
        consent_type=consent_type,
        granted=granted,
        method=method,
        evidence_ref=evidence_ref,
        note=note,
        recorded_by=actor_id,
        recorded_at=now,
    )
    session.add(consent)
    session.flush()
    return consent


def _current_consent(
    session: Session, student_id: uuid.UUID, consent_type: str
) -> StudentConsent | None:
    return session.scalars(
        select(StudentConsent).where(
            StudentConsent.student_id == student_id,
            StudentConsent.consent_type == consent_type,
            StudentConsent.superseded_at.is_(None),
        )
    ).first()


def current_consents(session: Session, student_id: uuid.UUID) -> dict[str, StudentConsent]:
    """The live decision per consent type. A type with no row is simply absent."""
    rows = session.scalars(
        select(StudentConsent).where(
            StudentConsent.student_id == student_id,
            StudentConsent.superseded_at.is_(None),
        )
    )
    return {row.consent_type: row for row in rows}


def has_consent(session: Session, student_id: uuid.UUID, consent_type: str) -> bool:
    """Absence is a refusal, not a default yes (08 §6.1)."""
    current = _current_consent(session, student_id, consent_type)
    return current is not None and current.granted


def consent_history(session: Session, student_id: uuid.UUID) -> list[StudentConsent]:
    return list(
        session.scalars(
            select(StudentConsent)
            .where(StudentConsent.student_id == student_id)
            .order_by(StudentConsent.recorded_at.desc())
        )
    )
