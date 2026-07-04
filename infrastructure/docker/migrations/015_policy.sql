-- Policy Engine schema
CREATE SCHEMA IF NOT EXISTS policy;

CREATE TABLE IF NOT EXISTS policy.policies (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    domain VARCHAR(32) NOT NULL,
    key VARCHAR(128) NOT NULL,
    name VARCHAR(256) NOT NULL,
    description TEXT,
    organization_id VARCHAR(64),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (tenant_id, domain, key)
);

CREATE TABLE IF NOT EXISTS policy.policy_versions (
    id UUID PRIMARY KEY,
    policy_id UUID NOT NULL REFERENCES policy.policies(id) ON DELETE CASCADE,
    tenant_id VARCHAR(63) NOT NULL,
    version INTEGER NOT NULL,
    status VARCHAR(32) NOT NULL,
    effective_from TIMESTAMPTZ NOT NULL,
    expires_at TIMESTAMPTZ,
    priority INTEGER NOT NULL DEFAULT 100,
    conditions JSONB NOT NULL DEFAULT '[]'::jsonb,
    rules JSONB NOT NULL DEFAULT '[]'::jsonb,
    exceptions JSONB NOT NULL DEFAULT '[]'::jsonb,
    approval_required BOOLEAN NOT NULL DEFAULT TRUE,
    workflow_key VARCHAR(128),
    require_passing_tests BOOLEAN NOT NULL DEFAULT FALSE,
    cache_allowed BOOLEAN NOT NULL DEFAULT TRUE,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (policy_id, version)
);

CREATE INDEX IF NOT EXISTS idx_policy_policies_tenant ON policy.policies(tenant_id);
CREATE INDEX IF NOT EXISTS idx_policy_versions_tenant ON policy.policy_versions(tenant_id);
CREATE INDEX IF NOT EXISTS idx_policy_versions_active ON policy.policy_versions(tenant_id, status, effective_from);
