"""Assessment slice: exams, items, versioned rubrics, candidates, scripts, item results.

Revision ID: 0002
Revises: 0001
Create Date: 2026-09-28

Vertical slice 1 (exam -> rubric -> lock -> answer -> AI evaluation -> review -> lock).
Marks are ``numeric(6,2)``: the mark grid is whole or half marks, never binary floats.
Rubric payloads and AI suggestions are stored as JSONB exactly as the pure engines
(:mod:`khata.engines`) serialise them, so a stored result stays reproducible.
"""

from __future__ import annotations

from rls_helpers import enable_tenant_rls, grant_app, run_sql

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None

# ExamState / ItemState in khata.engines.workflow. Kept in sync by
# tests/integration/test_state_vocabulary.py, which compares these lists to the enums.
EXAM_STATES = (
    "draft",
    "rubric_locked",
    "capturing",
    "processing",
    "reviewing",
    "moderation",
    "marks_locked",
    "published",
    "recheck",
)
ITEM_STATES = (
    "pending",
    "unmapped",
    "processing",
    "failed",
    "manual_ready",
    "evidence_only",
    "suggested",
    "confirmed",
    "edited",
    "flagged",
    "moderated",
    "locked",
    "recheck",
)


def _sql_list(values: tuple[str, ...]) -> str:
    return ", ".join(f"'{value}'" for value in values)


