# ADR-323: Identity Intelligence — Behavioral Identity Analytics (P207-H)

## Status

Accepted — P207-H Behavioral Identity Analytics Platform

## Context

P207-A–G established strategy through predictive risk on SoR `identity_intelligence`. P207-H delivers the **Behavioral Identity Analytics Platform** (UEBA): behavior profiles, baselines, anomaly detection, entity analytics, privacy-by-design, AI behavior agents, and continuous trust signals — without rule-only analysis, absent learning, unexplained anomalies, missing privacy, ungoverned AI models, or absent risk-intelligence integration.

**Hard laws:** SoR remains `identity_intelligence`. Surfaces under `/behavior*` (distinct from `/risk*`). Learning required (ML/statistical/pattern/graph). Explainable anomalies. Privacy controls mandatory. AI via AI Platform + governance. Risk scores feed P207-G. Graph via directory. Twin simulation via P207-F. Never invent sibling UEBA BC. Never embed LLM SDK.

## Decision

1. SoR remains `identity_intelligence`
2. Surfaces under `/api/v1/identity-intelligence/behavior*`
3. Law: `ENTERPRISE_IDENTITY_INTELLIGENCE_BEHAVIORAL_ANALYTICS.md`
4. Catalogs: `II_BEHAVIOR_*.v1.yaml`
5. Runtime: `ii_platform_behavior.py`; aggregates: `ii_behavior_aggregates.py`; ACL: `ii_behavior_acl.py`; validator: `ii_behavior_foundation.py`
6. Quality gates reject rule-only UEBA, absent learning, unexplained anomalies, missing privacy, ungoverned AI, absent risk integration

## Consequences

- Risk engine (P207-G) remains predictive scoring SoR surface; behavior deepens signal analytics
- AuthZ PDP remains `authorization`; continuous trust is a consumer signal

## References

ADR-316–322 · Zero Trust · AI Platform · AI Governance · directory · Platform Charter
