# Enterprise Business Intelligence — Decision Intelligence Knowledge Graph (P213-L)

**SoR:** `analytics` · **ADR:** 416 · **API:** `/api/v1/analytics/graph*` · **Capability:** `CAP-PLT-BI-001`

## Principle

**Every enterprise decision SHALL become a governed, connected, explainable, versioned knowledge asset.**

## Vision

MEOS Enterprise Decision Knowledge Fabric where every Business Goal → Capability → KPI → Insight → Prediction → Recommendation → Decision → Outcome → Business Value is a connected graph — continuously updated, searchable, AI-consumable, fully explainable, and historically traceable.

## Core domain

Enterprise Decision Knowledge Management

## Aggregate

DecisionKnowledgeGraphAggregate — DecisionNode · DecisionEdge · DecisionContext · DecisionEvidence · BusinessObjective · Recommendation · Outcome · DecisionRule · DecisionOntology · DecisionSession

## Supporting domains (logical — same SoR)

Decision Graph · Decision Context · Decision Lineage · Decision Ontology · Graph Analytics · Decision Relationship · Decision Reasoning · Graph Governance

## Logical bounded contexts (same SoR — not sibling BCs)

| ID | Context |
|---|---|
| BC-01 | Decision Graph |
| BC-02 | Decision Context |
| BC-03 | Decision Lineage |
| BC-04 | Decision Ontology |
| BC-05 | Graph Analytics |
| BC-06 | Decision Reasoning |

## Hard laws (quality gates)

- Never Enterprise decision knowledge graph is missing
- Never Enterprise decision ontology is missing
- Never Enterprise decision memory is missing
- Never Graph analytics is missing
- Never AI reasoning is missing
- Never Decision lineage is missing
- Never Knowledge graph federation is missing
- Never Digital twin integration is missing
- Never CQRS architecture is missing
- Never Event sourcing architecture is missing
- Never Microservice architecture is missing
- Never API first architecture is missing
- Never Zero trust security is missing
- Never Cloud native deployment is missing
- Never Decision knowledge graph architecture is incomplete
- Never Sibling business intelligence BC

## Decision lineage path

Goal → Policy → Data → Metric → Insight → Prediction → Recommendation → Decision → Execution → Outcome → Business Impact

## Boundaries

| Concern | Owner |
|---|---|
| Decision knowledge graph catalog | `analytics` |
| Enterprise data intelligence KG federation | `data_governance` (P212-J) |
| Twin decision simulation | `data_governance` (P212-L) |
| Certified metrics / semantic | P213-G |
| Predictive nodes | P213-J |
| Prescriptive / recommendation nodes | P213-K |
| Identity / AuthZ | P207 / P208 |
| Graph privacy / masking | P211 |
| AI graph reasoning | Enterprise AI |
| Event transport | Enterprise Event Bus |
| Public edge | API Gateway |

## Forbidden

- Sibling BC (`business_intelligence`, `decision_intelligence`, `reporting_platform`, …)
- Module-local graph DB replacing P212-J federation for enterprise data KG
- Module-local LLM SDKs
- Cross-schema joins to peer BCs
- Ungoverned node/edge publication without ontology and authorization
