-- Identity Governance (IGA) — matches Iga* ORM rows in shared.infrastructure.database.orm
-- Migration 037 — schema identity_governance

CREATE SCHEMA IF NOT EXISTS identity_governance;

CREATE TABLE IF NOT EXISTS identity_governance.ref_counters (
    tenant_id VARCHAR(63) NOT NULL,
    prefix VARCHAR(64) NOT NULL,
    value INT NOT NULL DEFAULT 0,
    PRIMARY KEY (tenant_id, prefix)
);

CREATE TABLE IF NOT EXISTS identity_governance.profiles (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    profile_ref VARCHAR(64) NOT NULL,
    access_review_frequency_days INT NOT NULL DEFAULT 90,
    certification_required BOOLEAN NOT NULL DEFAULT TRUE,
    sod_enforcement BOOLEAN NOT NULL DEFAULT TRUE,
    temporary_access_max_hours INT NOT NULL DEFAULT 72,
    emergency_access_max_hours INT NOT NULL DEFAULT 4,
    metadata JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (tenant_id, profile_ref)
);

CREATE INDEX IF NOT EXISTS idx_iga_profiles_tenant
    ON identity_governance.profiles (tenant_id);

CREATE TABLE IF NOT EXISTS identity_governance.access_requests (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    request_ref VARCHAR(64) NOT NULL,
    requester_id VARCHAR(128) NOT NULL,
    target_user_id VARCHAR(128) NOT NULL,
    requested_roles JSONB NOT NULL DEFAULT '[]',
    justification TEXT NOT NULL DEFAULT '',
    status VARCHAR(32) NOT NULL,
    approver_id VARCHAR(128) NOT NULL DEFAULT '',
    sod_checked BOOLEAN NOT NULL DEFAULT FALSE,
    sod_valid BOOLEAN NOT NULL DEFAULT TRUE,
    metadata JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (tenant_id, request_ref)
);

CREATE INDEX IF NOT EXISTS idx_iga_requests_tenant
    ON identity_governance.access_requests (tenant_id, created_at DESC);

CREATE TABLE IF NOT EXISTS identity_governance.access_reviews (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    review_ref VARCHAR(64) NOT NULL,
    title VARCHAR(256) NOT NULL,
    reviewer_id VARCHAR(128) NOT NULL,
    scope_user_ids JSONB NOT NULL DEFAULT '[]',
    status VARCHAR(32) NOT NULL,
    findings JSONB NOT NULL DEFAULT '[]',
    completed_at TIMESTAMPTZ,
    metadata JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (tenant_id, review_ref)
);

CREATE INDEX IF NOT EXISTS idx_iga_reviews_tenant
    ON identity_governance.access_reviews (tenant_id, created_at DESC);

CREATE TABLE IF NOT EXISTS identity_governance.privilege_certifications (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    certification_ref VARCHAR(64) NOT NULL,
    user_id VARCHAR(128) NOT NULL,
    role_ids JSONB NOT NULL DEFAULT '[]',
    certifier_id VARCHAR(128) NOT NULL DEFAULT '',
    status VARCHAR(32) NOT NULL,
    notes TEXT NOT NULL DEFAULT '',
    certified_at TIMESTAMPTZ,
    metadata JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (tenant_id, certification_ref)
);

CREATE INDEX IF NOT EXISTS idx_iga_certs_tenant
    ON identity_governance.privilege_certifications (tenant_id, created_at DESC);

CREATE TABLE IF NOT EXISTS identity_governance.temporary_access_grants (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    grant_ref VARCHAR(64) NOT NULL,
    user_id VARCHAR(128) NOT NULL,
    roles JSONB NOT NULL DEFAULT '[]',
    granted_by VARCHAR(128) NOT NULL,
    expires_at TIMESTAMPTZ NOT NULL,
    status VARCHAR(32) NOT NULL,
    justification TEXT NOT NULL DEFAULT '',
    metadata JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (tenant_id, grant_ref)
);

CREATE INDEX IF NOT EXISTS idx_iga_tmp_grants_tenant
    ON identity_governance.temporary_access_grants (tenant_id, created_at DESC);

CREATE TABLE IF NOT EXISTS identity_governance.emergency_access_grants (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    grant_ref VARCHAR(64) NOT NULL,
    user_id VARCHAR(128) NOT NULL,
    roles JSONB NOT NULL DEFAULT '[]',
    granted_by VARCHAR(128) NOT NULL,
    expires_at TIMESTAMPTZ NOT NULL,
    status VARCHAR(32) NOT NULL,
    incident_ref VARCHAR(128) NOT NULL DEFAULT '',
    justification TEXT NOT NULL DEFAULT '',
    metadata JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (tenant_id, grant_ref)
);

CREATE INDEX IF NOT EXISTS idx_iga_emg_grants_tenant
    ON identity_governance.emergency_access_grants (tenant_id, created_at DESC);

CREATE TABLE IF NOT EXISTS identity_governance.audit_entries (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    entry_ref VARCHAR(64) NOT NULL,
    action VARCHAR(128) NOT NULL,
    actor_id VARCHAR(128) NOT NULL,
    resource_type VARCHAR(64) NOT NULL,
    resource_ref VARCHAR(128) NOT NULL,
    details JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (tenant_id, entry_ref)
);

CREATE INDEX IF NOT EXISTS idx_iga_audit_tenant
    ON identity_governance.audit_entries (tenant_id, created_at DESC);

ALTER TABLE identity_governance.ref_counters ENABLE ROW LEVEL SECURITY;
ALTER TABLE identity_governance.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE identity_governance.access_requests ENABLE ROW LEVEL SECURITY;
ALTER TABLE identity_governance.access_reviews ENABLE ROW LEVEL SECURITY;
ALTER TABLE identity_governance.privilege_certifications ENABLE ROW LEVEL SECURITY;
ALTER TABLE identity_governance.temporary_access_grants ENABLE ROW LEVEL SECURITY;
ALTER TABLE identity_governance.emergency_access_grants ENABLE ROW LEVEL SECURITY;
ALTER TABLE identity_governance.audit_entries ENABLE ROW LEVEL SECURITY;

DO $$ BEGIN
    CREATE POLICY iga_ref_tenant ON identity_governance.ref_counters
        USING (tenant_id = current_setting('app.tenant_id', true));
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE POLICY iga_profiles_tenant ON identity_governance.profiles
        USING (tenant_id = current_setting('app.tenant_id', true));
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE POLICY iga_requests_tenant ON identity_governance.access_requests
        USING (tenant_id = current_setting('app.tenant_id', true));
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE POLICY iga_reviews_tenant ON identity_governance.access_reviews
        USING (tenant_id = current_setting('app.tenant_id', true));
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE POLICY iga_certs_tenant ON identity_governance.privilege_certifications
        USING (tenant_id = current_setting('app.tenant_id', true));
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE POLICY iga_tmp_tenant ON identity_governance.temporary_access_grants
        USING (tenant_id = current_setting('app.tenant_id', true));
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE POLICY iga_emg_tenant ON identity_governance.emergency_access_grants
        USING (tenant_id = current_setting('app.tenant_id', true));
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE POLICY iga_audit_tenant ON identity_governance.audit_entries
        USING (tenant_id = current_setting('app.tenant_id', true));
EXCEPTION WHEN duplicate_object THEN NULL; END $$;
