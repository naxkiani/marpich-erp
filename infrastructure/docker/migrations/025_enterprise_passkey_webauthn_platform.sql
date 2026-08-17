-- Passkey / WebAuthn credentials — Authentication SoR
-- Migration 025 — extends authentication schema from 022

CREATE SCHEMA IF NOT EXISTS authentication;

CREATE TABLE IF NOT EXISTS authentication.webauthn_credentials (
    tenant_id VARCHAR(63) NOT NULL,
    id UUID NOT NULL,
    credential_ref VARCHAR(64) NOT NULL,
    user_id VARCHAR(128) NOT NULL,
    credential_id VARCHAR(512) NOT NULL,
    public_key TEXT NOT NULL,
    sign_count INT NOT NULL DEFAULT 0,
    nickname VARCHAR(128) NOT NULL DEFAULT '',
    transports JSONB NOT NULL DEFAULT '[]',
    aaguid VARCHAR(64),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_used_at TIMESTAMPTZ,
    PRIMARY KEY (tenant_id, id),
    UNIQUE (tenant_id, credential_ref),
    UNIQUE (tenant_id, credential_id)
);

CREATE INDEX IF NOT EXISTS idx_webauthn_credentials_user
    ON authentication.webauthn_credentials (tenant_id, user_id);

ALTER TABLE authentication.webauthn_credentials ENABLE ROW LEVEL SECURITY;

DO $$ BEGIN
    CREATE POLICY authentication_webauthn_tenant ON authentication.webauthn_credentials
        USING (tenant_id = current_setting('app.tenant_id', true));
EXCEPTION WHEN duplicate_object THEN NULL; END $$;
