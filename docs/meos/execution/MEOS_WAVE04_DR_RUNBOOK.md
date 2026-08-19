# MEOS Wave 04 — Backup & Disaster Recovery Runbook

**Status:** PARTIAL (P313 recert 2026-08-18: object-store backup+restore PASS `RTO_MS=22762`; geographic AWS + monitored SLO still required for a production cluster) · **Date:** 2026-08-18  
**P328:** Production RTO/RPO **NOT_VERIFIED**. Local `RTO_MS` is **LOCAL_ONLY**. See [MEOS_RESILIENCE_STANDARD.md](./MEOS_RESILIENCE_STANDARD.md).

## Scope

Postgres (SoR) · object storage for Document Exchange blobs · Redis (cache — reconstructible) · Event outbox / broker offsets.

## RPO / RTO targets (demo → production)

| Tier | RPO | RTO |
|------|-----|-----|
| Demo / staging | 24h | 4h |
| Production (target) | ≤15m | ≤1h |

## Backup (automated script)

```bash
# Local / mounted offsite directory (preferred over ephemeral container disk)
export MEOS_BACKUP_DIR=/mnt/meos-backups   # or leave default: .meos-backups/
export PGHOST=127.0.0.1 PGPORT=5433 PGUSER=marpich PGPASSWORD=… PGDATABASE=marpich_platform

# Optional object storage copy
export MEOS_BACKUP_S3_URI=s3://your-bucket/meos/postgres

./scripts/meos-postgres-backup.sh
```

1. **Postgres:** `pg_dump` + gzip (logical). Enable continuous WAL archive when streaming replication is on (production RPO).
2. **Migrations:** store applied versions (`platform.schema_migrations`); restore requires replay via `scripts/run-migrations.sh` after base restore if schema lag.
3. **Documents:** bucket versioning + cross-region replica (Integration / file_storage — not module FS).
4. **Secrets:** never in DB dumps committed to git; restore from Secrets Manager / env only.
5. **Git:** `.meos-backups/` is gitignored — never commit dumps.

## Restore drill

```bash
# Uses latest dump under MEOS_BACKUP_DIR (or MEOS_RESTORE_DUMP=/path/to.dump.sql.gz)
# Restores into a *separate* database by default (marpich_platform_restore)
export MEOS_RESTORE_DATABASE=marpich_platform_restore
./scripts/meos-postgres-restore-drill.sh

# Optional API smoke after pointing API at the restored DB:
# RUN_SMOKE=1 API_URL=http://127.0.0.1:8000 ./scripts/meos-postgres-restore-drill.sh
```

Drill writes `docs/meos/execution/.last_restore_drill.json` (gitignored). Copy the timestamp into [MEOS_PRODUCTION_READINESS.md](./MEOS_PRODUCTION_READINESS.md) when declaring a successful monitored drill.

Also recommended after restore:

```bash
./scripts/meos-wave01-user-loop.sh
./scripts/meos-wave02-q2c-loop.sh
./scripts/meos-healthcare-loop.sh
```

## Failover notes

- Ephemeral filesystem (Render/containers): **do not** rely on local disk for SoR.
- Bind services to `0.0.0.0:$PORT`.
- Document last successful drill date in `MEOS_PRODUCTION_READINESS.md`.

## Last execution (P311, 2026-08-17)

| Step | Result |
|------|--------|
| `pg_isready` 127.0.0.1:5433 | no response |
| `pg_isready` 127.0.0.1:5432 | no response |
| `./scripts/meos-postgres-backup.sh` | **FAIL** exit 2 |
| `./scripts/meos-postgres-restore-drill.sh` | **FAIL** exit 1 (no dump) |

P311 local DR was **BLOCKED** (no Postgres).

## Last execution (P313 recertification, 2026-08-17)

| Step | Result |
|------|--------|
| `MEOS_REQUIRE_OFFSITE=1` + `MEOS_BACKUP_S3_URI` | **PASS** dump 373320 bytes + WAL tar listed (`offsite=copied_listed`) |
| Offsite restore | **PASS** `RTO_MS=33299` → `marpich_platform_offsite_restore` |
| WAL | `archive_mode=on`, `wal_level=replica`, `archive_timeout=60` |

Object store is MinIO on a separate Docker volume (not AWS multi-region). Scheduled alerting SLO remains **PENDING**.

## Last execution (P313 recertification, 2026-08-18)

| Step | Result |
|------|--------|
| `MEOS_REQUIRE_OFFSITE=1` + MinIO `:9000` | **PASS** dump 373323 bytes + WAL tar 5772011 listed (`offsite=copied_listed`) |
| Offsite restore | **PASS** `RTO_MS=22762` → `marpich_platform_p313_restore` |
| WAL | `archive_mode=on`, `wal_level=replica`, `archive_timeout=60` (reconfirmed on running `marpich-postgres`) |

## Current gap to PASS

| Item | Status |
|------|--------|
| Backup script `meos-postgres-backup.sh` | **LANDED** |
| Restore drill script `meos-postgres-restore-drill.sh` | **LANDED** |
| Local restore drill into `marpich_platform_restore` | **P313 PASS** 2026-08-17T07:26:09Z — `platform.outbox` + `clinic.encounters` + `tenant.tenants` |
| Offsite restore 2026-08-18 | **P313 PASS** `RTO_MS=22762` → `marpich_platform_p313_restore` (dump 373323 bytes listed) |
| Offsite object storage configured in every env (`MEOS_BACKUP_S3_URI`) | **PENDING ops** — this-host MinIO evidenced; production AWS multi-region **not** configured |
| gzip integrity check (`gzip -t`) | **LANDED** |
| JWT cookie HS256 selftest | `scripts/meos-jwt-cookie-selftest.mjs` |
| Scheduled job + alert on backup failure | **PENDING ops** |
| Quarterly monitored restore SLO recorded | **PENDING ops** |
