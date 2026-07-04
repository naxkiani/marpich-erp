-- Organization schema
CREATE SCHEMA IF NOT EXISTS organization;

CREATE TABLE IF NOT EXISTS organization.organizations (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL UNIQUE,
    name VARCHAR(256) NOT NULL,
    legal_name VARCHAR(256) NOT NULL,
    root_unit_id UUID,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS organization.org_units (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    organization_id UUID NOT NULL REFERENCES organization.organizations(id) ON DELETE CASCADE,
    parent_id UUID REFERENCES organization.org_units(id) ON DELETE SET NULL,
    unit_type VARCHAR(32) NOT NULL,
    code VARCHAR(32) NOT NULL,
    name VARCHAR(128) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (tenant_id, code)
);

CREATE TABLE IF NOT EXISTS organization.memberships (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    org_unit_id UUID NOT NULL REFERENCES organization.org_units(id) ON DELETE CASCADE,
    user_id VARCHAR(64) NOT NULL,
    title VARCHAR(128) NOT NULL,
    is_primary BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (tenant_id, org_unit_id, user_id)
);

CREATE INDEX IF NOT EXISTS idx_org_units_tenant ON organization.org_units(tenant_id);
CREATE INDEX IF NOT EXISTS idx_org_units_org ON organization.org_units(organization_id);
CREATE INDEX IF NOT EXISTS idx_memberships_user ON organization.memberships(tenant_id, user_id);
CREATE INDEX IF NOT EXISTS idx_memberships_unit ON organization.memberships(tenant_id, org_unit_id);