ASSESSMENT_TABLES = rf"""
CREATE TABLE exam (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id uuid NOT NULL CONSTRAINT fk_exam_tenant_id REFERENCES organization (id),
    school_id uuid NOT NULL,
    name text NOT NULL,
    subject_code text NOT NULL,
    class_level smallint NOT NULL CONSTRAINT fk_exam_class_level REFERENCES class_level (code),
    state text NOT NULL DEFAULT 'draft',
    total_marks numeric(6,2) NOT NULL DEFAULT 0,
    rubric_locked_at timestamptz,
    marks_locked_at timestamptz,
    published_at timestamptz,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    CONSTRAINT fk_exam_tenant_id_school_id FOREIGN KEY (tenant_id, school_id)
        REFERENCES school (tenant_id, id),
    CONSTRAINT uq_exam_tenant_id_id UNIQUE (tenant_id, id),
    CONSTRAINT ck_exam_name_length CHECK (char_length(name) BETWEEN 1 AND 200),
    CONSTRAINT ck_exam_state CHECK (state IN ({_sql_list(EXAM_STATES)})),
    CONSTRAINT ck_exam_total_marks CHECK (total_marks >= 0)
);
CREATE INDEX ix_exam_tenant_id_school_id ON exam (tenant_id, school_id);

CREATE TABLE exam_item (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id uuid NOT NULL,
    exam_id uuid NOT NULL,
    item_no integer NOT NULL,
    prompt_bn text NOT NULL DEFAULT '',
    prompt_en text NOT NULL DEFAULT '',
    max_marks numeric(6,2) NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT fk_exam_item_tenant_id_exam_id FOREIGN KEY (tenant_id, exam_id)
        REFERENCES exam (tenant_id, id) ON DELETE CASCADE,
    CONSTRAINT uq_exam_item_tenant_id_id UNIQUE (tenant_id, id),
    CONSTRAINT uq_exam_item_exam_id_item_no UNIQUE (exam_id, item_no),
    CONSTRAINT ck_exam_item_item_no CHECK (item_no > 0),
    CONSTRAINT ck_exam_item_max_marks CHECK (max_marks > 0)
);
CREATE INDEX ix_exam_item_tenant_id_exam_id ON exam_item (tenant_id, exam_id);

-- One row per rubric version. The locked version is the one evaluation reads;
-- versions are never mutated after locking, so a score stays reproducible.
CREATE TABLE item_rubric (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id uuid NOT NULL,
    exam_id uuid NOT NULL,
    item_id uuid NOT NULL,
    version integer NOT NULL,
    payload jsonb NOT NULL,
    ai_eligible boolean NOT NULL DEFAULT false,
    locked_at timestamptz,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    CONSTRAINT fk_item_rubric_tenant_id_item_id FOREIGN KEY (tenant_id, item_id)
        REFERENCES exam_item (tenant_id, id) ON DELETE CASCADE,
    CONSTRAINT uq_item_rubric_tenant_id_id UNIQUE (tenant_id, id),
    CONSTRAINT uq_item_rubric_item_id_version UNIQUE (item_id, version),
    CONSTRAINT ck_item_rubric_version CHECK (version >= 1)
);
CREATE INDEX ix_item_rubric_tenant_id_exam_id ON item_rubric (tenant_id, exam_id);

CREATE TABLE exam_candidate (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id uuid NOT NULL,
    exam_id uuid NOT NULL,
    roll text NOT NULL,
    name text NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT fk_exam_candidate_tenant_id_exam_id FOREIGN KEY (tenant_id, exam_id)
        REFERENCES exam (tenant_id, id) ON DELETE CASCADE,
    CONSTRAINT uq_exam_candidate_tenant_id_id UNIQUE (tenant_id, id),
    CONSTRAINT uq_exam_candidate_exam_id_roll UNIQUE (exam_id, roll),
    CONSTRAINT ck_exam_candidate_roll_length CHECK (char_length(roll) BETWEEN 1 AND 32),
    CONSTRAINT ck_exam_candidate_name_length CHECK (char_length(name) BETWEEN 1 AND 200)
);
CREATE INDEX ix_exam_candidate_tenant_id_exam_id ON exam_candidate (tenant_id, exam_id);

CREATE TABLE script (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id uuid NOT NULL,
    exam_id uuid NOT NULL,
    candidate_id uuid NOT NULL,
    total_marks numeric(6,2),
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT fk_script_tenant_id_exam_id FOREIGN KEY (tenant_id, exam_id)
        REFERENCES exam (tenant_id, id) ON DELETE CASCADE,
    CONSTRAINT fk_script_tenant_id_candidate_id FOREIGN KEY (tenant_id, candidate_id)
        REFERENCES exam_candidate (tenant_id, id) ON DELETE CASCADE,
    CONSTRAINT uq_script_tenant_id_id UNIQUE (tenant_id, id),
    CONSTRAINT uq_script_exam_id_candidate_id UNIQUE (exam_id, candidate_id),
    CONSTRAINT ck_script_total_marks CHECK (total_marks IS NULL OR total_marks >= 0)
);
CREATE INDEX ix_script_tenant_id_exam_id ON script (tenant_id, exam_id);

-- One row per (script, item): the captured answer, the AI suggestion and the
-- teacher's decision all live together, which is what the review screen reads.
CREATE TABLE item_result (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id uuid NOT NULL,
    script_id uuid NOT NULL,
    item_id uuid NOT NULL,
    state text NOT NULL DEFAULT 'pending',
    answer_text text NOT NULL DEFAULT '',
    rubric_version integer,
    ai_suggestion jsonb,
    ai_confidence numeric(4,3),
    ai_model text,
    score jsonb,
    total numeric(6,2),
    decided_by uuid CONSTRAINT fk_item_result_decided_by REFERENCES app_user (id),
    decided_at timestamptz,
    locked_at timestamptz,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT fk_item_result_tenant_id_script_id FOREIGN KEY (tenant_id, script_id)
        REFERENCES script (tenant_id, id) ON DELETE CASCADE,
    CONSTRAINT fk_item_result_tenant_id_item_id FOREIGN KEY (tenant_id, item_id)
        REFERENCES exam_item (tenant_id, id) ON DELETE CASCADE,
    CONSTRAINT uq_item_result_tenant_id_id UNIQUE (tenant_id, id),
    CONSTRAINT uq_item_result_script_id_item_id UNIQUE (script_id, item_id),
    CONSTRAINT ck_item_result_state CHECK (state IN ({_sql_list(ITEM_STATES)})),
    CONSTRAINT ck_item_result_total CHECK (total IS NULL OR total >= 0),
    CONSTRAINT ck_item_result_confidence
        CHECK (ai_confidence IS NULL OR ai_confidence BETWEEN 0 AND 1)
);
CREATE INDEX ix_item_result_tenant_id_script_id ON item_result (tenant_id, script_id);
CREATE INDEX ix_item_result_tenant_id_state ON item_result (tenant_id, state);
"""

TENANT_TABLES = (
    "exam",
    "exam_item",
    "item_rubric",
    "exam_candidate",
    "script",
    "item_result",
)

GRANTS = (
    ("exam", "SELECT, INSERT, UPDATE"),
    ("exam_item", "SELECT, INSERT, UPDATE, DELETE"),
    ("item_rubric", "SELECT, INSERT, UPDATE"),
    ("exam_candidate", "SELECT, INSERT, UPDATE, DELETE"),
    ("script", "SELECT, INSERT, UPDATE"),
    ("item_result", "SELECT, INSERT, UPDATE"),
)


def upgrade() -> None:
    run_sql(ASSESSMENT_TABLES)
    for table in TENANT_TABLES:
        enable_tenant_rls(table)
    for table, privileges in GRANTS:
        grant_app(table, privileges)


def downgrade() -> None:
    raise NotImplementedError("Migrations are forward-only (TR-DB-06)")
