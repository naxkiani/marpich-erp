# ADR 492 — Enterprise Robotics Government Intelligence (P216-T)

## Status

Accepted

## Context

P216-R established financial robotics / autonomous banking. P216-S (legal) remains planned (ADR 491 reserved). P216-J/M/N remain planned. P216-T extends MEOS Robotics into government robotics, autonomous public services, digital government intelligence, and smart governance automation — preparing for P216-U military/defense robotics.

## Decision

1. SoR remains `robotics` / `CAP-PLT-RB-001`.
2. Fabric: `meos_government_intelligence_fabric`.
3. API: `/api/v1/robotics/government*`.
4. Core domain: Enterprise Government Intelligence; aggregate GovernmentIntelligenceAggregate.
5. Eight bounded contexts (citizen experience through governance & compliance).
6. Citizen identity via Identity Platform; national ID/government ERP via Integration Platform — never module-local auth or vendor embeds in domain.
7. Physical AI via P214-Z / P216-E ACL; never module-local LLM.
8. Never duplicate government or municipality core logic; government ≠ municipality; store peer IDs only.
9. Privacy by design, human governance oversight, and explainable AI; ungated physical autonomy forbidden.
10. Never replace Core, AI, Quantum, Identity, or prior delivered P216 fabrics (through P216-R).
11. ADR 491 reserved for planned P216-S; ADRs 482/485/486 remain reserved for planned J/M/N.

## Consequences

Positive: unified government cyber-physical intelligence under robotics SoR.  
Negative: government/municipality/national ID remain external SoRs; robotics projects via ACL and events.

## Alternatives rejected

- Sibling `government_robotics` BC outside SoR robotics.
- Embedding government ERP or national identity engines in robotics domain.
- Merging government with municipality bounded contexts.
- Fully autonomous public-service agents without human oversight and explainability envelopes.

## Related

Law: `ENTERPRISE_ROBOTICS_GOVERNMENT.md`  
Roadmap: `robotics/P216_MASTER_SERIES_ROADMAP.v1.yaml`
