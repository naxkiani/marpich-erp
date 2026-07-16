-- Phase P5 — PostgreSQL RLS + principal HASH partitioning
-- Applies tenant isolation policies and principals registry for MEIAAP

CREATE SCHEMA IF NOT EXISTS authorization;

-- Unified principals registry (users + service principals), HASH partitioned by tenant_id
CREATE TABLE IF NOT EXISTS identity.principals (
    tenant_id VARCHAR(63) NOT NULL,
    id UUID NOT NULL,
    principal_ref VARCHAR(64) NOT NULL,
    principal_type VARCHAR(32) NOT NULL CHECK (principal_type IN ('user', 'service')),
    email VARCHAR(256),
    display_name VARCHAR(128) NOT NULL DEFAULT '',
    status VARCHAR(32) NOT NULL DEFAULT 'active',
    partition_bucket INT NOT NULL,
    metadata JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tenant_id, id)
) PARTITION BY HASH (tenant_id);

DO $$
DECLARE
    i INT;
    partition_count INT := 8;
BEGIN
    FOR i IN 0..(partition_count - 1) LOOP
        EXECUTE format(
            'CREATE TABLE IF NOT EXISTS identity.principals_p%s PARTITION OF identity.principals FOR VALUES WITH (MODULUS %s, REMAINDER %s)',
            lpad(i::text, 2, '0'),
            partition_count,
            i
        );
    END LOOP;
END $$;

CREATE INDEX IF NOT EXISTS idx_principals_tenant_ref ON identity.principals(tenant_id, principal_ref);
CREATE INDEX IF NOT EXISTS idx_principals_email ON identity.principals(tenant_id, email);

-- Access decisions (authorization PDP) — RANGE partitioned by decided_at (monthly parent)
CREATE TABLE IF NOT EXISTS authorization.access_decisions (
    tenant_id VARCHAR(63) NOT NULL,
    id UUID NOT NULL,
    decision_ref VARCHAR(64) NOT NULL,
    principal_id UUID NOT NULL,
    resource VARCHAR(512) NOT NULL DEFAULT '',
    action VARCHAR(128) NOT NULL DEFAULT '',
    permission_code VARCHAR(256),
    decision VARCHAR(16) NOT NULL,
    reason TEXT,
    decided_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    context JSONB NOT NULL DEFAULT '{}',
    PRIMARY KEY (tenant_id, id, decided_at)
) PARTITION BY RANGE (decided_at);

CREATE TABLE IF NOT EXISTS authorization.access_decisions_default
    PARTITION OF authorization.access_decisions DEFAULT;

CREATE INDEX IF NOT EXISTS idx_access_decisions_tenant_principal
    ON authorization.access_decisions(tenant_id, principal_id, decided_at DESC);

-- RLS helper
CREATE OR REPLACE FUNCTION identity.current_tenant_id() RETURNS TEXT AS $$
    SELECT NULLIF(current_setting('app.tenant_id', true), '');
$$ LANGUAGE SQL STABLE;

-- Enable RLS on identity tenant-scoped tables
ALTER TABLE IF EXISTS identity.users ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS identity.roles ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS identity.sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS identity.principals ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS authorization.access_decisions ENABLE ROW LEVEL SECURITY;

ALTER TABLE IF EXISTS identity.users FORCE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS identity.roles FORCE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS identity.sessions FORCE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS identity.principals FORCE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS authorization.access_decisions FORCE ROW LEVEL SECURITY;

DO $$ BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_policies WHERE schemaname = 'identity' AND tablename = 'users' AND policyname = 'tenant_isolation_users'
    ) THEN
        CREATE POLICY tenant_isolation_users ON identity.users
            USING (tenant_id = identity.current_tenant_id())
            WITH CHECK (tenant_id = identity.current_tenant_id());
    END IF;
END $$;

DO $$ BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_policies WHERE schemaname = 'identity' AND tablename = 'roles' AND policyname = 'tenant_isolation_roles'
    ) THEN
        CREATE POLICY tenant_isolation_roles ON identity.roles
            USING (tenant_id = identity.current_tenant_id())
            WITH CHECK (tenant_id = identity.current_tenant_id());
    END IF;
END $$;

DO $$ BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_policies WHERE schemaname = 'identity' AND tablename = 'sessions' AND policyname = 'tenant_isolation_sessions'
    ) THEN
        CREATE POLICY tenant_isolation_sessions ON identity.sessions
            USING (tenant_id = identity.current_tenant_id())
            WITH CHECK (tenant_id = identity.current_tenant_id());
    END IF;
END $$;

DO $$ BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_policies WHERE schemaname = 'identity' AND tablename = 'principals' AND policyname = 'tenant_isolation_principals'
    ) THEN
        CREATE POLICY tenant_isolation_principals ON identity.principals
            USING (tenant_id = identity.current_tenant_id())
            WITH CHECK (tenant_id = identity.current_tenant_id());
    END IF;
END $$;

DO $$ BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_policies WHERE schemaname = 'authorization' AND tablename = 'access_decisions' AND policyname = 'tenant_isolation_access_decisions'
    ) THEN
        CREATE POLICY tenant_isolation_access_decisions ON authorization.access_decisions
            USING (tenant_id = identity.current_tenant_id())
            WITH CHECK (tenant_id = identity.current_tenant_id());
    END IF;
END $$;
