# Identity Service

Enterprise identity and access management for Marpich ERP.

## Capabilities

| Layer | Implementation |
|-------|----------------|
| **Architecture** | Clean / Hexagonal — domain → application → infrastructure → presentation |
| **API** | REST `/api/v1` — Auth, Users, Roles |
| **Database** | PostgreSQL `identity.*` schema (in-memory bootstrap for dev) |
| **Permissions** | RBAC + ABAC on every protected endpoint |
| **Validation** | `class-validator` DTOs |
| **Audit Trail** | `platform.audit_log` via `IAuditLogger` |
| **Logging** | Structured JSON logs |
| **Caching** | Redis / in-memory permission & session cache |
| **Background Jobs** | Session cleanup (hourly; BullMQ-ready) |
| **Notifications** | Login alerts, MFA enabled (console → Kafka/email in prod) |
| **Events** | Domain events → `platform.outbox` |
| **Monitoring** | `GET /api/v1/health` |
| **Swagger** | `GET /api/docs` |
| **Localization** | `Accept-Language` — en-US, fa-IR, ar-SA |
| **RTL/LTR** | `direction` field in API responses |

## Authentication Flow

```
1. POST /auth/register  (public, X-Tenant-ID required)
2. POST /auth/login     → JWT access + refresh OR mfaRequired + mfaToken
3. POST /auth/login     + mfaCode → full JWT
4. Bearer token on all protected routes
```

## MFA (TOTP)

```
1. POST /users/me/mfa/setup   → QR code + secret (cached 10 min)
2. POST /users/me/mfa/verify  → enable MFA + backup codes
3. Login requires mfaCode when mfaEnabled=true
```

## RBAC Permissions

| Code | Description |
|------|-------------|
| `identity.users.read` | View users |
| `identity.users.write` | Create/update users |
| `identity.users.delete` | Deactivate users |
| `identity.roles.read` | View roles |
| `identity.roles.write` | Manage roles |
| `identity.mfa.manage` | MFA setup |
| `identity.sessions.revoke` | Logout |
| `identity.audit.read` | View audit logs |

Admin role receives `*` (all permissions).

## ABAC

Policies stored in `identity.abac_policies` — evaluated at login and via `PermissionEvaluator`.

## Run

```bash
cd services/identity-service
npx pnpm dev
# Swagger: http://localhost:4001/api/docs
```

## Test

```bash
npx pnpm test
npx pnpm test:integration
```

## Gateway Routes

```
POST /api/v1/auth/register  → identity-service
POST /api/v1/auth/login     → identity-service
GET  /api/v1/users          → identity-service
GET  /api/v1/roles          → identity-service
```
