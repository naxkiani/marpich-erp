-- EIFTP SoR depth — unique refs + counters (extends 017/028)

CREATE SCHEMA IF NOT EXISTS federation;

CREATE UNIQUE INDEX IF NOT EXISTS uq_federation_idp_tenant_ref
    ON federation.identity_providers (tenant_id, provider_ref);

CREATE TABLE IF NOT EXISTS federation.ref_counters (
    tenant_id VARCHAR(63) NOT NULL,
    prefix VARCHAR(64) NOT NULL,
    next_value INT NOT NULL DEFAULT 1,
    PRIMARY KEY (tenant_id, prefix)
);

ALTER TABLE federation.identity_providers
    ADD COLUMN IF NOT EXISTS plugin_id VARCHAR(128);
