-- Trusted devices (MFA / adaptive auth supporting store)
-- Migration 024 — isolated schema; mfa application package may still be deferred

CREATE SCHEMA IF NOT EXISTS trusted_devices;

CREATE TABLE IF NOT EXISTS trusted_devices.devices (
    tenant_id VARCHAR(63) NOT NULL,
    id UUID NOT NULL,
    device_ref VARCHAR(64) NOT NULL,
    user_id VARCHAR(128) NOT NULL,
    device_fingerprint VARCHAR(256) NOT NULL,
    display_name VARCHAR(256) NOT NULL DEFAULT '',
    platform VARCHAR(64) NOT NULL DEFAULT '',
    trusted BOOLEAN NOT NULL DEFAULT TRUE,
    last_seen_at TIMESTAMPTZ,
    expires_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tenant_id, id),
    UNIQUE (tenant_id, device_ref),
    UNIQUE (tenant_id, user_id, device_fingerprint)
);

CREATE INDEX IF NOT EXISTS idx_trusted_devices_user
    ON trusted_devices.devices (tenant_id, user_id, trusted);

ALTER TABLE trusted_devices.devices ENABLE ROW LEVEL SECURITY;

DO $$ BEGIN
    CREATE POLICY trusted_devices_tenant ON trusted_devices.devices
        USING (tenant_id = current_setting('app.tenant_id', true));
EXCEPTION WHEN duplicate_object THEN NULL; END $$;
