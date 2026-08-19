# MEOS Go-Live Checklist

**P313 decision (2026-08-18):** **not `GO_LIVE_READY`.**  
**P314:** Pre-deployment gate remains **FAIL** — **no production deploy**. See [MEOS_P314_GO_LIVE_REPORT.md](./MEOS_P314_GO_LIVE_REPORT.md).  
**P342 (2026-08-19):** Recert **OUTCOME_B**. GO_LIVE is **not** completed. See [MEOS_P342_PRODUCTION_GATE_CLOSURE.md](./MEOS_P342_PRODUCTION_GATE_CLOSURE.md).  
**P343 (2026-08-19):** Final gate **OUTCOME_B**. **PRODUCTION_CERTIFIED = NO**. **GO_LIVE_READY = NO**. Checklist uses CERTIFIED / PENDING / BLOCKED / REQUIRES_HUMAN_APPROVAL. P343 does **not** authorize GO-LIVE. See [MEOS_P343_FINAL_PRODUCTION_CERTIFICATION.md](./MEOS_P343_FINAL_PRODUCTION_CERTIFICATION.md).  
**P344 (2026-08-19):** Launch **STOPPED** at entry gate. No deploy. See [MEOS_P344_GO_LIVE_EXECUTION.md](./MEOS_P344_GO_LIVE_EXECUTION.md).  
**P345 (2026-08-19):** G26 provisioning **BLOCKED** (credentials missing). See [MEOS_P345_G26_PROVISIONING.md](./MEOS_P345_G26_PROVISIONING.md).  
**P346 (2026-08-19):** G26 evidence gate **STOPPED**. See [MEOS_P346_G26_BLOCKER_CLOSURE.md](./MEOS_P346_G26_BLOCKER_CLOSURE.md).  
**P347 (2026-08-19):** **EXT-G26** frozen **UNRESOLVED**. G26 re-entry checklist below. **WAIT** — do not GO-LIVE. See [MEOS_P347_EXTERNAL_HANDOFF.md](./MEOS_P347_EXTERNAL_HANDOFF.md).  
**P349 (2026-08-19):** Infrastructure **REQUIREMENTS_IDENTIFIED**. **G26_READY = FALSE**. Do not GO-LIVE. See [MEOS_EXT_G26_PROVIDER_COMPATIBILITY.md](./MEOS_EXT_G26_PROVIDER_COMPATIBILITY.md).  
**P350 (2026-08-19):** Provisioning **BLOCKED**. Do not GO-LIVE. See [MEOS_P350_PROVISIONING_REPORT.md](./MEOS_P350_PROVISIONING_REPORT.md).  
**P351 (2026-08-19):** Product launch packages. Adapters ≠ GO-LIVE. See [MEOS_LAUNCH_PROFILES.md](./MEOS_LAUNCH_PROFILES.md).  
**P353 (2026-08-19):** Clean release engineering + launch fabric. Adapters and DEMO compose are **not** GO-LIVE. See [MEOS_P353_LAUNCH_FABRIC.md](./MEOS_P353_LAUNCH_FABRIC.md) · [MEOS_P353_TARGET_STATUS.v1.yaml](./MEOS_P353_TARGET_STATUS.v1.yaml).  
**P354 (2026-08-19):** Installer is **PLAN_ONLY**. Launch control requires `--confirm yes` and cannot bypass G26. Release-candidate engineering is **not** GO-LIVE. Dirty worktree cannot become `RELEASE_CANDIDATE`. See [MEOS_P354_UNIVERSAL_INSTALLATION.md](./MEOS_P354_UNIVERSAL_INSTALLATION.md) · [MEOS_P354_LAUNCH_CONTROL_REPORT.md](./MEOS_P354_LAUNCH_CONTROL_REPORT.md) · [MEOS_P354_RELEASE_CANDIDATE.md](./MEOS_P354_RELEASE_CANDIDATE.md).  
**P355 (2026-08-19):** Productization is not GO-LIVE. See [MEOS_P355_PRODUCTIZATION.md](./MEOS_P355_PRODUCTIZATION.md).

Do not declare go-live until every mandatory row is evidence-backed. Demo loops and local pytest are not go-live. Workstation evidence is **not** CERTIFIED for production.

