# ADR-187: Enterprise Directory Platform (Phase P6)

## Status

Accepted

## Context

Phases P1–P5 delivered Authorization PDP, Permission Registry, centralized auth provider, WebAuthn/OIDC authentication, and PostgreSQL RLS with principal partitioning. Enterprise tenants require **SAML federation**, **LDAP/Active Directory sync**, and **SCIM provisioning** as a dedicated Directory bounded context — separate from Identity (per ADR-036: Identity consumes `integration.directory.synced`, not direct LDAP).

## Decision

Implement **Directory Platform** at `/api/v1/directory` as bounded context `directory`.

### 10 Platform Capabilities

1. SAML Provider Registry
2. SAML Authorization
3. SAML Assertion Consumer
4. LDAP Connector Registry
5. LDAP Directory Sync
6. SCIM Provider Registry
7. SCIM User Provisioning
8. Directory Sync Worker
9. Policy-Driven Directory
10. Directory API

### Aggregates

- `DirectoryProfile`
- `SamlProvider`
- `LdapConnector`
- `ScimProvider`
- `DirectorySyncJob`

### Policy Keys

- `directory.saml.enabled`
- `directory.ldap.enabled`
- `directory.scim.enabled`
- `directory.sync.auto_provision`

### Events

- `directory.saml.provider.registered`
- `directory.ldap.connector.registered`
- `directory.sync.completed`
- `directory.scim.user.provisioned`
- `integration.directory.synced` (cross-context contract per ADR-036)

### API Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/directory/catalog` | Capability catalog |
| POST | `/directory/seed` | Bootstrap tenant profile |
| GET | `/directory/dashboard` | Directory platform dashboard |
| GET/POST | `/directory/federation/saml/providers` | SAML IdP registry |
| POST | `/directory/federation/saml/authorize` | SAML SP-initiated login (public) |
| POST | `/directory/federation/saml/acs` | SAML ACS callback (public) |
| GET/POST | `/directory/ldap/connectors` | LDAP connector registry |
| POST | `/directory/ldap/sync` | Immediate LDAP user sync |
| POST | `/directory/sync/enqueue` | Enqueue background sync job |
| POST | `/directory/sync/run` | Run directory sync worker |
| GET | `/directory/sync/jobs` | List sync jobs |
| GET/POST | `/directory/scim/providers` | SCIM bearer-token registry |
| POST | `/directory/scim/v2/Users` | SCIM user provisioning (public, token auth) |

### Identity delegation

User provisioning delegates to `IdentityApplicationService.provision_directory_user()` — creates users with random password hash (external-auth only). Token issuance after SAML ACS delegates to `issue_tokens_for_user()`.

### LDAP client

`StubLdapDirectoryClient` for dev/test; `.mock` host suffix returns fixture users. Production path: swap to `ldap3` client behind `ILdapDirectoryClient`.

## Consequences

- **Positive:** SAML/LDAP/SCIM foundation aligned with Integration Platform event contract.
- **Positive:** Background sync worker with job queue for scheduled directory imports.
- **Neutral:** SAML signature validation deferred — ACS extracts NameID from assertion XML; production should add `python3-saml` or gateway-level validation.
- **Follow-up (P7+):** AI risk scoring on directory sync anomalies; multi-region HA for sync workers.

## References

- ADR-036 Integration Platform
- ADR-185 Enterprise Authentication Platform
- ADR-186 PostgreSQL RLS + Principal Partitioning
- `docs/architecture/INTEGRATION_PLATFORM.md`
