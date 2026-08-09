# ADR 597 — Enterprise Autonomous Energy Intelligence & Sustainable Resource Platform (P237)

## Status
Accepted

## Context
P236 established EAMII (manufacturing intelligence). P237 opens the Enterprise Autonomous Energy Intelligence & Sustainable Resource Platform (EAEISR) for intelligent energy management, renewable optimization, smart grid analytics, demand forecast, carbon signals and climate scenario assist under MEOS 11.0. P222 EGSRIP remains sustainability/ESG SoR; P220 remains planetary climate SoR — EAEISR is energy/resource intelligence only and must never issue ungated grid/OT actuation or dual-write carbon ledgers.

## Decision
1. SoR `energy_intelligence`; fabric `meos_enterprise_autonomous_energy_intelligence_sustainable_resource_platform_framework`; API `/api/v1/energy-intelligence*`; capability `CAP-PLT-EAEISR-001`.
2. Ten logical BCs inside one SoR: Energy Management, Renewable Systems, Resource Intelligence, Smart Grid Operations, Sustainability Management (energy lens), Carbon Management (signals), Environmental Intelligence, Energy Trading Intelligence, Climate Governance, Resource Optimization.
3. Federate with P222, P220, P221, P236, P227, P228, P225, P224, P229 via ACL/events — never replace them.
4. Inference only via P214-Z; actuation via Workflow + Integration utility/OT adapters; policy via Policy Engine; audit via Audit; settlements via Financial Kernel.
5. Never ungated grid/OT actuation; never SCADA/EMS SDKs in domain; never dual-write ESG carbon ledgers or GL; never module-local LLM; never bypass environmental/safety interlocks.
6. Roadmap: P237 foundation → P237-A…D (energy domain → AI/twin/KG → autonomous assist → civilization-scale gated energy intel).

## Consequences
Positive: governed energy control-tower intelligence federated with sustainability and planetary peers.  
Negative: ESG ledgers, crisis ops and utility control remain peer-owned — EAEISR stores energy models, forecasts, grid intel and peer refs only.

## Links
Law: `ENTERPRISE_AUTONOMOUS_ENERGY_INTELLIGENCE_SUSTAINABLE_RESOURCE_PLATFORM.md` · Prior: ADR 596 · Next: P237-A · Peer: ADR 598 (P238 EASCUI)
