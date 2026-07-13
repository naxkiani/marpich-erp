# ADR-186: PostgreSQL RLS + Principal Partitioning (Phase P5)

## Status

Accepted

## Context

Phases P1–P4 delivered Authorization PDP, Permission Registry, centralized auth frontend, and WebAuthn/OIDC authentication. Tenant isolation relied on application-level `tenant_id` filters in repositories. MEIAAP Phase P5 requires **PostgreSQL Row-Level Security** and **HASH-partitioned principal registry** for defense-in-depth at the database layer.

## Decision

Implement **Data Isolation Platform** at `/api/v1/data-isolation` and shared database infrastructure for RLS session binding.

### 10 Platform Capabilities

1. RLS Catalog
2. RLS Policy Registry
3. Principal Registry
4. Principal Partitioning
5. Tenant Context Binding
6. Isolation Verification
7. Policy-Driven Isolation
8. Data Isolation Dashboard
9. Principal Sync
10. Data Isolation API

### Database changes (migration `016_identity_rls_principals.sql`)

- `identity.principals` — HASH partitioned by `tenant_id` (8 partitions default)
- `authorization.access_decisions` — RANGE partitioned by `decided_at`
- RLS policies on `identity.users`, `roles`, `sessions`, `principals`, `authorization.access_decisions`
- Session variable: `app.tenant_id` via `set_config(..., true)` per transaction

### Runtime infrastructure

- `shared/infrastructure/database/rls_context.py` — ContextVar for tenant/principal
- `session_scope(tenant_id=..., principal_id=...)` — applies RLS session vars when `marpich_rls_enabled=true`
- `TenantRlsMiddleware` — binds tenant from `X-Tenant-ID` and JWT `sub` per request
- Identity `postgres_store` passes `tenant_id` into `session_scope`

### Settings

- `MARPICH_RLS_ENABLED` (default `false` — opt-in for production Postgres)
- `MARPICH_PRINCIPAL_PARTITION_MODULUS` (default `8`)

### API Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/data-isolation/catalog` | RLS catalog + runtime flags |
| POST | `/data-isolation/seed` | Bootstrap isolation profile |
| GET | `/data-isolation/dashboard` | Partition + RLS summary |
| GET | `/data-isolation/principals` | List synced principals |
| POST | `/data-isolation/principals/sync` | Sync from Identity users |
| POST | `/data-isolation/verify` | Verify RLS configuration |
| GET | `/data-isolation/partitions` | Partition distribution map |

## Consequences

- **Positive:** Defense-in-depth tenant isolation; unified principal registry ready for 10M+ principals per tenant architecture.
- **Positive:** Authorization decisions have partitioned storage path for compliance retention.
- **Neutral:** RLS disabled by default — memory/test mode unchanged; enable with `MARPICH_RLS_ENABLED=true` + migration 016.
- **Follow-up (P6+):** SAML/LDAP directory sync; monthly access_decisions partition automation; CMK column encryption.

## References

- ADR-185 — Authentication Platform
- `docs/architecture/MULTI_TENANCY.md`
- `infrastructure/docker/migrations/016_identity_rls_principals.sql`
