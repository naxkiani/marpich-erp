# ADR 483 — Enterprise Robotics Construction Intelligence (P216-K)

## Status

Accepted

## Context

P216-I established healthcare robotics. P216-J (agriculture) remains planned. P216-K extends MEOS Robotics into construction robotics, smart infrastructure, autonomous building systems, BIM-native digital twins, and construction knowledge graphs — preparing for P216-L defense robotics.

## Decision

1. SoR remains `robotics` / `CAP-PLT-RB-001`.
2. Fabric: `meos_construction_intelligence_fabric`.
3. API: `/api/v1/robotics/construction*`.
4. Core domain: Enterprise Construction Intelligence; aggregate ConstructionAggregate.
5. Eight bounded contexts (construction management through safety & compliance).
6. BIM/GIS/SCADA/IoT via Integration Platform — never direct vendor embeds in domain.
7. Physical AI via P214-Z / P216-E ACL; never module-local LLM.
8. Never duplicate construction core logic; store peer IDs only.
9. ISO 19650 / BIM-native; ungated physical autonomy forbidden.
10. Never replace Core, AI, Quantum, or prior P216 fabrics (through P216-I).
11. ADR 482 reserved for planned P216-J agriculture.

## Consequences

Positive: unified construction cyber-physical intelligence under robotics SoR.  
Negative: construction/BIM/facility peer SoRs remain external; robotics projects via ACL and events.

## Alternatives rejected

- Sibling `construction_robotics` BC outside SoR robotics.
- Embedding BIM/SCADA stacks in robotics domain.
- Ungated autonomous heavy equipment without safety envelopes.

## Related

Law: `ENTERPRISE_ROBOTICS_CONSTRUCTION.md`  
Roadmap: `robotics/P216_MASTER_SERIES_ROADMAP.v1.yaml`
