-- Enterprise Authorization Platform — profiles, ABAC, ReBAC tuples
-- Migration 030 — extends "authorization" schema created in 016
-- Note: "authorization" is a reserved keyword — always quote the schema name.

CREATE SCHEMA IF NOT EXISTS "authorization";

CREATE TABLE IF NOT EXISTS "authorization".profiles (
    tenant_id VARCHAR(63) NOT NULL,
    id UUID NOT NULL,
    profile_ref VARCHAR(64) NOT NULL,
    rbac_enabled BOOLEAN NOT NULL DEFAULT TRUE,
    rebac_enabled BOOLEAN NOT NULL DEFAULT TRUE,
    abac_enabled BOOLEAN NOT NULL DEFAULT TRUE,
    pbac_enabled BOOLEAN NOT NULL DEFAULT TRUE,
    default_decision VARCHAR(16) NOT NULL DEFAULT 'deny',
    decision_cache_ttl_seconds INT NOT NULL DEFAULT 30,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tenant_id, id),
    UNIQUE (tenant_id, profile_ref)
);

CREATE INDEX IF NOT EXISTS idx_authz_profiles_tenant
    ON "authorization".profiles (tenant_id);

CREATE TABLE IF NOT EXISTS "authorization".abac_policies (
    tenant_id VARCHAR(63) NOT NULL,
    id UUID NOT NULL,
    policy_ref VARCHAR(64) NOT NULL,
    name VARCHAR(256) NOT NULL,
    effect VARCHAR(8) NOT NULL CHECK (effect IN ('allow', 'deny')),
    permission_pattern VARCHAR(256) NOT NULL,
    conditions JSONB NOT NULL DEFAULT '[]',
    priority INT NOT NULL DEFAULT 100,
    active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tenant_id, id),
    UNIQUE (tenant_id, policy_ref)
);

CREATE INDEX IF NOT EXISTS idx_authz_abac_tenant
    ON "authorization".abac_policies (tenant_id, active, priority);

CREATE TABLE IF NOT EXISTS "authorization".relation_tuples (
    tenant_id VARCHAR(63) NOT NULL,
    id UUID NOT NULL,
    relation_ref VARCHAR(64) NOT NULL,
    object_type VARCHAR(64) NOT NULL,
    object_id VARCHAR(128) NOT NULL,
    relation VARCHAR(64) NOT NULL,
    subject_type VARCHAR(64) NOT NULL,
    subject_id VARCHAR(128) NOT NULL,
    active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tenant_id, id),
    UNIQUE (tenant_id, relation_ref)
);

CREATE INDEX IF NOT EXISTS idx_authz_tuples_object
    ON "authorization".relation_tuples (tenant_id, object_type, object_id, active);
CREATE INDEX IF NOT EXISTS idx_authz_tuples_subject
    ON "authorization".relation_tuples (tenant_id, subject_type, subject_id, active);
CREATE INDEX IF NOT EXISTS idx_authz_tuples_exact
    ON "authorization".relation_tuples (
        tenant_id, object_type, object_id, relation, subject_type, subject_id
    );

CREATE TABLE IF NOT EXISTS "authorization".ref_counters (
    tenant_id VARCHAR(63) NOT NULL,
    prefix VARCHAR(64) NOT NULL,
    next_value INT NOT NULL DEFAULT 1,
    PRIMARY KEY (tenant_id, prefix)
);

-- Extend 016 access_decisions with PDP audit fields used by AuthorizationApplicationService
ALTER TABLE "authorization".access_decisions
    ADD COLUMN IF NOT EXISTS model VARCHAR(32) NOT NULL DEFAULT 'rbac',
    ADD COLUMN IF NOT EXISTS reason_codes JSONB NOT NULL DEFAULT '[]',
    ADD COLUMN IF NOT EXISTS policy_keys JSONB NOT NULL DEFAULT '[]',
    ADD COLUMN IF NOT EXISTS obligations JSONB NOT NULL DEFAULT '[]',
    ADD COLUMN IF NOT EXISTS facts JSONB NOT NULL DEFAULT '{}';

ALTER TABLE "authorization".profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE "authorization".abac_policies ENABLE ROW LEVEL SECURITY;
ALTER TABLE "authorization".relation_tuples ENABLE ROW LEVEL SECURITY;
ALTER TABLE "authorization".ref_counters ENABLE ROW LEVEL SECURITY;
ALTER TABLE "authorization".access_decisions ENABLE ROW LEVEL SECURITY;

DO $$ BEGIN
    CREATE POLICY authz_profiles_tenant ON "authorization".profiles
        USING (tenant_id = current_setting('app.tenant_id', true));
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE POLICY authz_abac_tenant ON "authorization".abac_policies
        USING (tenant_id = current_setting('app.tenant_id', true));
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE POLICY authz_tuples_tenant ON "authorization".relation_tuples
        USING (tenant_id = current_setting('app.tenant_id', true));
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE POLICY authz_ref_tenant ON "authorization".ref_counters
        USING (tenant_id = current_setting('app.tenant_id', true));
EXCEPTION WHEN duplicate_object THEN NULL; END $$;
