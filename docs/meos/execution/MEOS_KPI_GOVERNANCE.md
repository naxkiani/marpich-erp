# MEOS KPI Governance

**Date:** 2026-08-18T12:20:00Z  
**SoR (catalog):** [MEOS_METRIC_GOVERNANCE.md](./MEOS_METRIC_GOVERNANCE.md) — **do not duplicate** the metric table here.  
**Runtime pulse:** `GET /api/v1/analytics/home-pulse` · `production_kpis: DATA_NOT_AVAILABLE` · `signal_class: CATALOG_COUNT`

## Law

A number on a dashboard is not an enterprise KPI. Authoritative KPIs need source, formula, tenant scope, and a measured ACTUAL. Production ACTUAL for the P318 catalog: **NOT_AVAILABLE**.

## TARGET / ACTUAL / STATUS (P326 overlay)

| Field | Production value |
|-------|------------------|
| TARGET | **NOT_SET** (no SLA/KPI targets committed) |
| ACTUAL | **NOT_MEASURED** |
| STATUS | **DATA_NOT_AVAILABLE** |
| OWNER | Context in metric catalog; people owners **NOT_AVAILABLE** |
| FREQUENCY | on request / event-driven (code) — not a live ops cadence |

Do not invent revenue, NPS, ROI, or DAU targets.

## Quality

| Check | Pulse / catalog |
|-------|-----------------|
| DATA_SOURCE | analytics lists + optional domain APIs |
| CALCULATION | `len()` of catalog records — not business formulas |
| FRESHNESS | `DATA_NOT_AVAILABLE` on pulse |
| COMPLETENESS | Incomplete for enterprise decisions |
| ACCURACY | Counts are counts; **not** outcome accuracy |

Conflicts (revenue, customers, orders, headcount): still **not** merged — see metric governance § conflicts.

**P338:** business KPI trust for decisions remains **NOT_GOVERNED** / **NOT_MEASURED**. See [MEOS_P338_DECISION_INTELLIGENCE.md](./MEOS_P338_DECISION_INTELLIGENCE.md).

## Duplicate engines

Forbidden: second KPI engine, warehouse, or BI product. Analytics context remains SoR.
