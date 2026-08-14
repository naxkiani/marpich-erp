-- Enterprise Directory Service (SAML / LDAP / SCIM) — schema isolated from identity.*
-- Migration 018 — tenant-scoped RLS via app.tenant_id

CREATE SCHEMA IF NOT EXISTS directory;

CREATE TABLE IF NOT EXISTS directory.profiles (
    tenant_id VARCHAR(63) NOT NULL,
    id UUID NOT NULL,
    profile_ref VARCHAR(64) NOT NULL,
    saml_enabled BOOLEAN NOT NULL DEFAULT TRUE,
    ldap_enabled BOOLEAN NOT NULL DEFAULT TRUE,
    scim_enabled BOOLEAN NOT NULL DEFAULT TRUE,
    auto_provision BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tenant_id, id),
    UNIQUE (tenant_id, profile_ref)
);

CREATE INDEX IF NOT EXISTS idx_directory_profiles_tenant
    ON directory.profiles (tenant_id);

CREATE TABLE IF NOT EXISTS directory.saml_providers (
    tenant_id VARCHAR(63) NOT NULL,
    id UUID NOT NULL,
    provider_ref VARCHAR(64) NOT NULL,
    name VARCHAR(256) NOT NULL,
    entity_id VARCHAR(512) NOT NULL,
    sso_url VARCHAR(1024) NOT NULL,
    x509_cert TEXT NOT NULL DEFAULT '',
    enabled BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tenant_id, id),
    UNIQUE (tenant_id, provider_ref)
);

CREATE INDEX IF NOT EXISTS idx_directory_saml_tenant
    ON directory.saml_providers (tenant_id, enabled);

CREATE TABLE IF NOT EXISTS directory.ldap_connectors (
    tenant_id VARCHAR(63) NOT NULL,
    id UUID NOT NULL,
    connector_ref VARCHAR(64) NOT NULL,
    name VARCHAR(256) NOT NULL,
    host VARCHAR(256) NOT NULL,
    port INT NOT NULL DEFAULT 389,
    bind_dn VARCHAR(512) NOT NULL DEFAULT '',
    bind_password TEXT NOT NULL DEFAULT '',
    base_dn VARCHAR(512) NOT NULL DEFAULT '',
    user_filter VARCHAR(256) NOT NULL DEFAULT '(objectClass=person)',
    enabled BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tenant_id, id),
    UNIQUE (tenant_id, connector_ref)
);

CREATE INDEX IF NOT EXISTS idx_directory_ldap_tenant
    ON directory.ldap_connectors (tenant_id, enabled);

CREATE TABLE IF NOT EXISTS directory.scim_providers (
    tenant_id VARCHAR(63) NOT NULL,
    id UUID NOT NULL,
    provider_ref VARCHAR(64) NOT NULL,
    name VARCHAR(256) NOT NULL,
    bearer_token TEXT NOT NULL DEFAULT '',
    enabled BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tenant_id, id),
    UNIQUE (tenant_id, provider_ref)
);

CREATE INDEX IF NOT EXISTS idx_directory_scim_tenant
    ON directory.scim_providers (tenant_id, enabled);

CREATE TABLE IF NOT EXISTS directory.sync_jobs (
    tenant_id VARCHAR(63) NOT NULL,
    id UUID NOT NULL,
    job_ref VARCHAR(64) NOT NULL,
    source_type VARCHAR(32) NOT NULL,
    source_ref VARCHAR(64) NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'pending',
    users_synced INT NOT NULL DEFAULT 0,
    users_created INT NOT NULL DEFAULT 0,
    error_message TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMPTZ,
    PRIMARY KEY (tenant_id, id),
    UNIQUE (tenant_id, job_ref)
);

CREATE INDEX IF NOT EXISTS idx_directory_sync_tenant_status
    ON directory.sync_jobs (tenant_id, status);

CREATE TABLE IF NOT EXISTS directory.saml_relay_states (
    tenant_id VARCHAR(63) NOT NULL,
    relay_state VARCHAR(256) NOT NULL,
    payload JSONB NOT NULL DEFAULT '{}',
    expires_at TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tenant_id, relay_state)
);

CREATE INDEX IF NOT EXISTS idx_directory_relay_expires
    ON directory.saml_relay_states (expires_at);

CREATE TABLE IF NOT EXISTS directory.ref_counters (
    tenant_id VARCHAR(63) NOT NULL,
    prefix VARCHAR(64) NOT NULL,
    next_value INT NOT NULL DEFAULT 1,
    PRIMARY KEY (tenant_id, prefix)
);

ALTER TABLE directory.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE directory.saml_providers ENABLE ROW LEVEL SECURITY;
ALTER TABLE directory.ldap_connectors ENABLE ROW LEVEL SECURITY;
ALTER TABLE directory.scim_providers ENABLE ROW LEVEL SECURITY;
ALTER TABLE directory.sync_jobs ENABLE ROW LEVEL SECURITY;
ALTER TABLE directory.saml_relay_states ENABLE ROW LEVEL SECURITY;
ALTER TABLE directory.ref_counters ENABLE ROW LEVEL SECURITY;

DO $$ BEGIN
    CREATE POLICY directory_profiles_tenant ON directory.profiles
        USING (tenant_id = current_setting('app.tenant_id', true));
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE POLICY directory_saml_tenant ON directory.saml_providers
        USING (tenant_id = current_setting('app.tenant_id', true));
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE POLICY directory_ldap_tenant ON directory.ldap_connectors
        USING (tenant_id = current_setting('app.tenant_id', true));
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE POLICY directory_scim_tenant ON directory.scim_providers
        USING (tenant_id = current_setting('app.tenant_id', true));
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE POLICY directory_sync_tenant ON directory.sync_jobs
        USING (tenant_id = current_setting('app.tenant_id', true));
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE POLICY directory_relay_tenant ON directory.saml_relay_states
        USING (tenant_id = current_setting('app.tenant_id', true));
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE POLICY directory_ref_tenant ON directory.ref_counters
        USING (tenant_id = current_setting('app.tenant_id', true));
EXCEPTION WHEN duplicate_object THEN NULL; END $$;
