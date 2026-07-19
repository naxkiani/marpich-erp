# ADR-217: Enterprise Identity Federation & Trust — DDD Strategic Design (P200-B3)

## Status

Accepted — Official strategic domain architecture for EIFTP (V03-C03)

## Context

P200-B2 defined solution/C4 architecture. P200-B3 establishes the **strategic DDD model** (core/supporting/generic domains, bounded contexts, context map, ubiquitous language, event ownership) so tactical DDD (B4+) can proceed without redesign.

## Decision

1. Law: `docs/architecture/ENTERPRISE_IDENTITY_FEDERATION_TRUST_DDD_STRATEGIC.md`
2. Catalogs: `docs/architecture/identity/eiftp/DDD_*.v1.yaml`
3. **Single deployable SoR BC** remains `identity_federation` — subdomains (Federation, Trust, Session, Token, External IdP, Certificate, AI/Machine/Device identity facets) are **logical domains inside** that BC or companions, never a sibling `eiftp` BC
4. Companion platform BCs (Identity, AuthN, AuthZ, Policy, Audit, …) are **separate bounded contexts** with explicit context-map relationships
5. Published language + ACLs enforced in code: ubiquitous language registry, event ownership matrix, `infrastructure/acl/`

## Consequences

- B4 Domain Model must respect aggregate ownership in `DDD_AGGREGATE_CATALOG`
- Circular context dependencies are rejected by `eiftp_ddd_strategic` validator
- AuthZ/Policy/Secrets remain non-negotiable Separate Ways / Customer-Supplier — not Shared Kernel with industry modules

## References

ADR-202× · 212–216 · 204 · DDD_DOMAIN_ARCHITECTURE · SERVICE_BOUNDARIES
