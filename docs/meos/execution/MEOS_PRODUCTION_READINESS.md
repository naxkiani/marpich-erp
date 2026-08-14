# MEOS Production Readiness

**Overall status:** `NOT_READY`  
**Date:** 2026-08-14 · **P0 slice:** mitigated for Platform Core (migrations / router honesty / settings gates)

## Launch gates

| Gate | Status |
|------|--------|
| Architecture | PARTIAL (docs strong; drift) |
| UI/UX | PARTIAL (AuthZ nav + shell) |
| Frontend | PARTIAL (orphan clients gated) |
| Backend | PARTIAL |
| Database | PARTIAL (Postgres :5433 path + migrations; identity/authz 018–027/030/037 SQL landed P1) |
| API | PARTIAL (ROUTER honesty + `DEFERRED_CONTEXT_IDS`) |
| Authentication | PASS (core JWT; production rejects default secret) |
| Authorization | PARTIAL → UI nav/command/search filtered |
| Multi-tenancy | PARTIAL |
| Workflow | PARTIAL (API + Task Center UI) |
| Events | PARTIAL (production forces `event_bus_mode=outbox`) |
| AI | PARTIAL |
| Search | PARTIAL |
| Notifications | PARTIAL |
| Analytics | PARTIAL |
| Audit | PARTIAL |
| Security | PARTIAL |
| Privacy | PARTIAL (activation pack + Policy desk — Wave 04) |
| Testing | PARTIAL (Wave 01/02 + healthcare + money-path + Wave03/05 CI) |
| Performance | PARTIAL (baseline script `meos-wave04-perf-baseline.sh`) |
| Observability | PARTIAL (OTel warn-if-off in production) |
| Backup / DR | PARTIAL — see [MEOS_WAVE04_DR_RUNBOOK.md](./MEOS_WAVE04_DR_RUNBOOK.md) |
| CI/CD | PARTIAL (wave01–05 smoke/governance workflows) |
| Documentation | PARTIAL (this pack + Wave 03–05 status) |
| Production hardening | PARTIAL (P0 settings gates shipped; offsite backup automation still pending) |

## P0 mitigations (2026-08-14)

| Item | Mitigation |
|------|------------|
| Missing migrations 018–027, 030, 037 | **P1:** SQL files on disk and listed in `POST_WAVE01_MIGRATIONS` (see `DEFERRED_MIGRATIONS.md`). `apply_migration` still skips a file if absent (safety net). |
| Empty scaffolds / missing packages as live routers | `DEFERRED_CONTEXT_IDS` + `_module_available` / `filter_available_specs` in `startup_registry.py` — deferred contexts never register |
| Production JWT / outbox / OTel | `MARPICH_ENVIRONMENT=production` hard gates in `shared/infrastructure/settings.py`: reject default/short JWT, require Postgres, force outbox, warn if OTel or document signing secret off |
| DR checklist | Wave 04 runbook: [MEOS_WAVE04_DR_RUNBOOK.md](./MEOS_WAVE04_DR_RUNBOOK.md) (RPO/RTO, backup, restore drill, failover notes) |

## Critical blockers

1. ~~Unauthenticated shell widgets~~ → **Mitigated Wave 01** (session headers)
2. ~~Memory-only default undocumented~~ → **Postgres on :5433** + runbook + local `.env` postgres default
3. ~~Silent missing routers~~ → **Mitigated Wave 01** (pre-filter unavailable modules)
4. ~~No Workflow Task Center~~ → **Added** `/enterprise/workflows`
5. ~~No Wave 01 CI gate~~ → **Hardened** memory + Postgres jobs; typecheck no longer soft-fails
6. ~~Nav without AuthZ~~ → **Mitigated P0** (`permission` on registry + `hasPermission` wildcard)
7. ~~Dead FE clients without pages~~ → **Gated** under `frontend/apps/admin_portal/src/lib/_orphan/`
8. ~~Identity Postgres register crash~~ → **Fixed** `tenant_id` in role/user/session saves
9. ~~Wave 02 first business app~~ → **CRM Functional** (CAP-ENT-001) TESTED
10. ~~Wave 02 Q2C closed loop~~ → **harden script + CI** (`meos-wave02-q2c-loop.sh`)
11. ~~Healthcare Functional loop~~ → **Hospital→Lab→Pharmacy** TESTED (`meos-healthcare-loop.sh`)
12. ~~Money-path migrations missing from runner~~ → **038–045 wired** + CI

## Wave 01 / P0 verification marks

| Item | Status |
|------|--------|
| Audit pack `docs/meos/execution/` | verified |
| Auth-wired search / notifications / AI | verified |
| Registry nav + command palette + mobile drawer | verified |
| Permission-aware nav / palette / search | verified |
| Workflow Task Center | verified |
| ROUTER honesty filter | verified |
| Postgres Wave 01 runbook (:5433) | verified |
| Migration fixes (`authorization` quote, ltree, sessions PK) | verified |
| Orphan FE clients gated | verified |
| Wave 01 CI smoke workflow | verified |
| User-loop script `scripts/meos-wave01-user-loop.sh` | verified |
| Wave 02 Q2C loop `scripts/meos-wave02-q2c-loop.sh` | verified |
| Wave 02 CI smoke workflow | verified |
| Healthcare loop `scripts/meos-healthcare-loop.sh` | verified |
| Money-path migrations 038–045 + CI | verified |
| Activate→nav FE unit tests | verified |
| Wave 02 audit proof script | verified |
| Identity/authz SQL 018–027/030/037 on disk (P1) | verified |
| `DEFERRED_CONTEXT_IDS` router/service honesty | verified |
| Production settings gates (JWT/Postgres/outbox/OTel) | verified |
| DR runbook link (`MEOS_WAVE04_DR_RUNBOOK.md`) | verified |
| P2 blueprint fabrics gated (`BLUEPRINT_CONTEXT_IDS`) | verified |
| P2 empty scaffolds frozen `coming_soon` | verified |
| P3 router package contracts + CI | verified |

## After Wave 01 / P0 / Healthcare harden / Waves 03–05 gates / P2–P3 honesty

Overall remains **`NOT_READY`** for full production. Platform Core + Wave 02 Q2C + Healthcare care loop are **CONDITIONALLY_READY** for demos with Postgres. Wave 03 Intelligence smoke activated; Wave 04 Privacy/DR/Policy desk + perf baseline shipped; Wave 05 Autonomy is **deny-by-default gated**. Empty industry scaffolds remain `coming_soon` and are excluded via `DEFERRED_CONTEXT_IDS`. Speculative fabrics (`quantum` / `robotics` / `biotechnology` / `space` / `civilization`) are **`BLUEPRINT`** — APIs off unless `MARPICH_ENABLE_BLUEPRINT_APIS` or `MARPICH_APP_PROFILE=blueprint` (see `docs/adr/p2-blueprint-scaffold-honesty.md`). P3 freezes missing ROUTER/SERVICE modules in `missing_router_packages_baseline.json` and fails CI on growth (`.github/workflows/meos-p3-router-contracts.yml`).

**Remaining production risks:** automated offsite backup + monitored restore SLO (see DR runbook); industry scaffolds not live (`DEFERRED_CONTEXT_IDS`); grandfathered missing router modules still need real packages over time. Identity/authz SQL 018–027/030/037 landed (P1) with postgres adapters when `use_postgres()` — not a `PRODUCTION_READY` claim.