| # | Prerequisite | Status | Evidence / gap |
|---|--------------|--------|----------------|
| 1 | Production deployment procedure | **BLOCKED** | Runbook exists; G26 no production cluster. |
| 2 | Production configuration distinct from development | **PENDING** | `.env.meos-prod` gitignored; recert used demo `:5433`/`:8000`. |
| 3 | Backup | **PENDING** | Workstation MinIO 2026-08-18. Production backup UNVERIFIED. |
| 4 | Restore evidence | **PENDING** | Workstation restore `RTO_MS=22762`. Production restore UNVERIFIED. |
| 5 | Monitoring | **PENDING** | Local `/health` `/live` `/ready` 200. Not production. |
| 6 | Alerting | **BLOCKED** | G23 FAIL. |
| 7 | Rollback | **BLOCKED** | G27 BLOCKED. |
| 8 | Incident response | **PENDING** | Runbook notes; no on-call owner. |
| 9 | Operational ownership | **PENDING** | NOT_AVAILABLE. |
| 10 | Smoke-test plan | **PENDING** | Scripts READY; not production smoke. |
| 11 | User onboarding readiness | **PENDING** | No production IdP/tenant run. |
| 12 | Release identification | **PENDING** | Local clean SHA `565f5b70`. **Not** a production deploy. GHCR digest **NOT_AVAILABLE**. |
| 13 | P0 = 0 | **BLOCKED** | P0 = **1** (G26). |
| 14 | PRODUCTION_CERTIFIED | **BLOCKED** | **NO** — P343 final gate. |
| 15 | P314 GO_LIVE | **REQUIRES_HUMAN_APPROVAL** | NOT APPROVED. P344 STOPPED; must not complete this row. |

## P314 launch checklist (all remain unchecked)

- [ ] P313 PRODUCTION_CERTIFIED
- [ ] P313 GO_LIVE_READY
- [ ] P0 = 0
- [ ] production release identified (immutable SHA/tag)
- [ ] production configuration verified
- [ ] secrets verified
- [ ] PostgreSQL verified (production)
- [ ] database migrations verified (production)
- [ ] production backup completed (offsite)
- [ ] restore procedure verified (offsite)
- [ ] application deployed
- [ ] health checks pass (liveness + readiness)
- [ ] authentication verified
- [ ] authorization verified
- [ ] tenant isolation verified
- [ ] critical business flows verified
- [ ] events/outbox verified
- [ ] workflows verified
- [ ] notifications verified
- [ ] audit verified
- [ ] search verified
- [ ] AI controls verified
- [ ] observability active
- [ ] alerts active
- [ ] rollback ready
- [ ] UI smoke test passed
- [ ] accessibility critical paths verified
- [ ] performance baseline captured
- [ ] user onboarding ready
- [ ] incident response ready

**Go-live rule:** all of 1–8, 11, 13, 14 must be closed with current production evidence **before** a human P314 decision. Smoke scripts (10) and git SHA (12) are not sufficient. Even if those close, row 15 remains **REQUIRES_HUMAN_APPROVAL**.

**P343:** Rows 1, 6–7, 12–14 **BLOCKED**. Row 15 **REQUIRES_HUMAN_APPROVAL**. No row is **CERTIFIED**. P314 boxes remain unchecked. GO_LIVE is **not** completed.  
**P344:** Entry gate **FAIL**. Deploy **not executed**. Checklist unchanged except this note.

## G26 re-entry (P347) — not GO-LIVE

Authoritative blocker **EXT-G26** = **UNRESOLVED**. Do **not** start P313 recertification or P344 until every box below is evidence-backed. Reuse existing Helm/Flux/CI. `47258dfd-dirty` is **FORBIDDEN**. Workstation `:5433` / compose `:5444` are **NON_PRODUCTION**.

External resources (all required):

- [ ] Authorized production hosting account
- [ ] Production cluster/server
- [ ] Managed PostgreSQL
- [ ] Public DNS
- [ ] Public-CA TLS
- [ ] Production secret manager
- [ ] CI deploy credentials
- [ ] Container registry access
- [ ] Clean git release (`git status --short` empty)
- [ ] Production deployment identity (commit + image digest)

G26 sub-gates (no averaging; one BLOCKED keeps G26 BLOCKED):

- [ ] G26-01 PRODUCTION_CLUSTER = PASS
- [ ] G26-02 MANAGED_POSTGRES = PASS
- [ ] G26-03 PUBLIC_CA_TLS = PASS
- [ ] G26-04 SECRET_MANAGER = PASS
- [ ] G26-05 CLEAN_IMMUTABLE_RELEASE = PASS
- [ ] G26-06 CI_DEPLOY = PASS
- [ ] G26-07 PRODUCTION_NETWORK = PASS
- [ ] G26-08 PRODUCTION_RUNTIME = PASS
- [ ] G26-09 DEPLOYMENT_IDENTITY = PASS
- [ ] G26-10 ROLLBACK_CAPABILITY = VERIFIED

Then, in order: G26 re-validation → P313 recertification (recalculate P0) → human `GO_LIVE_AUTHORIZATION = APPROVED` → P344. **Do not generate architecture-expansion prompts while EXT-G26 is unresolved.**

**P348:** Automated gate: `python3 scripts/meos-ext-g26-readiness.py`. Current **G26_READY = FALSE**. See [MEOS_EXT_G26_INFRASTRUCTURE_HANDOFF.md](./MEOS_EXT_G26_INFRASTRUCTURE_HANDOFF.md).
