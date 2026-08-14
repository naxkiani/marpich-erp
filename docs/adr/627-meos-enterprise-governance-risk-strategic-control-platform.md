# ADR 627 — MEOS Enterprise Governance, Risk & Strategic Control Platform (P270)

## Status
Accepted

## Context
P269 established MEPCRI over P230/Compliance peers. P270 productizes Enterprise Governance, Risk & Strategic Control as the MEOS Enterprise Governance Operating Layer. P240 already owns `governance_intelligence`; P221 owns `resilience`; P261/P224 own decision intelligence overlays and SoR; Policy Engine owns evaluate/simulate. MEGRSC must federate those SoRs — never fork `/api/v1/governance-intelligence*`, never dual-write peer GRC catalogs, and never ungated board-class strategic execution. P271 is planned for Financial Intelligence & Autonomous Finance over P231 / Financial Kernel.

## Decision
1. SoR `governance_risk_operating`; fabric `meos_enterprise_governance_risk_strategic_control_platform_framework`; API `/api/v1/governance-risk-operating*`; capability `CAP-PLT-MEGRSC-001`; acronym **MEGRSC**.
2. Logical BCs inside one SoR: Enterprise Governance Operating, Risk Intelligence Operating, Strategic Management Operating, Decision Governance Operating, Control Framework Operating, Performance Governance.
3. Federate with P240, P221, P261/P224, Policy Engine, P269/Compliance, P268, P262, Workflow, Audit, P214-Z — never replace them; never dual-write peer governance/resilience/decision catalogs.
4. Inference only via P214-Z; board/critical strategic actions require Workflow + human approval; simulation ≠ execute; no opaque autonomous board decisions.
5. Roadmap: P270 foundation → P270-A…D; unblocks P271.

## Consequences
Positive: governed Enterprise GRC / Strategic Control OS (board intelligence, OKR/strategy campaigns, integrated risk overlays) over canonical governance peers.  
Negative: institutional governance intel, crisis/resilience and policy/decision truth remain peer-owned — MEGRSC stores operating campaigns and peer refs only.

## Links
Law: `ENTERPRISE_MEOS_GOVERNANCE_RISK_STRATEGIC_CONTROL_PLATFORM.md` · Prior: ADR 626 · Next: P270-A · Peer: ADR 628 (P271 MEFIAF) · Canonical: P240 · P221 · P261 · Policy Engine
