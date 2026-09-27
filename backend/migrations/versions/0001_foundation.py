"""Foundation: RLS context functions, identity, org, audit, outbox, jobs, keys, idempotency.

Revision ID: 0001
Revises:
Create Date: 2026-09-28
"""

from __future__ import annotations

from pathlib import Path

from rls_helpers import APP_ROLE, enable_tenant_rls, grant_app, run_sql

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None

PROCRASTINATE_SCHEMA = Path(__file__).resolve().parents[1] / "sql" / "procrastinate_3.10.0_schema.sql"

CONTEXT_FUNCTIONS = r"""
REVOKE ALL ON SCHEMA public FROM PUBLIC;
GRANT USAGE ON SCHEMA public TO khata_app;

CREATE FUNCTION app_current_tenant() RETURNS uuid
    LANGUAGE sql STABLE PARALLEL SAFE
    AS $$ SELECT nullif(current_setting('app.tenant_id', true), '')::uuid $$;
CREATE FUNCTION app_current_user() RETURNS uuid
    LANGUAGE sql STABLE PARALLEL SAFE
    AS $$ SELECT nullif(current_setting('app.user_id', true), '')::uuid $$;
CREATE FUNCTION app_platform_scope() RETURNS boolean
    LANGUAGE sql STABLE PARALLEL SAFE
    AS $$ SELECT coalesce(current_setting('app.platform_scope', true), '') = 'on' $$;
"""

IDENTITY_TABLES = r"""
CREATE TABLE app_user (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    mobile text NOT NULL,
    name text NOT NULL,
    password_hash text,
    status text NOT NULL DEFAULT 'active',
    locale text NOT NULL DEFAULT 'bn',
    preferences jsonb NOT NULL DEFAULT '{}'::jsonb,
    platform_role text,
    failed_login_count integer NOT NULL DEFAULT 0,
    last_failed_login_at timestamptz,
    locked_until timestamptz,
    last_active_tenant_id uuid,
    password_changed_at timestamptz,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT uq_app_user_mobile UNIQUE (mobile),
    CONSTRAINT ck_app_user_mobile_e164 CHECK (mobile ~ '^\+[1-9][0-9]{7,14}$'),
    CONSTRAINT ck_app_user_name_length CHECK (char_length(name) BETWEEN 1 AND 200),
    CONSTRAINT ck_app_user_status CHECK (status IN ('invited', 'active', 'disabled')),
    CONSTRAINT ck_app_user_locale CHECK (locale IN ('bn', 'en')),
    CONSTRAINT ck_app_user_platform_role CHECK (platform_role IS NULL OR platform_role IN
        ('platform_admin', 'platform_aiq', 'platform_assessment', 'platform_support'))
);

CREATE TABLE device (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id uuid NOT NULL CONSTRAINT fk_device_user_id REFERENCES app_user (id),
    name text NOT NULL,
    kind text NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now(),
    last_seen_at timestamptz,
    revoked_at timestamptz,
    CONSTRAINT ck_device_kind CHECK (kind IN ('web', 'capture'))
);
CREATE INDEX ix_device_user_id ON device (user_id);

CREATE TABLE auth_session (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id uuid NOT NULL CONSTRAINT fk_auth_session_user_id REFERENCES app_user (id),
    device_id uuid NOT NULL CONSTRAINT fk_auth_session_device_id REFERENCES device (id),
    client text NOT NULL,
    active_tenant_id uuid,
    created_at timestamptz NOT NULL DEFAULT now(),
    last_seen_at timestamptz NOT NULL DEFAULT now(),
    expires_at timestamptz NOT NULL,
    revoked_at timestamptz,
    revoke_reason text,
    CONSTRAINT ck_auth_session_client CHECK (client IN ('web', 'capture'))
);
CREATE INDEX ix_auth_session_user_id ON auth_session (user_id);

CREATE TABLE refresh_token (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    token_hash text NOT NULL,
    family_id uuid NOT NULL CONSTRAINT fk_refresh_token_family_id REFERENCES auth_session (id),
    user_id uuid NOT NULL CONSTRAINT fk_refresh_token_user_id REFERENCES app_user (id),
    device_id uuid NOT NULL CONSTRAINT fk_refresh_token_device_id REFERENCES device (id),
    created_at timestamptz NOT NULL DEFAULT now(),
    expires_at timestamptz NOT NULL,
    idle_expires_at timestamptz NOT NULL,
    rotated_at timestamptz,
    revoked_at timestamptz,
    CONSTRAINT uq_refresh_token_token_hash UNIQUE (token_hash)
);
CREATE INDEX ix_refresh_token_family_id ON refresh_token (family_id);

CREATE TABLE otp_challenge (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id uuid NOT NULL CONSTRAINT fk_otp_challenge_user_id REFERENCES app_user (id),
    purpose text NOT NULL,
    step_up_purpose text,
    session_id uuid CONSTRAINT fk_otp_challenge_session_id REFERENCES auth_session (id),
    client text NOT NULL,
    code_hmac text NOT NULL,
    attempts integer NOT NULL DEFAULT 0,
    send_count integer NOT NULL DEFAULT 1,
    expires_at timestamptz NOT NULL,
    last_sent_at timestamptz NOT NULL,
    consumed_at timestamptz,
    dead_at timestamptz,
    created_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT ck_otp_challenge_purpose CHECK (purpose IN ('login', 'reset', 'step_up')),
    CONSTRAINT ck_otp_challenge_client CHECK (client IN ('web', 'capture')),
    CONSTRAINT ck_otp_challenge_step_up CHECK ((purpose = 'step_up') = (step_up_purpose IS NOT NULL))
);
CREATE INDEX ix_otp_challenge_user_id ON otp_challenge (user_id);

CREATE TABLE otp_send (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id uuid NOT NULL CONSTRAINT fk_otp_send_user_id REFERENCES app_user (id),
    challenge_id uuid NOT NULL CONSTRAINT fk_otp_send_challenge_id REFERENCES otp_challenge (id),
    sent_at timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX ix_otp_send_user_id_sent_at ON otp_send (user_id, sent_at);
"""

