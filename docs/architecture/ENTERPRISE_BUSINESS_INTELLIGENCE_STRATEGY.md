# Enterprise Business Intelligence — Strategy Foundation (P213-A)

**SoR:** `analytics` · **ADR:** 394 · **API:** `/api/v1/analytics/strategy*` · **Capability:** `CAP-PLT-BI-001`

## Principle

**Enterprise intelligence transforms trusted data into strategic organizational decisions.**

## Vision

Transform governed data assets into actionable business intelligence, predictive insights, and intelligent enterprise decisions through the MEOS Enterprise Intelligence Fabric: Insight → Recommendation → Decision → Business Action.

## Core domain

Enterprise Decision Intelligence Management

## Aggregate

EnterpriseInsightAggregate

## Supporting domains (logical — same SoR)

Business Intelligence · Analytics Management · Metrics Management · Insight Generation · Decision Automation · Intelligence Governance

## Hard laws (quality gates)

- Never Enterprise BI architecture is incomplete
- Never Analytics architecture is missing
- Never Decision intelligence foundation is missing
- Never DDD domain model is missing
- Never CQRS architecture is missing
- Never Event-driven architecture is missing
- Never Microservices architecture is missing
- Never API first design is missing
- Never AI-native BI is missing
- Never Knowledge graph integration is missing
- Never Digital twin integration is missing
- Never Governance alignment is missing
- Never Data mesh alignment is missing
- Never Sibling business intelligence BC

## Boundaries

| Concern | Owner |
|---|---|
| BI strategy / fabric catalog | `analytics` |
| Data products / mesh / KG / twin | `data_governance` (P212) |
| Data security / privacy | `data_security` (P211) |
| Identity | Identity Intelligence (P207) |
| Authorization PDP | Authorization (P208) |
| AI inference | Enterprise AI |

## Forbidden

- Sibling BC (`business_intelligence`, `reporting_platform`, `decision_intelligence`, …)
- Module-local LLM SDKs
- Cross-schema joins to peer BCs
