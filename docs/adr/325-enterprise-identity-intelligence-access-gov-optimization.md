# ADR-325: Identity Intelligence — AI Governance & Access Optimization (P207-J)

## Status

Accepted — P207-J AI Driven Governance & Access Optimization Platform

## Context

P207-A–I established strategy through self-healing on SoR `identity_intelligence`. P207-J delivers **AI Driven Governance & Access Optimization**: continuous access evaluation, entitlement intelligence, least-privilege optimization, AI-assisted certification, role/policy intelligence, twin-simulated changes, and governed autonomous workflows — without periodic-only governance, unexplained AI, business-context-blind optimization, absent human governance, unavailable compliance evidence, or disconnected risk intelligence.

**Hard laws:** SoR remains `identity_intelligence`. Surfaces under `/access-gov*`. Continuous governance required. Explainable recommendations. Business context required. HITL for high-impact changes. Compliance evidence required. Risk via P207-G. Twin sim via P207-F. Workflow for approvals. Never invent sibling governance BC. Never embed LLM SDK. P202 IGA remains peer SoR — orchestrate, do not duplicate.

## Decision

1. SoR remains `identity_intelligence`
2. Surfaces under `/api/v1/identity-intelligence/access-gov*`
3. Law: `ENTERPRISE_IDENTITY_INTELLIGENCE_ACCESS_GOV_OPTIMIZATION.md`
4. Catalogs: `II_ACCESS_GOV_*.v1.yaml`
5. Runtime: `ii_platform_access_gov.py`; aggregates: `ii_access_gov_aggregates.py`; ACL: `ii_access_gov_acl.py`; validator: `ii_access_gov_foundation.py`
6. Quality gates reject periodic-only, unexplained AI, business-blind optimization, absent human governance, unavailable compliance evidence, disconnected risk

## Consequences

- P202 IGA remains certification SoR; P207-J is continuous AI governance intelligence surface
- AuthZ PDP remains `authorization`; policy evaluation via Policy Engine

## References

ADR-316–324 · P202 IGA · Workflow · AI Platform · directory · identity_digital_twin · Platform Charter
