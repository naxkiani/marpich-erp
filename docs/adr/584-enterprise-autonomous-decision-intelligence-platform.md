# ADR 584 — Enterprise Autonomous Decision Intelligence Platform (P224)

## Status
Accepted

## Context
P223 established EGIKEP (innovation & knowledge evolution). P224 opens the Enterprise Autonomous Decision Intelligence Platform (EADIP) for intelligent decision orchestration, predictive analysis, autonomous recommendations and enterprise-wide decision governance under MEOS 11.0. P213 already provides BI / decision analytics under SoR `analytics`; EADIP is a dedicated decision-orchestration SoR that federates with P213 rather than forking it.

## Decision
1. SoR `decision_intelligence`; fabric `meos_enterprise_autonomous_decision_intelligence_platform_framework`; API `/api/v1/decision-intelligence*`; capability `CAP-PLT-EADIP-001`.
2. Ten logical BCs inside one SoR: Decision Management, Intelligence Analysis, Prediction, Simulation, Optimization, Governance, Human-AI Collaboration, Strategic Decisions, Operational Decisions, Decision Learning.
3. Federate with P213 analytics/decision intelligence, P219-Z/X, P221 via ACL/events — never replace them.
4. Inference only via P214-Z; approve/execute via Workflow; policy via Policy Engine; audit via Audit.
5. Never module-local LLM; never ungated decision execution; never opaque recommendations; never silent enterprise mutation.
6. Roadmap: P224 foundation → P224-A…D (decision core → AI/simulation → gated workflows → civilization-scale learning assist).

## Consequences
Positive: governed decision lifecycle (collect→learn) with explainability and human gates.  
Negative: analytics metrics remain owned by P213/`analytics` — EADIP stores decision cases, recommendations and outcomes with peer metric refs only.

## Links
Law: `ENTERPRISE_AUTONOMOUS_DECISION_INTELLIGENCE_PLATFORM.md` · Prior: ADR 583 · Next: P224-A · Peer: ADR 585 (P225 EAOSHP)
