# Enterprise Business Intelligence — Enterprise Testing, Governance, Compliance Validation & Definition of Done Platform (P213-P)

**SoR:** `analytics` · **ADR:** 420 · **API:** `/api/v1/analytics/qa*` · **Capability:** `CAP-PLT-BI-001`

## Principle

**BI systems SHALL prove correctness, security, compliance, and governance continuously.**

## Hard laws (quality gates)

- Never BI assurance architecture is incomplete
- Never Sibling business intelligence BC

## Boundaries

| Concern | Owner |
|---|---|
| Enterprise Testing, Governance, Compliance Validation & Definition of Done Platform catalog | `analytics` |
| Data products / mesh | `data_governance` (P212) |
| AI inference | Enterprise AI |
| Event transport | Enterprise Event Bus |
| Public edge | API Gateway |

## Forbidden

- Sibling BC (`business_intelligence`, `decision_intelligence`, `reporting_platform`, …)
- Module-local LLM SDKs
- Cross-schema joins to peer BCs
