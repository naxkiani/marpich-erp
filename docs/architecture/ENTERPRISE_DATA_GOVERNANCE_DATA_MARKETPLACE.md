# Enterprise Data Governance — Data Marketplace Platform (P212-G)

**SoR:** `data_governance` · **ADR:** 400 · **API:** `/api/v1/data-governance/marketplace*` · **Capability:** `CAP-PLT-DG-001`

## Principle

**Enterprise data SHALL become discoverable, understandable, accessible, and valuable through governed digital experiences.**

## Vision

Transform unknown and fragmented data sources into a **trusted, discoverable, governed, self-service enterprise data marketplace**.

Producers → Publish → Trusted Data Products → Marketplace Discovery → Governed Access → Enterprise Consumers.

## Core domain

Enterprise Data Marketplace Management

## Supporting domains (logical — same SoR)

Data Product Discovery · Data Catalog Management · Consumer Management · Access Request Management · Data Subscription Management · Marketplace Intelligence

## Aggregate

DataMarketplaceItem

## Entities

DataProduct · CatalogEntry · Consumer · Subscription · AccessRequest · UsageRecord

## Value objects

SearchTerm · ProductRating · AccessLevel · SubscriptionPlan · UsageMetric

## Bounded contexts (logical)

BC-01 Data Catalog · BC-02 Discovery · BC-03 Consumer Experience · BC-04 Data Access Governance · BC-05 Subscription Management · BC-06 Marketplace Intelligence

## Hard laws (quality gates)

- Never Enterprise data marketplace architecture is incomplete
- Never Data catalog architecture is missing
- Never Data discovery architecture is missing
- Never Data product consumption model is missing
- Never Data access governance is missing
- Never AI recommendation intelligence is missing
- Never Data mesh alignment is missing
- Never Knowledge graph integration is missing
- Never Digital twin integration is missing
- Never CQRS architecture is missing
- Never Event sourcing architecture is missing
- Never Microservices architecture is missing
- Never Zero trust security alignment is missing
- Never Enterprise scalability is missing
- Never Sibling data marketplace BC

## Boundaries

| Concern | Owner |
|---|---|
| Marketplace / catalog / discovery | `data_governance` |
| Data products | P212-F (same SoR) |
| Ownership / stewardship | P212-D |
| Quality scores | P212-E |
| Authorization PDP | P208 |
| Global search index | Enterprise Search |
| AI inference | Enterprise AI |
| Approvals | Workflow |

## Forbidden

- Sibling BC (`data_marketplace`, fragment catalog/discovery platforms)
- Module-local LLM SDKs or module-local search engines
- Cross-schema joins to peer BCs
