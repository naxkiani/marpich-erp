# ADR 538 — Enterprise Space Intelligence Exploration Intelligence (P218-L)

## Status

Accepted

## Context

P218-K established scientific intelligence. P218-L defines space exploration intelligence spanning lunar, Mars, deep-space and interplanetary operations — before Space Manufacturing (P218-M).

## Decision

1. SoR remains `space` / `CAP-PLT-SP-001`.
2. Fabric: `meos_space_exploration_intelligence_fabric`.
3. API: `/api/v1/space/exploration*`.
4. Five exploration layers; lunar + Mars + deep-space + exploration-AI + autonomy catalogs.
5. All exploration AI via P214-Z / P218-E ACL only — `no_module_local_llm`.
6. Planetary landing, planetary protection and crew safety require Workflow + Policy — never ungated planetary landing authorization; never skip planetary protection compliance.
7. Never replace Core, AI, Quantum, Robotics, Biotechnology, prior P218 fabrics (including P218-K scientific).
8. Foundation for P218-M.

## Consequences

Positive: enterprise exploration platform for all future planetary missions.  
Negative: surface operations must stay aligned with Mission Intel (P218-J), Scientific (P218-K), Navigation (P218-I), Robotics (P216-Z) and planetary-protection contracts.

## Alternatives rejected

- Sibling `exploration` BC outside SoR space.
- Fully autonomous landing without planetary protection gates.
- Module-local LLM for terrain/hazard decisions.

## Related

Law: `ENTERPRISE_SPACE_INTELLIGENCE_EXPLORATION.md` · Prior: ADR 526–537 · Next: P218-M
