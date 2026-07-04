# Identity Module (Phase 1)

JWT · RBAC · ABAC · MFA · Sessions · Audit · Events

## API prefix

`/api/v1/auth`, `/api/v1/users`, `/api/v1/roles`

## Permissions

See legacy implementation: `services/identity-service/` (TypeScript) — migrate to this module.

## Database schema

`identity.*` — all tables include `tenant_id`.
