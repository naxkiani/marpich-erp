# ADR 622 — MEOS Enterprise Digital Twin Intelligence Platform (P265)

## Status
Accepted

## Context
P264 established MEKGSI over P228 knowledge graph. P265 productizes Digital Twin Intelligence as the MEOS Reality Intelligence Operating Layer. P227 EDTISP already owns `digital_twin` and `/api/v1/digital-twin*`. MEDTIP must federate that SoR — never fork the twin API, never embed IoT/SCADA SDKs in domain, and never treat simulation as production execute. P266 is planned for AI Agent Orchestration & Autonomous Intelligence over P214-Z / AI Platform.

## Decision
1. SoR `twin_intelligence`; fabric `meos_enterprise_digital_twin_intelligence_operating_platform_framework`; API `/api/v1/twin-intelligence*`; capability `CAP-PLT-MEDTIP-001`; acronym **MEDTIP**.
2. Logical BCs inside one SoR: Twin Management operating, Simulation Management, Optimization, Predictive Twin, Synchronization Operating, Twin Governance.
3. Federate with P227, Integration Platform, P228/P264, P229/P263, P262, P261, P260, P257–P259, P214-Z, Policy, Audit — never replace them; never dual-write `digital_twin_*`.
4. Inference only via P214-Z; simulation ≠ execute; IoT via Integration only; critical optimization requires human authority + Workflow.
5. Roadmap: P265 foundation → P265-A…D; unblocks P266.

## Consequences
Positive: governed Twin OS (scenarios, predictive/optimization campaigns) over canonical digital twin.  
Negative: twin model/state/simulation-run truth remains P227-owned — MEDTIP stores operating campaigns, scenario packs and peer refs only.

## Links
Law: `ENTERPRISE_MEOS_DIGITAL_TWIN_INTELLIGENCE_PLATFORM.md` · Prior: ADR 621 · Next: P265-A · Peer: ADR 623 (P266 MEAAOI) · Canonical: P227 EDTISP
