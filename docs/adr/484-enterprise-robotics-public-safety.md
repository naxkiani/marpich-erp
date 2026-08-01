# ADR 484 — Enterprise Robotics Public Safety & Civil Protection (P216-L)

## Status

Accepted

## Context

P216-K established construction intelligence. P216-J (agriculture) remains planned. P216-L extends MEOS Robotics into public safety robotics, emergency operations, disaster recovery, civil protection, and disaster digital twins — preparing for P216-M space robotics. (Earlier roadmap draft labeled P216-L as defense; this ADR supersedes that draft title with the civil protection scope defined by the P216-L prompt.)

## Decision

1. SoR remains `robotics` / `CAP-PLT-RB-001`.
2. Fabric: `meos_civil_protection_intelligence_fabric`.
3. API: `/api/v1/robotics/public-safety*`.
4. Core domain: Enterprise Emergency & Civil Protection Intelligence; aggregate EmergencyManagementAggregate.
5. Eight bounded contexts (incident management through community resilience).
6. GIS/Weather/IoT via Integration Platform; citizen alerts via Notification Platform.
7. Physical AI via P214-Z / P216-E ACL; never module-local LLM.
8. Never duplicate hospital/clinic core logic; store peer IDs only.
9. Human-centered, explainable AI; ungated physical autonomy forbidden.
10. Never replace Core, AI, Quantum, or prior P216 fabrics (through P216-K).
11. ADR 482 remains reserved for planned P216-J agriculture.

## Consequences

Positive: unified civil protection cyber-physical intelligence under robotics SoR.  
Negative: agency/EOC/HIS peer systems remain external SoRs; robotics projects via ACL and events.

## Alternatives rejected

- Sibling `public_safety` BC outside SoR robotics.
- Embedding weather/GIS stacks or SMTP alerts in robotics domain.
- Fully autonomous emergency robotics without human oversight.

## Related

Law: `ENTERPRISE_ROBOTICS_PUBLIC_SAFETY.md`  
Roadmap: `robotics/P216_MASTER_SERIES_ROADMAP.v1.yaml`
