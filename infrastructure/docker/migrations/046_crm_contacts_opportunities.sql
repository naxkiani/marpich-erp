-- Wave 02 — CRM (CAP-ENT-001) contacts + opportunities
CREATE SCHEMA IF NOT EXISTS crm;

CREATE TABLE IF NOT EXISTS crm.contacts (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    email VARCHAR(256) NOT NULL,
    full_name VARCHAR(128) NOT NULL,
    company VARCHAR(128),
    phone VARCHAR(32),
    status VARCHAR(32) NOT NULL DEFAULT 'active',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE UNIQUE INDEX IF NOT EXISTS ix_crm_contacts_tenant_email
    ON crm.contacts (tenant_id, email);
CREATE INDEX IF NOT EXISTS ix_crm_contacts_tenant
    ON crm.contacts (tenant_id);

CREATE TABLE IF NOT EXISTS crm.opportunities (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    contact_id UUID NOT NULL REFERENCES crm.contacts(id),
    title VARCHAR(256) NOT NULL,
    amount NUMERIC(18, 4) NOT NULL,
    currency VARCHAR(3) NOT NULL DEFAULT 'USD',
    stage VARCHAR(32) NOT NULL DEFAULT 'qualifying',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    closed_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS ix_crm_opportunities_tenant
    ON crm.opportunities (tenant_id, stage);
CREATE INDEX IF NOT EXISTS ix_crm_opportunities_contact
    ON crm.opportunities (tenant_id, contact_id);
