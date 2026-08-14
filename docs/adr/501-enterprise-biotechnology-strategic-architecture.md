# ADR 501 — Enterprise Biotechnology Strategic Architecture (P217-B)

## Status

Accepted

## Context

P217-A established mission/vision. P217-B defines strategic architecture layers, capability model, operating framework, service/org/governance models, data/security/integration, maturity, transformation roadmap, CQRS and events — without owning deep DDD aggregates (P217-C).

## Decision

1. SoR remains `biotechnology` / `CAP-PLT-BIO-001`.
2. Fabric: `meos_biotechnology_strategic_architecture_framework`.
3. API: `/api/v1/biotechnology/strategy*`.
4. Five architecture layers (Strategy → Capability → Intelligence Platform → Execution → Governance).
5. Six capability groups; five operating-model components; five platform teams; four service categories.
6. Never replace Core, AI, Quantum, Robotics, P217 foundation, P217-A mission, hospital EMR, laboratory LIMS, or pharmacy.
7. Genomic privacy, ethical bioengineering, scientific integrity required; opaque bio safety forbidden.
8. Serve as strategic architecture foundation for P217-C.

## Consequences

Positive: scalable bio operating model and capability-driven planning.  
Negative: strategy catalog must stay aligned with P217-C bounded contexts.

## Alternatives rejected

- Merging strategy into mission fabric (scope explosion).
- Sibling `bio_strategy` BC outside SoR biotechnology.
- Owning hospital/laboratory/pharmacy clinical SoRs.

## Related

Law: `ENTERPRISE_BIOTECHNOLOGY_STRATEGY.md`  
Prior: ADR 499 · ADR 500 · Next: P217-C
