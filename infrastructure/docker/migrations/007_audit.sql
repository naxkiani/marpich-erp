-- Audit schema
CREATE SCHEMA IF NOT EXISTS audit;

CREATE TABLE IF NOT EXISTS audit.entries (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    event_name VARCHAR(128) NOT NULL,
    source_context VARCHAR(64) NOT NULL,
    correlation_id VARCHAR(64) NOT NULL,
    action VARCHAR(128) NOT NULL,
    resource_type VARCHAR(64) NOT NULL,
    resource_id VARCHAR(128),
    actor_id VARCHAR(64),
    severity VARCHAR(16) NOT NULL DEFAULT 'info',
    payload JSONB NOT NULL DEFAULT '{}',
    occurred_at TIMESTAMPTZ NOT NULL,
    recorded_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS audit.exports (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    status VARCHAR(16) NOT NULL,
    format VARCHAR(8) NOT NULL,
    filters JSONB NOT NULL DEFAULT '{}',
    entry_count INT NOT NULL DEFAULT 0,
    data JSONB NOT NULL DEFAULT '[]',
    error TEXT,
    requested_by VARCHAR(64),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS audit.retention_policies (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL UNIQUE,
    retention_days INT NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_audit_entries_tenant ON audit.entries(tenant_id);
CREATE INDEX IF NOT EXISTS idx_audit_entries_event ON audit.entries(tenant_id, event_name);
CREATE INDEX IF NOT EXISTS idx_audit_entries_occurred ON audit.entries(tenant_id, occurred_at DESC);
CREATE INDEX IF NOT EXISTS idx_audit_entries_severity ON audit.entries(tenant_id, severity);