ORG_TABLES = r"""
CREATE TABLE class_level (
    code smallint PRIMARY KEY,
    name_bn text NOT NULL,
    name_en text NOT NULL,
    CONSTRAINT ck_class_level_code CHECK (code BETWEEN 6 AND 12)
);
INSERT INTO class_level (code, name_bn, name_en) VALUES
    (6, 'ষষ্ঠ শ্রেণি', 'Class 6'), (7, 'সপ্তম শ্রেণি', 'Class 7'),
    (8, 'অষ্টম শ্রেণি', 'Class 8'), (9, 'নবম শ্রেণি', 'Class 9'),
    (10, 'দশম শ্রেণি', 'Class 10'), (11, 'একাদশ শ্রেণি', 'Class 11'),
    (12, 'দ্বাদশ শ্রেণি', 'Class 12');

CREATE TABLE organization (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    name text NOT NULL,
    plan_id uuid,
    status text NOT NULL DEFAULT 'active',
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT ck_organization_status CHECK (status IN ('active', 'suspended', 'closed'))
);

CREATE TABLE school (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id uuid NOT NULL CONSTRAINT fk_school_tenant_id REFERENCES organization (id),
    name_bn text NOT NULL,
    name_en text NOT NULL,
    eiin text,
    board text NOT NULL,
    versions text[] NOT NULL DEFAULT '{}',
    shifts text[] NOT NULL DEFAULT '{}',
    logo_ref text,
    booklet_profile jsonb NOT NULL DEFAULT '{}'::jsonb,
    settings jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT uq_school_tenant_id_id UNIQUE (tenant_id, id),
    CONSTRAINT ck_school_versions CHECK (versions <@ ARRAY['BM', 'EV']::text[]),
    CONSTRAINT ck_school_eiin CHECK (eiin IS NULL OR eiin ~ '^[0-9]{6}$')
);
CREATE UNIQUE INDEX uq_school_tenant_id_eiin ON school (tenant_id, eiin) WHERE eiin IS NOT NULL;

CREATE TABLE academic_year (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id uuid NOT NULL,
    school_id uuid NOT NULL,
    year smallint NOT NULL,
    starts_on date NOT NULL,
    ends_on date NOT NULL,
    is_current boolean NOT NULL DEFAULT false,
    created_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT fk_academic_year_tenant_id_school_id FOREIGN KEY (tenant_id, school_id)
        REFERENCES school (tenant_id, id),
    CONSTRAINT uq_academic_year_school_id_year UNIQUE (school_id, year),
    CONSTRAINT uq_academic_year_tenant_id_school_id_id UNIQUE (tenant_id, school_id, id),
    CONSTRAINT ck_academic_year_year CHECK (year BETWEEN 2000 AND 2100),
    CONSTRAINT ck_academic_year_dates CHECK (ends_on > starts_on)
);

CREATE TABLE section (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id uuid NOT NULL,
    school_id uuid NOT NULL,
    academic_year_id uuid NOT NULL,
    class_level smallint NOT NULL CONSTRAINT fk_section_class_level REFERENCES class_level (code),
    group_code text NOT NULL,
    version text NOT NULL,
    shift text NOT NULL DEFAULT 'day',
    name text NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT fk_section_tenant_id_school_id_academic_year_id
        FOREIGN KEY (tenant_id, school_id, academic_year_id)
        REFERENCES academic_year (tenant_id, school_id, id),
    CONSTRAINT uq_section_identity
        UNIQUE (academic_year_id, class_level, group_code, version, shift, name),
    CONSTRAINT uq_section_tenant_id_school_id_academic_year_id_id
        UNIQUE (tenant_id, school_id, academic_year_id, id),
    CONSTRAINT ck_section_group CHECK (group_code IN ('science', 'humanities', 'business', 'none')),
    CONSTRAINT ck_section_version CHECK (version IN ('BM', 'EV'))
);

CREATE TABLE role_assignment (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id uuid NOT NULL CONSTRAINT fk_role_assignment_tenant_id REFERENCES organization (id),
    user_id uuid NOT NULL CONSTRAINT fk_role_assignment_user_id REFERENCES app_user (id),
    school_id uuid,
    role text NOT NULL,
    subject_code text,
    valid_from timestamptz NOT NULL DEFAULT now(),
    valid_to timestamptz,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    CONSTRAINT fk_role_assignment_tenant_id_school_id FOREIGN KEY (tenant_id, school_id)
        REFERENCES school (tenant_id, id),
    CONSTRAINT ck_role_assignment_role CHECK (role IN ('org_owner', 'school_admin',
        'exam_coordinator', 'hod', 'teacher', 'capture_operator', 'principal')),
    CONSTRAINT ck_role_assignment_school_scope CHECK ((role = 'org_owner') = (school_id IS NULL)),
    CONSTRAINT ck_role_assignment_subject CHECK (subject_code IS NULL OR role IN ('hod', 'teacher')),
    CONSTRAINT ck_role_assignment_validity CHECK (valid_to IS NULL OR valid_to >= valid_from)
);
CREATE UNIQUE INDEX uq_role_assignment_active ON role_assignment (
    tenant_id, user_id, coalesce(school_id, '00000000-0000-0000-0000-000000000000'::uuid),
    role, coalesce(subject_code, '')
) WHERE valid_to IS NULL;
CREATE INDEX ix_role_assignment_user_id ON role_assignment (user_id);

CREATE TABLE teaching_assignment (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id uuid NOT NULL,
    user_id uuid NOT NULL CONSTRAINT fk_teaching_assignment_user_id REFERENCES app_user (id),
    school_id uuid NOT NULL,
    academic_year_id uuid NOT NULL,
    section_id uuid NOT NULL,
    subject_code text NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    CONSTRAINT fk_teaching_assignment_section FOREIGN KEY
        (tenant_id, school_id, academic_year_id, section_id)
        REFERENCES section (tenant_id, school_id, academic_year_id, id),
    CONSTRAINT uq_teaching_assignment_user_id_section_id_subject_code
        UNIQUE (user_id, section_id, subject_code)
);
CREATE INDEX ix_teaching_assignment_school_year
    ON teaching_assignment (tenant_id, school_id, academic_year_id);
"""

