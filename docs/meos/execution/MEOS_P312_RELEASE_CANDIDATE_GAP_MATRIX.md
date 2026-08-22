# MEOS P312 — Release Candidate Gap Matrix

**Date:** 2026-08-17  
**Consumes:** [MEOS_POST_HARDENING_VERIFICATION.md](./MEOS_POST_HARDENING_VERIFICATION.md) (P311)  
**Does not overwrite P311 PASS/BLOCKED evidence.**

## External blockers (unchanged from P311)

| ID | Area | Priority | Status | Evidence |
|----|------|----------|--------|----------|
| P0-01 | DATABASE / DR | P0 | **BLOCKED** | Docker daemon not running; Postgres :5432/:5433 no listener |
| P0-02 | BACKUP | P0 | **BLOCKED** | backup script exit 2 (pg_isready) |
| P0-03 | RESTORE | P0 | **BLOCKED** | restore exit 1 (no dump) |
| P0-06 | EVENTS / OUTBOX | P0 | **BLOCKED** | Postgres outbox tests skip |
| P0-cookie | SECURITY | P0 | **OPEN** | Session cookie not HttpOnly (SPA `document.cookie`) |

## Code-side gaps P312 can address without live Postgres

| ID | Area | Priority | Status | Action |
|----|------|----------|--------|--------|
| P1-tenant | FUNCTIONALITY | P1 | **CLOSED this slice** | CRM negative test: tenant B cannot list/get tenant A contact |
| P1-authz-matrix | SECURITY | P1 | OPEN | Role matrix E2E not executed |
| P1-q2c-live | APPLICATIONS | P1 | **BLOCKED** | `meos-wave02-q2c-loop.sh` needs running API+Postgres |
| P1-healthcare-live | APPLICATIONS | P1 | **BLOCKED** | `meos-healthcare-loop.sh` needs running API+Postgres |
| P1-pr16 | DEPLOYMENT | P1 | OPEN | [PR #16](https://github.com/naxkiani/marpich-erp/pull/16) not on `main` |
| P2-aud | SECURITY | P2 | OPEN | JWT has no `aud` claim (not in current contract) |
| P2-a11y | ACCESSIBILITY | P2 | OPEN | Not measured |
| P2-playwright | TESTING | P2 | OPEN | No browser E2E this host |
| P3-cosmetic | UIUX | P3 | DEFER | Input `placeholder=` is legitimate, not fake UX |

## Release Candidate gate

P312 **cannot** declare `RELEASE_CANDIDATE`: P0 ≠ 0 (infra BLOCKED + HttpOnly cookie).  
**P324 (2026-08-18):** Same prohibition. Registry overall `NOT_RELEASE_CANDIDATE`. See [MEOS_P324_RELEASE_ENGINEERING.md](./MEOS_P324_RELEASE_ENGINEERING.md).

Stay: **`NOT_READY` / hardening in progress** (P311 language). Not HARDENED-complete.

## Application reality (script + test evidence, not menus)

See [MEOS_P312_COMPLETION_REPORT.md](./MEOS_P312_COMPLETION_REPORT.md) § applications.
