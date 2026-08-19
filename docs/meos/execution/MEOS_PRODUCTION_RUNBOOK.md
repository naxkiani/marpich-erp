# MEOS Production Runbook

**Status:** Operational procedure for **demo Postgres and workstation production-profile**. Not a production-certified cluster.  
**P313 recertification (2026-08-18):** object-store backup+restore **PASS** (`RTO_MS=22762`); G26 production cluster **BLOCKED**.  
**P314:** Go-live **not approved**. Do not treat this runbook as a live production cutover.  
**P341 (2026-08-19):** Infrastructure readiness **OUTCOME_B**. Production target **NOT_AVAILABLE**. Do not classify localhost, `:8000` `/health`, or stopped `meos-prod` as G26. See [MEOS_P341_PRODUCTION_INFRASTRUCTURE_READINESS.md](./MEOS_P341_PRODUCTION_INFRASTRUCTURE_READINESS.md).  
**P342 (2026-08-19):** P313 recert **OUTCOME_B**. Commands below remain **workstation-verified** only. See [MEOS_P342_PRODUCTION_GATE_CLOSURE.md](./MEOS_P342_PRODUCTION_GATE_CLOSURE.md).  
**P343 (2026-08-19):** Final gate **OUTCOME_B**. Production identity **NON_PRODUCTION**. Do not treat these commands as production cutover. See [MEOS_P343_FINAL_PRODUCTION_CERTIFICATION.md](./MEOS_P343_FINAL_PRODUCTION_CERTIFICATION.md).  
**P344 (2026-08-19):** Launch **STOPPED**. These commands were **not** used for production GO-LIVE. See [MEOS_P344_GO_LIVE_EXECUTION.md](./MEOS_P344_GO_LIVE_EXECUTION.md).  
**P345 (2026-08-19):** G26 provisioning **BLOCKED**. Do not treat this runbook as a live cluster. See [MEOS_P345_G26_PROVISIONING.md](./MEOS_P345_G26_PROVISIONING.md).  
**P346 (2026-08-19):** G26 evidence **STOPPED**. Commands below are **not** production. See [MEOS_P346_G26_BLOCKER_CLOSURE.md](./MEOS_P346_G26_BLOCKER_CLOSURE.md).  
**P347 (2026-08-19):** **EXT-G26 UNRESOLVED**. Do not treat this runbook as a live cluster. See [MEOS_P347_EXTERNAL_HANDOFF.md](./MEOS_P347_EXTERNAL_HANDOFF.md).  
**P349 (2026-08-19):** Discovery plan only. **G26_READY = FALSE**. Do not treat this runbook as provisioned infrastructure. See [MEOS_EXT_G26_INFRASTRUCTURE_IMPLEMENTATION_PLAN.md](./MEOS_EXT_G26_INFRASTRUCTURE_IMPLEMENTATION_PLAN.md).  
**P350 (2026-08-19):** Provisioning **BLOCKED**. No production cluster. See [MEOS_P350_PROVISIONING_REPORT.md](./MEOS_P350_PROVISIONING_REPORT.md) · [MEOS_PRODUCTION_ENVIRONMENT_RECORD.md](./MEOS_PRODUCTION_ENVIRONMENT_RECORD.md).  
**P353 (2026-08-19):** VPS/K8s packages consume `MEOS_IMAGE` / `image.digest`, not `:latest`. No production deploy. See [MEOS_P353_RELEASE_ENGINEERING_REPORT.md](./MEOS_P353_RELEASE_ENGINEERING_REPORT.md).

Companion: [MEOS_WAVE01_POSTGRES_RUNBOOK.md](./MEOS_WAVE01_POSTGRES_RUNBOOK.md) · [MEOS_WAVE04_DR_RUNBOOK.md](./MEOS_WAVE04_DR_RUNBOOK.md)

## Release identification

```bash
git rev-parse HEAD
git describe --always --dirty
```

Record SHA in the incident ticket and backup manifest.

## Start (this host pattern)

```bash
docker compose -f infrastructure/docker/compose/docker-compose.dev.yml up -d postgres
export PGHOST=127.0.0.1 PGPORT=5433 PGUSER=marpich PGPASSWORD=marpich PGDATABASE=marpich_platform
./scripts/run-migrations.sh

cd backend
export PERSISTENCE_BACKEND=postgres
export DATABASE_URL=postgresql+asyncpg://marpich:marpich@127.0.0.1:5433/marpich_platform
.venv/bin/uvicorn core.presentation.api.main:app --host 0.0.0.0 --port "${PORT:-8000}"
```

