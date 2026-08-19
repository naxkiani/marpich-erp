# MEOS Executive Cockpit

**Date:** 2026-08-19T07:10:00Z  
**Experience SoR:** [MEOS_EXECUTIVE_COMMAND_CENTER.md](./MEOS_EXECUTIVE_COMMAND_CENTER.md) — **do not fork** a second shell or dashboard framework.  
**P338 overlay:** decision-intelligence views contract only.

## Law

The executive cockpit **extends existing MEOS shell** (`DashboardPage` + `KpiStrip` + AppShell). It is **not** a new BI product, dashboard engine, or executive ERP module.

## Current state

| View | Backend | Production display |
|------|---------|-------------------|
| Strategy | P327 PLATFORM_GATE drafts | **Do not show** as ACTIVE OKRs |
| Finance | Financial Kernel / accounting | **NOT_AVAILABLE** |
| Operations | Workflow tasks + pulse | Open **task count** only (catalog) |
| Customer | CRM / banking | **NOT_AVAILABLE** |
| People | HR | **NOT_AVAILABLE** (privacy) |
| Risk | P328 register | Qualitative R-01…R-07 only |
| Security | P317 | **NOT_AVAILABLE** |
| Data | P337 overlay | **NOT_AVAILABLE** as HEALTHY mesh |
| Applications | P336 registry | **0 ACTIVE** — no usage/cost tiles |
| Portfolio | P335 | **NOT_MEASURED** investment/ROI |
| Value | P326 outcomes | **IDENTIFIED** / **NOT_MEASURED** |
| Decisions | Decision registry | Four **documented** phase gates only |

**State:** `WORKSTATION_OPERATOR_HOME` — not a production executive command platform.

## Decision queue (mandate §29)

| Queue | Status |
|-------|--------|
| DECISIONS_PENDING | **NOT_IMPLEMENTED** (no runtime queue) |
| DECISIONS_AT_RISK | **NOT_IMPLEMENTED** |
| DECISIONS_OVERDUE | **NOT_IMPLEMENTED** |
| DECISIONS_BLOCKED | Documented blockers only (G26, G19, …) |
| DECISIONS_COMPLETED | **0** executed |

Do not render fake queue badges or dead Approve/Reject buttons.

**P339 execution control:** DECISIONS → ACTIONS → BLOCKERS → OUTCOMES → BENEFITS. Authorized actions **0**. Benefits **0**. See [MEOS_EXECUTION_CONTROL_RUNBOOK.md](./MEOS_EXECUTION_CONTROL_RUNBOOK.md).

## UX

Royal blue / white / grey / silver. RTL/LTR. Shared `KpiStrip`, tables, filters. `DATA_QUALITY_WARNING` when pulse says so. No fake KPI cards, charts, or HEALTHY status.

## Next evidence

After `PRODUCTION_ACTIVE`: bind each tile to [MEOS_METRIC_GOVERNANCE.md](./MEOS_METRIC_GOVERNANCE.md) with SOURCE, FRESHNESS, OWNER, and permission facets. Connect workflow Task Center to decision registry IDs.
