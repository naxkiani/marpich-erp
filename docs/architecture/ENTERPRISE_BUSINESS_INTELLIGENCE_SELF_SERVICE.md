# Enterprise Business Intelligence — Self-Service BI Platform (P213-H)

**SoR:** `analytics` · **ADR:** 412 · **API:** `/api/v1/analytics/self-service*` · **Capability:** `CAP-PLT-BI-001`

## Principle

**Every business user SHALL be capable of creating trusted analytics without compromising governance, security, or enterprise consistency.**

## Vision

MEOS Enterprise Analytics Experience Fabric where every authorized user can Discover → Explore → Create → Build Dashboards → Share Insights → Collaborate → Make Decisions while remaining fully governed by Enterprise Data Governance policies.

## Core domain

Enterprise Self-Service Analytics Management

## Aggregate

SelfServiceAnalyticsWorkspaceAggregate — Workspace · AnalyticsProject · SavedQuery · Dashboard · Notebook · Visualization · Insight · DatasetBookmark

## Supporting domains (logical — same SoR)

Workspace · Analytics Authoring · Dashboard Builder · Dataset Discovery · Collaboration · Insight Sharing · AI Analytics Assistance · Analytics Governance

## Logical bounded contexts (same SoR — not sibling BCs)

| ID | Context |
|---|---|
| BC-01 | Analytics Workspace |
| BC-02 | Analytics Exploration |
| BC-03 | Dashboard Builder |
| BC-04 | Ad-Hoc Analytics |
| BC-05 | Collaboration |
| BC-06 | AI Analytics Assistant |

## Hard laws (quality gates)

- Never Enterprise self-service BI platform is missing
- Never Citizen analytics platform is missing
- Never No-code analytics platform is missing
- Never Low-code analytics platform is missing
- Never Natural language analytics is missing
- Never AI analytics assistant is missing
- Never Collaborative analytics is missing
- Never Semantic layer integration is missing
- Never Knowledge graph integration is missing
- Never Digital twin integration is missing
- Never CQRS architecture is missing
- Never Event sourcing architecture is missing
- Never Microservice architecture is missing
- Never API first architecture is missing
- Never Zero trust security is missing
- Never Enterprise governance is missing
- Never Cloud native deployment is missing
- Never Self-service BI architecture is incomplete
- Never Analytics workspace is missing
- Never Ad-hoc analytics is missing
- Never Sibling business intelligence BC

## Experience flow

Discover Data → Explore Data → Create Analytics → Build Dashboards → Share Insights → Collaborate → Make Decisions

## Personas

Business Users · Managers · Executives · Domain Experts · Citizen Analysts · Data Stewards · Business Owners

## Boundaries

| Concern | Owner |
|---|---|
| Self-service workspace / builder catalog | `analytics` |
| Certified metrics / semantic | P213-G |
| Reporting consumption patterns | P213-D |
| Metadata / marketplace | `data_governance` (P212-I/G) |
| Knowledge graph navigation | `data_governance` (P212-J) |
| Digital twin what-if | `data_governance` (P212-L) |
| Identity / AuthZ / RLS | P207 / P208 |
| Masking / privacy | P211 |
| AI inference | Enterprise AI |
| Discovery search | Enterprise Search |

## Forbidden

- Sibling BC (`business_intelligence`, `reporting_platform`, …)
- Module-local LLM SDKs
- Cross-schema joins to peer BCs
- Ungoverned / uncertified metrics in self-service publish paths
- Shadow IT analytics outside workspace isolation
