-- Event Fabric — transactional outbox + idempotent consumer ledger
CREATE SCHEMA IF NOT EXISTS platform;

-- Align legacy column name with tenant_id convention
DO $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_schema = 'platform' AND table_name = 'outbox' AND column_name = 'tenant_slug'
    ) AND NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_schema = 'platform' AND table_name = 'outbox' AND column_name = 'tenant_id'
    ) THEN
        ALTER TABLE platform.outbox RENAME COLUMN tenant_slug TO tenant_id;
    END IF;
END $$;

-- Extend outbox for enterprise dispatch (idempotent publish pipeline)
ALTER TABLE platform.outbox ADD COLUMN IF NOT EXISTS event_id UUID;
ALTER TABLE platform.outbox ADD COLUMN IF NOT EXISTS correlation_id VARCHAR(64);
ALTER TABLE platform.outbox ADD COLUMN IF NOT EXISTS source_context VARCHAR(64);
ALTER TABLE platform.outbox ADD COLUMN IF NOT EXISTS envelope JSONB;
ALTER TABLE platform.outbox ADD COLUMN IF NOT EXISTS published_at TIMESTAMPTZ;
ALTER TABLE platform.outbox ADD COLUMN IF NOT EXISTS retry_count INT NOT NULL DEFAULT 0;
ALTER TABLE platform.outbox ADD COLUMN IF NOT EXISTS last_error TEXT;

CREATE UNIQUE INDEX IF NOT EXISTS idx_outbox_event_id ON platform.outbox(event_id)
    WHERE event_id IS NOT NULL;

CREATE INDEX IF NOT EXISTS idx_outbox_unpublished_v2 ON platform.outbox(published, created_at)
    WHERE published = FALSE;

-- Consumer deduplication — (tenant_id, event_id, consumer_id)
CREATE TABLE IF NOT EXISTS platform.processed_events (
    tenant_id VARCHAR(63) NOT NULL,
    event_id UUID NOT NULL,
    consumer_id VARCHAR(128) NOT NULL,
    event_name VARCHAR(256) NOT NULL,
    processed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tenant_id, event_id, consumer_id)
);

CREATE INDEX IF NOT EXISTS idx_processed_events_tenant_time
    ON platform.processed_events(tenant_id, processed_at DESC);

-- Dead letter for failed dispatches / handlers
CREATE TABLE IF NOT EXISTS platform.dead_letter_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id VARCHAR(63) NOT NULL,
    event_id UUID,
    event_name VARCHAR(256) NOT NULL,
    consumer_id VARCHAR(128),
    envelope JSONB NOT NULL,
    error TEXT NOT NULL,
    retry_count INT NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_dead_letter_tenant ON platform.dead_letter_events(tenant_id, created_at DESC);
