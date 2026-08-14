# ADR 488 — Enterprise Robotics Hospitality Intelligence (P216-P)

## Status

Accepted

## Context

P216-O established autonomous commerce / retail robotics. P216-J/M/N remain planned. P216-P extends MEOS Robotics into hospitality robotics, smart hotels, autonomous guest services, and intelligent hospitality experience — preparing for P216-Q education robotics.

## Decision

1. SoR remains `robotics` / `CAP-PLT-RB-001`.
2. Fabric: `meos_hospitality_intelligence_fabric`.
3. API: `/api/v1/robotics/hospitality*`.
4. Core domain: Enterprise Hospitality Intelligence; aggregate HospitalityIntelligenceAggregate.
5. Eight bounded contexts (guest experience through hospitality governance).
6. Booking/PMS/payment via Integration Platform and peer APIs — never direct vendor embeds in domain.
7. Physical AI via P214-Z / P216-E ACL; never module-local LLM.
8. Never duplicate hotel/PMS core logic; store peer IDs only.
9. Privacy by design and human-centered hospitality; ungated physical autonomy forbidden.
10. Never replace Core, AI, Quantum, or prior delivered P216 fabrics (through P216-O).
11. ADRs 482/485/486 remain reserved for planned J/M/N.

## Consequences

Positive: unified hospitality cyber-physical intelligence under robotics SoR.  
Negative: hotel/PMS/booking remain external SoRs; robotics projects via ACL and events.

## Alternatives rejected

- Sibling `hospitality_robotics` BC outside SoR robotics.
- Embedding PMS/booking engines in robotics domain.
- Fully autonomous guest robots without privacy and safety envelopes.

## Related

Law: `ENTERPRISE_ROBOTICS_HOSPITALITY.md`  
Roadmap: `robotics/P216_MASTER_SERIES_ROADMAP.v1.yaml`
