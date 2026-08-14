# ADR 533 — Enterprise Space Intelligence Orbital Intelligence (P218-G)

## Status

Accepted

## Context

P218-F established satellite/constellation operations. P218-G defines SSA, orbital traffic management, conjunction assessment, collision avoidance, debris intelligence, orbital digital twin and knowledge graph — before Space Communications (P218-H).

## Decision

1. SoR remains `space` / `CAP-PLT-SP-001`.
2. Fabric: `meos_orbital_intelligence_fabric`.
3. API: `/api/v1/space/orbital*`.
4. Five orbital intelligence layers; SSA + OTM + collision avoidance + debris catalogs.
5. All orbital AI via P214-Z / P218-E ACL only — `no_module_local_llm`.
6. Sensor / SSA feeds via Integration Platform — `no_module_local_ssa_sensor_stack`.
7. Maneuver execution requires Workflow + Policy — never ungated collision avoidance maneuver; human override always available.
8. Never replace Core, AI, Quantum, Robotics, Biotechnology, prior P218 fabrics (including P218-F).
9. Foundation for P218-H.

## Consequences

Positive: safety-critical orbital awareness foundation for autonomous space ops.  
Negative: conjunction pipelines must stay aligned with Satellite (P218-F), Quantum (P215-Z) and Space AI (P218-E) contracts.

## Alternatives rejected

- Sibling `orbital` BC outside SoR space.
- Fully autonomous maneuver execution without human override.
- Module-local SSA sensor brokers.

## Related

Law: `ENTERPRISE_SPACE_INTELLIGENCE_ORBITAL.md` · Prior: ADR 526–532 · Next: P218-H