Health: `GET /api/v1/health` and `GET /api/v1/ready` (Postgres `SELECT 1`) on the production-profile API `:8080`.

Production must **not** use default `marpich:marpich` credentials (`MARPICH_ENVIRONMENT=production` rejects them). Workstation production-profile: `./scripts/meos-prod-env-init.sh` then Postgres `:5444` + `./scripts/meos-prod-api-up.sh`. Compose project **must** be `meosprod` so it never replaces the demo stack.

## Smoke after start

```bash
export API_URL=http://127.0.0.1:8000
./scripts/meos-wave01-user-loop.sh
./scripts/meos-wave02-q2c-loop.sh
./scripts/meos-healthcare-loop.sh
```

## Backup

```bash
export MEOS_BACKUP_S3_URI=s3://meos-backups/postgres
export MEOS_S3_ENDPOINT_URL=http://127.0.0.1:9000   # MinIO; omit for AWS
export AWS_ACCESS_KEY_ID=… AWS_SECRET_ACCESS_KEY=…
./scripts/meos-postgres-backup.sh
./scripts/meos-offsite-restore-drill.sh
```

Dumps land in `.meos-backups/` (gitignored). Prefer `marpich-postgres` container `pg_dump` so dump dialect matches Postgres 16.

## Restore (non-destructive drill)

```bash
export MEOS_RESTORE_DATABASE=marpich_platform_restore
./scripts/meos-postgres-restore-drill.sh
```

Last local drill: **2026-08-17T07:26:09Z** → `marpich_platform_restore` (`platform.outbox`, `clinic.encounters`, `tenant.tenants`).

Restore sanitizes PG 18-only `SET transaction_timeout` and `\\restrict` tokens.

**Do not** restore over the live production database without an approved change window.

## Rollback / forward recovery

| Layer | Strategy |
|-------|----------|
| Application | Redeploy previous container/image SHA. |
| Configuration | Revert env/secret version in the secret store. |
| Database | SQL migrations in `scripts/run-migrations.sh` are **forward-only**. Do **not** pretend down-migrations exist. Recover by restoring a dump into a new database and cutting over `DATABASE_URL`, or by shipping a forward-fix migration. |
| Failure detection | `/api/v1/health` + smoke scripts above. Alerting SLO is **not** certified (G23). |

## Incident response (minimum)

1. Capture `X-Request-ID` / `X-Correlation-ID` from the gateway.  
2. Do not disable auth or tenant headers to “unblock” users.  
3. Prefer restore-to-new-DB over in-place mutation.  
4. Audit remains append-only — do not truncate audit tables.

## Secrets

Never commit dumps, `.env` production secrets, or JWT keys. Inject via the platform secret store at deploy time.

## G26 re-entry (EXT-G26)

**Status:** **EXTERNAL_DEPENDENCY_BLOCKED**. Responsible party: **NOT_AVAILABLE**.  
**Do not deploy** until the G26 re-entry boxes in [MEOS_GO_LIVE_CHECKLIST.md](./MEOS_GO_LIVE_CHECKLIST.md) are evidence-backed.

When those resources exist, reuse **existing** paths only:

1. Clean tree: `git status --short` must be empty. Never deploy `47258dfd-dirty`.  
2. CI: `.github/workflows/identity-federation-enterprise.yml` → image `ghcr.io/marpich/marpich-backend` with digest.  
3. Helm: `infrastructure/kubernetes/helm/marpich-iam/` + `values-production.yaml`.  
4. Flux: `infrastructure/fluxcd/marpich-iam-helmrelease.yaml`.  
5. Verify deployed commit = certified SHA and deployed digest = certified artifact.  
6. Then **P313 recertification** (recalculate P0). Then human GO_LIVE approval. Then P344.

Do **not** create a second deployment engine. Do **not** treat compose `:5444` or demo `:5433` as production Postgres.

**P348 validator:** `python3 scripts/meos-ext-g26-readiness.py` — current **G26_READY = FALSE**. Does not print secret values. P313 is **not** auto-started. See [MEOS_EXT_G26_INFRASTRUCTURE_HANDOFF.md](./MEOS_EXT_G26_INFRASTRUCTURE_HANDOFF.md).
