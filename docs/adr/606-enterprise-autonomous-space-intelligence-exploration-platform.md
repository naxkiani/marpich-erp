# ADR 606 — Enterprise Autonomous Space Intelligence & Exploration Platform (P247)

## Status
Accepted

## Context
P246 established EASC-DTIP (security–trust intelligence). P247 opens the Enterprise Autonomous Space Intelligence & Exploration Platform (EASIEP) for exploration/mission-evolution intelligence, orbital assist, planetary exploration modeling and gated autonomous space operations under MEOS 11.0. P218 already completed the canonical Space Intelligence series with SoR `space` (CAP-PLT-SP-001, `/api/v1/space*`) — EASIEP must not fork that SoR and must never issue ungated spacecraft/ground-segment actuation.

## Decision
1. SoR `space_exploration_intelligence` (not `space`); fabric `meos_enterprise_autonomous_space_intelligence_exploration_platform_framework`; API `/api/v1/space-exploration-intelligence*`; capability `CAP-PLT-EASIEP-001`.
2. Ten logical BCs inside one SoR: Space Mission Management, Orbital Operations, Satellite Intelligence, Planetary Intelligence, Space Exploration, Space Resource Management, Space Data Management, Mission Simulation, Space Governance, Space Evolution.
3. Federate with P218, P242, P220, P216, P215, P246/P226/P210, P227, P228, P229, P224, P221 via ACL/events — never replace them; never dual-write P218; never fork `/api/v1/space*`.
4. Inference only via P214-Z; execute via Workflow + P218/Integration ground-segment adapters; simulation ≠ execute; mission safety fail-closed.
5. Never TT&C/spacecraft SDKs in domain; never module-local LLM; never opaque unexplainable mission recommendations; never bypass human authority for critical maneuvers.
6. Roadmap: P247 foundation → P247-A…D (exploration domain → AI/KG/twin → autonomous assist → civilization-scale gated space exploration intel).

## Consequences
Positive: governed exploration control-tower intelligence federated with the completed P218 Space SoR.  
Negative: canonical missions, satellites and orbital ops remain P218-owned — EASIEP stores exploration/evolution models and peer refs only.

## Links
Law: `ENTERPRISE_AUTONOMOUS_SPACE_INTELLIGENCE_EXPLORATION_PLATFORM.md` · Prior: ADR 605 · Next: P247-A · Peer: ADR 607 (P248 EAEIPSP)
