# MEOS Change Management Standard

**Date:** 2026-08-18T17:15:00Z  
**Procedure SoR:** [MEOS_CHANGE_MANAGEMENT.md](./MEOS_CHANGE_MANAGEMENT.md) — **not in force** on production.  
**Object overlay:** [MEOS_CHANGE_REGISTRY.v1.yaml](./MEOS_CHANGE_REGISTRY.v1.yaml)  
**Release gates:** [MEOS_RELEASE_GOVERNANCE.md](./MEOS_RELEASE_GOVERNANCE.md)  
**P334:** this file is the **standard overlay**. It does **not** replace the procedure and does **not** create an ITSM product.

## Change object (documented, sparsely populated)

| Field | Actual now |
|-------|------------|
| CHANGE_ID / NAME | `CHG-G26`…`CHG-G19` (mapped from INIT-*) |
| OWNER / SPONSOR | **NOT_AVAILABLE** |
| OBJECTIVE | P327 PLATFORM_GATE DRAFT ids |
| SCOPE | Launch debt only |
| AFFECTED_TENANTS / ROLES | **NOT_AVAILABLE** |
| AFFECTED_APPLICATIONS / PROCESSES | Tagged; none ACTIVE in production |
| STATUS | **PROPOSED** or **ASSESSED** only |
| START / TARGET_DATE | **NOT_SET** |

Vocabulary (not claimed as current facts):  
`PROPOSED` → `ASSESSED` → `APPROVED` → `PLANNED` → `IN_PROGRESS` → `VALIDATION` → `COMPLETED` | `ROLLED_BACK` | `CANCELLED`

**Forbidden without production evidence:** APPROVED, IN_PROGRESS, VALIDATION, COMPLETED, ROLLED_BACK.

## Classification (do not fork)

| Layer | Values | SoR |
|-------|--------|-----|
| Procedure | STANDARD · NORMAL · EMERGENCY | CHANGE_MANAGEMENT.md |
| Initiative | OPERATIONAL_RESILIENCE · RISK_REDUCTION · COMPLIANCE | Initiative portfolio |
| P334 tag | TECHNOLOGY · OPERATIONAL · SECURITY · POLICY | Overlay only |

Do **not** invent STRATEGIC/PRODUCT/REGULATORY classes as a second register. Current rows are launch gates, not a product portfolio.

## Impact analysis

```
CHANGE → PROCESS → APPLICATION → SERVICE → ROLE → CAPABILITY → DATA → TENANT → RISK
```

G26 would affect the whole platform **if** production existed. Live knowledge/dependency graph **NOT_AVAILABLE**. Role/tenant impact **NOT_MEASURED**.

## Change risk (P328)

Material rows map to existing risks only: R-01 (cluster), R-02 (rollback), R-03 (alerting), R-04 (AI stub), R-05 (DSAR), R-06 (dirty SHA). Accountable owner still **NOT_AVAILABLE**. Do not invent BUSINESS_IMPACT money figures.

## Readiness (P333)

CAPABILITY / SKILL / KNOWLEDGE / PROCESS / TECHNOLOGY / OPERATIONAL readiness: **NOT_MEASURED** or **BLOCKED**. Procedure must not skip the readiness gate by assertion.

## Stakeholders

Identify **roles**, not personalities: change owner, sponsor, technical lead. All **NOT_AVAILABLE**. Avoid personal profiling. Identity RBAC remains authorization SoR.

## Dependencies

| Change | Blocked by |
|--------|------------|
| All production changes | CHG-G26 (G26) |
| CHG-G25 immutable SHA | Working tree dirty; still needs cluster for prod artifact |
| CHG-G27 rollback | No production deploy |
| CHG-G23/G18/G19 | CHG-G26 |

Blocked dependencies are listed in YAML `blockers`.

## Gates (reuse, do not duplicate)

READINESS (P333) · SECURITY (P317/P328) · TESTING (P324 G02–G05) · TRAINING (P333, none assigned) · COMMUNICATION (notifications) · DEPLOYMENT (G26 BLOCKED) · VALIDATION · ROLLBACK (G13/G27 BLOCKED).

A gate is not passed because this document exists.
