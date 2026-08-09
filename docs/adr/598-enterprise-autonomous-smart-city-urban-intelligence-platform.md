# ADR 598 — Enterprise Autonomous Smart City & Urban Intelligence Platform (P238)

## Status
Accepted

## Context
P237 established EAEISR (energy intelligence). P238 opens the Enterprise Autonomous Smart City & Urban Intelligence Platform (EASCUI) for urban intelligence, adaptive infrastructure, citizen-centric services, mobility, public safety and city twin assist under MEOS 11.0. Municipality remains local-government SoR; Government remains national/regional SoR (never merge); P230 remains privacy/trust SoR — EASCUI is urban intelligence only and must never issue ungated city OT actuation or silent consent overrides.

## Decision
1. SoR `urban_intelligence`; fabric `meos_enterprise_autonomous_smart_city_urban_intelligence_platform_framework`; API `/api/v1/urban-intelligence*`; capability `CAP-PLT-EASCUI-001`.
2. Ten logical BCs inside one SoR: Urban Management, Infrastructure Intelligence, Citizen Services, Mobility Management, Public Safety, Environmental Intelligence, City Planning, Resource Management, Urban Governance, Digital City Twin.
3. Federate with municipality, government, P230, P237, P222, P221, P220, P227, P228, P225, P224, P229 via ACL/events — never replace them; never merge municipality and government.
4. Inference only via P214-Z; actuation via Workflow + Municipality/Integration city OT adapters; consent via P230 + Identity; policy via Policy Engine; audit via Audit.
5. Never ungated city OT actuation; never traffic/SCADA SDKs in domain; never local citizen PII vaults; never dual-write permit/utility/case tables; never module-local LLM; never silent consent override.
6. Roadmap: P238 foundation → P238-A…D (urban domain → twin/AI/KG → autonomous assist → civilization-scale gated city intel).

## Consequences
Positive: governed smart-city control-tower intelligence federated with municipal, energy, privacy and resilience peers.  
Negative: permits, utility bills, cases and identity remain peer-owned — EASCUI stores city models, intel profiles and peer refs only.

## Links
Law: `ENTERPRISE_AUTONOMOUS_SMART_CITY_URBAN_INTELLIGENCE_PLATFORM.md` · Prior: ADR 597 · Next: P238-A · Peer: ADR 599 (P239 EATMIP)
