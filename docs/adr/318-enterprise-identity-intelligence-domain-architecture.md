# ADR-318: Identity Intelligence — Domain Architecture DDD (P207-C)

## Status

Accepted — P207-C Enterprise Identity Intelligence Domain Architecture (DDD)

## Context

P207-A/B established strategy and mission/scope on SoR `identity_intelligence`. P207-C defines strategic and tactical DDD: domain purpose, MEOS placement, core/supporting/generic classification, logical bounded contexts, ubiquitous language, aggregates, entities, value objects, domain services, CQRS, events, context map, and invariants — without inventing sibling BCs or replacing Directory, IGA, AM, PAM, Twin, AuthZ, or credentials.

**Hard laws:** SoR remains `identity_intelligence`. Surfaces under `/domain*` (distinct from `/strategy*`, `/mission*`). DDD boundaries clear. CQRS + event-driven + outbox. Explainable decisions. HITL for high-impact. AI via AI Platform. Twin/graph via peer SoRs (refs only). Never chatbot-only. Never ungoverned automation. Never anemic domain model for owned aggregates.

## Decision

1. SoR remains `identity_intelligence`
2. Surfaces under `/api/v1/identity-intelligence/domain*`
3. Law: `ENTERPRISE_IDENTITY_INTELLIGENCE_DOMAIN_ARCHITECTURE.md`
4. Catalogs: `II_DOMAIN_*.v1.yaml`
5. Runtime: `ii_platform_domain.py`; aggregates: `ii_domain_aggregates.py`; ACL: `ii_domain_acl.py`; validator: `ii_domain_foundation.py`
6. Logical BCs live inside SoR; ultra-prompt microservices remain logical deployables
7. Quality gates reject unclear DDD boundaries, anemic aggregates, peer SoR replacement, missing CQRS/events, chatbot-only, removed human control, sibling BC

## Consequences

- P207-D+ runtimes (agents, twin, risk, behavior, healing) extend aggregates defined here
- Context map partnerships remain ACL/event only

## References

ADR-316 · ADR-317 · DDD_DOMAIN_ARCHITECTURE · MODULE_ARCHITECTURE · Platform Charter
