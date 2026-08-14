# ADR 480 — Enterprise Robotics Autonomous Mobility (P216-H)

## Status

Accepted

## Context

P216-G established autonomous logistics/warehouse automation. P216-H extends MEOS Robotics into connected vehicles, autonomous navigation, drone/UAS operations, fleet mobility, traffic intelligence, and transportation digital twins — preparing for P216-I healthcare robotics.

## Decision

1. SoR remains `robotics` / `CAP-PLT-RB-001`.
2. Fabric: `meos_autonomous_mobility_fabric`.
3. API: `/api/v1/robotics/mobility*`.
4. Core domain: Enterprise Autonomous Mobility Intelligence; aggregate MobilityAggregate.
5. Eight bounded contexts (connected vehicle through vehicle maintenance).
6. V2X/telematics/OTA via Integration Platform — never direct vendor embeds in domain.
7. Physical AI via P214-Z ACL; runtime/fleet via P216-D; logistics sync via P216-G.
8. Never replace Core, AI, Quantum, or prior P216 fabrics.

## Consequences

Positive: unified autonomous mobility under MEOS robotics SoR.  
Negative: public ITS / airspace authorities remain external SoR; robotics stores peer IDs and local projections.

## Alternatives rejected

- Sibling `mobility` BC outside SoR robotics.
- Embedding V2X stacks in robotics domain.
- Ungated autonomous driving without safety envelopes.

## Related

Law: `ENTERPRISE_ROBOTICS_MOBILITY.md`  
Roadmap: `robotics/P216_MASTER_SERIES_ROADMAP.v1.yaml`
