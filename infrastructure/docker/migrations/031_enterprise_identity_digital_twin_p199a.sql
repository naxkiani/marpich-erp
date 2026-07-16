-- Enterprise Identity Digital Twin Platform — Prompt 199-A expansion (ADR-203a)
-- Extends schema identity_twin from migration 029. Production-ready DDL.

CREATE SCHEMA IF NOT EXISTS identity_twin;

-- Kind catalog (metadata-driven twin types)
CREATE TABLE IF NOT EXISTS identity_twin.twin_kinds (
    tenant_id VARCHAR(63) NOT NULL,
    kind VARCHAR(128) NOT NULL,
    label VARCHAR(256) NOT NULL,
    subject_context VARCHAR(128) NOT NULL,
    facets JSONB NOT NULL DEFAULT '[]',
    constraints JSONB NOT NULL DEFAULT '[]',
    schema_version INT NOT NULL DEFAULT 1,
    enabled BOOLEAN NOT NULL DEFAULT TRUE,
    metadata JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tenant_id, kind)
);

-- Expand digital_twins for multi-kind subjects (compat columns retained)
ALTER TABLE identity_twin.digital_twins
    ADD COLUMN IF NOT EXISTS kind VARCHAR(128) NOT NULL DEFAULT 'identity.user',
    ADD COLUMN IF NOT EXISTS subject_ref VARCHAR(128),
    ADD COLUMN IF NOT EXISTS lifecycle VARCHAR(64) NOT NULL DEFAULT 'active',
    ADD COLUMN IF NOT EXISTS health_score NUMERIC(5,2),
    ADD COLUMN IF NOT EXISTS metadata JSONB NOT NULL DEFAULT '{}';

UPDATE identity_twin.digital_twins
SET subject_ref = identity_ref
WHERE subject_ref IS NULL;

CREATE UNIQUE INDEX IF NOT EXISTS uq_twin_kind_subject
    ON identity_twin.digital_twins (tenant_id, kind, subject_ref);

CREATE INDEX IF NOT EXISTS idx_twins_kind_updated
    ON identity_twin.digital_twins (tenant_id, kind, updated_at DESC);

CREATE TABLE IF NOT EXISTS identity_twin.twin_states (
    tenant_id VARCHAR(63) NOT NULL,
    twin_ref VARCHAR(64) NOT NULL,
    facet VARCHAR(64) NOT NULL,
    state JSONB NOT NULL DEFAULT '{}',
    schema_version INT NOT NULL DEFAULT 1,
    source_event VARCHAR(128),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tenant_id, twin_ref, facet)
);

CREATE TABLE IF NOT EXISTS identity_twin.twin_versions (
    tenant_id VARCHAR(63) NOT NULL,
    id UUID NOT NULL,
    twin_ref VARCHAR(64) NOT NULL,
    version BIGINT NOT NULL,
    snapshot_ref VARCHAR(64),
    change_summary JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tenant_id, id),
    UNIQUE (tenant_id, twin_ref, version)
);

CREATE TABLE IF NOT EXISTS identity_twin.twin_events (
    tenant_id VARCHAR(63) NOT NULL,
    id UUID NOT NULL,
    twin_ref VARCHAR(64),
    event_name VARCHAR(128) NOT NULL,
    event_id VARCHAR(64) NOT NULL,
    payload JSONB NOT NULL DEFAULT '{}',
    occurred_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tenant_id, id),
    UNIQUE (tenant_id, event_id)
);

CREATE INDEX IF NOT EXISTS idx_twin_events_occurred
    ON identity_twin.twin_events (tenant_id, occurred_at DESC);

CREATE TABLE IF NOT EXISTS identity_twin.twin_relationships (
    tenant_id VARCHAR(63) NOT NULL,
    id UUID NOT NULL,
    edge_ref VARCHAR(64) NOT NULL,
    from_twin_ref VARCHAR(64) NOT NULL,
    to_twin_ref VARCHAR(64) NOT NULL,
    edge_type VARCHAR(64) NOT NULL,
    metadata JSONB NOT NULL DEFAULT '{}',
    active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tenant_id, id),
    UNIQUE (tenant_id, edge_ref)
);

CREATE INDEX IF NOT EXISTS idx_twin_rel_from
    ON identity_twin.twin_relationships (tenant_id, from_twin_ref, edge_type);
CREATE INDEX IF NOT EXISTS idx_twin_rel_to
    ON identity_twin.twin_relationships (tenant_id, to_twin_ref, edge_type);

