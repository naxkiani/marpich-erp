-- Enterprise Identity Federation & SSO Platform — P198 Part A
-- Migration 028 — extends federation schema (017)

CREATE SCHEMA IF NOT EXISTS federation;

-- Extend identity_providers protocol constraint for all pluggable provider types
ALTER TABLE federation.identity_providers DROP CONSTRAINT IF EXISTS identity_providers_protocol_check;
ALTER TABLE federation.identity_providers ADD CONSTRAINT identity_providers_protocol_check
    CHECK (protocol IN (
        'oidc', 'saml', 'ldap', 'azure_ad', 'entra_id', 'ad', 'google', 'apple',
        'github', 'gitlab', 'keycloak', 'okta', 'auth0', 'cognito', 'government_eid',
        'university', 'hospital', 'bank', 'tax_authority', 'national_digital_id',
        'custom', 'legacy', 'partner', 'scim'
    ));

CREATE TABLE IF NOT EXISTS federation.federation_partners (
    tenant_id VARCHAR(63) NOT NULL,
    id UUID NOT NULL,
    partner_ref VARCHAR(64) NOT NULL,
    name VARCHAR(256) NOT NULL,
    partner_type VARCHAR(64) NOT NULL DEFAULT 'organization',
    trust_level VARCHAR(32) NOT NULL DEFAULT 'medium',
    metadata JSONB NOT NULL DEFAULT '{}',
    enabled BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tenant_id, id),
    UNIQUE (tenant_id, partner_ref)
);

CREATE TABLE IF NOT EXISTS federation.trust_relationships (
    tenant_id VARCHAR(63) NOT NULL,
    id UUID NOT NULL,
    trust_ref VARCHAR(64) NOT NULL,
    source_entity_type VARCHAR(32) NOT NULL,
    source_entity_id VARCHAR(128) NOT NULL,
    target_entity_type VARCHAR(32) NOT NULL,
    target_entity_id VARCHAR(128) NOT NULL,
    trust_score INT NOT NULL DEFAULT 50,
    trust_level VARCHAR(16) NOT NULL DEFAULT 'medium',
    status VARCHAR(32) NOT NULL DEFAULT 'active',
    valid_from TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    valid_until TIMESTAMPTZ,
    metadata JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tenant_id, id),
    UNIQUE (tenant_id, trust_ref)
);

CREATE INDEX IF NOT EXISTS idx_federation_trust_source
    ON federation.trust_relationships(tenant_id, source_entity_type, source_entity_id);
CREATE INDEX IF NOT EXISTS idx_federation_trust_target
    ON federation.trust_relationships(tenant_id, target_entity_type, target_entity_id);

CREATE TABLE IF NOT EXISTS federation.claims_mappings (
    tenant_id VARCHAR(63) NOT NULL,
    id UUID NOT NULL,
    mapping_ref VARCHAR(64) NOT NULL,
    provider_id UUID NOT NULL,
    source_claim VARCHAR(128) NOT NULL,
    target_claim VARCHAR(128) NOT NULL,
    transform_type VARCHAR(32) NOT NULL DEFAULT 'direct',
    transform_config JSONB NOT NULL DEFAULT '{}',
    enabled BOOLEAN NOT NULL DEFAULT TRUE,
    priority INT NOT NULL DEFAULT 100,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tenant_id, id),
    UNIQUE (tenant_id, mapping_ref)
);

CREATE TABLE IF NOT EXISTS federation.attribute_mappings (
    tenant_id VARCHAR(63) NOT NULL,
    id UUID NOT NULL,
    mapping_ref VARCHAR(64) NOT NULL,
    provider_id UUID NOT NULL,
    external_attribute VARCHAR(128) NOT NULL,
    internal_attribute VARCHAR(128) NOT NULL,
    required BOOLEAN NOT NULL DEFAULT FALSE,
    default_value VARCHAR(512),
    transform JSONB NOT NULL DEFAULT '{}',
    enabled BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tenant_id, id),
    UNIQUE (tenant_id, mapping_ref)
);

CREATE TABLE IF NOT EXISTS federation.provisioning_policies (
    tenant_id VARCHAR(63) NOT NULL,
    id UUID NOT NULL,
    policy_ref VARCHAR(64) NOT NULL,
    provider_id UUID,
    jit_enabled BOOLEAN NOT NULL DEFAULT TRUE,
    auto_role_assignment BOOLEAN NOT NULL DEFAULT FALSE,
    default_roles JSONB NOT NULL DEFAULT '[]',
    sync_mode VARCHAR(32) NOT NULL DEFAULT 'jit',
    rules JSONB NOT NULL DEFAULT '[]',
    enabled BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tenant_id, id),
    UNIQUE (tenant_id, policy_ref)
);

