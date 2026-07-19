# ADR-220: Enterprise Trust Fabric (P200-B6)

## Status

Accepted — Official Trust Fabric baseline (V03-C03)

## Context

P200-B5 hardened the Federation Engine. P200-B6 elevates **trust from static configuration to a continuous, explainable enterprise capability** — the foundation of Zero Trust fact production for AuthZ (ADR-204), without merging Permit/Deny into federation.

## Decision

1. Law: `docs/architecture/ENTERPRISE_IDENTITY_FEDERATION_TRUST_FABRIC.md`
2. Catalogs: `docs/architecture/identity/eiftp/TRUST_FABRIC_*.v1.yaml`
3. Logical subdomains (Trust Management, Evaluation, Policy, Evidence, Intelligence) live **inside** `identity_federation` — not new BCs
4. Facade: `trust_fabric_engine` composes `trust_management`, `trust_graph`, `zero_trust`, scoring, evidence
5. Enterprise trust levels **0–5** (Unknown → Continuous Adaptive) with scored transitions
6. Trust decisions emit **facts + explanations** for AuthZ/Risk — never Permit/Deny
7. CQRS + REST `/api/v1/federation/trust-fabric/*`; GraphQL/gRPC deferred to B10
8. Cross-tenant trust requires explicit `TenantFederation` + lifecycle approval path (workflow via events)

## Consequences

- B8 Cross-Tenant Trust deepens governance/approval on this fabric
- B9 Security & ZT consumes fabric evaluation outputs

## References

ADR-202c · 213 Vision Trust Fabric · 217–219 · AuthZ ADR-204 · Policy Engine ADR-205
