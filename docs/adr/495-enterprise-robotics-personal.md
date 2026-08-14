# ADR 495 — Enterprise Robotics Personal Intelligence (P216-W)

## Status

Accepted

## Context

P216-V established science robotics / autonomous laboratories. P216-S (legal) and P216-J/M/N remain planned. P216-W extends MEOS Robotics into personal robotics, consumer autonomous assistants, home intelligence, personal AI robotics, and human augmentation — preparing for P216-X entertainment robotics.

## Decision

1. SoR remains `robotics` / `CAP-PLT-RB-001`.
2. Fabric: `meos_personal_intelligence_fabric`.
3. API: `/api/v1/robotics/personal*`.
4. Core domain: Personal Intelligence Management; aggregate PersonalIntelligenceAggregate.
5. Eight bounded contexts (personal AI assistant through personal governance).
6. Identity via Identity Platform; IoT/smart home/wearables via Integration Platform — never module-local auth or vendor IoT hubs in domain.
7. Physical AI via P214-Z / P216-E ACL; never module-local LLM.
8. Privacy first, personal data sovereignty, human control by design, and consent management are mandatory; ungated physical autonomy forbidden.
9. Never replace Core, AI, Quantum, Identity, or prior delivered P216 fabrics (through P216-V).
10. ADRs 482/485/486/491 remain reserved for planned J/M/N/S.

## Consequences

Positive: unified personal cyber-physical intelligence under robotics SoR with privacy sovereignty.  
Negative: IoT/smart-home platforms remain external SoRs; robotics projects via ACL and events.

## Alternatives rejected

- Sibling `personal_robotics` BC outside SoR robotics.
- Embedding consumer IoT hubs or personal auth engines in robotics domain.
- Fully autonomous personal robots without consent, privacy, and human-control envelopes.

## Related

Law: `ENTERPRISE_ROBOTICS_PERSONAL.md`  
Roadmap: `robotics/P216_MASTER_SERIES_ROADMAP.v1.yaml`
