# ADR-420: Analytics — Enterprise Testing, Governance, Compliance Validation & Definition of Done Platform (P213-P)

## Status

Accepted — P213-P Enterprise Testing, Governance, Compliance Validation & Definition of Done Platform

## Context

P213 SoR remains `analytics` (CAP-PLT-BI-001). P213-P delivers **Enterprise BI Testing, Governance, Compliance Validation & DoD Platform** without inventing sibling BI BCs.

**Hard laws:** Surfaces under `/api/v1/analytics/qa*`. BI systems SHALL prove correctness, security, compliance, and governance continuously. Reuse Event Fabric, API Gateway, Enterprise AI, Observability, and P212 data products via ACL.

## Decision

1. SoR remains `analytics`
2. Surfaces under `/api/v1/analytics/qa*`
3. Law: `ENTERPRISE_BUSINESS_INTELLIGENCE_QA.md`
4. Catalogs: `BI_QA_*.v1.yaml`
5. Runtime: `bi_platform_qa.py`; aggregates; ACL; foundation

## Consequences

- Extends P213 series toward complete Decision Intelligence Fabric
- Forbidden siblings remain forbidden

## References

ADR-394–396 · prior P213 phases · P212 · CORE_PLATFORM.md
