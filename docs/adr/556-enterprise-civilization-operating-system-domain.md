# ADR 556 — Enterprise Civilization Operating System Domain Architecture (P219-C)

## Status
Accepted

## Context
P219-B defined strategic architecture and operating framework. P219-C establishes DDD bounded contexts, aggregates, entities, value objects, domain services, events, CQRS, knowledge graph and digital twin domain models before P219-D planetary infrastructure intelligence.

## Decision
1. Fabric `meos_civilization_os_domain_architecture_framework`; API `/api/v1/civilization/domain*`.
2. Eight bounded contexts: Core, Planetary, Human, Infrastructure, Resource, Governance, Knowledge, Economic.
3. Core domain is Civilization Management; supporting and generic domains per MEOS charter (generic via Core).
4. Aggregate consistency + domain events + CQRS; no cross-context aggregate imports.
5. Knowledge graph and digital twin are first-class domain models.
6. Never replace P219 / P219-A / P219-B or P214–P218-Z peers; never merge P218-T space civilization phase.
7. Foundation for P219-D planetary infrastructure intelligence.

## Consequences
Positive: clear DDD boundaries before infrastructure-focused phases.  
Negative: must keep peer IDs only across contexts and SoRs.

## Links
Law: `ENTERPRISE_CIVILIZATION_OPERATING_SYSTEM_DOMAIN.md` · Prior: ADR 555 · Next: P219-D
