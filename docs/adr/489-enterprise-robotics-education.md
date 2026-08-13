# ADR 489 — Enterprise Robotics Education Intelligence (P216-Q)

## Status

Accepted

## Context

P216-P established hospitality robotics / smart hotels. P216-J/M/N remain planned. P216-Q extends MEOS Robotics into education robotics, intelligent learning systems, autonomous campus operations, and AI education intelligence — preparing for P216-R financial robotics.

## Decision

1. SoR remains `robotics` / `CAP-PLT-RB-001`.
2. Fabric: `meos_education_intelligence_fabric`.
3. API: `/api/v1/robotics/education*`.
4. Core domain: Enterprise Education Intelligence; aggregate EducationIntelligenceAggregate.
5. Eight bounded contexts (student intelligence through education governance).
6. SIS/LMS/library/research via Integration Platform and peer APIs — never direct vendor embeds in domain.
7. Physical AI via P214-Z / P216-E ACL; never module-local LLM.
8. Never duplicate SIS/LMS core logic; store peer IDs only.
9. Privacy by design, accessibility by design, and human-centered learning; ungated physical autonomy forbidden.
10. Never replace Core, AI, Quantum, or prior delivered P216 fabrics (through P216-P).
11. ADRs 482/485/486 remain reserved for planned J/M/N.

## Consequences

Positive: unified education cyber-physical intelligence under robotics SoR.  
Negative: SIS/LMS remain external SoRs; robotics projects via ACL and events.

## Alternatives rejected

- Sibling `education_robotics` BC outside SoR robotics.
- Embedding SIS/LMS engines in robotics domain.
- Fully autonomous teaching robots without privacy, accessibility, and safety envelopes.

## Related

Law: `ENTERPRISE_ROBOTICS_EDUCATION.md`  
Roadmap: `robotics/P216_MASTER_SERIES_ROADMAP.v1.yaml`
