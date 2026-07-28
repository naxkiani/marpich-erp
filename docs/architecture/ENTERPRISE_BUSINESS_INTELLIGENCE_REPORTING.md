# Enterprise Business Intelligence — Reporting, Dashboard & Visualization (P213-D)

**SoR:** `analytics` · **ADR:** 408 · **API:** `/api/v1/analytics/reporting*` · **Capability:** `CAP-PLT-BI-001`

## Principle

**Enterprise reporting SHALL not only describe what happened, it SHALL explain why it happened and what should happen next.**

## Vision

MEOS Enterprise Intelligence Experience Fabric where Business Data + Governed Metrics + Analytics Results + AI Insights + Decision Models are delivered through Reports + Dashboards + Visual Analytics + Executive Intelligence Portals + Mobile Intelligence Experiences.

## Core domain

Enterprise Intelligence Experience Management

## Aggregate

EnterpriseVisualizationExperienceAggregate — Report · Dashboard · Widget · Visualization · Subscription · DistributionChannel

## Supporting domains (logical — same SoR)

Report Management · Dashboard Management · Visualization Management · User Experience Management · Distribution Management · Intelligence Consumption Governance

## Logical bounded contexts (same SoR — not sibling BCs)

| ID | Context |
|---|---|
| BC-01 | Enterprise Reporting |
| BC-02 | Executive Dashboard |
| BC-03 | Operational Dashboard |
| BC-04 | Visualization Management |
| BC-05 | Distribution & Consumption |

## Hard laws (quality gates)

- Never Enterprise reporting platform is missing
- Never Dashboard architecture is missing
- Never Visualization platform is missing
- Never Self-service BI capability is missing
- Never AI reporting intelligence is missing
- Never Real-time analytics experience is missing
- Never CQRS architecture is missing
- Never Event driven design is missing
- Never Microservice architecture is missing
- Never API first architecture is missing
- Never Security governance is missing
- Never Enterprise scalability is missing
- Never Reporting architecture is incomplete
- Never Knowledge graph visualization is missing
- Never Digital twin visualization is missing
- Never Sibling business intelligence BC

## Layers

Data Source → Semantic Intelligence → Reporting Engine → Visualization → Consumption Experience

## Dashboard categories

Executive · Management · Operational · AI Intelligence

## Self-service governance

Certified metrics only · Policy controlled access · Data lineage visibility

## AI agents (via Enterprise AI only)

AI Report Generator · AI Dashboard Designer · AI Visualization Advisor · AI Insight Narrator · AI Executive Assistant

## Boundaries

| Concern | Owner |
|---|---|
| Reporting / dashboards / visualization catalog | `analytics` |
| Data products / mesh / marketplace | `data_governance` (P212-F/G) |
| Knowledge graph views | `data_governance` (P212-J) |
| Digital twin simulation views | `data_governance` (P212-L) |
| Encryption / masking / privacy | `data_security` (P211) |
| Identity | P207 |
| Authorization PDP | P208 |
| AI inference | Enterprise AI |
| Public edge | API Gateway |
| Event transport | Enterprise Event Bus (P212-M) |

## Forbidden

- Sibling BC (`business_intelligence`, `reporting_platform`, `visualization_platform`, …)
- Module-local LLM SDKs
- Cross-schema joins to peer BCs
- Ungoverned / uncertified metrics on published dashboards
