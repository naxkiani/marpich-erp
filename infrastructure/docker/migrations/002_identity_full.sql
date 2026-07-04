-- Identity Service v2 — RBAC, ABAC, MFA, Sessions
-- Every table includes tenant_id for multi-tenant isolation

-- Rename tenant_slug → tenant_id on existing tables (idempotent)
DO $$ BEGIN
  IF EXISTS (
    SELECT 1 FROM information_schema.columns
    WHERE table_schema = 'identity' AND table_name = 'users' AND column_name = 'tenant_slug'
  ) THEN
    ALTER TABLE identity.users RENAME COLUMN tenant_slug TO tenant_id;
  END IF;
END $$;

ALTER TABLE identity.users
  ADD COLUMN IF NOT EXISTS locale VARCHAR(16) NOT NULL DEFAULT 'en-US',
  ADD COLUMN IF NOT EXISTS attributes JSONB NOT NULL DEFAULT '{}',
  ADD COLUMN IF NOT EXISTS mfa_secret VARCHAR(256),
  ADD COLUMN IF NOT EXISTS backup_codes JSONB NOT NULL DEFAULT '[]',
  ADD COLUMN IF NOT EXISTS last_login_at TIMESTAMPTZ,
  ADD COLUMN IF NOT EXISTS failed_login_attempts INT NOT NULL DEFAULT 0,
  ADD COLUMN IF NOT EXISTS locked_until TIMESTAMPTZ;

CREATE INDEX IF NOT EXISTS idx_users_tenant_id ON identity.users(tenant_id);
CREATE INDEX IF NOT EXISTS idx_users_email ON identity.users(tenant_id, email);

-- Roles (tenant-scoped)
CREATE TABLE IF NOT EXISTS identity.roles (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    code VARCHAR(64) NOT NULL,
    name VARCHAR(128) NOT NULL,
    description TEXT,
    is_system BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (tenant_id, code)
);

CREATE INDEX IF NOT EXISTS idx_roles_tenant ON identity.roles(tenant_id);

-- Permissions (global catalog, seeded once)
CREATE TABLE IF NOT EXISTS identity.permissions (
    id UUID PRIMARY KEY,
    code VARCHAR(128) NOT NULL UNIQUE,
    resource VARCHAR(128) NOT NULL,
    action VARCHAR(64) NOT NULL,
    module VARCHAR(64) NOT NULL DEFAULT 'identity',
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Role ↔ Permission (tenant-scoped assignments)
CREATE TABLE IF NOT EXISTS identity.role_permissions (
    tenant_id VARCHAR(63) NOT NULL,
    role_id UUID NOT NULL REFERENCES identity.roles(id) ON DELETE CASCADE,
    permission_id UUID NOT NULL REFERENCES identity.permissions(id) ON DELETE CASCADE,
    granted_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tenant_id, role_id, permission_id)
);

-- User ↔ Role
CREATE TABLE IF NOT EXISTS identity.user_roles (
    tenant_id VARCHAR(63) NOT NULL,
    user_id UUID NOT NULL REFERENCES identity.users(id) ON DELETE CASCADE,
    role_id UUID NOT NULL REFERENCES identity.roles(id) ON DELETE CASCADE,
    assigned_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    assigned_by UUID,
    PRIMARY KEY (tenant_id, user_id, role_id)
);

CREATE INDEX IF NOT EXISTS idx_user_roles_user ON identity.user_roles(tenant_id, user_id);

-- Sessions & refresh tokens
CREATE TABLE IF NOT EXISTS identity.sessions (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    user_id UUID NOT NULL REFERENCES identity.users(id) ON DELETE CASCADE,
    refresh_token_hash VARCHAR(256) NOT NULL,
    ip_address INET,
    user_agent TEXT,
    expires_at TIMESTAMPTZ NOT NULL,
    revoked_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_sessions_user ON identity.sessions(tenant_id, user_id);
CREATE INDEX IF NOT EXISTS idx_sessions_expires ON identity.sessions(expires_at) WHERE revoked_at IS NULL;

-- ABAC policies (tenant-scoped)
CREATE TABLE IF NOT EXISTS identity.abac_policies (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    name VARCHAR(128) NOT NULL,
    effect VARCHAR(8) NOT NULL CHECK (effect IN ('allow', 'deny')),
    resource VARCHAR(128) NOT NULL,
    action VARCHAR(64) NOT NULL,
    conditions JSONB NOT NULL DEFAULT '{}',
    priority INT NOT NULL DEFAULT 100,
    enabled BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_abac_tenant ON identity.abac_policies(tenant_id, resource, action);

-- Seed identity permissions
INSERT INTO identity.permissions (id, code, resource, action, module, description) VALUES
  ('00000000-0000-4000-8000-000000000001', 'identity.users.read', 'users', 'read', 'identity', 'View users'),
  ('00000000-0000-4000-8000-000000000002', 'identity.users.write', 'users', 'write', 'identity', 'Create and update users'),
  ('00000000-0000-4000-8000-000000000003', 'identity.users.delete', 'users', 'delete', 'identity', 'Deactivate users'),
  ('00000000-0000-4000-8000-000000000004', 'identity.roles.read', 'roles', 'read', 'identity', 'View roles'),
  ('00000000-0000-4000-8000-000000000005', 'identity.roles.write', 'roles', 'write', 'identity', 'Manage roles'),
  ('00000000-0000-4000-8000-000000000006', 'identity.mfa.manage', 'mfa', 'manage', 'identity', 'Manage MFA settings'),
  ('00000000-0000-4000-8000-000000000007', 'identity.sessions.read', 'sessions', 'read', 'identity', 'View active sessions'),
  ('00000000-0000-4000-8000-000000000008', 'identity.sessions.revoke', 'sessions', 'revoke', 'identity', 'Revoke sessions'),
  ('00000000-0000-4000-8000-000000000009', 'identity.audit.read', 'audit', 'read', 'identity', 'View audit logs'),
  ('00000000-0000-4000-8000-000000000010', 'identity.policies.write', 'policies', 'write', 'identity', 'Manage ABAC policies')
ON CONFLICT (code) DO NOTHING;

-- Normalize audit_log tenant column
DO $$ BEGIN
  IF EXISTS (
    SELECT 1 FROM information_schema.columns
    WHERE table_schema = 'platform' AND table_name = 'audit_log' AND column_name = 'tenant_slug'
  ) THEN
    ALTER TABLE platform.audit_log RENAME COLUMN tenant_slug TO tenant_id;
  END IF;
END $$;

DO $$ BEGIN
  IF EXISTS (
    SELECT 1 FROM information_schema.columns
    WHERE table_schema = 'platform' AND table_name = 'outbox' AND column_name = 'tenant_slug'
  ) THEN
    ALTER TABLE platform.outbox RENAME COLUMN tenant_slug TO tenant_id;
  END IF;
END $$;
