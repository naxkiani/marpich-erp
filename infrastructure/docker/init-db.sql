-- Marpich ERP Platform Database Initialization
-- Hybrid multi-tenancy: shared platform schema + tenant schemas

CREATE SCHEMA IF NOT EXISTS platform;
CREATE SCHEMA IF NOT EXISTS identity;
CREATE SCHEMA IF NOT EXISTS tenant;
CREATE SCHEMA IF NOT EXISTS module_registry;

-- Platform tenants registry (control plane)
CREATE TABLE IF NOT EXISTS tenant.tenants (
    id UUID PRIMARY KEY,
    slug VARCHAR(63) NOT NULL UNIQUE,
    name VARCHAR(128) NOT NULL,
    industry_pack VARCHAR(64) NOT NULL,
    tier VARCHAR(32) NOT NULL DEFAULT 'professional',
    isolation_strategy VARCHAR(16) NOT NULL DEFAULT 'row',
    status VARCHAR(32) NOT NULL DEFAULT 'provisioning',
    enabled_modules JSONB NOT NULL DEFAULT '[]',
    locale VARCHAR(16) NOT NULL DEFAULT 'en-US',
    timezone VARCHAR(64) NOT NULL DEFAULT 'UTC',
    data_region VARCHAR(32) NOT NULL DEFAULT 'us-east',
    config JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_tenants_slug ON tenant.tenants(slug);
CREATE INDEX idx_tenants_status ON tenant.tenants(status);
CREATE INDEX idx_tenants_industry_pack ON tenant.tenants(industry_pack);

-- Module registry
CREATE TABLE IF NOT EXISTS module_registry.modules (
    module_id VARCHAR(128) PRIMARY KEY,
    module_version VARCHAR(32) NOT NULL,
    display_name VARCHAR(256) NOT NULL,
    category VARCHAR(64) NOT NULL,
    manifest JSONB NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'registered',
    registered_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS module_registry.tenant_modules (
    tenant_slug VARCHAR(63) NOT NULL REFERENCES tenant.tenants(slug),
    module_id VARCHAR(128) NOT NULL REFERENCES module_registry.modules(module_id),
    activated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    config JSONB NOT NULL DEFAULT '{}',
    PRIMARY KEY (tenant_slug, module_id)
);

-- Identity (shared with RLS in row-level mode)
CREATE TABLE IF NOT EXISTS identity.users (
    id UUID PRIMARY KEY,
    tenant_slug VARCHAR(63) NOT NULL,
    email VARCHAR(256) NOT NULL,
    password_hash VARCHAR(256) NOT NULL,
    display_name VARCHAR(128) NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'active',
    roles JSONB NOT NULL DEFAULT '[]',
    mfa_enabled BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (tenant_slug, email)
);

CREATE INDEX idx_users_tenant ON identity.users(tenant_slug);

-- Audit log (immutable, append-only)
CREATE TABLE IF NOT EXISTS platform.audit_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_slug VARCHAR(63) NOT NULL,
    correlation_id UUID NOT NULL,
    actor_id UUID,
    action VARCHAR(128) NOT NULL,
    resource_type VARCHAR(128) NOT NULL,
    resource_id VARCHAR(256),
    payload JSONB,
    ip_address INET,
    occurred_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_audit_tenant_time ON platform.audit_log(tenant_slug, occurred_at DESC);

-- Outbox for reliable event publishing
CREATE TABLE IF NOT EXISTS platform.outbox (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id VARCHAR(63) NOT NULL,
    event_name VARCHAR(256) NOT NULL,
    event_version INT NOT NULL,
    payload JSONB NOT NULL,
    published BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_outbox_unpublished ON platform.outbox(published, created_at)
    WHERE published = FALSE;
