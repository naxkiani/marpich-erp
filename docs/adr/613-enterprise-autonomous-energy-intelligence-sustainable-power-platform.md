# ADR 613 — Enterprise Autonomous Energy Intelligence & Sustainable Power Platform (P254)

## Status
Accepted

## Context
P253 established EAHILSP (health–life-sciences intelligence). P254 opens the Enterprise Autonomous Energy Intelligence & Sustainable Power Platform (EAEISPP) for smart-grid, renewables, storage, power trading and energy-transition intelligence under MEOS 11.0. P237 already owns SoR `energy_intelligence` and `/api/v1/energy-intelligence*`; P222 remains ESG/carbon SoR; Financial Kernel remains settlement SoR — EAEISPP must not fork those SoRs and must never issue ungated grid/OT actuation or dual-write carbon ledgers.

## Decision
1. SoR `sustainable_power_intelligence` (not `energy_intelligence`); fabric `meos_enterprise_autonomous_energy_intelligence_sustainable_power_platform_framework`; API `/api/v1/sustainable-power-intelligence*`; capability `CAP-PLT-EAEISPP-001`.
2. Ten logical BCs inside one SoR: Energy Management, Grid Intelligence, Renewable Energy, Energy Assets, Energy Trading, Storage Management, Carbon Intelligence, Energy Analytics, Energy Governance, Energy Evolution.
3. Federate with P237, P222, Financial Kernel, P231/P244, P252, P248, P221, P227, P228, P229, P224 via ACL/events — never replace them; never dual-write P237/P222; never fork `/api/v1/energy-intelligence*`.
4. Inference only via P214-Z; execute/trade via Workflow + Integration + Financial Kernel; carbon signals only to P222; simulation ≠ execute.
5. Never SCADA/EMS/PSP SDKs in domain; never local GL; never module-local LLM; never opaque unexplainable dispatch/trade recommendations; never ungated grid actuation.
6. Roadmap: P254 foundation → P254-A…D (power domain → AI/KG/twin → autonomous assist → civilization-scale gated sustainable power intel).

## Consequences
Positive: governed power/grid control-tower intelligence federated with energy-resource and ESG peers.  
Negative: broader energy intel, carbon ledgers and settlements remain peer-owned — EAEISPP stores power models, grid/storage/trading intents and peer refs only.

## Links
Law: `ENTERPRISE_AUTONOMOUS_ENERGY_INTELLIGENCE_SUSTAINABLE_POWER_PLATFORM.md` · Prior: ADR 612 · Next: P254-A · Peer: ADR 614 (P257 MERAF)
