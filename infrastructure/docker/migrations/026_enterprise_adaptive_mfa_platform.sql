-- Adaptive MFA platform store (factors + challenges)
-- Migration 026 — isolated schema; contexts.mfa package may still be deferred

CREATE SCHEMA IF NOT EXISTS adaptive_mfa;

CREATE TABLE IF NOT EXISTS adaptive_mfa.factors (
    tenant_id VARCHAR(63) NOT NULL,
    id UUID NOT NULL,
    factor_ref VARCHAR(64) NOT NULL,
    user_id VARCHAR(128) NOT NULL,
    factor_type VARCHAR(32) NOT NULL,
    secret_ref VARCHAR(128) NOT NULL DEFAULT '',
    enabled BOOLEAN NOT NULL DEFAULT TRUE,
    verified_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tenant_id, id),
    UNIQUE (tenant_id, factor_ref)
);

CREATE INDEX IF NOT EXISTS idx_adaptive_mfa_factors_user
    ON adaptive_mfa.factors (tenant_id, user_id, factor_type);

CREATE TABLE IF NOT EXISTS adaptive_mfa.challenges (
    tenant_id VARCHAR(63) NOT NULL,
    id UUID NOT NULL,
    challenge_ref VARCHAR(64) NOT NULL,
    user_id VARCHAR(128) NOT NULL,
    factor_type VARCHAR(32) NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'pending',
    expires_at TIMESTAMPTZ NOT NULL,
    consumed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tenant_id, id),
    UNIQUE (tenant_id, challenge_ref)
);

CREATE INDEX IF NOT EXISTS idx_adaptive_mfa_challenges_user
    ON adaptive_mfa.challenges (tenant_id, user_id, status);

CREATE TABLE IF NOT EXISTS adaptive_mfa.policies (
    tenant_id VARCHAR(63) NOT NULL,
    id UUID NOT NULL,
    policy_ref VARCHAR(64) NOT NULL,
    step_up_on_risk BOOLEAN NOT NULL DEFAULT TRUE,
    require_mfa_for_admin BOOLEAN NOT NULL DEFAULT TRUE,
    remember_device_days INT NOT NULL DEFAULT 30,
    enabled BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tenant_id, id),
    UNIQUE (tenant_id, policy_ref)
);

ALTER TABLE adaptive_mfa.factors ENABLE ROW LEVEL SECURITY;
ALTER TABLE adaptive_mfa.challenges ENABLE ROW LEVEL SECURITY;
ALTER TABLE adaptive_mfa.policies ENABLE ROW LEVEL SECURITY;

DO $$ BEGIN
    CREATE POLICY adaptive_mfa_factors_tenant ON adaptive_mfa.factors
        USING (tenant_id = current_setting('app.tenant_id', true));
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE POLICY adaptive_mfa_challenges_tenant ON adaptive_mfa.challenges
        USING (tenant_id = current_setting('app.tenant_id', true));
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE POLICY adaptive_mfa_policies_tenant ON adaptive_mfa.policies
        USING (tenant_id = current_setting('app.tenant_id', true));
EXCEPTION WHEN duplicate_object THEN NULL; END $$;
