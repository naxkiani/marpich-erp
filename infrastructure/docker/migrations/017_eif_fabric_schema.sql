-- EIF Phase 9+ — Enterprise Digital Identity Fabric PostgreSQL schema
-- Extends MEIAAP (migrations 002, 003, 016)
-- All tenant-scoped tables use RLS via app.tenant_id session variable

CREATE SCHEMA IF NOT EXISTS federation;
CREATE SCHEMA IF NOT EXISTS credential;
CREATE SCHEMA IF NOT EXISTS trust;
CREATE SCHEMA IF NOT EXISTS session_mgmt;
CREATE SCHEMA IF NOT EXISTS consent;
CREATE SCHEMA IF NOT EXISTS device;
CREATE SCHEMA IF NOT EXISTS certificate;
CREATE SCHEMA IF NOT EXISTS ai_identity;

-- ─── Organizations & Departments ───────────────────────────────────────────

CREATE TABLE IF NOT EXISTS identity.organizations (
    tenant_id VARCHAR(63) NOT NULL,
    id UUID NOT NULL,
    org_ref VARCHAR(64) NOT NULL,
    legal_name VARCHAR(256) NOT NULL,
    display_name VARCHAR(256) NOT NULL,
    industry_pack VARCHAR(64) NOT NULL DEFAULT 'generic',
    status VARCHAR(32) NOT NULL DEFAULT 'active',
    metadata JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tenant_id, id)
);

CREATE TABLE IF NOT EXISTS identity.departments (
    tenant_id VARCHAR(63) NOT NULL,
    id UUID NOT NULL,
    organization_id UUID NOT NULL,
    dept_ref VARCHAR(64) NOT NULL,
    name VARCHAR(256) NOT NULL,
    parent_id UUID,
    path LTREE,
    metadata JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tenant_id, id),
    FOREIGN KEY (tenant_id, organization_id) REFERENCES identity.organizations(tenant_id, id)
);

CREATE INDEX IF NOT EXISTS idx_departments_org ON identity.departments(tenant_id, organization_id);

-- ─── Identity Graph (relationships) ──────────────────────────────────────────

CREATE TABLE IF NOT EXISTS identity.identity_graph_edges (
    tenant_id VARCHAR(63) NOT NULL,
    id UUID NOT NULL,
    from_principal_id UUID NOT NULL,
    to_principal_id UUID NOT NULL,
    relationship_type VARCHAR(64) NOT NULL,
    weight NUMERIC(5,2) NOT NULL DEFAULT 1.0,
    metadata JSONB NOT NULL DEFAULT '{}',
    valid_from TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    valid_until TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tenant_id, id)
);

CREATE INDEX IF NOT EXISTS idx_graph_from ON identity.identity_graph_edges(tenant_id, from_principal_id);
CREATE INDEX IF NOT EXISTS idx_graph_to ON identity.identity_graph_edges(tenant_id, to_principal_id);
CREATE INDEX IF NOT EXISTS idx_graph_type ON identity.identity_graph_edges(tenant_id, relationship_type);

-- ─── Devices ───────────────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS device.devices (
    tenant_id VARCHAR(63) NOT NULL,
    id UUID NOT NULL,
    device_ref VARCHAR(64) NOT NULL,
    principal_id UUID,
    device_type VARCHAR(32) NOT NULL,
    platform VARCHAR(64),
    fingerprint VARCHAR(256) NOT NULL,
    trust_level VARCHAR(32) NOT NULL DEFAULT 'unknown',
    status VARCHAR(32) NOT NULL DEFAULT 'active',
    last_seen_at TIMESTAMPTZ,
    metadata JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tenant_id, id)
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_devices_fingerprint ON device.devices(tenant_id, fingerprint);

-- ─── API Clients (machine identity) ─────────────────────────────────────────

CREATE TABLE IF NOT EXISTS credential.api_clients (
    tenant_id VARCHAR(63) NOT NULL,
    id UUID NOT NULL,
    client_ref VARCHAR(64) NOT NULL,
    name VARCHAR(256) NOT NULL,
    client_id VARCHAR(128) NOT NULL,
    client_secret_hash VARCHAR(256),
    principal_id UUID NOT NULL,
    scopes TEXT[] NOT NULL DEFAULT '{}',
    status VARCHAR(32) NOT NULL DEFAULT 'active',
    rotated_at TIMESTAMPTZ,
    expires_at TIMESTAMPTZ,
    metadata JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tenant_id, id)
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_api_clients_client_id ON credential.api_clients(tenant_id, client_id);

-- ─── Certificates ───────────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS certificate.certificates (
    tenant_id VARCHAR(63) NOT NULL,
    id UUID NOT NULL,
    cert_ref VARCHAR(64) NOT NULL,
    principal_id UUID,
    subject_dn VARCHAR(512) NOT NULL,
    issuer_dn VARCHAR(512) NOT NULL,
    serial_number VARCHAR(128) NOT NULL,
    pem TEXT NOT NULL,
    not_before TIMESTAMPTZ NOT NULL,
    not_after TIMESTAMPTZ NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'active',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tenant_id, id)
);

-- ─── Identity Providers (federation registry) ───────────────────────────────

CREATE TABLE IF NOT EXISTS federation.identity_providers (
    tenant_id VARCHAR(63) NOT NULL,
    id UUID NOT NULL,
    provider_ref VARCHAR(64) NOT NULL,
    protocol VARCHAR(32) NOT NULL CHECK (protocol IN ('oidc', 'saml', 'ldap', 'azure_ad', 'ad')),
    name VARCHAR(256) NOT NULL,
    config JSONB NOT NULL DEFAULT '{}',
    enabled BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tenant_id, id)
);

