# ADR-383: Data Security — Data Access Governance (P211-H)

## Status

Accepted — P211-H Enterprise Data Access Governance Platform

## Context

ADR-376–382 established SoR `data_security` through discovery, classification, DSPM, and DLP. P211-H delivers the **data access governance control layer**: entitlements, access requests, zero-trust evaluation, ABAC/ReBAC, AI agent access, certification reviews, risk intelligence, KG/twin bindings — without inventing sibling `data_access_governance` / `entitlement_management` BCs.

**Hard laws:** SoR remains `data_security`. Surfaces under `/data-security/access*`. Never invisible permissions. Never undefined ownership. Never manual-only access reviews. Never missing risk evaluation. Never unmanaged AI access. Never unenforceable least privilege. Never non-auditable authorization decisions. PDP/enforcement via P208. Identity via P207. Crypto via P209. Approvals/reviews via Workflow. Inference via Enterprise AI. Policies via Policy Engine.

## Decision

1. SoR remains `data_security`
2. Surfaces under `/api/v1/data-security/access*`
3. Law: `ENTERPRISE_DATA_SECURITY_ACCESS_GOVERNANCE.md`
4. Catalogs: `DATA_SECURITY_ACCESS_*.v1.yaml`
5. Runtime: `ds_platform_access.py`; aggregates; ACL; foundation
6. Quality gates enforce permission visibility, ownership, automated reviews, risk evaluation, AI access management, least privilege, auditable decisions

## Consequences

- Data authorization control layer connecting Identity → P208 → Classification → DSPM → DLP → Cyber Ops
- Forbidden siblings: `data_access_governance`, `entitlement_management`, `access_certification`

## References

ADR-376–382 · P207 · P208 · P209 · P210 · ENTERPRISE_WORKFLOW_ENGINE.md · ENTERPRISE_POLICY_ENGINE.md · AI_PLATFORM_STANDARD.md
