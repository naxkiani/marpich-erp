# ADR-202: Enterprise Identity Federation & SSO Platform (P198 Part A)

## Status

Accepted

## Context

Marpich requires a central Identity Fabric supporting federation with external organizations, enterprise SSO, identity brokering, JIT provisioning, and cross-tenant trust. OIDC flows exist in `authentication` and SAML in `directory`, but lack a unified federation bounded context.

## Decision

Create `identity_federation` bounded context as the canonical federation layer:

### Bounded Contexts (DDD)

| Context | Responsibility |
|---------|----------------|
| Identity Registry | Provider and partner registration |
| Federation Engine | Lifecycle, SSO, logout orchestration |
| Identity Broker | Routing, discovery, federation flow |
| Claims Transformation | Attribute/claims mapping |
| Trust Management | Trust hierarchy, scoring, lifecycle |
| Provisioning | JIT provisioning, sync, de-provisioning |
| Directory Integration | LDAP/AD server registry |

### Database

Migration `028_enterprise_identity_federation_platform.sql` extends `federation` schema with partners, trust relationships, claims mappings, identity links, sessions, audit, tenant federation, policies.

### APIs

| Method | Path | Description |
|--------|------|-------------|
| GET | `/federation/catalog` | Capabilities and plugin registry |
| POST | `/federation/providers` | Register IdP (pluggable) |
| POST | `/federation/broker/authenticate` | Identity broker flow |
| POST | `/federation/discover` | Identity discovery |
| POST | `/federation/claims/transform` | Claims transformation |
| POST | `/federation/provision/jit` | JIT provisioning |
| POST | `/federation/logout` | Federated logout |
| POST | `/federation/trust` | Trust relationship |
| POST | `/federation/tenant-federation` | Multi-tenant federation config |

### Policy Keys

`federation.enabled`, `federation.broker.enabled`, `federation.jit_provisioning.enabled`, `federation.identity_discovery.enabled`, `federation.single_logout.enabled`, `federation.cross_tenant.enabled`

### Plugin Registry

20+ built-in provider plugins (OIDC, SAML, LDAP, Entra ID, Google, Okta, Auth0, government eID, university, hospital, bank, etc.) — all configurable, never hardcoded at runtime.

## Consequences

- Federation becomes first-class bounded context alongside authentication and directory
- Existing OIDC/SAML endpoints remain; federation context orchestrates and extends them
- All trust relationships, mappings, and provisioning rules are policy-driven

## References

- [ENTERPRISE_IDENTITY_FEDERATION_PLATFORM.md](../architecture/ENTERPRISE_IDENTITY_FEDERATION_PLATFORM.md)
- Migration 017 (EIF federation schema), 028 (P198 extension)
