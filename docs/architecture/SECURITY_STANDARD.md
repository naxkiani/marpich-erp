# Marpich Security Standard

**Status:** Canonical — **security is mandatory, never optional**  
**Audience:** Engineering, AI agents, security reviewers, integrators  
**Companions:** [PLATFORM_CHARTER.md](PLATFORM_CHARTER.md) · [CORE_PLATFORM.md](CORE_PLATFORM.md) · [ENTERPRISE_AUDIT_PLATFORM.md](ENTERPRISE_AUDIT_PLATFORM.md) · [ENTERPRISE_OBSERVABILITY_PLATFORM.md](ENTERPRISE_OBSERVABILITY_PLATFORM.md) · [ENTERPRISE_POLICY_ENGINE.md](ENTERPRISE_POLICY_ENGINE.md) · [API_GATEWAY_ARCHITECTURE.md](API_GATEWAY_ARCHITECTURE.md) · [PERFORMANCE_STANDARD.md](PERFORMANCE_STANDARD.md)

**Rule: Security is mandatory. Never optional.**

---

## Platform Law

| Principle | Meaning |
|-----------|---------|
| **Everything requires authentication** | No anonymous access to business APIs (except explicit public auth endpoints) |
| **Everything requires authorization** | Every mutating and sensitive read action checks RBAC + ABAC |
| **Every action creates audit logs** | Immutable audit trail via Audit Service + integration events |
| **Zero trust** | Verify identity and policy on every request — no implicit trust by network |
| **Secrets never in source code** | Env / secret manager only; `.env` gitignored |

---

## Mandatory Controls (every system)

| # | Control | Implementation |
|---|---------|----------------|
| 1 | **Authentication** | Authentication Service — `/api/v1/auth/login`, JWT issuance |
| 2 | **Authorization** | Authorization Service — `POST /authorization/check` (RBAC + ABAC) |
| 3 | **Audit logs** | Audit Service — every mutation + security events |
| 4 | **File validation** | MIME, size, malware scan hook; Media/Documents services |
| 5 | **API permission validation** | `module.resource.action` on every route |
| 6 | **Sensitive data encryption** | AES-256 at rest; TLS in transit |
| 7 | **Secrets management** | `pydantic-settings` / env; never commit keys |
| 8 | **Session management** | Refresh tokens, TTL, revoke, MFA state |
| 9 | **Threat detection** | Anomaly events → audit + notifications + AI layer |
| 10 | **Rate limiting** | Gateway + Redis per tenant/user/IP |

---

## Supported Standards & Algorithms

| Standard | Use in Marpich |
|----------|----------------|
| **RBAC** | Role → permission sets; registered at module activation |
| **ABAC** | Policy context: tenant, locale, resource attributes, time |
| **JWT** | Access + refresh tokens; `sub`, `tenant_id`, scopes |
| **OAuth2** | External IdP integration; client credentials for services |
| **OpenID Connect** | SSO for enterprise tenants (OIDC discovery + ID token) |
| **Digital signature** | Document signing; webhook HMAC; signed audit exports |
| **AES-256** | Encryption at rest (DB fields, object storage, backups) |
| **RSA** | Asymmetric keys for JWT (RS256), signing, key exchange |
| **Zero trust** | Gateway authn/authz on every call; mTLS optional between services |

---

## Backend Requirements

### Every API route

```python
# presentation/router.py — pattern
@router.post("/items", dependencies=[Depends(require_permission("module.item.write"))])
async def create_item(..., tenant_id: TenantId = Depends(get_tenant)):
    ...
    # → publishes integration event → audit consumer
```

| Check | Required |
|-------|----------|
| Bearer JWT or service token | Yes |
| `tenant_id` matches token | Yes |
| Permission for action | Yes |
| Input validation (Pydantic) | Yes |
| Audit event on mutation | Yes |

### Public endpoints (only these classes)

- `/auth/login`, `/auth/register`, `/auth/refresh`
- `/health` (no sensitive data)
- OIDC callback routes (when enabled)

### File upload

- Max size from tenant settings
- Allowlist MIME types
- Store outside web root (S3 / object storage)
- Virus scan hook before `documents.document.uploaded` event
- Never execute uploaded content

### Encryption

| Data | Method |
|------|--------|
| Passwords | bcrypt (never reversible) |
| PII / financial fields | AES-256-GCM column-level or vault |
| Transit | TLS 1.2+ everywhere |
| JWT signing | HS256 (dev) / RS256 (production) |

### Secrets (forbidden in repo)

```
❌ jwt_secret = "hardcoded"
❌ API keys in Python/TS/JSON committed
✅ os.environ / .env.local (gitignored)
✅ Render/K8s secrets, Vault, AWS SM
```

Pre-commit: reject patterns matching `password=`, `secret=`, `api_key=` in tracked files.

---

## Frontend Requirements

| Control | Implementation |
|---------|----------------|
| Auth | Store tokens in httpOnly cookies or secure memory; no localStorage for refresh in production |
| Authorization | Hide UI by permission; server still enforces |
| CSRF | SameSite cookies + CSRF token on mutations |
| XSS | React escaping; sanitize rich text |
| Files | Client-side type/size check; server is source of truth |

---

## Session Management

| Setting | Default |
|---------|---------|
| Access token TTL | 15 min (`jwt_access_ttl`) |
| Refresh token TTL | 7 days |
| Revoke on logout | Yes |
| MFA | TOTP for privileged roles |
| Concurrent sessions | Configurable per tenant |

---

## Threat Detection & Rate Limiting

| Signal | Response |
|--------|----------|
| Failed logins | `identity.login.failed` → audit + rate limit |
| Permission denied spike | Audit + alert |
| Unusual geo / device | ABAC deny or step-up MFA |
| API abuse | Redis rate limit → 429 |

Gateway headers: `X-Request-ID`, `X-Tenant-ID` — never trust without JWT validation.

---

## Module Security Checklist (copy per module)

```markdown
## Security (mandatory — never optional)

- [ ] Authentication required on all business routes
- [ ] Authorization (RBAC + ABAC) on every action
- [ ] Permissions registered: `{moduleId}.*`
- [ ] Audit events for all mutations
- [ ] File uploads validated (type, size, scan hook)
- [ ] Sensitive fields encrypted (AES-256) or hashed
- [ ] No secrets in source code
- [ ] Input validation (Pydantic / schema)
- [ ] Rate limiting considered for public-ish endpoints
- [ ] Tenant isolation verified (`tenant_id` on all queries)
```

---

## Anti-Patterns (forbidden)

- Optional auth "for dev" merged to main
- `if user.is_admin: skip_check`
- Logging passwords, tokens, or PII
- Returning stack traces to clients in production
- Cross-tenant data access without platform-admin scope
- Authorization only in UI, not API

---

## Enforcement

| Mechanism | Location |
|-----------|----------|
| Cursor rule | `.cursor/rules/marpich-security.mdc` |
| Identity context | `backend/contexts/identity/` |
| Core platform auth docs | [CORE_PLATFORM.md](CORE_PLATFORM.md) § AuthN/AuthZ |
| Audit context | `backend/contexts/audit/` |

**Review rejection:** Any PR bypassing auth, skipping permission checks, or committing secrets is blocked.
