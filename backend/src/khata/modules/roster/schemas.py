"""Request and response shapes for the roster endpoints."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from khata.engines.roster import RawRow
from khata.modules.roster.service import CONSENT_TYPES

MAX_IMPORT_ROWS = 5000


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


# --------------------------------------------------------------------------- import


class RosterImportCreate(StrictModel):
    """A parsed spreadsheet. The client does the file parsing; the server validates.

    Rows are sent already split into fields so that XLSX parsing — the part most
    likely to need a library update — stays out of the request path.
    """

    academic_year_id: uuid.UUID
    filename: str = Field(min_length=1, max_length=255)
    rows: list[RawRow] = Field(max_length=MAX_IMPORT_ROWS)


class RosterImportOut(BaseModel):
    id: uuid.UUID
    school_id: uuid.UUID
    academic_year_id: uuid.UUID
    filename: str
    state: str
    row_count: int
    accepted_count: int
    error_count: int
    report: dict[str, Any]
    students_created: int
    students_updated: int
    sections_created: int
    created_at: datetime
    committed_at: datetime | None


class RosterImportCommitOut(BaseModel):
    """What the commit changed, so the admin sees the effect and not just "done"."""

    import_id: uuid.UUID
    students_created: int
    students_updated: int
    sections_created: int
    enrolments_created: int
    enrolments_updated: int


# --------------------------------------------------------------------------- students


class StudentOut(BaseModel):
    id: uuid.UUID
    student_uid: str
    name_bn: str
    name_en: str
    guardian_mobile: str | None
    status: str


class EnrolmentOut(BaseModel):
    section_id: uuid.UUID
    academic_year_id: uuid.UUID
    roll: str
    fourth_subject_code: str | None


class StudentRow(BaseModel):
    """A student as the roster screen lists them: identity plus where they sit."""

    student: StudentOut
    enrolment: EnrolmentOut | None


# --------------------------------------------------------------------------- consent


class ConsentPut(StrictModel):
    consent_type: str = Field(pattern="|".join(CONSENT_TYPES))
    granted: bool
    method: str = Field(pattern="paper_form|digital|verbal_recorded")
    evidence_ref: str | None = Field(default=None, max_length=500)
    note: str | None = Field(default=None, max_length=1000)


class ConsentOut(BaseModel):
    id: uuid.UUID
    consent_type: str
    granted: bool
    method: str
    evidence_ref: str | None
    note: str | None
    recorded_at: datetime
    superseded_at: datetime | None


class ConsentStateOut(BaseModel):
    """Everything a caller needs to decide what may be done with this student.

    ``capture_allowed`` and ``ai_allowed`` are stated rather than left to the caller
    to derive, so that no client can get the "absence means no" rule wrong.
    """

    student_id: uuid.UUID
    current: list[ConsentOut]
    capture_allowed: bool
    ai_allowed: bool
