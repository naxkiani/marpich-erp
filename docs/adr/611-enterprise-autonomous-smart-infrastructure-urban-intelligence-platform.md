# ADR 611 — Enterprise Autonomous Smart Infrastructure & Urban Intelligence Platform (P252)

## Status
Accepted

## Context
P251 established EAHCDWIP (human capability intelligence). P252 opens the Enterprise Autonomous Smart Infrastructure & Urban Intelligence Platform (EASIUIP) for infrastructure asset/lifecycle/ops depth, urban infra twin assist and gated city OT orchestration under MEOS 11.0. P238 already owns SoR `urban_intelligence` and `/api/v1/urban-intelligence*` — EASIUIP must not fork that SoR. Municipality and Government remain distinct service SoRs; P239/P237 remain mobility/energy depth SoRs.

## Decision
1. SoR `smart_infrastructure_intelligence` (not `urban_intelligence`); fabric `meos_enterprise_autonomous_smart_infrastructure_urban_intelligence_platform_framework`; API `/api/v1/smart-infrastructure-intelligence*`; capability `CAP-PLT-EASIUIP-001`.
2. Ten logical BCs inside one SoR: Urban Management, Infrastructure Management, Mobility Management, Energy Management, Public Services, Community Intelligence, Environmental Management, Urban Planning, City Simulation, Urban Governance.
3. Federate with P238, P239, P237, P248, municipality, government, P230, P221, P240, P225, P227, P228, P229, P224 via ACL/events — never replace them; never dual-write P238; never fork `/api/v1/urban-intelligence*`; never merge municipality and government.
4. Inference only via P214-Z; execute via Workflow + Municipality/Integration; privacy via P230; simulation ≠ execute.
5. Never ungated city OT; never SCADA/traffic SDKs in domain; never local citizen PII vaults; never silent consent override; never module-local LLM.
6. Roadmap: P252 foundation → P252-A…D (infra domain → AI/KG/twin → autonomous assist → civilization-scale gated smart infrastructure intel).

## Consequences
Positive: governed infrastructure control-tower intelligence federated with urban, mobility and energy peers.  
Negative: city-wide urban intel, mobility/energy SoRs and municipal cases remain peer-owned — EASIUIP stores infrastructure models and peer refs only.

## Links
Law: `ENTERPRISE_AUTONOMOUS_SMART_INFRASTRUCTURE_URBAN_INTELLIGENCE_PLATFORM.md` · Prior: ADR 610 · Next: P252-A · Peer: ADR 612 (P253 EAHILSP)
