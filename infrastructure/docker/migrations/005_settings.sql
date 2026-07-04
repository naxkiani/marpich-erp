-- Settings schema
CREATE SCHEMA IF NOT EXISTS settings;

CREATE TABLE IF NOT EXISTS settings.tenant_settings (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL UNIQUE,
    industry_pack VARCHAR(64) NOT NULL,
    config JSONB NOT NULL DEFAULT '{}',
    features JSONB NOT NULL DEFAULT '{}',
    branding JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_settings_tenant ON settings.tenant_settings(tenant_id);
