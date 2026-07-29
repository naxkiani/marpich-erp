# Enterprise Data Security — Domain Architecture / DDD (P211-C)

**SoR:** `data_security` · **ADR:** 378 · **API:** `/api/v1/data-security/domain*` · **Capability:** `CAP-PLT-DS-001`

## Core domain

Enterprise Data Security Intelligence Domain

## Supporting domains (logical — same SoR)

Data Discovery · Classification · Protection · Privacy · Access Governance · Security Risk · Lineage Intelligence · DLP · Compliance · Intelligence Graph · AI Data Security · Digital Twin

## Hard laws (quality gates)

- Never Domains are tightly coupled
- Never Data ownership is unclear
- Never Privacy is separated from security
- Never Events are missing
- Never Aggregates are undefined
- Never Integration boundaries are unclear

## Boundaries

| Concern | Owner |
|---|---|
| Data security domain map / aggregates catalog | `data_security` |
| Consent ledger / DSAR | `consent` |
| Encryption keys | `secrets` (P209) |
| Access decisions (PDP) | `authorization` (P208) |
| Threat detection / SOC | `cyber_security` (P210) |
| Compliance reports | Compliance Framework |

## Forbidden

- Sibling BC per supporting domain (`dspm`, `privacy_intelligence`, `data_classification`, …)
- Privacy fabric as a separate SoR from data security
- Tight coupling / shared mutable state between logical domains
- Cross-schema joins to peer BCs
