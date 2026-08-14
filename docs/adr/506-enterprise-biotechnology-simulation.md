# ADR 506 — Enterprise Biotechnology Biological Simulation Intelligence Platform (P217-G)

## Status

Accepted

## Context

P217-F established synthetic design and engineering automation. P217-G defines Biological Simulation Intelligence: bio digital twins, computational simulation engine, multi-scale life modeling, model lifecycle, simulation governance — before Digital Health (P217-H).

## Decision

1. SoR remains `biotechnology` / `CAP-PLT-BIO-001`.
2. Fabric: `meos_biological_simulation_intelligence_fabric`.
3. API: `/api/v1/biotechnology/simulation*`.
4. Six twin architecture layers; five twin domains; five simulation engine components; five multi-scale levels.
5. All inference via P214-Z ACL only — `no_module_local_llm`.
6. Quantum readiness via P215-Z ACL; physical validation via P216-Z ACL.
7. Never unvalidated simulation claims — scientific validation + expert review required.
8. Never replace Core, AI, Quantum, Robotics, hospital EMR, LIMS, pharmacy, prior P217 fabrics.
9. Foundation for P217-H.

## Consequences

Positive: governed simulation/twin layer for digital-health and precision-medicine phases.  
Negative: accuracy certification catalogs must stay aligned as multi-scale models deepen.

## Alternatives rejected

- Sibling `bio_simulation` BC outside SoR biotechnology.
- Module-local LLM or owning EMR clinical simulation SoR.
- Shipping predictions without validation workflow.

## Related

Law: `ENTERPRISE_BIOTECHNOLOGY_SIMULATION.md` · Prior: ADR 499–505 · Next: P217-H
