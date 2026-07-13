# ADR-184: Centralized Auth Provider (Phase P3)

## Status

Accepted

## Context

Phases P1 (Authorization PDP) and P2 (Permission Registry) delivered backend IAM capabilities, but the Admin Portal still duplicated authentication in 15+ dashboard API clients. Each module maintained its own `sessionStorage` key, login/register flow, and fetch headers — causing fragmented sessions and repeated boilerplate.

## Decision

Implement **`@marpich/auth-provider`** as a shared frontend package and wire it into the Admin Portal.

### Package capabilities

1. **Unified session** — single `marpich_auth_session` in `sessionStorage` with optional cookie mirror for middleware
2. **Auth service** — login, register-on-first-use, refresh, logout, `GET /users/me`
3. **API client** — `apiGet` / `apiPost` / `apiPut` / `apiDelete` with `X-Tenant-ID` and `Authorization` headers
4. **Authorization hooks** — PDP `check` and Permission Registry principal resolution
5. **React integration** — `AuthProvider`, `useAuth`, `usePermission`, `useAuthorization`, `LoginGate`
6. **Route protection** — Next.js `middleware.ts` for `/enterprise`, `/tax`, `/currency-exchange`

### Admin Portal integration

- Root layout wraps `AuthProvider` inside `MarpichProviders`
- `/login` page for centralized sign-in with `returnTo` redirect
- `ShellNav` shows tenant, user email, and sign-out
- `clientAuth.ts` thin wrapper for legacy dashboard clients
- All `*Client.ts` modules delegate session/login to shared auth (backward-compatible export names preserved)
- `EnterpriseSchedulerDashboardPage` migrated to `useAuth` + `LoginGate` as reference pattern

### Session cookie

Middleware cannot read `sessionStorage`. A lightweight `marpich_auth=1` cookie is set on login so edge middleware can gate protected routes. Tokens remain client-side in session storage.

## Consequences

- **Positive:** One sign-in unlocks all dashboards; token refresh and user profile loading are centralized; hooks connect UI to PDP and Permission Registry.
- **Positive:** Dashboard clients shrink to domain API functions only.
- **Neutral:** Other dashboard pages still use legacy inline connect forms but share the same session via refactored clients.
- **Follow-up (P4+):** Migrate remaining dashboards to `useAuth`/`LoginGate`; httpOnly cookie sessions; SSO/OIDC; WebAuthn.

## References

- ADR-182 — Authorization PDP
- ADR-183 — Permission Registry
- `frontend/auth-provider/`
- `frontend/apps/admin_portal/src/middleware.ts`
