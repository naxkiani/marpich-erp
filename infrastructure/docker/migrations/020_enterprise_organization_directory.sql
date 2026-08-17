-- Enterprise Organization Directory — identity-facing org projection
-- Migration 020 — NOT organization.* (Core Organization owns that schema)

CREATE SCHEMA IF NOT EXISTS organization_directory;

CREATE TABLE IF NOT EXISTS organization_directory.entries (
    tenant_id VARCHAR(63) NOT NULL,
    id UUID NOT NULL,
    entry_ref VARCHAR(64) NOT NULL,
    organization_id VARCHAR(64) NOT NULL,
    org_unit_id VARCHAR(64),
    display_name VARCHAR(256) NOT NULL,
    entry_type VARCHAR(32) NOT NULL DEFAULT 'unit',
    parent_entry_ref VARCHAR(64),
    directory_dn VARCHAR(1024),
    attributes JSONB NOT NULL DEFAULT '{}',
    enabled BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tenant_id, id),
    UNIQUE (tenant_id, entry_ref)
);

CREATE INDEX IF NOT EXISTS idx_orgdir_entries_org
    ON organization_directory.entries (tenant_id, organization_id);
CREATE INDEX IF NOT EXISTS idx_orgdir_entries_unit
    ON organization_directory.entries (tenant_id, org_unit_id);

CREATE TABLE IF NOT EXISTS organization_directory.memberships (
    tenant_id VARCHAR(63) NOT NULL,
    id UUID NOT NULL,
    membership_ref VARCHAR(64) NOT NULL,
    entry_ref VARCHAR(64) NOT NULL,
    principal_id VARCHAR(128) NOT NULL,
    role_code VARCHAR(64) NOT NULL DEFAULT 'member',
    status VARCHAR(32) NOT NULL DEFAULT 'active',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tenant_id, id),
    UNIQUE (tenant_id, membership_ref),
    UNIQUE (tenant_id, entry_ref, principal_id)
);

CREATE INDEX IF NOT EXISTS idx_orgdir_memberships_principal
    ON organization_directory.memberships (tenant_id, principal_id);

ALTER TABLE organization_directory.entries ENABLE ROW LEVEL SECURITY;
ALTER TABLE organization_directory.memberships ENABLE ROW LEVEL SECURITY;

DO $$ BEGIN
    CREATE POLICY orgdir_entries_tenant ON organization_directory.entries
        USING (tenant_id = current_setting('app.tenant_id', true));
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE POLICY orgdir_memberships_tenant ON organization_directory.memberships
        USING (tenant_id = current_setting('app.tenant_id', true));
EXCEPTION WHEN duplicate_object THEN NULL; END $$;