CREATE TABLE IF NOT EXISTS federation.synchronization_jobs (
    tenant_id VARCHAR(63) NOT NULL,
    id UUID NOT NULL,
    job_ref VARCHAR(64) NOT NULL,
    provider_id UUID NOT NULL,
    direction VARCHAR(16) NOT NULL DEFAULT 'inbound',
    status VARCHAR(32) NOT NULL DEFAULT 'pending',
    records_processed INT NOT NULL DEFAULT 0,
    records_failed INT NOT NULL DEFAULT 0,
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    error_message TEXT,
    metadata JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tenant_id, id),
    UNIQUE (tenant_id, job_ref)
);

CREATE TABLE IF NOT EXISTS federation.identity_links (
    tenant_id VARCHAR(63) NOT NULL,
    id UUID NOT NULL,
    link_ref VARCHAR(64) NOT NULL,
    user_id UUID NOT NULL,
    provider_id UUID NOT NULL,
    external_subject VARCHAR(256) NOT NULL,
    link_status VARCHAR(32) NOT NULL DEFAULT 'active',
    linked_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_used_at TIMESTAMPTZ,
    metadata JSONB NOT NULL DEFAULT '{}',
    PRIMARY KEY (tenant_id, id),
    UNIQUE (tenant_id, link_ref),
    UNIQUE (tenant_id, provider_id, external_subject)
);

CREATE INDEX IF NOT EXISTS idx_federation_links_user
    ON federation.identity_links(tenant_id, user_id);

CREATE TABLE IF NOT EXISTS federation.external_accounts (
    tenant_id VARCHAR(63) NOT NULL,
    id UUID NOT NULL,
    account_ref VARCHAR(64) NOT NULL,
    provider_id UUID NOT NULL,
    external_id VARCHAR(256) NOT NULL,
    email VARCHAR(320),
    display_name VARCHAR(256),
    attributes JSONB NOT NULL DEFAULT '{}',
    status VARCHAR(32) NOT NULL DEFAULT 'active',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tenant_id, id),
    UNIQUE (tenant_id, account_ref),
    UNIQUE (tenant_id, provider_id, external_id)
);

CREATE TABLE IF NOT EXISTS federation.federation_sessions (
    tenant_id VARCHAR(63) NOT NULL,
    id UUID NOT NULL,
    session_ref VARCHAR(64) NOT NULL,
    user_id UUID,
    provider_id UUID NOT NULL,
    protocol VARCHAR(32) NOT NULL,
    idp_session_id VARCHAR(256),
    status VARCHAR(32) NOT NULL DEFAULT 'active',
    ip_address INET,
    user_agent TEXT,
    expires_at TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tenant_id, id, created_at)
) PARTITION BY RANGE (created_at);

CREATE TABLE IF NOT EXISTS federation.federation_sessions_default
    PARTITION OF federation.federation_sessions DEFAULT;

CREATE TABLE IF NOT EXISTS federation.identity_tokens (
    tenant_id VARCHAR(63) NOT NULL,
    id UUID NOT NULL,
    token_ref VARCHAR(64) NOT NULL,
    session_ref VARCHAR(64) NOT NULL,
    token_type VARCHAR(32) NOT NULL DEFAULT 'id_token',
    token_hash VARCHAR(256) NOT NULL,
    issued_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    expires_at TIMESTAMPTZ NOT NULL,
    claims JSONB NOT NULL DEFAULT '{}',
    PRIMARY KEY (tenant_id, id, issued_at)
) PARTITION BY RANGE (issued_at);

CREATE TABLE IF NOT EXISTS federation.identity_tokens_default
    PARTITION OF federation.identity_tokens DEFAULT;

CREATE TABLE IF NOT EXISTS federation.identity_metadata (
    tenant_id VARCHAR(63) NOT NULL,
    id UUID NOT NULL,
    entity_type VARCHAR(32) NOT NULL,
    entity_id VARCHAR(128) NOT NULL,
    metadata_key VARCHAR(128) NOT NULL,
    metadata_value JSONB NOT NULL DEFAULT '{}',
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tenant_id, id),
    UNIQUE (tenant_id, entity_type, entity_id, metadata_key)
);

CREATE TABLE IF NOT EXISTS federation.directory_servers (
    tenant_id VARCHAR(63) NOT NULL,
    id UUID NOT NULL,
    server_ref VARCHAR(64) NOT NULL,
    server_type VARCHAR(32) NOT NULL DEFAULT 'ldap',
    host VARCHAR(256) NOT NULL,
    port INT NOT NULL DEFAULT 389,
    base_dn VARCHAR(512),
    bind_config JSONB NOT NULL DEFAULT '{}',
    tls_enabled BOOLEAN NOT NULL DEFAULT TRUE,
    enabled BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tenant_id, id),
    UNIQUE (tenant_id, server_ref)
);

