# ADR-218: Enterprise Identity Federation & Trust — Tactical Domain Model (P200-B4)

## Status

Accepted — Official tactical domain model for EIFTP (V03-C03)

## Context

P200-B3 strategic design classified domains and ownership. P200-B4 produces the **tactical DDD model** (aggregates, entities, VOs, factories, specifications, policies, commands, queries, events, persistence, KG/twin) that engineering implements without redesign.

## Decision

1. Law: `docs/architecture/ENTERPRISE_IDENTITY_FEDERATION_TRUST_DOMAIN_MODEL.md`
2. Catalogs: `docs/architecture/identity/eiftp/MODEL_*.v1.yaml`
3. **Federation SoR aggregates** enriched with behavior (non-anemic): Trust, Federation Session, Identity Link, IdP, Partner, AI Federated Agent, …
4. **Identity / Tenant / Organization / Credential / Policy** full aggregates remain owned by companion BCs; EIFTP consumes via refs + published language and holds federation-side handles (`IdentityLink`, `TenantFederation`, federation policies)
5. Event sourcing ready: aggregates raise domain events → mapped to integration events at application boundary
6. Persistence: PostgreSQL `federation` schema + outbox event store; graph/twin are projections

## Consequences

- B5+ engines call aggregate methods / domain services — not anemic setters from routers
- AuthZ/Policy never gain second homes inside federation

## References

ADR-217 Strategic DDD · ADR-216 EA · ADR-202× · ADR-204 AuthZ