-- ─── Sessions (extracted from identity) ─────────────────────────────────────

CREATE TABLE IF NOT EXISTS session_mgmt.sessions (
    tenant_id VARCHAR(63) NOT NULL,
    id UUID NOT NULL,
    session_ref VARCHAR(64) NOT NULL,
    principal_id UUID NOT NULL,
    device_id UUID,
    auth_method VARCHAR(32) NOT NULL,
    risk_score INT NOT NULL DEFAULT 0,
    ip_address INET,
    user_agent TEXT,
    refresh_token_hash VARCHAR(256),
    status VARCHAR(32) NOT NULL DEFAULT 'active',
    expires_at TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_activity_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tenant_id, id)
) PARTITION BY RANGE (created_at);

CREATE TABLE IF NOT EXISTS session_mgmt.sessions_default
    PARTITION OF session_mgmt.sessions DEFAULT;

-- ─── Consent ────────────────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS consent.consent_records (
    tenant_id VARCHAR(63) NOT NULL,
    id UUID NOT NULL,
    consent_ref VARCHAR(64) NOT NULL,
    principal_id UUID NOT NULL,
    purpose VARCHAR(256) NOT NULL,
    scope TEXT[] NOT NULL DEFAULT '{}',
    granted BOOLEAN NOT NULL,
    granted_at TIMESTAMPTZ,
    revoked_at TIMESTAMPTZ,
    policy_version VARCHAR(32),
    metadata JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tenant_id, id)
);

-- ─── Trust scores (materialized from identity_risk) ───────────────────────

CREATE TABLE IF NOT EXISTS trust.trust_scores (
    tenant_id VARCHAR(63) NOT NULL,
    id UUID NOT NULL,
    score_ref VARCHAR(64) NOT NULL,
    principal_id UUID,
    score INT NOT NULL,
    risk_level VARCHAR(16) NOT NULL,
    factors JSONB NOT NULL DEFAULT '[]',
    explanation TEXT,
    computed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tenant_id, id, computed_at)
) PARTITION BY RANGE (computed_at);

CREATE TABLE IF NOT EXISTS trust.trust_scores_default
    PARTITION OF trust.trust_scores DEFAULT;

-- ─── AI Identity agents ─────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS ai_identity.agents (
    tenant_id VARCHAR(63) NOT NULL,
    id UUID NOT NULL,
    agent_ref VARCHAR(64) NOT NULL,
    name VARCHAR(256) NOT NULL,
    agent_type VARCHAR(64) NOT NULL,
    principal_id UUID NOT NULL,
    capabilities TEXT[] NOT NULL DEFAULT '{}',
    policy_binding JSONB NOT NULL DEFAULT '{}',
    status VARCHAR(32) NOT NULL DEFAULT 'active',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tenant_id, id)
);

-- ─── Audit (identity-scoped, append-only) ───────────────────────────────────

CREATE TABLE IF NOT EXISTS identity.audit_log (
    tenant_id VARCHAR(63) NOT NULL,
    id UUID NOT NULL,
    correlation_id VARCHAR(64) NOT NULL,
    actor_principal_id UUID,
    action VARCHAR(128) NOT NULL,
    resource_type VARCHAR(64) NOT NULL,
    resource_id VARCHAR(128),
    payload JSONB NOT NULL DEFAULT '{}',
    ip_address INET,
    occurred_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tenant_id, id, occurred_at)
) PARTITION BY RANGE (occurred_at);

CREATE TABLE IF NOT EXISTS identity.audit_log_default
    PARTITION OF identity.audit_log DEFAULT;

-- ─── Row-Level Security ─────────────────────────────────────────────────────

ALTER TABLE identity.organizations ENABLE ROW LEVEL SECURITY;
ALTER TABLE identity.departments ENABLE ROW LEVEL SECURITY;
ALTER TABLE identity.identity_graph_edges ENABLE ROW LEVEL SECURITY;
ALTER TABLE device.devices ENABLE ROW LEVEL SECURITY;
ALTER TABLE credential.api_clients ENABLE ROW LEVEL SECURITY;
ALTER TABLE certificate.certificates ENABLE ROW LEVEL SECURITY;
ALTER TABLE federation.identity_providers ENABLE ROW LEVEL SECURITY;
ALTER TABLE session_mgmt.sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE consent.consent_records ENABLE ROW LEVEL SECURITY;
ALTER TABLE trust.trust_scores ENABLE ROW LEVEL SECURITY;
ALTER TABLE ai_identity.agents ENABLE ROW LEVEL SECURITY;
ALTER TABLE identity.audit_log ENABLE ROW LEVEL SECURITY;

DO $$
DECLARE
    tbl RECORD;
BEGIN
    FOR tbl IN
        SELECT schemaname, tablename FROM pg_tables
        WHERE schemaname IN ('identity','device','credential','certificate','federation','session_mgmt','consent','trust','ai_identity')
        AND tablename NOT IN ('principals')
    LOOP
        EXECUTE format(
            'CREATE POLICY tenant_isolation_%s ON %I.%I USING (tenant_id = identity.current_tenant_id())',
            tbl.tablename, tbl.schemaname, tbl.tablename
        );
    END LOOP;
END $$;
