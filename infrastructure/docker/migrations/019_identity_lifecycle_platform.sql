-- Enterprise Identity Lifecycle Platform — PostgreSQL schema
-- Migration 019 — tenant-scoped RLS via app.tenant_id

CREATE SCHEMA IF NOT EXISTS identity_lifecycle;

CREATE TABLE IF NOT EXISTS identity_lifecycle.profiles (
    tenant_id VARCHAR(63) NOT NULL,
    id UUID NOT NULL,
    profile_ref VARCHAR(64) NOT NULL,
    registration_enabled BOOLEAN NOT NULL DEFAULT TRUE,
    invitation_enabled BOOLEAN NOT NULL DEFAULT TRUE,
    kyc_required BOOLEAN NOT NULL DEFAULT FALSE,
    aml_required BOOLEAN NOT NULL DEFAULT FALSE,
    consent_required BOOLEAN NOT NULL DEFAULT TRUE,
    soft_delete_retention_days INT NOT NULL DEFAULT 30,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tenant_id, id)
);

CREATE TABLE IF NOT EXISTS identity_lifecycle.cases (
    tenant_id VARCHAR(63) NOT NULL,
    id UUID NOT NULL,
    case_ref VARCHAR(64) NOT NULL,
    identity_ref VARCHAR(128) NOT NULL,
    email VARCHAR(320) NOT NULL,
    display_name VARCHAR(256) NOT NULL,
    state VARCHAR(32) NOT NULL DEFAULT 'draft',
    user_id UUID,
    merged_into VARCHAR(64),
    metadata JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tenant_id, id)
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_lc_cases_ref ON identity_lifecycle.cases(tenant_id, case_ref);
CREATE INDEX IF NOT EXISTS idx_lc_cases_state ON identity_lifecycle.cases(tenant_id, state);
CREATE INDEX IF NOT EXISTS idx_lc_cases_email ON identity_lifecycle.cases(tenant_id, email);

CREATE TABLE IF NOT EXISTS identity_lifecycle.transitions (
    tenant_id VARCHAR(63) NOT NULL,
    id UUID NOT NULL,
    transition_ref VARCHAR(64) NOT NULL,
    case_ref VARCHAR(64) NOT NULL,
    action VARCHAR(64) NOT NULL,
    from_state VARCHAR(32) NOT NULL,
    to_state VARCHAR(32) NOT NULL,
    actor_id UUID,
    reason TEXT NOT NULL DEFAULT '',
    metadata JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tenant_id, id)
);

CREATE INDEX IF NOT EXISTS idx_lc_transitions_case ON identity_lifecycle.transitions(tenant_id, case_ref);

CREATE TABLE IF NOT EXISTS identity_lifecycle.verification_tasks (
    tenant_id VARCHAR(63) NOT NULL,
    id UUID NOT NULL,
    task_ref VARCHAR(64) NOT NULL,
    case_ref VARCHAR(64) NOT NULL,
    verification_type VARCHAR(64) NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'pending',
    result JSONB NOT NULL DEFAULT '{}',
    expires_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tenant_id, id)
);

CREATE INDEX IF NOT EXISTS idx_lc_verifications_case ON identity_lifecycle.verification_tasks(tenant_id, case_ref);

CREATE TABLE IF NOT EXISTS identity_lifecycle.consent_records (
    tenant_id VARCHAR(63) NOT NULL,
    id UUID NOT NULL,
    consent_ref VARCHAR(64) NOT NULL,
    case_ref VARCHAR(64) NOT NULL,
    purpose VARCHAR(256) NOT NULL,
    granted BOOLEAN NOT NULL,
    version VARCHAR(32) NOT NULL DEFAULT '1.0',
    granted_at TIMESTAMPTZ,
    revoked_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tenant_id, id)
);

CREATE INDEX IF NOT EXISTS idx_lc_consents_case ON identity_lifecycle.consent_records(tenant_id, case_ref);

CREATE TABLE IF NOT EXISTS identity_lifecycle.audit_entries (
    tenant_id VARCHAR(63) NOT NULL,
    id UUID NOT NULL,
    audit_ref VARCHAR(64) NOT NULL,
    case_ref VARCHAR(64) NOT NULL,
    action VARCHAR(64) NOT NULL,
    actor_id UUID,
    details JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tenant_id, id)
);

CREATE INDEX IF NOT EXISTS idx_lc_audit_case ON identity_lifecycle.audit_entries(tenant_id, case_ref);
CREATE INDEX IF NOT EXISTS idx_lc_audit_action ON identity_lifecycle.audit_entries(tenant_id, action);

CREATE TABLE IF NOT EXISTS identity_lifecycle.invitations (
    tenant_id VARCHAR(63) NOT NULL,
    id UUID NOT NULL,
    invitation_ref VARCHAR(64) NOT NULL,
    case_ref VARCHAR(64) NOT NULL,
    email VARCHAR(320) NOT NULL,
    token VARCHAR(256) NOT NULL,
    expires_at TIMESTAMPTZ NOT NULL,
    accepted_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tenant_id, id)
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_lc_invitations_token ON identity_lifecycle.invitations(tenant_id, token);

-- Row-Level Security
ALTER TABLE identity_lifecycle.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE identity_lifecycle.cases ENABLE ROW LEVEL SECURITY;
ALTER TABLE identity_lifecycle.transitions ENABLE ROW LEVEL SECURITY;
ALTER TABLE identity_lifecycle.verification_tasks ENABLE ROW LEVEL SECURITY;
ALTER TABLE identity_lifecycle.consent_records ENABLE ROW LEVEL SECURITY;
ALTER TABLE identity_lifecycle.audit_entries ENABLE ROW LEVEL SECURITY;
ALTER TABLE identity_lifecycle.invitations ENABLE ROW LEVEL SECURITY;

DO $$ BEGIN
    CREATE POLICY lc_profiles_tenant ON identity_lifecycle.profiles
        USING (tenant_id = current_setting('app.tenant_id', true));
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE POLICY lc_cases_tenant ON identity_lifecycle.cases
        USING (tenant_id = current_setting('app.tenant_id', true));
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE POLICY lc_transitions_tenant ON identity_lifecycle.transitions
        USING (tenant_id = current_setting('app.tenant_id', true));
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE POLICY lc_verifications_tenant ON identity_lifecycle.verification_tasks
        USING (tenant_id = current_setting('app.tenant_id', true));
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE POLICY lc_consents_tenant ON identity_lifecycle.consent_records
        USING (tenant_id = current_setting('app.tenant_id', true));
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE POLICY lc_audit_tenant ON identity_lifecycle.audit_entries
        USING (tenant_id = current_setting('app.tenant_id', true));
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE POLICY lc_invitations_tenant ON identity_lifecycle.invitations
        USING (tenant_id = current_setting('app.tenant_id', true));
EXCEPTION WHEN duplicate_object THEN NULL; END $$;
