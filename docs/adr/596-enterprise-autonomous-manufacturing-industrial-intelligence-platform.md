# ADR 596 — Enterprise Autonomous Manufacturing & Industrial Intelligence Platform (P236)

## Status
Accepted

## Context
P235 established EAHRWIP (workforce intelligence). P236 opens the Enterprise Autonomous Manufacturing & Industrial Intelligence Platform (EAMII) for smart factory intelligence, autonomous production assist, IIoT analytics, predictive maintenance, quality intelligence and robotics coordination under MEOS 11.0. Manufacturing remains production SoR; Robotics/P216 remains physical AI SoR — EAMII is industrial intelligence only and must never issue ungated OT actuation.

## Decision
1. SoR `manufacturing_intelligence`; fabric `meos_enterprise_autonomous_manufacturing_industrial_intelligence_platform_framework`; API `/api/v1/manufacturing-intelligence*`; capability `CAP-PLT-EAMII-001`.
2. Ten logical BCs inside one SoR: Manufacturing Management, Production Intelligence, Industrial IoT, Quality, Maintenance, Robotics Operations plans, Factory Simulation, Resource Optimization, Industrial Safety, Governance.
3. Federate with manufacturing, robotics/P216, P225, P232, P227, P228, P224 via ACL/events — never replace them.
4. Inference only via P214-Z; actuation via Workflow + Manufacturing/Robotics; OT/IIoT via Integration Platform; policy via Policy Engine; audit via Audit.
5. Never ungated physical/OT actuation; never PLC/robot SDKs in domain; never dual-write production control tables; never module-local LLM; never bypass safety interlocks.
6. Roadmap: P236 foundation → P236-A…D (factory models → AI/twin/IIoT → autonomous assist → civilization-scale gated industrial intel).

## Consequences
Positive: governed smart-factory control-tower intelligence across manufacturing and robotics peers.  
Negative: work orders, machine control and robot missions remain peer-owned — EAMII stores factory models, predictions, plans and safety cases with peer refs only.

## Links
Law: `ENTERPRISE_AUTONOMOUS_MANUFACTURING_INDUSTRIAL_INTELLIGENCE_PLATFORM.md` · Prior: ADR 595 · Next: P236-A · Peer: ADR 597 (P237 EAEISR)