CREATE TABLE IF NOT EXISTS identity_twin.twin_metadata (
    tenant_id VARCHAR(63) NOT NULL,
    twin_ref VARCHAR(64) NOT NULL,
    tags JSONB NOT NULL DEFAULT '[]',
    labels JSONB NOT NULL DEFAULT '{}',
    classification VARCHAR(64),
    region VARCHAR(64),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tenant_id, twin_ref)
);

CREATE TABLE IF NOT EXISTS identity_twin.twin_health (
    tenant_id VARCHAR(63) NOT NULL,
    twin_ref VARCHAR(64) NOT NULL,
    score NUMERIC(5,2) NOT NULL DEFAULT 100,
    sync_lag_seconds INT NOT NULL DEFAULT 0,
    completeness NUMERIC(5,2) NOT NULL DEFAULT 100,
    status VARCHAR(32) NOT NULL DEFAULT 'healthy',
    details JSONB NOT NULL DEFAULT '{}',
    checked_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tenant_id, twin_ref)
);

CREATE TABLE IF NOT EXISTS identity_twin.twin_risk (
    tenant_id VARCHAR(63) NOT NULL,
    twin_ref VARCHAR(64) NOT NULL,
    score NUMERIC(5,2),
    band VARCHAR(32),
    signal_refs JSONB NOT NULL DEFAULT '[]',
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tenant_id, twin_ref)
);

CREATE TABLE IF NOT EXISTS identity_twin.twin_trust (
    tenant_id VARCHAR(63) NOT NULL,
    twin_ref VARCHAR(64) NOT NULL,
    score NUMERIC(5,2),
    band VARCHAR(32),
    signal_refs JSONB NOT NULL DEFAULT '[]',
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tenant_id, twin_ref)
);

CREATE TABLE IF NOT EXISTS identity_twin.twin_predictions (
    tenant_id VARCHAR(63) NOT NULL,
    id UUID NOT NULL,
    prediction_ref VARCHAR(64) NOT NULL,
    twin_ref VARCHAR(64) NOT NULL,
    horizon VARCHAR(64) NOT NULL,
    outcome JSONB NOT NULL DEFAULT '{}',
    confidence NUMERIC(5,4),
    explanation_ref VARCHAR(128),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tenant_id, id),
    UNIQUE (tenant_id, prediction_ref)
);

CREATE INDEX IF NOT EXISTS idx_twin_predictions_twin
    ON identity_twin.twin_predictions (tenant_id, twin_ref, created_at DESC);

CREATE TABLE IF NOT EXISTS identity_twin.twin_policies (
    tenant_id VARCHAR(63) NOT NULL,
    twin_ref VARCHAR(64) NOT NULL,
    policy_key VARCHAR(128) NOT NULL,
    parameters JSONB NOT NULL DEFAULT '{}',
    evaluated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tenant_id, twin_ref, policy_key)
);

CREATE TABLE IF NOT EXISTS identity_twin.twin_audits (
    tenant_id VARCHAR(63) NOT NULL,
    id UUID NOT NULL,
    twin_ref VARCHAR(64),
    action VARCHAR(128) NOT NULL,
    actor_id VARCHAR(128),
    details JSONB NOT NULL DEFAULT '{}',
    occurred_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tenant_id, id)
);

CREATE INDEX IF NOT EXISTS idx_twin_audits_twin
    ON identity_twin.twin_audits (tenant_id, twin_ref, occurred_at DESC);

-- RLS (enable in environments that set app.tenant_id)
ALTER TABLE identity_twin.twin_kinds ENABLE ROW LEVEL SECURITY;
ALTER TABLE identity_twin.twin_states ENABLE ROW LEVEL SECURITY;
ALTER TABLE identity_twin.twin_versions ENABLE ROW LEVEL SECURITY;
ALTER TABLE identity_twin.twin_events ENABLE ROW LEVEL SECURITY;
ALTER TABLE identity_twin.twin_relationships ENABLE ROW LEVEL SECURITY;
ALTER TABLE identity_twin.twin_metadata ENABLE ROW LEVEL SECURITY;
ALTER TABLE identity_twin.twin_health ENABLE ROW LEVEL SECURITY;
ALTER TABLE identity_twin.twin_risk ENABLE ROW LEVEL SECURITY;
ALTER TABLE identity_twin.twin_trust ENABLE ROW LEVEL SECURITY;
ALTER TABLE identity_twin.twin_predictions ENABLE ROW LEVEL SECURITY;
ALTER TABLE identity_twin.twin_policies ENABLE ROW LEVEL SECURITY;
ALTER TABLE identity_twin.twin_audits ENABLE ROW LEVEL SECURITY;
