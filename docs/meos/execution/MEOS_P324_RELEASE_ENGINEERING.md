# MEOS P324 — Release Engineering & Extension Lifecycle Governance

**Date:** 2026-08-18T11:50:00Z  
**Decision:** GitHub Actions + compose + migration/backup scripts are **the** release infrastructure. This phase **does not** declare RELEASE_CANDIDATE or PRODUCTION_RELEASE. Git: **`e941141-dirty`**. Production: **BLOCKED**.  
**Maturity:** `DOCUMENTED` / `DEVELOPMENT` — **not** CERTIFIED / APPROVED / DEPLOYED / VERIFIED.  
**P325:** opened as continuous-evolution governance. Production learning loop **BLOCKED** (no production release).  
**P326:** expected vs actual release outcomes remain **BLOCKED** (0 production releases). See [MEOS_P326_BUSINESS_VALUE.md](./MEOS_P326_BUSINESS_VALUE.md).  
**P327:** strategic initiatives that need system change still must pass this release path. See [MEOS_INITIATIVE_PORTFOLIO.md](./MEOS_INITIATIVE_PORTFOLIO.md).  
**P328:** high-risk changes still require risk/security/rollback review on this path. Production change review: **N/A** (0 releases).  
**P329:** crisis recovery still must not bypass this release path. Live rollback **BLOCKED** (G27).  
**P334:** inventoried `CHG-*` rows still must pass this path; none are DEPLOYED. See [MEOS_CHANGE_REGISTRY.v1.yaml](./MEOS_CHANGE_REGISTRY.v1.yaml).

P324 is **release governance**, not a new CI/CD, Kubernetes, package manager, marketplace, or plugin engine.

## 1. Actual P323 status (precondition)

| Signal | Actual |
|--------|--------|
| P323 | SDK **DEVELOPABLE** (validate/init). pack/sign/publish **exit 2**. **Not PUBLISHABLE**. |
| P322 | **0 CERTIFIED** extensions · install ≠ activate |
| P321 | **0 ACTIVE** integrations |
| P320 | UX FUNCTIONAL · G20/G21 FAIL |
| P319 | **BLOCK_AUTOMATION** |
| `CI_CD_STATE` | GitHub Actions smoke/contract workflows |
| `RELEASE_STATE` | **NOT_RELEASE_CANDIDATE** (P312/P313/P314) |
| `ARTIFACT_STATE` | Git tree only · no production digest |
| `DEPLOYMENT_STATE` | G26 **BLOCKED** |
| `VERSION_STATE` | API v1 · SDK 0.1.0 · untagged HEAD |
| `SECURITY_STATE` | TRUST_CRITICAL |
| `OBSERVABILITY_STATE` | Health endpoints · alerting FAIL (G23) |
| `ROLLBACK_STATE` | G27 **BLOCKED** · DB restore drill exists |

## 2. Existing release infrastructure (inventory)

| Kind | Evidence | Production |
|------|----------|------------|
| CI | `.github/workflows/meos-wave01-smoke.yml`, `meos-wave02-smoke.yml`, `meos-wave03-smoke.yml`, `meos-wave04-05-governance.yml`, `meos-healthcare-smoke.yml`, `meos-money-path-smoke.yml`, `meos-p3-router-contracts.yml`, plus federation/twin workflows | CI ≠ production deploy |
| Containers | `docker-compose.dev.yml`, `docker-compose.meos-prod.yml` (self-signed TLS, **not** cloud prod) | **Not** G26 |
| Migrations | `scripts/run-migrations.sh` | LOCAL/CI |
| Backup/restore | `meos-postgres-backup.sh`, restore drills | Drills ≠ live rollback |
| Feature flags | `/api/v1/feature-flags/evaluate` | Not a deploy platform |
| Artifact store | **NOT_IMPLEMENTED** (no Nexus/GHCR production digest evidenced) | — |
| Orchestrator (K8s/Helm prod) | **NOT_IMPLEMENTED** on this host | — |
| Release dashboard app | **NOT_IMPLEMENTED** | Docs + observability desk only |

