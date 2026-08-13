# ADR 494 — Enterprise Robotics Scientific Intelligence (P216-V)

## Status

Accepted

## Context

P216-U established defense robotics / strategic security intelligence. P216-S (legal) and P216-J/M/N remain planned. P216-V extends MEOS Robotics into science robotics, research automation, autonomous laboratories, scientific AI intelligence, and discovery acceleration — preparing for P216-W personal robotics.

## Decision

1. SoR remains `robotics` / `CAP-PLT-RB-001`.
2. Fabric: `meos_scientific_intelligence_fabric`.
3. API: `/api/v1/robotics/science*`.
4. Core domain: Enterprise Scientific Intelligence; aggregate ScientificIntelligenceAggregate.
5. Eight bounded contexts (scientific research through research governance).
6. LIMS/scientific databases via Integration Platform; healthcare via P216-I ACL; Physical AI via P214-Z / P216-E.
7. Never module-local LLM; AI Scientist surfaces via P214-Z ACL only.
8. Human scientific oversight, reproducibility by design, research ethics, and explainable AI are mandatory; ungated physical autonomy forbidden.
9. Never replace Core, AI, Quantum, or prior delivered P216 fabrics (through P216-U).
10. ADRs 482/485/486/491 remain reserved for planned J/M/N/S.

## Consequences

Positive: unified scientific cyber-physical intelligence under robotics SoR.  
Negative: LIMS and institutional research systems remain external SoRs; robotics projects via ACL and events.

## Alternatives rejected

- Sibling `science_robotics` BC outside SoR robotics.
- Embedding LIMS or institutional research engines in robotics domain.
- Fully autonomous discovery without human scientific oversight and reproducibility envelopes.

## Related

Law: `ENTERPRISE_ROBOTICS_SCIENCE.md`  
Roadmap: `robotics/P216_MASTER_SERIES_ROADMAP.v1.yaml`
