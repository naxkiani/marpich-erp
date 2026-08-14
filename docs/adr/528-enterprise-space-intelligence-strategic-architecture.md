# ADR 528 — Enterprise Space Intelligence Strategic Architecture (P218-B)

## Status

Accepted

## Context

P218-A established mission/vision/capability framework. P218-B defines strategic architecture layers, enterprise capability model, operating model, space operating framework, value network, maturity, governance, MEOS integration and transformation blueprint — without owning deep DDD aggregates (P218-C).

## Decision

1. SoR remains `space` / `CAP-PLT-SP-001`.
2. Fabric: `meos_space_intelligence_strategic_architecture_framework`.
3. API: `/api/v1/space/strategy*`.
4. Five architecture layers (Business Strategy → Capability → Process → Application → Technology).
5. Twenty L1 capabilities in six groups; ten operating dimensions; six space operating framework layers.
6. Six maturity levels (Manual → Self Optimising); four transformation phases.
7. Never replace Core, AI, Quantum, Robotics, Biotechnology, P218 foundation, or P218-A mission.
8. Human mission oversight, space cybersecurity and sustainability required; opaque / ungated autonomous mission strategy forbidden.
9. Serve as strategic architecture foundation for P218-C.

## Consequences

Positive: scalable space operating model and capability-driven planning.  
Negative: strategy catalog must stay aligned with P218-C bounded contexts.

## Alternatives rejected

- Merging strategy into mission fabric (scope explosion).
- Sibling `space_strategy` BC outside SoR space.
- Ungated autonomous mission operating model.

## Related

Law: `ENTERPRISE_SPACE_INTELLIGENCE_STRATEGY.md`  
Prior: ADR 526 · ADR 527 · Next: P218-C
