# ADR 436 — Enterprise AI Governance, Compliance, Audit & Continuous AI Trust (P214-P)

## Status

Accepted

## Context

MEOS AI (P214-A–O) needs a continuous trust control plane: policy intelligence, compliance monitoring, audit orchestration, Trust Index, transparency, explainability governance, and regulatory intelligence. P214-H already owns Responsible AI / risk foundations (`/governance*`). P214-P deepens continuous trust without a sibling BC.

## Decision

1. SoR remains **`ai`** (`CAP-PLT-AI-001`).
2. Fabric: **`meos_continuous_ai_trust_fabric`**.
3. API surface: **`/api/v1/ai/aitrust*`** (distinct from P214-H `/governance*`).
4. Seven logical bounded contexts (BC-01–BC-07) on SoR `ai`.
5. Audit evidence → platform Audit Service via ACL; policies → Policy Engine via ACL.
6. Principle: continuous intelligent trust management (not static compliance).

## Consequences

- P214-Q (Autonomous AI Ecosystem / Digital Workforce) consumes Trust Index and certification gates.
- Modules never embed local AI governance/compliance stores.
