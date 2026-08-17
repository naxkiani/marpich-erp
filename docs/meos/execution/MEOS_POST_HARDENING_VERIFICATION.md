# MEOS Post-Hardening Verification (P311)

**Date:** 2026-08-17  
**Method:** Re-run code + tests + scripts on this host. Documentation claims ignored unless re-executed.  
**Overall:** `NOT_READY` — **not** Release Candidate (P0 DR blocked; outbox Postgres not executed)

## Matrix

| Area | Expected | Actual | Evidence | Status |
|------|----------|--------|----------|--------|
| AUTHENTICATION | HS256 + exp + iss | Backend verify + unit tests; Edge cookie HS256 when secret set | `test_jwt_token_service.py`; `meos-jwt-cookie-selftest.mjs` PASS | **PASS** (API) / **PARTIAL** (cookie not HttpOnly; no `aud`) |
| AUTHORIZATION | Server `require_permissions` | Present on routes; no full role matrix E2E this run | `dependencies.py` | **PARTIAL** |
| SESSION | Valid JWT cookie | Cookie stores access JWT; presence `=1` rejected | `jwtCookie.ts`, middleware | **PARTIAL** |
| TENANCY | Isolation tests | Header required; dedicated negative suite not re-run | `get_tenant_id` 400 without header | **PARTIAL** |
| DATABASE | Prod = Postgres | Hard gate + reject `marpich:marpich` | `test_production_settings_gates.py` 5 passed | **PASS** (config) |
| PERSISTENCE | No memory in prod | Production rejects `memory` | same tests | **PASS** (config) |
| BACKUP | Run dump + offsite | `pg_isready` 5432/5433 **no response**; script exit 2 | this host 2026-08-17 | **BLOCKED** |
| RESTORE | Restore drill | No dump because backup failed; restore exit 1 | this host | **BLOCKED** |
| EVENTS | Outbox path | In-process fabric tests PASS | `test_event_fabric.py` | **PARTIAL** (memory) |
| OUTBOX | Postgres E2E | Tests skip without `PERSISTENCE_BACKEND=postgres` | 2 skipped | **BLOCKED** |
| WORKFLOW | Task Center + API | Scripts exist; not re-run vs live API | `meos-wave01-user-loop.sh` | **PARTIAL** |
| NOTIFICATIONS | Inbox API | Not re-run this session | — | **PARTIAL** |
| SEARCH | Permissioned query | Not re-run this session | — | **PARTIAL** |
| AUDIT | Immutable ingest | Not re-run this session | — | **PARTIAL** |
| AI | Gated / permissioned | Not re-run this session | — | **PARTIAL** |
| SECURITY | Deny-by-default | JWT issuer now verified; cookie XSS still open | this commit | **PARTIAL** |
| PRIVACY | P269 pack | Docs/scripts; not runtime | Wave 04 | **PARTIAL** |
| REGISTRY | YAML ↔ startup | Contract tests 5 passed | `test_application_registry_yaml.py` | **PASS** |
| UI/UX | One shell | KpiStrip + home pulse on branch | PR #16 | **PARTIAL** |
| ACCESSIBILITY | WCAG-oriented | Not measured this run | — | **PARTIAL** |
| TESTING | Unit/integration | P0 subset 14 passed + 2 skipped | pytest this host | **PARTIAL** |
| E2E | Browser + Postgres loops | Not executed (no DB/API) | — | **BLOCKED** |
| PERFORMANCE | Baseline script | Not executed | — | **PARTIAL** |
| OBSERVABILITY | OTel warn in prod | Config only | settings | **PARTIAL** |
| CI/CD | MEOS workflows | Files present; this run did not wait on GitHub | `.github/workflows/meos-*.yml` | **PARTIAL** |
| DISASTER RECOVERY | Successful drill | Infrastructure missing | backup/restore scripts | **BLOCKED** |
| DEPLOYMENT | Reproducible | Docker/compose exist; prod deploy not proven | — | **PARTIAL** |

## P0 revalidation (this host)

| ID | Result | Evidence |
|----|--------|----------|
| P0-01 Offsite backup | **BLOCKED** | Postgres not listening; backup exit 2 |
| P0-02 Restore drill | **BLOCKED** | No dump; restore exit 1 |
| P0-03 JWT validation | **PASS** (API unit) | valid / tamper / expired / wrong iss / wrong type |
| P0-04 `/` `/modules` | **PARTIAL** | Middleware present; not a substitute for API AuthZ |
| P0-05 Prod not memory | **PASS** | settings gate test |
| P0-06 Postgres outbox E2E | **BLOCKED** | skipped without postgres |
| P0-07 Registry drift | **PASS** | YAML contract tests (uncommitted until this slice) |

## Gap list (verified)

**P0**
1. Live Postgres + executed backup/restore (+ offsite) — **BLOCKED** (infra)
2. Postgres outbox E2E executed — **BLOCKED** (infra)
3. HttpOnly session cookie (BFF) — still **OPEN** (code)

**P1**
4. Authorization role matrix E2E  
5. Cross-tenant negative tests  
6. Wave 01/02/healthcare loops against running Postgres API  
7. Merge PR #16 to `main`

**P2**
8. Audience (`aud`) claim — not in current JWT contract  
9. Full Playwright E2E  
10. Accessibility measurement

## Tests executed (this verification)

```
node scripts/meos-jwt-cookie-selftest.mjs          → PASS
pytest settings gates + registry + fabric + outbox → 14 passed, 2 skipped
pytest test_application_registry_yaml.py           → 5 passed
./scripts/meos-postgres-backup.sh                  → FAIL (pg_isready, exit 2)
./scripts/meos-postgres-restore-drill.sh           → FAIL (no dump, exit 1)
```

## Release Candidate

**Not created.** Criteria (P0 = 0) not met: DR and Postgres outbox remain **BLOCKED** until a running database exists.

Final status: **`NOT_READY`** (hardening in progress; config/JWT/registry evidence improved).
