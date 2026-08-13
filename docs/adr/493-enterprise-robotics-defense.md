# ADR 493 — Enterprise Robotics Defense Intelligence (P216-U)

## Status

Accepted

## Context

P216-T established government robotics / smart governance. P216-S (legal) remains planned (ADR 491 reserved). P216-J/M/N remain planned. P216-U extends MEOS Robotics into military robotics management, autonomous defense system governance, strategic security intelligence, and national defense AI decision support — preparing for P216-V science robotics.

## Decision

1. SoR remains `robotics` / `CAP-PLT-RB-001`.
2. Fabric: `meos_defense_intelligence_fabric`.
3. API: `/api/v1/robotics/defense*`.
4. Core domain: Enterprise Defense Intelligence; aggregate DefenseIntelligenceAggregate.
5. Eight bounded contexts (strategic intelligence through defense governance).
6. Public safety via P216-L ACL; government via P216-T peer IDs; cybersecurity/emergency via Integration Platform.
7. Physical AI via P214-Z / P216-E ACL; never module-local LLM.
8. Never duplicate public safety core logic; store peer IDs only.
9. Human authorization control, responsible AI governance, and explainable AI are mandatory; ungated physical autonomy forbidden.
10. Autonomous system activation requires Workflow-gated human authorization.
11. Never replace Core, AI, Quantum, or prior delivered P216 fabrics (through P216-T).
12. ADR 491 reserved for planned P216-S; ADRs 482/485/486 remain reserved for planned J/M/N.

## Consequences

Positive: unified defense cyber-physical intelligence under robotics SoR with human oversight.  
Negative: public safety/government/cyber platforms remain external SoRs; robotics projects via ACL and events.

## Alternatives rejected

- Sibling `military_robotics` BC outside SoR robotics.
- Embedding public safety or national C2 engines in robotics domain.
- Fully autonomous mission activation without human authorization envelopes.

## Related

Law: `ENTERPRISE_ROBOTICS_DEFENSE.md`  
Roadmap: `robotics/P216_MASTER_SERIES_ROADMAP.v1.yaml`
