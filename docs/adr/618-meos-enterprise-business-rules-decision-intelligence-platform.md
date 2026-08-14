# ADR 618 — MEOS Enterprise Business Rules & Decision Intelligence Platform (P261)

## Status
Accepted

## Context
P260 established MEWEOP over the Workflow Engine. P261 productizes business rules and decision intelligence as the MEOS Cognitive Business Execution Layer. Policy Engine already owns evaluate/simulate and versioned policies; P224 already owns `decision_intelligence`. MEBRDI must federate those SoRs — never fork `/api/v1/policies*` or `/api/v1/decision-intelligence*`, and never reintroduce hardcoded module rules. P262 is planned for Analytics & Operational Insight productization.

## Decision
1. SoR `business_decision`; fabric `meos_enterprise_business_rules_decision_intelligence_platform_framework`; API `/api/v1/business-decision*`; capability `CAP-PLT-MEBRDI-001`; acronym **MEBRDI**.
2. Logical BCs inside one SoR: Business Rules, Decision Management, Policy Governance overlay, Explanation, Optimization, Decision Governance.
3. Federate with Policy Engine, P224, Workflow/P260, P257–P259, P214-Z, P228, Compliance, Audit — never replace them; never dual-write policy catalogs; never opaque AI decisions.
4. Inference only via P214-Z; recommendation ≠ enforce; critical decisions require human governance; simulation ≠ production enforce; no local policy tables in modules.
5. Roadmap: P261 foundation → P261-A…D; unblocks P262.

## Consequences
Positive: governed adaptive rules/decision studio with mandatory explainability over canonical policy/decision peers.  
Negative: policy evaluate truth and decision-intel SoR remain peer-owned — MEBRDI stores rule/decision productization state, explanations, campaigns and peer refs only.

## Links
Law: `ENTERPRISE_MEOS_BUSINESS_RULES_DECISION_INTELLIGENCE_PLATFORM.md` · Prior: ADR 617 · Next: P261-A · Peer: ADR 619 (P262 MEIAOI) · Canonical: `ENTERPRISE_POLICY_ENGINE.md` · P224 EADIP
