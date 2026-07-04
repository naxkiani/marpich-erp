-- Analytics schema
CREATE SCHEMA IF NOT EXISTS analytics;

CREATE TABLE IF NOT EXISTS analytics.metric_definitions (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    key VARCHAR(64) NOT NULL,
    name VARCHAR(128) NOT NULL,
    event_pattern VARCHAR(128) NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (tenant_id, key)
);

CREATE TABLE IF NOT EXISTS analytics.metric_snapshots (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    metric_key VARCHAR(64) NOT NULL,
    value INT NOT NULL,
    event_name VARCHAR(128),
    recorded_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS analytics.dashboards (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    name VARCHAR(128) NOT NULL,
    widgets JSONB NOT NULL DEFAULT '[]',
    is_default BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS analytics.alert_rules (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    metric_key VARCHAR(64) NOT NULL,
    name VARCHAR(128) NOT NULL,
    threshold INT NOT NULL,
    operator VARCHAR(8) NOT NULL DEFAULT 'gte',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    last_triggered_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_analytics_snapshots_metric ON analytics.metric_snapshots(tenant_id, metric_key, recorded_at DESC);
CREATE INDEX IF NOT EXISTS idx_analytics_dashboards_tenant ON analytics.dashboards(tenant_id);
