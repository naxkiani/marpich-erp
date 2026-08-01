# ADR 474 — Enterprise Robotics Strategic Architecture (P216-B)

## Status

Accepted

## Context

P216-A established mission/vision. P216-B defines strategic architecture layers, capability model, operating framework, service/org/governance models, data/security/integration, maturity, CQRS and events — without owning deep DDD aggregates (P216-C).

## Decision

1. SoR remains `robotics` / `CAP-PLT-RB-001`.
2. Fabric: `meos_robotics_strategic_architecture_framework`.
3. API: `/api/v1/robotics/strategy*`.
4. Five architecture layers (Physical → Edge → Platform → Enterprise Intelligence → MEOS Control).
5. Seven capability domains; five operating-model layers; CoE + Governance Board as catalog surfaces.
6. Core robotics services catalogued with purpose/ownership/APIs/events/data/security — runtime implementation in later phases.
7. Never replace Core, AI, Quantum, P216 foundation, or P216-A mission fabrics.

## Consequences

Positive: scalable operating model and capability-driven planning.  
Negative: strategy catalog must stay aligned with P216-C bounded contexts.

## Alternatives rejected

- Merging strategy into mission fabric (scope explosion).
- Module-local ROS/fleet DBs as enterprise SoR.
- Ungated physical autonomy.

## Related

Law: `ENTERPRISE_ROBOTICS_STRATEGY.md`  
Roadmap: `robotics/P216_MASTER_SERIES_ROADMAP.v1.yaml`
