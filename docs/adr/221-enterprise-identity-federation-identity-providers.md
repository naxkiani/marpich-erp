# ADR-221: Enterprise Identity Provider Management & Federation Protocol Layer (P200-B7)

## Status

Accepted — Official IdP Management & Protocol Layer baseline (V03-C03)

## Context

P200-B5 delivered Federation Engine composition; P200-B6 delivered continuous Trust Fabric. P200-B7 hardens **universal Identity Provider management**, **protocol-plugin independence**, lifecycle governance, mapping, sync monitoring, and **provider trust evaluation** that consumes Trust Fabric facts — without vendor SDKs in domain or a sibling `eiftp` BC.

## Decision

1. Law: `docs/architecture/ENTERPRISE_IDENTITY_FEDERATION_IDENTITY_PROVIDERS.md`
2. Catalogs: `docs/architecture/identity/eiftp/IDENTITY_PROVIDERS_*.v1.yaml`
3. Logical domains (IdP Management, Federation Connection, Protocol Abstraction, Mapping, Provider Trust, Sync) remain **inside** `identity_federation`
4. First-class VOs: `ProviderType`, `ProviderStatus`, `ProviderTrustLevel` (aligned to fabric levels 0–5)
5. `IdentityProvider` gains lifecycle (`registered`→`verified`→`active`→`suspended`…) + typed configuration metadata
6. Protocol plugins are versioned, installable descriptors (`IProtocolPlugin` + registry); execution of external IdPs via **Integration Platform**
7. Provider trust evaluation **reads** Trust Fabric facts — never emits Permit/Deny
8. CQRS + REST `/api/v1/federation/providers/*`; GraphQL/gRPC deferred to B10
9. Certificate rotation and plugin install are explicit commands with audit metrics

## Consequences

- B8 Cross-Tenant Trust reuses shared/enterprise provider modes
- B9 Security & ZT deepens mTLS / cert / threat paths on this layer
- Future protocols = new plugin descriptors — no engine rewrite

## References

ADR-202b · 219–220 · Integration Platform · Plugin Platform · AuthZ ADR-204
