# ADR-322: Identity Intelligence — Predictive Identity Risk Engine (P207-G)

## Status

Accepted — P207-G Predictive Identity Risk Intelligence Engine

## Context

P207-A–F established strategy through digital twin orchestration on SoR `identity_intelligence`. P207-G delivers the **Predictive Identity Risk Intelligence Engine**: continuous risk scoring, predictive forecasting, adaptive trust, behavioral/graph/twin risk analysis, AI risk agents, and governed automated response — without static-only risk, absent prediction, unexplained scores, unaudited AI decisions, undefined trust, or ungoverned automation.

**Hard laws:** SoR remains `identity_intelligence`. Surfaces under `/risk*` (distinct from `/twins*`, `/agents*`, `/behavior*`). Explainable scores required. Prediction required. Trust engine defined. AI via AI Platform. Graph via directory. Twin simulation via P207-F. Autonomous response via P207-D + Workflow HITL. Never invent sibling risk BC. Never embed LLM SDK.

## Decision

1. SoR remains `identity_intelligence`
2. Surfaces under `/api/v1/identity-intelligence/risk*`
3. Law: `ENTERPRISE_IDENTITY_INTELLIGENCE_PREDICTIVE_RISK.md`
4. Catalogs: `II_RISK_*.v1.yaml`
5. Runtime: `ii_platform_risk.py`; aggregates: `ii_risk_aggregates.py`; ACL: `ii_risk_acl.py`; validator: `ii_risk_foundation.py`
6. Quality gates reject static-only risk, absent prediction, unavailable explanation, unauditable AI, undefined trust, ungoverned automated response

## Consequences

- Behavior (P207-H) deepens signal analytics; risk engine remains the predictive scoring SoR surface
- Zero Trust consumers read continuous trust scores; AuthZ PDP remains `authorization`

## References

ADR-316–321 · Zero Trust · AI Platform · Workflow · Policy · directory · identity_digital_twin · Platform Charter