CREATE TABLE IF NOT EXISTS federation.federation_audit (
    tenant_id VARCHAR(63) NOT NULL,
    id UUID NOT NULL,
    audit_ref VARCHAR(64) NOT NULL,
    event_type VARCHAR(64) NOT NULL,
    actor_id VARCHAR(128),
    resource_type VARCHAR(64),
    resource_id VARCHAR(128),
    payload JSONB NOT NULL DEFAULT '{}',
    ip_address INET,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tenant_id, id, created_at)
) PARTITION BY RANGE (created_at);

CREATE TABLE IF NOT EXISTS federation.federation_audit_default
    PARTITION OF federation.federation_audit DEFAULT;

CREATE TABLE IF NOT EXISTS federation.tenant_federation (
    tenant_id VARCHAR(63) NOT NULL,
    id UUID NOT NULL,
    federation_ref VARCHAR(64) NOT NULL,
    federation_mode VARCHAR(32) NOT NULL DEFAULT 'dedicated',
    partner_tenant_id VARCHAR(63),
    region VARCHAR(32),
    shared_providers JSONB NOT NULL DEFAULT '[]',
    enabled BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tenant_id, id),
    UNIQUE (tenant_id, federation_ref)
);

CREATE TABLE IF NOT EXISTS federation.federation_policies (
    tenant_id VARCHAR(63) NOT NULL,
    id UUID NOT NULL,
    policy_ref VARCHAR(64) NOT NULL,
    policy_key VARCHAR(128) NOT NULL,
    policy_value JSONB NOT NULL DEFAULT '{}',
    enabled BOOLEAN NOT NULL DEFAULT TRUE,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tenant_id, id),
    UNIQUE (tenant_id, policy_ref),
    UNIQUE (tenant_id, policy_key)
);

CREATE TABLE IF NOT EXISTS federation.federation_events (
    tenant_id VARCHAR(63) NOT NULL,
    id UUID NOT NULL,
    event_ref VARCHAR(64) NOT NULL,
    event_name VARCHAR(128) NOT NULL,
    source VARCHAR(64) NOT NULL DEFAULT 'federation_engine',
    payload JSONB NOT NULL DEFAULT '{}',
    correlation_id VARCHAR(64),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tenant_id, id, created_at)
) PARTITION BY RANGE (created_at);

CREATE TABLE IF NOT EXISTS federation.federation_events_default
    PARTITION OF federation.federation_events DEFAULT;

-- Row-Level Security
ALTER TABLE federation.federation_partners ENABLE ROW LEVEL SECURITY;
ALTER TABLE federation.trust_relationships ENABLE ROW LEVEL SECURITY;
ALTER TABLE federation.claims_mappings ENABLE ROW LEVEL SECURITY;
ALTER TABLE federation.attribute_mappings ENABLE ROW LEVEL SECURITY;
ALTER TABLE federation.provisioning_policies ENABLE ROW LEVEL SECURITY;
ALTER TABLE federation.synchronization_jobs ENABLE ROW LEVEL SECURITY;
ALTER TABLE federation.identity_links ENABLE ROW LEVEL SECURITY;
ALTER TABLE federation.external_accounts ENABLE ROW LEVEL SECURITY;
ALTER TABLE federation.federation_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE federation.identity_tokens ENABLE ROW LEVEL SECURITY;
ALTER TABLE federation.identity_metadata ENABLE ROW LEVEL SECURITY;
ALTER TABLE federation.directory_servers ENABLE ROW LEVEL SECURITY;
ALTER TABLE federation.federation_audit ENABLE ROW LEVEL SECURITY;
ALTER TABLE federation.tenant_federation ENABLE ROW LEVEL SECURITY;
ALTER TABLE federation.federation_policies ENABLE ROW LEVEL SECURITY;
ALTER TABLE federation.federation_events ENABLE ROW LEVEL SECURITY;

CREATE POLICY federation_tenant_isolation ON federation.federation_partners
    USING (tenant_id = current_setting('app.current_tenant', true));
CREATE POLICY federation_trust_tenant ON federation.trust_relationships
    USING (tenant_id = current_setting('app.current_tenant', true));
CREATE POLICY federation_links_tenant ON federation.identity_links
    USING (tenant_id = current_setting('app.current_tenant', true));
CREATE POLICY federation_audit_tenant ON federation.federation_audit
    USING (tenant_id = current_setting('app.current_tenant', true));
