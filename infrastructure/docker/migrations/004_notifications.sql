-- Notifications schema
CREATE SCHEMA IF NOT EXISTS notifications;

CREATE TABLE IF NOT EXISTS notifications.inbox_messages (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    user_id UUID,
    channel VARCHAR(32) NOT NULL DEFAULT 'inbox',
    title VARCHAR(256) NOT NULL,
    body TEXT NOT NULL,
    category VARCHAR(64) NOT NULL DEFAULT 'general',
    source_event VARCHAR(128) NOT NULL DEFAULT '',
    status VARCHAR(16) NOT NULL DEFAULT 'unread',
    metadata JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    read_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_inbox_tenant_user ON notifications.inbox_messages(tenant_id, user_id);
CREATE INDEX IF NOT EXISTS idx_inbox_status ON notifications.inbox_messages(tenant_id, status);

CREATE TABLE IF NOT EXISTS notifications.deliveries (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    channel VARCHAR(32) NOT NULL,
    recipient VARCHAR(256) NOT NULL,
    template_key VARCHAR(64) NOT NULL,
    source_event VARCHAR(128) NOT NULL DEFAULT '',
    status VARCHAR(16) NOT NULL DEFAULT 'pending',
    error TEXT,
    payload JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    delivered_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_deliveries_tenant ON notifications.deliveries(tenant_id);
