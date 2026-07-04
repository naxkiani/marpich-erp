-- Integration schema
CREATE SCHEMA IF NOT EXISTS integration;

CREATE TABLE IF NOT EXISTS integration.connectors (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    connector_type VARCHAR(16) NOT NULL,
    name VARCHAR(128) NOT NULL,
    config JSONB NOT NULL DEFAULT '{}',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS integration.webhook_subscriptions (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    target_url VARCHAR(512) NOT NULL,
    event_pattern VARCHAR(128) NOT NULL,
    secret VARCHAR(256) NOT NULL DEFAULT '',
    description TEXT NOT NULL DEFAULT '',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS integration.sync_jobs (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    connector_id UUID NOT NULL REFERENCES integration.connectors(id) ON DELETE CASCADE,
    job_type VARCHAR(64) NOT NULL,
    status VARCHAR(16) NOT NULL,
    result JSONB NOT NULL DEFAULT '{}',
    error TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS integration.logs (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    log_type VARCHAR(16) NOT NULL,
    status VARCHAR(16) NOT NULL,
    reference_id VARCHAR(64) NOT NULL,
    event_name VARCHAR(128),
    detail JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_integration_connectors_tenant ON integration.connectors(tenant_id);
CREATE INDEX IF NOT EXISTS idx_integration_webhooks_tenant ON integration.webhook_subscriptions(tenant_id);
CREATE INDEX IF NOT EXISTS idx_integration_logs_tenant ON integration.logs(tenant_id, created_at DESC);
