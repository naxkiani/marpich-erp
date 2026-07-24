# ADR-222: Cross-Tenant Trust & Enterprise Delegation Platform (P200-B8)

## Status

Accepted — Official Cross-Tenant Trust & Delegation baseline (V03-C03)

## Context

P200-B6 delivered continuous Trust Fabric; P200-B7 hardened IdP connectivity. P200-B8 enables **governed collaboration across independent tenant boundaries** — B2B, partner, guest, and AI-agent delegation — without implicit trust, shared DBs, or AuthZ Permit/Deny in federation.

## Decision

1. Law: `docs/architecture/ENTERPRISE_IDENTITY_FEDERATION_CROSS_TENANT_TRUST.md`
2. Catalogs: `docs/architecture/identity/eiftp/CROSS_TENANT_*.v1.yaml`
3. Logical domains (Cross-Tenant Trust, Delegation, Partner Access, External Identity) live **inside** `identity_federation`
4. `TenantFederation` gains explicit trust lifecycle (request → assess → approve → activate → monitor → revoke)
5. New aggregates: `DelegationAgreement`, `PartnerAccess`, `ExternalIdentity` — tenant-scoped, expiration mandatory
6. Trust decisions consume Trust Fabric + CrossTenantTrustPolicy + Policy Engine port — **never** Permit/Deny
7. Workflow approvals via local lifecycle + `workflow.*` events (Workflow Engine owns visual approvals)
8. CQRS + REST `/api/v1/federation/cross-tenant/*`; GraphQL/gRPC deferred to B10
9. Isolation law: no cross-schema SQL; peer tenants referenced by `partner_tenant_id` only

## Consequences

- B9 Security & ZT deepens continuous evaluation on every cross-tenant hop
- Unlimited privileges rejected at delegation scope validation

## References

ADR-220 · 221 · 205 Policy Engine · Workflow Engine · AuthZ ADR-204