# Read-only visibility of a user's own memberships while no tenant is bound (/v1/me,
# login tenant selection) and of tenant ids for platform maintenance. See ADR-016.
ORG_EXTRA_POLICIES = r"""
CREATE POLICY membership_read ON role_assignment FOR SELECT
    USING (app_current_tenant() IS NULL AND user_id = app_current_user());
CREATE POLICY membership_read ON organization FOR SELECT
    USING (app_current_tenant() IS NULL AND EXISTS (
        SELECT 1 FROM role_assignment ra
        WHERE ra.tenant_id = organization.id AND ra.user_id = app_current_user()
          AND ra.valid_from <= now() AND (ra.valid_to IS NULL OR ra.valid_to > now())));
CREATE POLICY membership_read ON school FOR SELECT
    USING (app_current_tenant() IS NULL AND EXISTS (
        SELECT 1 FROM role_assignment ra
        WHERE ra.tenant_id = school.tenant_id AND ra.user_id = app_current_user()
          AND (ra.school_id = school.id OR ra.school_id IS NULL)
          AND ra.valid_from <= now() AND (ra.valid_to IS NULL OR ra.valid_to > now())));
CREATE POLICY platform_read ON organization FOR SELECT USING (app_platform_scope());
"""

INFRA_TABLES = r"""
CREATE TABLE tenant_key (
    tenant_id uuid NOT NULL CONSTRAINT fk_tenant_key_tenant_id REFERENCES organization (id),
    key_version integer NOT NULL,
    wrapped_dek bytea,
    kms_key_id text NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now(),
    shredded_at timestamptz,
    CONSTRAINT pk_tenant_key PRIMARY KEY (tenant_id, key_version),
    CONSTRAINT ck_tenant_key_version CHECK (key_version > 0)
);

CREATE TABLE idempotency_record (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id uuid NOT NULL,
    user_id uuid NOT NULL,
    key text NOT NULL,
    request_hash text NOT NULL,
    state text NOT NULL,
    status_code smallint,
    response_body jsonb,
    response_hash text,
    created_at timestamptz NOT NULL DEFAULT now(),
    completed_at timestamptz,
    CONSTRAINT uq_idempotency_record_tenant_id_user_id_key UNIQUE (tenant_id, user_id, key),
    CONSTRAINT ck_idempotency_record_state CHECK (state IN ('pending', 'completed'))
);
CREATE INDEX ix_idempotency_record_created_at ON idempotency_record (created_at);

CREATE TABLE audit_chain_head (
    tenant_id uuid PRIMARY KEY,
    last_seq bigint NOT NULL,
    last_hash text NOT NULL,
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE audit_event (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id uuid NOT NULL,
    seq bigint NOT NULL,
    school_id uuid,
    actor_user_id uuid,
    actor_role text,
    action text NOT NULL,
    entity_type text NOT NULL,
    entity_id text,
    before jsonb,
    after jsonb,
    reason text,
    correlation_id text,
    client text,
    created_at timestamptz NOT NULL,
    prev_hash text NOT NULL,
    hash text NOT NULL,
    CONSTRAINT uq_audit_event_tenant_id_seq UNIQUE (tenant_id, seq),
    CONSTRAINT ck_audit_event_seq CHECK (seq > 0)
);
CREATE INDEX ix_audit_event_entity ON audit_event (tenant_id, entity_type, entity_id);
CREATE INDEX ix_audit_event_actor ON audit_event (tenant_id, actor_user_id);
CREATE INDEX ix_audit_event_action ON audit_event (tenant_id, action);

CREATE FUNCTION audit_event_append_only() RETURNS trigger
    LANGUAGE plpgsql AS $$
BEGIN
    RAISE EXCEPTION 'audit_event is append-only' USING ERRCODE = 'insufficient_privilege';
END;
$$;
CREATE TRIGGER audit_event_no_update_delete BEFORE UPDATE OR DELETE ON audit_event
    FOR EACH ROW EXECUTE FUNCTION audit_event_append_only();
CREATE TRIGGER audit_event_no_truncate BEFORE TRUNCATE ON audit_event
    FOR EACH STATEMENT EXECUTE FUNCTION audit_event_append_only();

CREATE TABLE domain_event (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id uuid,
    type text NOT NULL,
    payload jsonb NOT NULL,
    correlation_id text,
    created_at timestamptz NOT NULL DEFAULT now(),
    dispatched_at timestamptz
);
CREATE INDEX ix_domain_event_undispatched ON domain_event (created_at) WHERE dispatched_at IS NULL;

CREATE TABLE async_operation (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id uuid NOT NULL CONSTRAINT fk_async_operation_tenant_id REFERENCES organization (id),
    kind text NOT NULL,
    status text NOT NULL DEFAULT 'queued',
    progress smallint NOT NULL DEFAULT 0,
    result jsonb,
    error_code text,
    procrastinate_job_id bigint,
    created_by uuid,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    started_at timestamptz,
    finished_at timestamptz,
    CONSTRAINT ck_async_operation_status
        CHECK (status IN ('queued', 'running', 'succeeded', 'failed')),
    CONSTRAINT ck_async_operation_progress CHECK (progress BETWEEN 0 AND 100)
);
"""

