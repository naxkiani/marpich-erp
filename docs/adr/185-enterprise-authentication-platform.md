# ADR-185: Enterprise Authentication Platform (Phase P4)

## Status

Accepted

## Context

Phases P1–P3 delivered Authorization PDP, Permission Registry, and centralized `@marpich/auth-provider`. Authentication remained embedded in `contexts/identity/` (password + TOTP MFA only). MEIAAP Phase P4 requires **WebAuthn/passkeys** and **OIDC federation** as a dedicated Authentication bounded context.

## Decision

Implement **Authentication Platform** at `/api/v1/authentication` as bounded context `authentication`.

### 10 Platform Capabilities

1. WebAuthn Registration
2. WebAuthn Authentication
3. Passkey Management
4. OIDC Provider Registry
5. OIDC Authorization
6. OIDC Callback
7. Auth Method Catalog
8. Policy-Driven Authentication
9. Authentication Dashboard
10. Authentication API

### Aggregates

- `AuthenticationProfile`
- `WebAuthnCredential`
- `OidcProvider`

### Policy Keys

- `authentication.webauthn.enabled`
- `authentication.passkeys.required`
- `authentication.oidc.enabled`
- `authentication.password.enabled`

### Events

- `authentication.passkey.registered`
- `authentication.passkey.revoked`
- `authentication.oidc.provider.registered`
- `authentication.login.success`

### API Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/authentication/catalog` | Capability catalog |
| POST | `/authentication/seed` | Bootstrap tenant profile |
| GET | `/authentication/dashboard` | Auth platform dashboard |
| POST | `/authentication/webauthn/register/options` | Begin passkey registration |
| POST | `/authentication/webauthn/register/verify` | Complete passkey registration |
| POST | `/authentication/webauthn/login/options` | Begin passkey login (public) |
| POST | `/authentication/webauthn/login/verify` | Complete passkey login (public) |
| GET | `/authentication/webauthn/credentials` | List user passkeys |
| DELETE | `/authentication/webauthn/credentials/{ref}` | Revoke passkey |
| GET/POST | `/authentication/federation/providers` | OIDC provider registry |
| POST | `/authentication/federation/oidc/authorize` | OIDC authorization URL |
| POST | `/authentication/federation/oidc/callback` | OIDC code exchange + token issue |

### Identity delegation

Token issuance delegates to `IdentityApplicationService.issue_tokens_for_user()` after successful WebAuthn or OIDC authentication.

### Frontend

`@marpich/auth-provider` extended with `loginWithPasskey()` and `PasskeyLoginButton` on `/login`.

## Consequences

- **Positive:** Passwordless login path; OIDC federation foundation; policy-gated auth methods per tenant.
- **Positive:** WebAuthn uses standard `webauthn` Python library with challenge TTL and credential lifecycle.
- **Neutral:** OIDC callback requires reachable IdP token endpoint (integration tests cover provider registration and authorize URL only).
- **Follow-up (P5+):** PostgreSQL credential store; SAML; passkey-required enforcement at gateway.

## References

- ADR-184 — Centralized Auth Provider
- `backend/contexts/authentication/`
- `frontend/auth-provider/src/webauthn.ts`
