-- Password Authentication Engine — history + policy (hashes only, never plaintext)
-- Migration 023 — does not replace identity.users.password_hash

CREATE SCHEMA IF NOT EXISTS password_auth;

CREATE TABLE IF NOT EXISTS password_auth.policies (
    tenant_id VARCHAR(63) NOT NULL,
    id UUID NOT NULL,
    policy_ref VARCHAR(64) NOT NULL,
    min_length INT NOT NULL DEFAULT 12,
    require_complexity BOOLEAN NOT NULL DEFAULT TRUE,
    history_count INT NOT NULL DEFAULT 5,
    max_failed_attempts INT NOT NULL DEFAULT 5,
    lockout_minutes INT NOT NULL DEFAULT 15,
    enabled BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tenant_id, id),
    UNIQUE (tenant_id, policy_ref)
);

CREATE TABLE IF NOT EXISTS password_auth.password_history (
    tenant_id VARCHAR(63) NOT NULL,
    id UUID NOT NULL,
    user_id VARCHAR(128) NOT NULL,
    password_hash VARCHAR(256) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tenant_id, id)
);

CREATE INDEX IF NOT EXISTS idx_password_history_user
    ON password_auth.password_history (tenant_id, user_id, created_at DESC);

CREATE TABLE IF NOT EXISTS password_auth.lockouts (
    tenant_id VARCHAR(63) NOT NULL,
    user_id VARCHAR(128) NOT NULL,
    failed_attempts INT NOT NULL DEFAULT 0,
    locked_until TIMESTAMPTZ,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tenant_id, user_id)
);

ALTER TABLE password_auth.policies ENABLE ROW LEVEL SECURITY;
ALTER TABLE password_auth.password_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE password_auth.lockouts ENABLE ROW LEVEL SECURITY;

DO $$ BEGIN
    CREATE POLICY password_auth_policies_tenant ON password_auth.policies
        USING (tenant_id = current_setting('app.tenant_id', true));
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE POLICY password_auth_history_tenant ON password_auth.password_history
        USING (tenant_id = current_setting('app.tenant_id', true));
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE POLICY password_auth_lockouts_tenant ON password_auth.lockouts
        USING (tenant_id = current_setting('app.tenant_id', true));
EXCEPTION WHEN duplicate_object THEN NULL; END $$;
