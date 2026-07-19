# ADR-216: Enterprise Identity Federation & Trust — Enterprise Architecture (P200-B2)

## Status

Accepted — Enterprise Architecture baseline (V03-C03)

## Context

P200-B1 established Mission/Vision/Drivers/Goals. P200-B2 defines the **official technical architecture** every MEOS microservice uses when interacting with identity federation and trust — comparable in rigor to Entra ID / Keycloak Enterprise / Okta / Google Cloud Identity, while remaining Marpich-native (single SoR, no vendor fork).

Runtime already exists under `identity_federation` (ADR-202×). B2 **formalizes C4, flows, data/mesh strategies, and production package layout** without creating `contexts/eiftp/`.

## Decision

1. Law: `docs/architecture/ENTERPRISE_IDENTITY_FEDERATION_TRUST_ARCHITECTURE.md`
2. Catalogs: `docs/architecture/identity/eiftp/ARCH_*.v1.yaml` + index of 50 views
3. Shared consumer port: `shared/application/ports/identity_federation.py` (`IFederationTrustFacts`)
4. SoR package layout hardens toward MODULE_ARCHITECTURE (CQRS folders, messaging/caching) incrementally — existing routers/services remain the active path
5. AuthZ PDP (ADR-204), Secrets platform paths, Integration connectors, Audit, AI Platform remain **reused**, not reimplemented

## Consequences

- P200-B3+ refine DDD/domain/engine details against this EA baseline
- Microservice PEPs consume `IFederationTrustFacts` + `IAuthorizationEvaluator` — never peer domain imports

## References

ADR-202× · 212–215 · 204 · Integration Platform · Event Bus · Observability
