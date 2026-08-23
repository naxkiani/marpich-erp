# MEOS Stop List — ACTIVE (through P410)

**Status:** ACTIVE  
**Phase:** P410 G26 Consolidation — G26 NOT PASSED  
**Rule:** Until G26_READY=TRUE and formal P313 readiness, do **not** expand the platform, certify, or enable traffic.

This list is an execution brake, not an architecture change.

---

## Hard stops (do not start)

| ID | Stop | Reason |
|----|------|--------|
| STOP-01 | `NEW_MAJOR_MODULES` | 81 contexts already; 12 stubs; OpenAPI already 3651 paths |
| STOP-02 | `NEW_ARCHITECTURE` | Architecture baseline P001–P400 is frozen |
| STOP-03 | `NEW_DEPLOYMENT_ENGINE` | `deploy/*` adapters + `meos-deploy*` / orchestrators already exist |
| STOP-04 | `NEW_CONTROL_PLANE` | P399 control plane IMPLEMENTED+WIRED+TESTED — reuse, do not rebuild |
| STOP-05 | `NEW_AI_PLATFORM` | AI surfaces already dominate OpenAPI volume; product core first |
| STOP-06 | `NEW_DATABASE_ENGINE` | PostgreSQL 16 + SQL migrations are the real system |
| STOP-07 | `NEW_FRONTEND_FRAMEWORK` | Next.js 15 admin_portal is the product UI |
| STOP-08 | `DUPLICATE_FEATURES` | Auth/RBAC/audit/notification/workflow duplicates must be reported, not copied again |
| STOP-09 | `NON_CRITICAL_REFACTORING` | No rewrite / framework replacement / microservice split / monolith merge without a later explicit decision gate |
| STOP-10 | `P313` / `GO_LIVE` / `PRODUCTION_TRAFFIC` | G26_READY=FALSE; P401 forbids |
| STOP-11 | `G26_BYPASS` | Keep G26_READY=FALSE until real gates pass |
| STOP-12 | `P0_CHANGE` that fakes readiness | No fake digests, credentials, or production_verified flags |
| STOP-13 | `PROMPT_CHAIN P402…P500` for greenfield features | New prompts only for evidenced, necessary gaps |

---

## Allowed work (narrow)

1. Reality honesty fixes (docs/tests that match code)
2. Single Source of Truth designation for Auth/RBAC (without deleting duplicates yet)
3. Fixing admin_portal typecheck / broken imports
4. Stabilizing existing tests
5. Local demo reproducibility
6. Documenting Docker build context (`backend/`)
7. Human-driven dirty-tree triage (no auto-commit from agents unless asked)

---

## Prompt admission test (post-P401)

A new prompt is allowed only if **all** are true:

1. A real gap was discovered in the repository  
2. The gap is necessary for the product  
3. It is not already implemented  
4. It cannot be solved inside existing architecture  
5. Execution has clear value (VALUE ≥ EFFORT under Lane A or B)

Otherwise: **STOP** — update backlog only.

---

## Related artifacts

- `docs/meos/execution/MEOS_REALITY_MATRIX.v1.yaml`
- `docs/meos/execution/MEOS_EXECUTION_BACKLOG.v1.yaml`
- `docs/meos/execution/P403_CORE_STABILIZATION_REPORT.md`
- `docs/meos/execution/P404_PRODUCTIZATION_REPORT.md`
- Prior audit notes: `docs/meos/execution/MEOS_REALITY_AUDIT.md` (2026-08-17; superseded as SoT by Reality Matrix for P401)

## P404 (2026-08-23)

Stop list remains ACTIVE. P404 productized existing Core only (no new engines). **STOP after P404** — do not auto-run P405. G26 stays BLOCKED.

## P405 (2026-08-23)

Acceptance evidence completed. Decision **B — MVP ACCEPTED WITH NON-CRITICAL GAPS**. **STOP after P405** — do not auto-run P406. No G26 bypass. No production.

## P406 (2026-08-23)

Release hardening evidence completed. Decision **D — RELEASE BLOCKED BY INFRASTRUCTURE** (Docker/G26/clean SHA). **STOP after P406** — do not auto-run P407. No production traffic. No G26 bypass. No P313 certification.

## P407 (2026-08-23)

Deployment re-entry **BLOCKED_BY_P406** (P406 was not A/B). G26 evidence mapped only; **no provisioning**. Decision **D — INFRASTRUCTURE BLOCKER**. **STOP after P407** — do not auto-run P408. Do not fake G26. Do not enable traffic.

## P408 (2026-08-23)

G26 blocker closure **BLOCKED_BY_P407**. Activation **PLAN only** — **PROVISIONING=NOT_EXECUTED**. Decision **D — INFRASTRUCTURE BLOCKED**. **STOP after P408** — do not auto-run P409. Do not bypass G26. Do not certify P313. Production traffic OFF.

## P409 (2026-08-23)

Formal G26 execution **BLOCKED** (`G26_READY != TRUE`). **No production deployment.** Decision **D — G26 INFRASTRUCTURE BLOCKED**. **STOP after P409** — do not auto-run P410. Do not enable traffic. Do not certify P313. Do not declare GO-LIVE.

## P410 (2026-08-23)

G26 consolidation **COMPLETED**. Validator **G26_READY=FALSE**. Classification **G26_BLOCKED_INFRASTRUCTURE**. Decision **F — G26 NOT PASSED**. **P313_STATUS=NOT_READY**. **P313_READY=FALSE**. Path = **TARGETED REMEDIATION**. **STOP after P410** — do not auto-run P411. Do not certify P313. Do not enable production traffic. Do not declare GO-LIVE. Critical blockers remain on stop list (G26-01..G26-10).

## G26 Targeted Remediation — attempt 1 (2026-08-23)

Baseline + RCA + first attempt (G26-05) completed. **G26_READY remains FALSE**. **CLOSED_BLOCKERS=0**. Absolute stop: credentials / production cluster / managed DB / DNS / TLS / SM missing; docker down; dirty tree needs human triage. Decision **C — G26 BLOCKED BY EXTERNAL INFRASTRUCTURE**. **MEOS_STOP_LIST=ACTIVE**. Do **not** write P411. Do **not** certify P313. Production traffic **OFF**. Continue remediation only when real provider credentials + human clean-SHA triage are available.