TENANT_TABLES = (
    ("organization", "id", False),
    ("school", "tenant_id", False),
    ("academic_year", "tenant_id", False),
    ("section", "tenant_id", False),
    ("role_assignment", "tenant_id", False),
    ("teaching_assignment", "tenant_id", False),
    ("tenant_key", "tenant_id", False),
    ("idempotency_record", "tenant_id", False),
    ("audit_chain_head", "tenant_id", False),
    ("audit_event", "tenant_id", False),
    ("domain_event", "tenant_id", True),
    ("async_operation", "tenant_id", False),
)

GRANTS = (
    ("app_user", "SELECT, INSERT, UPDATE"),
    ("device", "SELECT, INSERT, UPDATE"),
    ("auth_session", "SELECT, INSERT, UPDATE"),
    ("refresh_token", "SELECT, INSERT, UPDATE, DELETE"),
    ("otp_challenge", "SELECT, INSERT, UPDATE, DELETE"),
    ("otp_send", "SELECT, INSERT, DELETE"),
    ("class_level", "SELECT"),
    ("organization", "SELECT, INSERT, UPDATE"),
    ("school", "SELECT, INSERT, UPDATE"),
    ("academic_year", "SELECT, INSERT, UPDATE"),
    ("section", "SELECT, INSERT, UPDATE"),
    ("role_assignment", "SELECT, INSERT, UPDATE"),
    ("teaching_assignment", "SELECT, INSERT, UPDATE, DELETE"),
    ("tenant_key", "SELECT, INSERT, UPDATE"),
    ("idempotency_record", "SELECT, INSERT, UPDATE, DELETE"),
    ("audit_chain_head", "SELECT, INSERT, UPDATE"),
    ("audit_event", "SELECT, INSERT"),
    ("domain_event", "SELECT, INSERT, UPDATE"),
    ("async_operation", "SELECT, INSERT, UPDATE"),
)

PROCRASTINATE_GRANTS = f"""
GRANT SELECT, INSERT, UPDATE, DELETE ON procrastinate_jobs, procrastinate_events,
    procrastinate_periodic_defers, procrastinate_workers TO {APP_ROLE};
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO {APP_ROLE};
"""


def upgrade() -> None:
    run_sql(CONTEXT_FUNCTIONS)
    run_sql(IDENTITY_TABLES)
    run_sql(ORG_TABLES)
    run_sql(INFRA_TABLES)
    for table, column, nullable in TENANT_TABLES:
        enable_tenant_rls(table, column, nullable=nullable)
    run_sql(ORG_EXTRA_POLICIES)
    for table, privileges in GRANTS:
        grant_app(table, privileges)
    run_sql(PROCRASTINATE_SCHEMA.read_text(encoding="utf-8"))
    run_sql(PROCRASTINATE_GRANTS)


def downgrade() -> None:
    raise NotImplementedError("Migrations are forward-only (TR-DB-06)")
