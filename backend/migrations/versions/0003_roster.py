"""Roster: students, enrolments, guardian consent and staged imports.

Revision ID: 0003
Revises: 0002
Create Date: 2026-09-29

Students are the entity everything after marking hangs off: results per student,
report cards, re-checks and privacy requests all need one. Until now the platform
had only ``exam_candidate`` — a name and a roll typed per exam, with no identity
that survives the exam.

Consent (FR-ORG-06, 08 §6.1) is stored as history, never overwritten: a withdrawal
is a new row that supersedes the old one, so "what was this school allowed to do on
the day this script was marked" stays answerable.
"""

from __future__ import annotations

from rls_helpers import enable_tenant_rls, grant_app, run_sql

revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None

#: 08 §6.1. CT-1 gates capture, CT-2 gates AI, CT-3 gates evaluation datasets.
CONSENT_TYPES = ("CT-1", "CT-2", "CT-3")
CONSENT_METHODS = ("paper_form", "digital", "verbal_recorded")
STUDENT_STATES = ("active", "transferred", "left")
IMPORT_STATES = ("validated", "committed", "discarded")


def _sql_list(values: tuple[str, ...]) -> str:
    return ", ".join(f"'{value}'" for value in values)


# `enrolment` and `student_consent` reference these by (tenant_id, ...) so that a
# cross-tenant row cannot be created even if RLS were somehow bypassed.
SECTION_KEYS = """
ALTER TABLE section ADD CONSTRAINT uq_section_tenant_id_id UNIQUE (tenant_id, id);
ALTER TABLE section ADD CONSTRAINT uq_section_tenant_id_academic_year_id_id
    UNIQUE (tenant_id, academic_year_id, id);
"""

