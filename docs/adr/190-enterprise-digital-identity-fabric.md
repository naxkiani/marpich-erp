# ADR-190: Enterprise Digital Identity Fabric (EIF)

## Status

Accepted

## Context

MEIAAP phases P1–P8 delivered eight IAM bounded contexts (authorization, permission registry, authentication, data isolation, directory, identity risk, identity resilience) plus centralized `@marpich/auth-provider`. Banking, Islamic Banking, Exchange, Government, University, Hospital, Construction, Manufacturing, Retail, Insurance, Real Estate, and NGO verticals require a **single authoritative identity fabric** for humans, organizations, applications, devices, services, and AI agents — without hardcoded identity logic in domain modules.

## Decision

Adopt **Enterprise Digital Identity Fabric (EIF)** as the umbrella architecture for all identity capabilities. EIF extends MEIAAP with additional bounded contexts and a unified policy-driven control plane.

### EIF Bounded Contexts (16)

| Context | API Prefix | Status |
|---------|------------|--------|
| `identity` | `/api/v1/identity` | Implemented |
| `authentication` | `/api/v1/authentication` | Implemented (P4) |
| `authorization` | `/api/v1/authorization` | Implemented (P1) |
| `permission_registry` | `/api/v1/permissions` | Implemented (P2) |
| `directory` | `/api/v1/directory` | Implemented (P6) |
| `federation` | `/api/v1/federation` | Planned (extract from directory/authentication) |
| `credential` | `/api/v1/credentials` | Planned |
| `trust` | `/api/v1/trust` | Partial (`identity_risk`) |
| `session` | `/api/v1/sessions` | Planned (extract from identity) |
| `consent` | `/api/v1/consent` | Planned |
| `device` | `/api/v1/devices` | Planned |
| `certificate` | `/api/v1/certificates` | Planned |
| `ai_identity` | `/api/v1/ai-identity` | Partial (`identity_risk`, `ai_security`) |
| `data_isolation` | `/api/v1/data-isolation` | Implemented (P5) |
| `identity_governance` | `/api/v1/identity-governance` | Implemented (ADR-161) |
| `identity_resilience` | `/api/v1/identity-resilience` | Implemented (P8) |

### Core Principles

1. **Policy-driven only** — no hardcoded authn/authz in domain modules; all decisions via Policy Engine + PDP.
2. **Published language** — integration events only; no shared domain models across contexts.
3. **Defense in depth** — application tenant filters + PostgreSQL RLS + gateway tenant resolution.
4. **Explainable AI** — risk scores and recommendations carry factor breakdown and evidence.
5. **Vertical packs** — industry policy packs (banking, hospital, etc.) configure EIF; no forked code.

### Canonical Documentation

- Master blueprint: `docs/architecture/ENTERPRISE_DIGITAL_IDENTITY_FABRIC.md`
- PostgreSQL EIF schema: `infrastructure/docker/migrations/017_eif_fabric_schema.sql`
- Event catalog: `docs/architecture/identity/EIF_EVENT_CATALOG.yaml`
- Acceptance checklist: `docs/architecture/identity/EIF_ACCEPTANCE_CHECKLIST.md`

## Consequences

- **Positive:** Single identity vocabulary across 12+ industry verticals; MEIAAP becomes Phase 1 of EIF rollout.
- **Positive:** Clear extraction path for session, federation, credential contexts without breaking existing APIs.
- **Neutral:** GraphQL/gRPC surfaces are gateway-mediated; REST + SCIM remain primary for P9–P12.
- **Follow-up:** Persist all EIF contexts to PostgreSQL; version all integration events; gateway step-up enforcement.

## References

- ADR-009, ADR-036, ADR-161, ADR-182–189
- `docs/architecture/CORE_PLATFORM.md` § Identity Plane
- `docs/architecture/SECURITY_STANDARD.md`
