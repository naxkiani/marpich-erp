# Enterprise Business Intelligence — Advanced Analytics Platform (P213-I)

**SoR:** `analytics` · **ADR:** 413 · **API:** `/api/v1/analytics/advanced*` · **Capability:** `CAP-PLT-BI-001`

## Principle

**Advanced Analytics SHALL transform enterprise data into scientific business intelligence that supports strategic decision making.**

## Vision

MEOS Enterprise Advanced Analytics Fabric where Enterprise Data + Semantic Intelligence + Knowledge Graph + Business Metrics + Historical Intelligence + AI Intelligence are transformed into Deep Analytical Knowledge that explains: What happened · Why it happened · What is happening · What may happen · What action should be evaluated.

## Core domain

Enterprise Advanced Analytics Management

## Aggregate

AdvancedAnalyticsAggregate — AnalyticsModel · Experiment · Hypothesis · Insight · Pattern · Correlation · AnalyticalNotebook · AnalyticalProject · FeatureSet · AnalyticalScenario

## Supporting domains (logical — same SoR)

Statistical Analytics · Analytical Modeling · Experiment Management · Pattern Discovery · Correlation Analysis · Root Cause Analysis · Behaviour Analytics · Insight Management · Data Science Workspace

## Logical bounded contexts (same SoR — not sibling BCs)

| ID | Context |
|---|---|
| BC-01 | Statistical Analytics |
| BC-02 | Analytical Modeling |
| BC-03 | Experimentation |
| BC-04 | Pattern Discovery |
| BC-05 | Root Cause Analytics |
| BC-06 | Insight Management |

## Hard laws (quality gates)

- Never Enterprise advanced analytics platform is missing
- Never Statistical intelligence platform is missing
- Never Enterprise experimentation platform is missing
- Never Pattern discovery platform is missing
- Never Root cause analytics is missing
- Never Insight management is missing
- Never AI assisted analytics is missing
- Never Knowledge graph integration is missing
- Never Digital twin integration is missing
- Never CQRS architecture is missing
- Never Event sourcing architecture is missing
- Never Microservice architecture is missing
- Never API first architecture is missing
- Never Zero trust security is missing
- Never Enterprise governance is missing
- Never Cloud native deployment is missing
- Never Advanced analytics architecture is incomplete
- Never Sibling business intelligence BC

## Workbench

Statistical · Data Science · Notebook · Research · Experiment · Model · Executive Analytics — with projects, versioning, templates, reusable models/experiments, collaborative analytics.

## Boundaries

| Concern | Owner |
|---|---|
| Advanced analytics / workbench catalog | `analytics` |
| Certified metrics / semantic | P213-G |
| Self-service publish paths | P213-H |
| Warehouse / lakehouse history | P213-E / P213-F |
| Metadata | `data_governance` (P212-I) |
| Analytical knowledge graph | `data_governance` (P212-J) |
| Scenario / twin simulation | `data_governance` (P212-L) |
| Identity / AuthZ | P207 / P208 |
| Analytical masking | P211 |
| AI inference | Enterprise AI |
| Event transport | Enterprise Event Bus |
| Public edge | API Gateway |

## Forbidden

- Sibling BC (`business_intelligence`, `decision_intelligence`, `reporting_platform`, …)
- Module-local LLM SDKs
- Cross-schema joins to peer BCs
- Ungoverned / uncertified metrics in advanced publish paths
- Shadow experimentation outside experiment governance