ROSTER_TABLES = rf"""
CREATE TABLE student (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id uuid NOT NULL CONSTRAINT fk_student_tenant_id REFERENCES organization (id),
    school_id uuid NOT NULL,
    student_uid text NOT NULL,
    name_bn text NOT NULL DEFAULT '',
    name_en text NOT NULL DEFAULT '',
    guardian_mobile text,
    status text NOT NULL DEFAULT 'active',
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    CONSTRAINT fk_student_tenant_id_school_id FOREIGN KEY (tenant_id, school_id)
        REFERENCES school (tenant_id, id),
    CONSTRAINT uq_student_tenant_id_id UNIQUE (tenant_id, id),
    CONSTRAINT uq_student_school_id_student_uid UNIQUE (school_id, student_uid),
    CONSTRAINT ck_student_uid_length CHECK (char_length(student_uid) BETWEEN 1 AND 64),
    CONSTRAINT ck_student_name_present CHECK (name_bn <> '' OR name_en <> ''),
    CONSTRAINT ck_student_name_bn_length CHECK (char_length(name_bn) <= 200),
    CONSTRAINT ck_student_name_en_length CHECK (char_length(name_en) <= 200),
    CONSTRAINT ck_student_status CHECK (status IN ({_sql_list(STUDENT_STATES)})),
    CONSTRAINT ck_student_guardian_mobile
        CHECK (guardian_mobile IS NULL OR guardian_mobile ~ '^\+8801[3-9][0-9]{{8}}$')
);
CREATE INDEX ix_student_tenant_id_school_id ON student (tenant_id, school_id);

-- One student, one section, one year (FR-ORG-02). `academic_year_id` is carried
-- here rather than read through `section` so the database itself can enforce that.
CREATE TABLE enrolment (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id uuid NOT NULL,
    student_id uuid NOT NULL,
    academic_year_id uuid NOT NULL,
    section_id uuid NOT NULL,
    roll text NOT NULL,
    fourth_subject_code text,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT fk_enrolment_tenant_id_student_id FOREIGN KEY (tenant_id, student_id)
        REFERENCES student (tenant_id, id) ON DELETE CASCADE,
    CONSTRAINT fk_enrolment_tenant_id_academic_year_id_section_id
        FOREIGN KEY (tenant_id, academic_year_id, section_id)
        REFERENCES section (tenant_id, academic_year_id, id),
    CONSTRAINT uq_enrolment_tenant_id_id UNIQUE (tenant_id, id),
    CONSTRAINT uq_enrolment_student_id_academic_year_id UNIQUE (student_id, academic_year_id),
    CONSTRAINT uq_enrolment_section_id_roll UNIQUE (section_id, roll),
    CONSTRAINT ck_enrolment_roll_length CHECK (char_length(roll) BETWEEN 1 AND 32),
    CONSTRAINT ck_enrolment_fourth_subject_length
        CHECK (fourth_subject_code IS NULL OR char_length(fourth_subject_code) <= 32)
);
CREATE INDEX ix_enrolment_tenant_id_section_id ON enrolment (tenant_id, section_id);

-- Append-only. Granting, changing or withdrawing a consent inserts a new row and
-- stamps `superseded_at` on the previous one; nothing is ever updated in place.
CREATE TABLE student_consent (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id uuid NOT NULL,
    student_id uuid NOT NULL,
    consent_type text NOT NULL,
    granted boolean NOT NULL,
    method text NOT NULL,
    evidence_ref text,
    note text,
    recorded_by uuid CONSTRAINT fk_student_consent_recorded_by REFERENCES app_user (id),
    recorded_at timestamptz NOT NULL DEFAULT now(),
    superseded_at timestamptz,
    CONSTRAINT fk_student_consent_tenant_id_student_id FOREIGN KEY (tenant_id, student_id)
        REFERENCES student (tenant_id, id) ON DELETE CASCADE,
    CONSTRAINT uq_student_consent_tenant_id_id UNIQUE (tenant_id, id),
    CONSTRAINT ck_student_consent_type CHECK (consent_type IN ({_sql_list(CONSENT_TYPES)})),
    CONSTRAINT ck_student_consent_method CHECK (method IN ({_sql_list(CONSENT_METHODS)})),
    CONSTRAINT ck_student_consent_note_length CHECK (note IS NULL OR char_length(note) <= 1000)
);
-- At most one live record per student per consent type; history stays queryable.
CREATE UNIQUE INDEX uq_student_consent_current
    ON student_consent (student_id, consent_type) WHERE superseded_at IS NULL;
CREATE INDEX ix_student_consent_tenant_id_student_id
    ON student_consent (tenant_id, student_id);

-- A validated-but-uncommitted import. `rows` holds the normalised rows the engine
-- accepted, so the commit applies exactly what the admin was shown — not a re-parse
-- of a file that may have changed underneath.
CREATE TABLE roster_import (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id uuid NOT NULL,
    school_id uuid NOT NULL,
    academic_year_id uuid NOT NULL,
    filename text NOT NULL,
    state text NOT NULL DEFAULT 'validated',
    row_count integer NOT NULL,
    accepted_count integer NOT NULL,
    error_count integer NOT NULL,
    report jsonb NOT NULL,
    rows jsonb NOT NULL,
    students_created integer NOT NULL DEFAULT 0,
    students_updated integer NOT NULL DEFAULT 0,
    sections_created integer NOT NULL DEFAULT 0,
    created_by uuid,
    created_at timestamptz NOT NULL DEFAULT now(),
    committed_at timestamptz,
    CONSTRAINT fk_roster_import_tenant_id_school_id FOREIGN KEY (tenant_id, school_id)
        REFERENCES school (tenant_id, id),
    CONSTRAINT fk_roster_import_tenant_id_school_id_academic_year_id
        FOREIGN KEY (tenant_id, school_id, academic_year_id)
        REFERENCES academic_year (tenant_id, school_id, id),
    CONSTRAINT uq_roster_import_tenant_id_id UNIQUE (tenant_id, id),
    CONSTRAINT ck_roster_import_state CHECK (state IN ({_sql_list(IMPORT_STATES)})),
    CONSTRAINT ck_roster_import_counts
        CHECK (row_count >= 0 AND accepted_count >= 0 AND error_count >= 0),
    CONSTRAINT ck_roster_import_committed
        CHECK ((state = 'committed') = (committed_at IS NOT NULL))
);
CREATE INDEX ix_roster_import_tenant_id_school_id ON roster_import (tenant_id, school_id);

-- Links a script to the student who wrote it. Nullable because an exam can still be
-- run on ad-hoc candidates before a roster exists, which is how the platform worked
-- until this migration.
ALTER TABLE exam_candidate ADD COLUMN student_id uuid;
ALTER TABLE exam_candidate ADD CONSTRAINT fk_exam_candidate_tenant_id_student_id
    FOREIGN KEY (tenant_id, student_id) REFERENCES student (tenant_id, id);
CREATE UNIQUE INDEX uq_exam_candidate_exam_id_student_id
    ON exam_candidate (exam_id, student_id) WHERE student_id IS NOT NULL;
"""

TENANT_TABLES = ("student", "enrolment", "student_consent", "roster_import")

GRANTS = (
    ("student", "SELECT, INSERT, UPDATE"),
    ("enrolment", "SELECT, INSERT, UPDATE, DELETE"),
    ("student_consent", "SELECT, INSERT, UPDATE"),
    ("roster_import", "SELECT, INSERT, UPDATE"),
)


def upgrade() -> None:
    run_sql(SECTION_KEYS)
    run_sql(ROSTER_TABLES)
    for table in TENANT_TABLES:
        enable_tenant_rls(table)
    for table, privileges in GRANTS:
        grant_app(table, privileges)


def downgrade() -> None:
    raise NotImplementedError("Migrations are forward-only (TR-DB-06)")
