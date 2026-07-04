-- Media schema
CREATE SCHEMA IF NOT EXISTS media;

CREATE TABLE IF NOT EXISTS media.assets (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    file_name VARCHAR(256) NOT NULL,
    content_type VARCHAR(128) NOT NULL,
    media_kind VARCHAR(16) NOT NULL,
    status VARCHAR(16) NOT NULL,
    storage_key VARCHAR(512),
    source_ref VARCHAR(256),
    metadata JSONB NOT NULL DEFAULT '{}',
    created_by VARCHAR(64),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS media.variants (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    asset_id UUID NOT NULL REFERENCES media.assets(id) ON DELETE CASCADE,
    profile VARCHAR(32) NOT NULL,
    url VARCHAR(512) NOT NULL,
    width INT,
    height INT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (asset_id, profile)
);

CREATE TABLE IF NOT EXISTS media.transcode_jobs (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    asset_id UUID NOT NULL REFERENCES media.assets(id) ON DELETE CASCADE,
    profile VARCHAR(32) NOT NULL,
    status VARCHAR(16) NOT NULL,
    error TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_media_assets_tenant ON media.assets(tenant_id);
CREATE INDEX IF NOT EXISTS idx_media_variants_asset ON media.variants(asset_id);
