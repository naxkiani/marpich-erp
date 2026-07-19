# ADR-219: Enterprise Identity Federation Engine (P200-B5)

## Status

Accepted — Official Federation Engine composition baseline (V03-C03)

## Context

P200-B4 delivered the tactical domain model. P200-B5 hardens the **Identity Federation Engine** as the central capability composing existing engines (protocol, broker, claims, token, trust, sync, ZT) behind CQRS handlers, first-class `FederationConnection`, health probes, and monitoring — without a sibling BC or rewriting the application monolith.

## Decision

1. Law: `docs/architecture/ENTERPRISE_IDENTITY_FEDERATION_ENGINE.md`
2. Catalogs: `docs/architecture/identity/eiftp/ENGINE_*.v1.yaml`
3. Facade: `domain/services/identity_federation_engine.py` composes engines (no business logic duplication)
4. First-class `FederationConnection` entity on `IdentityProvider`
5. CQRS handlers for register/connect provider, map identity, exchange token, sync, resolve conflict + queries
6. `IProviderHealthProbe` port + infrastructure adapter (plugin/protocol-agnostic)
7. GraphQL/gRPC deferred to B10 as OHS extensions — REST + events remain primary
8. Secrets/vendor SDKs stay out of domain; external IdP execution via Integration Platform

## Consequences

- PEPs/modules use CQRS + `IFederationTrustFacts`; routers stay thin
- B6 Trust Fabric deepens trust graph on this engine foundation

## References

ADR-202× · 216–218 · Integration Platform · AuthZ ADR-204
