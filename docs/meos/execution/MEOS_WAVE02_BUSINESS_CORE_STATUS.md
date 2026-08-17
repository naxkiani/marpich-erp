# MEOS Wave 02 — Business Core Status

**Date:** 2026-08-17 · **Evidence-based** (scripts + registry, not UI screenshots)

## Overall

**CONDITIONALLY_READY** for Postgres demos. Not HARDENED / PRODUCTION_READY.

## Application evidence

| App | Status | Evidence |
|-----|--------|----------|
| CRM | **TESTED** | `meos-wave02-q2c-loop.sh` + registry |
| Sales | **TESTED** | Q2C loop |
| Inventory | **TESTED** | Q2C loop |
| Accounts Receivable / Accounting | **TESTED** | Q2C / money-path |
| Procurement | **TESTED** | Q2C loop |
| HR | **PARTIAL** | Module present; depth below CRM |
| Payroll | **PARTIAL** | Module present; not full Functional loop claim |
| Tax | **PARTIAL** | Module present; Q2C-adjacent |
| Healthcare (Hospital→Lab→Pharmacy) | **TESTED** | `meos-healthcare-loop.sh` + CI |

## CI

- `.github/workflows/meos-wave02-smoke.yml`
- `.github/workflows/meos-healthcare-smoke.yml`
- `.github/workflows/meos-money-path-smoke.yml`

## Gaps to HARDENED

1. Postgres E2E for every Wave 02 app (not memory-only)
2. Education / banking desks still demo-depth (`MEOS_UIUX_STATUS.md`)
3. Tenant isolation negative tests per app
4. Full browser E2E (Playwright) for Q2C + healthcare

Do **not** upgrade status based on UI appearance alone.
