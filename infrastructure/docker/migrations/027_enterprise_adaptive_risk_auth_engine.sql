-- Adaptive risk auth engine — Identity Risk SoR
-- Migration 027 — schema identity_risk (not identity.*)

CREATE SCHEMA IF NOT EXISTS identity_risk;

CREATE TABLE IF NOT EXISTS identity_risk.profiles (
    tenant_id VARCHAR(63) NOT NULL,
    id UUID NOT NULL,
    profile_ref VARCHAR(64) NOT NULL,
    scoring_enabled BOOLEAN NOT NULL DEFAULT TRUE,
    score_threshold INT NOT NULL DEFAULT 50,
    step_up_threshold INT NOT NULL DEFAULT 75,
    bulk_create_threshold INT NOT NULL DEFAULT 10,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tenant_id, id),
    UNIQUE (tenant_id, profile_ref)
);

CREATE INDEX IF NOT EXISTS idx_identity_risk_profiles_tenant
    ON identity_risk.profiles (tenant_id);

CREATE TABLE IF NOT EXISTS identity_risk.signals (
    tenant_id VARCHAR(63) NOT NULL,
    id UUID NOT NULL,
    signal_ref VARCHAR(64) NOT NULL,
    source VARCHAR(32) NOT NULL,
    event_name VARCHAR(128) NOT NULL,
    user_id VARCHAR(128),
    factors JSONB NOT NULL DEFAULT '[]',
    raw_payload JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tenant_id, id),
    UNIQUE (tenant_id, signal_ref)
);

CREATE INDEX IF NOT EXISTS idx_identity_risk_signals_tenant
    ON identity_risk.signals (tenant_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_identity_risk_signals_user
    ON identity_risk.signals (tenant_id, user_id);

CREATE TABLE IF NOT EXISTS identity_risk.scores (
    tenant_id VARCHAR(63) NOT NULL,
    id UUID NOT NULL,
    score_ref VARCHAR(64) NOT NULL,
    signal_ref VARCHAR(64) NOT NULL,
    score INT NOT NULL,
    risk_level VARCHAR(16) NOT NULL,
    explanation TEXT NOT NULL DEFAULT '',
    factors JSONB NOT NULL DEFAULT '[]',
    step_up_recommended BOOLEAN NOT NULL DEFAULT FALSE,
    user_id VARCHAR(128),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tenant_id, id),
    UNIQUE (tenant_id, score_ref)
);

CREATE INDEX IF NOT EXISTS idx_identity_risk_scores_tenant
    ON identity_risk.scores (tenant_id, created_at DESC);

CREATE TABLE IF NOT EXISTS identity_risk.alerts (
    tenant_id VARCHAR(63) NOT NULL,
    id UUID NOT NULL,
    alert_ref VARCHAR(64) NOT NULL,
    score_ref VARCHAR(64) NOT NULL,
    title VARCHAR(256) NOT NULL,
    severity VARCHAR(16) NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    acknowledged BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tenant_id, id),
    UNIQUE (tenant_id, alert_ref)
);

CREATE INDEX IF NOT EXISTS idx_identity_risk_alerts_tenant
    ON identity_risk.alerts (tenant_id, acknowledged, created_at DESC);

CREATE TABLE IF NOT EXISTS identity_risk.ref_counters (
    tenant_id VARCHAR(63) NOT NULL,
    prefix VARCHAR(64) NOT NULL,
    next_value INT NOT NULL DEFAULT 1,
    PRIMARY KEY (tenant_id, prefix)
);

ALTER TABLE identity_risk.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE identity_risk.signals ENABLE ROW LEVEL SECURITY;
ALTER TABLE identity_risk.scores ENABLE ROW LEVEL SECURITY;
ALTER TABLE identity_risk.alerts ENABLE ROW LEVEL SECURITY;
ALTER TABLE identity_risk.ref_counters ENABLE ROW LEVEL SECURITY;

DO $$ BEGIN
    CREATE POLICY identity_risk_profiles_tenant ON identity_risk.profiles
        USING (tenant_id = current_setting('app.tenant_id', true));
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE POLICY identity_risk_signals_tenant ON identity_risk.signals
        USING (tenant_id = current_setting('app.tenant_id', true));
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE POLICY identity_risk_scores_tenant ON identity_risk.scores
        USING (tenant_id = current_setting('app.tenant_id', true));
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE POLICY identity_risk_alerts_tenant ON identity_risk.alerts
        USING (tenant_id = current_setting('app.tenant_id', true));
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE POLICY identity_risk_ref_tenant ON identity_risk.ref_counters
        USING (tenant_id = current_setting('app.tenant_id', true));
EXCEPTION WHEN duplicate_object THEN NULL; END $$;
