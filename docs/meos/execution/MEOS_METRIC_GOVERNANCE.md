# MEOS Metric Governance

**Date:** 2026-08-18T06:01:00Z · **P326 overlay:** 2026-08-18T12:20:00Z  
**SoR:** `analytics` (P213 / `CAP-PLT-BI-001`)  
**Companion:** [MEOS_P318_ENTERPRISE_INTELLIGENCE.md](./MEOS_P318_ENTERPRISE_INTELLIGENCE.md)  
**P326 KPI overlay (targets/actuals):** [MEOS_KPI_GOVERNANCE.md](./MEOS_KPI_GOVERNANCE.md) — **this catalog remains the SoR.** Do not fork a second KPI engine.  
**P338:** decision-intelligence overlay — KPI trust **NOT_MEASURED** for business decisions. See [MEOS_P338_DECISION_INTELLIGENCE.md](./MEOS_P338_DECISION_INTELLIGENCE.md).

Law: **do not invent KPIs.** Production values that are not sourced are `DATA_NOT_AVAILABLE`. Duplicate names across banking analytics vs platform analytics are **conflicts**, not silent merges.

## Provenance chain (required)

```
SOURCE → DATA PRODUCT → TRANSFORMATION → METRIC → INSIGHT → DECISION
```

For catalog pulse counts the chain stops at METRIC (count). Insight and Decision are **not** authorized from these numbers.

## Authoritative metric catalog (candidate definitions)

STATUS is the production measurement status, not “code exists”.

| METRIC_ID | NAME | DESCRIPTION | SOURCE | FORMULA | OWNER | FREQUENCY | TENANT_SCOPE | SECURITY_CLASSIFICATION | STATUS |
|-----------|------|-------------|--------|---------|-------|-----------|--------------|-------------------------|--------|
| `analytics.catalog.metrics_count` | Analytics metric definitions | Count of metric definitions for the tenant | `analytics` list_metrics | `len(definitions)` | analytics (SoR) | on request | tenant_id | internal | **CANDIDATE** — not a business KPI |
| `analytics.catalog.dashboards_count` | Analytics dashboards | Count of dashboard records | `analytics` list_dashboards | `len(dashboards)` | analytics | on request | tenant_id | internal | **CANDIDATE** |
| `analytics.catalog.alerts_count` | Analytics alert rules | Count of alert rules | `analytics` list_alerts | `len(alerts)` | analytics | on request | tenant_id | internal | **CANDIDATE** |
| `analytics.events.total` | Total events | Event-bus increment `*` | integration events | increment | analytics | event-driven | tenant_id | internal | **CANDIDATE** — zero unless events observed |
| `analytics.users.created` | Users created | `identity.user.created` | identity events | increment | identity (source) / analytics (counter) | event-driven | tenant_id | internal | **CANDIDATE** |
| `analytics.users.logged_in` | User logins | `identity.user.logged_in` | identity events | increment | identity / analytics | event-driven | tenant_id | internal | **CANDIDATE** |
| `analytics.encounters.completed` | Encounters completed | `hospital.encounter.completed` | hospital events | increment | hospital / analytics | event-driven | tenant_id | restricted (health) | **CANDIDATE** |
| `analytics.workflows.completed` | Workflows completed | `workflow.process.completed` | workflow events | increment | workflow / analytics | event-driven | tenant_id | internal | **CANDIDATE** |
| `analytics.documents.uploaded` | Documents uploaded | `documents.document.uploaded` | documents events | increment | documents / analytics | event-driven | tenant_id | internal | **CANDIDATE** |
| `notifications.inbox.unread` | Unread inbox | Notification inbox list | notifications API | `len(inbox)` | notifications | on request | tenant_id | internal | **CANDIDATE** (home pulse) |
| `workflow.tasks.open` | Open tasks | Workflow tasks list | workflow API | `len(tasks)` | workflow | on request | tenant_id | internal | **CANDIDATE** (home pulse) |
| `audit.entries.last_24h` | Audit entries 24h | Audit stats | audit API | source field `last_24h` | audit | on request | tenant_id | restricted | **CANDIDATE** |

Production measured values for all rows above: **NOT_AVAILABLE** (no production cluster).  
P326 TARGET / ACTUAL / STATUS overlay: **NOT_SET** / **NOT_MEASURED** / **DATA_NOT_AVAILABLE**.

## Explicitly not governed as enterprise KPIs (conflicts / missing SSOT)

| Name (ambiguous) | Conflicting surfaces | Authoritative production source | Resolution |
|------------------|----------------------|---------------------------------|------------|
| revenue | Banking analytics labels, finance/accounting contexts, policy key `analytics.revenue.target` | **NOT_AVAILABLE** — Financial Kernel / accounting posting, not home pulse | Do not merge; do not display as P318 fact |
| customers | Banking `customer_count`, CRM contacts | **NOT_AVAILABLE** | Domain-owned; no silent overwrite |
| orders | Sales context | **NOT_AVAILABLE** | sales SoR |
| employees / headcount | HR context | **NOT_AVAILABLE** | HR SoR; privacy-scoped |
| inventory | Inventory context | **NOT_AVAILABLE** | inventory SoR |
| risk | P317 register vs security incidents vs identity_intelligence catalogs | Launch register R-01…R-07 only | Do not invent residual scores |
| availability | `/health` on workstation vs production SLO | Production availability **NOT_AVAILABLE** | Demo `:8000` is not the SSOT |
| security incidents | cyber_security catalogs vs empty prod SIEM | **NOT_AVAILABLE** | P317 |

## Home pulse contract (implemented)

`GET /api/v1/analytics/home-pulse` (permission `analytics.dashboards.read`, tenant-scoped):

- `signal_class`: `CATALOG_COUNT`
- `production_kpis`: `DATA_NOT_AVAILABLE`
- `data_quality.status`: `DATA_QUALITY_WARNING`
- `provenance.source_system`: `analytics`

AI and executives must **not** treat these counts as revenue, risk, or availability.
