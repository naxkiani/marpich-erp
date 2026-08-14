-- Enterprise Authentication Platform — profiles, OIDC, challenge TTL
-- Migration 022 — schema isolated from identity.* (password hashes stay on identity.users)

CREATE SCHEMA IF NOT EXISTS authentication;

CREATE TABLE IF NOT EXISTS authentication.profiles (
    tenant_id VARCHAR(63) NOT NULL,
    id UUID NOT NULL,
    profile_ref VARCHAR(64) NOT NULL,
    webauthn_enabled BOOLEAN NOT NULL DEFAULT TRUE,
    passkeys_required BOOLEAN NOT NULL DEFAULT FALSE,
    oidc_enabled BOOLEAN NOT NULL DEFAULT TRUE,
    password_enabled BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tenant_id, id),
    UNIQUE (tenant_id, profile_ref)
);

CREATE INDEX IF NOT EXISTS idx_authentication_profiles_tenant
    ON authentication.profiles (tenant_id);

CREATE TABLE IF NOT EXISTS authentication.oidc_providers (
    tenant_id VARCHAR(63) NOT NULL,
    id UUID NOT NULL,
    provider_ref VARCHAR(64) NOT NULL,
    name VARCHAR(256) NOT NULL,
    issuer_url VARCHAR(1024) NOT NULL,
    client_id VARCHAR(256) NOT NULL,
    client_secret TEXT NOT NULL DEFAULT '',
    redirect_uri VARCHAR(1024) NOT NULL DEFAULT '',
    scopes VARCHAR(512) NOT NULL DEFAULT 'openid profile email',
    enabled BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tenant_id, id),
    UNIQUE (tenant_id, provider_ref)
);

CREATE INDEX IF NOT EXISTS idx_authentication_oidc_tenant
    ON authentication.oidc_providers (tenant_id, enabled);

CREATE TABLE IF NOT EXISTS authentication.oidc_states (
    tenant_id VARCHAR(63) NOT NULL,
    state VARCHAR(256) NOT NULL,
    payload JSONB NOT NULL DEFAULT '{}',
    expires_at TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tenant_id, state)
);

CREATE INDEX IF NOT EXISTS idx_authentication_oidc_states_exp
    ON authentication.oidc_states (expires_at);

CREATE TABLE IF NOT EXISTS authentication.webauthn_challenges (
    tenant_id VARCHAR(63) NOT NULL,
    challenge_id VARCHAR(256) NOT NULL,
    challenge_kind VARCHAR(32) NOT NULL,
    payload JSONB NOT NULL DEFAULT '{}',
    expires_at TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tenant_id, challenge_id)
);

CREATE INDEX IF NOT EXISTS idx_authentication_challenges_exp
    ON authentication.webauthn_challenges (expires_at);

CREATE TABLE IF NOT EXISTS authentication.ref_counters (
    tenant_id VARCHAR(63) NOT NULL,
    prefix VARCHAR(64) NOT NULL,
    next_value INT NOT NULL DEFAULT 1,
    PRIMARY KEY (tenant_id, prefix)
);

ALTER TABLE authentication.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE authentication.oidc_providers ENABLE ROW LEVEL SECURITY;
ALTER TABLE authentication.oidc_states ENABLE ROW LEVEL SECURITY;
ALTER TABLE authentication.webauthn_challenges ENABLE ROW LEVEL SECURITY;
ALTER TABLE authentication.ref_counters ENABLE ROW LEVEL SECURITY;

DO $$ BEGIN
    CREATE POLICY authentication_profiles_tenant ON authentication.profiles
        USING (tenant_id = current_setting('app.tenant_id', true));
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE POLICY authentication_oidc_tenant ON authentication.oidc_providers
        USING (tenant_id = current_setting('app.tenant_id', true));
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE POLICY authentication_oidc_states_tenant ON authentication.oidc_states
        USING (tenant_id = current_setting('app.tenant_id', true));
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE POLICY authentication_challenges_tenant ON authentication.webauthn_challenges
        USING (tenant_id = current_setting('app.tenant_id', true));
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE POLICY authentication_ref_tenant ON authentication.ref_counters
        USING (tenant_id = current_setting('app.tenant_id', true));
EXCEPTION WHEN duplicate_object THEN NULL; END $$;
