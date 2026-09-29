"""Roster endpoints: import, students and guardian consent (SD §12.1)."""

from __future__ import annotations

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from khata.core.roles import Role
from khata.modules.authz.deps import Principal, RequireRoles, TenantSession
from khata.modules.roster import service
from khata.modules.roster.models import RosterImport, StudentConsent
from khata.modules.roster.schemas import (
    AcademicYearOut,
    ConsentOut,
    ConsentPut,
    ConsentStateOut,
    EnrolmentOut,
    RosterImportCommitOut,
    RosterImportCreate,
    RosterImportOut,
    StudentOut,
    StudentRow,
)

router = APIRouter(tags=["roster"])

#: The roster is identity data, so only school administration may change it.
#: Teachers read students through their own review queues, not through this module.
CAN_MANAGE_ROSTER = RequireRoles(Role.SCHOOL_ADMIN, Role.ORG_OWNER, Role.EXAM_COORDINATOR)

RosterAdminDep = Annotated[Principal, Depends(CAN_MANAGE_ROSTER)]

STUDENT_PAGE_SIZE = 500


def _import_out(staged: RosterImport) -> RosterImportOut:
    return RosterImportOut.model_validate(staged, from_attributes=True)


# --------------------------------------------------------------------------- structure


@router.get("/schools/{school_id}/academic-years", response_model=list[AcademicYearOut])
def list_academic_years(
    school_id: uuid.UUID, principal: RosterAdminDep, session: TenantSession
) -> list[AcademicYearOut]:
    """The school's years, newest first. An import has to be filed against one."""
    service.get_school(session, school_id)
    return [
        AcademicYearOut.model_validate(year, from_attributes=True)
        for year in service.list_academic_years(session, school_id)
    ]


# --------------------------------------------------------------------------- import


@router.post(
    "/schools/{school_id}/roster-imports",
    response_model=RosterImportOut,
    status_code=status.HTTP_201_CREATED,
)
def create_roster_import(
    school_id: uuid.UUID,
    payload: RosterImportCreate,
    principal: RosterAdminDep,
    session: TenantSession,
) -> RosterImportOut:
    """Validate a roster file and report what committing it would do.

    Always 201, even for a file that is entirely wrong: the report *is* the result.
    Nothing is written to the roster here (FR-ORG-03).
    """
    school = service.get_school(session, school_id)
    academic_year = service.get_academic_year(session, payload.academic_year_id)
    staged = service.validate_import(
        session,
        tenant_id=principal.require_tenant(),
        school=school,
        academic_year=academic_year,
        filename=payload.filename,
        rows=payload.rows,
        created_by=principal.user_id,
    )
    return _import_out(staged)


@router.get("/roster-imports/{import_id}", response_model=RosterImportOut)
def read_roster_import(
    import_id: uuid.UUID, principal: RosterAdminDep, session: TenantSession
) -> RosterImportOut:
    return _import_out(service.get_import(session, import_id))


@router.post("/roster-imports/{import_id}/commit", response_model=RosterImportCommitOut)
def commit_roster_import(
    import_id: uuid.UUID, principal: RosterAdminDep, session: TenantSession
) -> RosterImportCommitOut:
    """Apply a validated import. Rejected while any row still has an error."""
    staged = service.get_import(session, import_id)
    outcome = service.commit_import(session, staged=staged, actor_id=principal.user_id)
    return RosterImportCommitOut(
        import_id=staged.id,
        students_created=outcome.students_created,
        students_updated=outcome.students_updated,
        sections_created=outcome.sections_created,
        enrolments_created=outcome.enrolments_created,
        enrolments_updated=outcome.enrolments_updated,
    )


# --------------------------------------------------------------------------- students


@router.get("/schools/{school_id}/students", response_model=list[StudentRow])
def list_students(
    school_id: uuid.UUID,
    principal: RosterAdminDep,
    session: TenantSession,
    section_id: Annotated[uuid.UUID | None, Query()] = None,
) -> list[StudentRow]:
    service.get_school(session, school_id)
    rows = service.list_students(
        session, school_id=school_id, section_id=section_id, limit=STUDENT_PAGE_SIZE
    )
    return [
        StudentRow(
            student=StudentOut.model_validate(student, from_attributes=True),
            enrolment=(
                EnrolmentOut.model_validate(enrolment, from_attributes=True)
                if enrolment is not None
                else None
            ),
        )
        for student, enrolment in rows
    ]


@router.get("/students/{student_id}", response_model=StudentOut)
def read_student(
    student_id: uuid.UUID, principal: RosterAdminDep, session: TenantSession
) -> StudentOut:
    student = service.get_student(session, student_id)
    return StudentOut.model_validate(student, from_attributes=True)


# --------------------------------------------------------------------------- consent


def _consent_state(session: TenantSession, student_id: uuid.UUID) -> ConsentStateOut:
    current = service.current_consents(session, student_id)
    return ConsentStateOut(
        student_id=student_id,
        current=[
            ConsentOut.model_validate(consent, from_attributes=True)
            for consent in sorted(current.values(), key=lambda c: c.consent_type)
        ],
        capture_allowed=service.has_consent(session, student_id, service.CAPTURE_CONSENT),
        ai_allowed=service.has_consent(session, student_id, service.AI_CONSENT),
    )


@router.put("/students/{student_id}/consents", response_model=ConsentStateOut)
def put_consent(
    student_id: uuid.UUID,
    payload: ConsentPut,
    principal: RosterAdminDep,
    session: TenantSession,
) -> ConsentStateOut:
    """Record a guardian decision. Withdrawing is the same call with ``granted`` false."""
    student = service.get_student(session, student_id)
    service.record_consent(
        session,
        tenant_id=principal.require_tenant(),
        student=student,
        consent_type=payload.consent_type,
        granted=payload.granted,
        method=payload.method,
        evidence_ref=payload.evidence_ref,
        note=payload.note,
        actor_id=principal.user_id,
    )
    return _consent_state(session, student.id)


@router.get("/students/{student_id}/consents", response_model=ConsentStateOut)
def read_consents(
    student_id: uuid.UUID, principal: RosterAdminDep, session: TenantSession
) -> ConsentStateOut:
    student = service.get_student(session, student_id)
    return _consent_state(session, student.id)


@router.get("/students/{student_id}/consents/history", response_model=list[ConsentOut])
def read_consent_history(
    student_id: uuid.UUID, principal: RosterAdminDep, session: TenantSession
) -> list[ConsentOut]:
    """Every decision ever recorded, newest first — what a privacy request asks for."""
    student = service.get_student(session, student_id)
    history: list[StudentConsent] = service.consent_history(session, student.id)
    return [ConsentOut.model_validate(consent, from_attributes=True) for consent in history]