## 3–6. Registry, states, traceability, versions

See [MEOS_RELEASE_REGISTRY.md](./MEOS_RELEASE_REGISTRY.md).  
`SOURCE → COMMIT` is possible (`git rev-parse`). `COMMIT → immutable artifact → production runtime` is **BLOCKED** (dirty tree + G26).  
Question “what exact source produced production?” — **unanswerable**; there is no production artifact.

## 7–10. RC, gates, security, database

P312 already forbids RELEASE_CANDIDATE while P0 ≠ 0. P313 **NOT_CERTIFIED**. P314 **GO_LIVE not approved**.  
Gate table: [MEOS_RELEASE_GOVERNANCE.md](./MEOS_RELEASE_GOVERNANCE.md).  
DB: migrations idempotent; production destructive-migration recovery **NOT_EXERCISED**.

## 11–16. Config, promotion, canary, health, rollback

Secrets via env/settings — production secret manager **NOT_AVAILABLE**.  
Progressive delivery / automatic rollback: **NOT_IMPLEMENTED**.  
Release health in production: **NOT_AVAILABLE** (do not invent error rates).  
Rollback standard: [MEOS_ROLLBACK_STANDARD.md](./MEOS_ROLLBACK_STANDARD.md).

## 17–23. Extensions, APIs, events, deps, flags, tenants

Reuse P322/P323/P321. No production bypass via CLI publish.  
Feature flags may support future canary — **not** used as fake production safety here.  
Tenant-safe production cohorts: **NOT_AVAILABLE**.

## 24–33. Audit, evidence, dashboard, operators, notifications, incidents, change, emergency, metrics

Change fields: existing CHANGE_MANAGEMENT.md.  
Release notifications / incident hooks for failed prod deploy: **NOT_IMPLEMENTED** (no prod deploy). Reuse Notification Center / SRE docs when production exists — do not add a second engine.  
DORA metrics (deploy frequency, CFR, MTTR): **NOT_AVAILABLE**. Do not fabricate.

Evidence script: `scripts/meos-release-evidence.sh`.

## 34–38. Docs, certification, smoke, post-release, retirement

This file + registry + governance + rollback standard. P312 matrix **updated** (pointer only).  
Production smoke: **not executed** (no production). Workstation Wave loops are **not** production success.  
Retirement process: documentary; no production component retired this phase.

## Architecture validation scorecard

| Dimension | Score | Pass? |
|-----------|-------|-------|
| Architecture | 4 | Reuse Actions + compose + migrations |
| DDD | 4 | No new business context |
| Security | 4 | Dirty SHA and G26 block release |
| Scalability | 3 | CI on GitHub; no prod cluster |
| Performance | 3 | Baseline only |
| Testing | 4 | Honesty test on registry |
| AI Integration | 3 | Unchanged stub |
| Documentation | 4 | Authoritative P324 set |
| Accessibility | 3 | No new UI |
| Localization | 3 | Docs English |
| Observability | 3 | G23 FAIL |
| Workflow | 3 | Unchanged |
| Audit | 4 | Registry + change procedure |
| Policy Compliance | 4 | Fail-closed production claims |
| Plugin Compatibility | 4 | Extension lifecycle via P322/P323 |

**Verdict:** ENTERPRISE_GRADE as **governance**. **PRODUCTION_RELEASE: false**.

## Reuse analysis

Reused GitHub Actions, docker compose, `run-migrations.sh`, backup/restore drills, feature flags, change management, P313 gate matrix, Plugin Platform.  
Rejected: new CI product, invented GHCR digest, invented dashboard KPIs, declaring RC.

## Required next action

Commit an **immutable SHA** (G25) after P0 work, provision **production** (G26), recertify P313 with P0=0, then P314 GO_LIVE. Only then can a release become RELEASE_CANDIDATE.
