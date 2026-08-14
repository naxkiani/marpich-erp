# ADR 529 — Enterprise Space Intelligence Domain Architecture (DDD) (P218-C)

## Status

Accepted

## Context

P218-B established strategic architecture. P218-C defines strategic DDD classification, bounded contexts, aggregates, entities, value objects, domain services, repositories, events, CQRS, knowledge graph and digital twin mapping — before infrastructure (P218-D).

## Decision

1. SoR remains `space` / `CAP-PLT-SP-001`.
2. Fabric: `meos_space_intelligence_domain_architecture_framework`.
3. API: `/api/v1/space/domain*`.
4. Core domain: Enterprise Space Intelligence Domain; supporting and generic domains via Core Platform where applicable.
5. Eight bounded contexts (BC-01..BC-08) with primary aggregate roots and consistency rules.
6. Never cross-context aggregate mutation; never peer domain imports; ACL + events only.
7. Space AI context stores intents/refs only — inference via P214-Z ACL.
8. Never replace Core, AI, Quantum, Robotics, Biotechnology, prior P218 fabrics.
9. Human mission oversight, cybersecurity and sustainability required; opaque / ungated autonomy forbidden.
10. Foundation for P218-D.

## Consequences

Positive: clear DDD boundaries for space intelligence series.  
Negative: catalog must stay aligned as P218-D+ runtime deepens.

## Alternatives rejected

- Sibling `space_ddd` BC outside SoR space.
- Module-local LLM ownership inside Space AI context.
- Cross-context ORM joins.

## Related

Law: `ENTERPRISE_SPACE_INTELLIGENCE_DOMAIN.md` · Prior: ADR 526–528 · Next: P218-D
