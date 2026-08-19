# MEOS Decision Fabric

**Date:** 2026-08-18T06:01:00Z  
**Maturity:** **FOUNDATION** (blocked before CONNECTED).  
**Companion:** [MEOS_P318_ENTERPRISE_INTELLIGENCE.md](./MEOS_P318_ENTERPRISE_INTELLIGENCE.md)  
**P327 overlay:** [MEOS_DECISION_INTELLIGENCE.md](./MEOS_DECISION_INTELLIGENCE.md) — phase decision registry only. Fabric remains SoR. No DECISION_READY claim.  
**P338 overlay:** [MEOS_P338_DECISION_INTELLIGENCE.md](./MEOS_P338_DECISION_INTELLIGENCE.md) — executive cockpit + decision flow inventory.

The Decision Fabric is the **governed connection** of existing MEOS capabilities — not a new product.

## Existing fabric (reuse)

```
Data Mesh (data_governance P212)
    → BI / Metrics (analytics P213)
        → Knowledge graph ACL (P213-L / P212-J)
        → Digital twin ACL (identity_digital_twin / P212-L)
        → AI assist (ai P214 — stub)
        → Search (search)
        → Audit / Workflow / Notifications
            → Human decision → Action → Audit
```

Forbidden siblings: new warehouse BC, new BI BC, new graph BC, module-local LLM, cross-schema joins.

## Execution loop (actual vs claimed)

| Step | Repository | Production |
|------|------------|------------|
| DISCOVER / INVENTORY | This P318 pass | n/a |
| SOURCE | Contexts + events + APIs | **NOT_AVAILABLE** |
| GOVERN | Metric catalog + AuthZ + tenant_id | Candidate only |
| CONNECT | ACLs `via_p212_*` | Not live-federated |
| MODEL | Catalogs (OLAP/predictive/prescriptive) | No production models |
| ANALYZE | Event counters / domain engines | **NOT_AVAILABLE** |
| VISUALIZE | Home pulse + domain desks | Demo only |
| EXPLAIN | AI stub echo | Must state DATA_NOT_AVAILABLE |
| DECIDE | Human only (HITL) | No autonomous high-impact path evidenced |
| ACT | Workflow / Task Center | Demo only |
| AUDIT | Audit platform | Demo only |
| MEASURE / IMPROVE | P316/P317 not started | Blocked |

## Alert-to-decision pipeline

Designed: `SIGNAL → ALERT → CONTEXT → ANALYSIS → RECOMMENDATION → DECISION → ACTION → AUDIT`.  
Production: **NOT_AVAILABLE** (G23 no production alerting). Analytics `AlertRule` exists in code.

## Human decision control

AI `assist()` returns a template echo. It must **not** silently execute enterprise actions. Consequential path remains:

`AI → RECOMMENDATION → HUMAN REVIEW → AUTHORIZATION → ACTION → AUDIT`

No governed low-risk autonomous production policy is evidenced as ACTIVE.

## AI safety (P318)

AI must not invent metrics, transactions, incidents, financial results, security events, compliance status, or decisions.  
If source data is missing: **`DATA_NOT_AVAILABLE`**.  
Stub replies are **not** FACT. They are not INFERENCE, PREDICTION, or RECOMMENDATION.

## Scenario / predictive

Predictive and prescriptive **catalogs** exist under analytics (`/predictive*`, `/prescriptive*`).  
Production predictions with MODEL / INPUT / TIME / CONFIDENCE / LIMITATION: **NOT_AVAILABLE**.  
Do not claim PREDICTIVE maturity.

## Cross-domain analysis

ACL DTOs carry `peer_ids_only: true` and tenant_id. Cross-domain production analysis: **NOT_AVAILABLE**. Cross-tenant: **prohibited**.

## Task Center connection

Home pulse lists recent workflow tasks (fail-soft). That is **INSIGHT → ACTION** only if the operator uses Task Center on real work items. Production executive action loop: **NOT_AVAILABLE**.
