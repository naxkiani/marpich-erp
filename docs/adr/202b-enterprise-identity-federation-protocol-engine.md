# ADR-202b: Enterprise Identity Federation Protocol Engine (P198-B)

## Status
Accepted

## Context
P198-A delivered the federation domain model (providers, trust, broker, claims, JIT).
Applications and external organizations still need a universal protocol gateway for
OAuth 2.1, OIDC, SAML, SCIM, and LDAP without hardcoding provider logic.

## Decision
1. Introduce a Federation Protocol Engine with pluggable adapters and negotiation.
2. Expose a public Federation Gateway under `/api/v1/federation/*` for login, token,
   introspect, revoke, provision, sync, OIDC discovery, and JWKS.
3. Expose identity discovery endpoints under `/api/v1/identity/{providers,claims,metadata}`.
4. Marpich operates as both:
   - OAuth 2.1 Authorization Server / OIDC Provider (token issuance)
   - Protocol RP/SP via bridge adapters into authentication and directory contexts
5. All protocol behavior remains configuration-, metadata-, and policy-driven.
6. Errors use RFC 9457 `application/problem+json`.
7. Integration events and Kafka topics cover auth success/failure, claims mapping,
   token exchange, and certificate rotation.

## Consequences
- Admin federation routes remain authenticated under the same `/federation` prefix;
  session logout and sync job start moved to `/sessions/logout` and `/jobs/sync`.
- Gateway token/login endpoints are public (tenant-scoped via `X-Tenant-ID`).
- In-memory OAuth/SCIM registries are suitable for CI; production uses PostgreSQL + HSM/Vault.

## Compliance
Enterprise Architecture Governance Standard 7.0 — Zero Trust, plugin-first, API-first.
