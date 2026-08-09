# ADR 599 — Enterprise Autonomous Transportation & Mobility Intelligence Platform (P239)

## Status
Accepted

## Context
P238 established EASCUI (urban intelligence). P239 opens the Enterprise Autonomous Transportation & Mobility Intelligence Platform (EATMIP) for mobility orchestration, traffic/fleet intelligence, route optimization, public transit intel and autonomous transportation assist under MEOS 11.0. P238 remains city SoR; P232 remains freight/supply SoR; P216 remains physical robot/AV mission SoR — EATMIP is mobility intelligence only and must never issue ungated vehicle/traffic OT actuation.

## Decision
1. SoR `mobility_intelligence`; fabric `meos_enterprise_autonomous_transportation_mobility_intelligence_platform_framework`; API `/api/v1/mobility-intelligence*`; capability `CAP-PLT-EATMIP-001`.
2. Ten logical BCs inside one SoR: Mobility Management, Transportation Intelligence, Fleet Operations, Autonomous Vehicles, Traffic Management, Route Optimization, Public Transit, Safety Management, Logistics Mobility, Mobility Governance.
3. Federate with P238, P232, P216, municipality, P237, P221, P227, P228, P225, P224, P229 via ACL/events — never replace them.
4. Inference only via P214-Z; actuation via Workflow + Robotics/Municipality/Integration adapters; policy via Policy Engine; audit via Audit; simulation ≠ execute.
5. Never ungated vehicle/traffic OT actuation; never V2X/traffic-controller SDKs in domain; never dual-write shipment or city control tables; never module-local LLM; never bypass transportation safety interlocks.
6. Roadmap: P239 foundation → P239-A…D (mobility domain → AI/twin/KG → autonomous assist → civilization-scale gated mobility intel).

## Consequences
Positive: governed mobility control-tower intelligence federated with city, freight and robotics peers.  
Negative: shipments, AV physical missions and municipal transit cases remain peer-owned — EATMIP stores mobility models, routes, fleets intel and peer refs only.

## Links
Law: `ENTERPRISE_AUTONOMOUS_TRANSPORTATION_MOBILITY_INTELLIGENCE_PLATFORM.md` · Prior: ADR 598 · Next: P239-A · Peer: ADR 600 (P240 EAGDGIP)
