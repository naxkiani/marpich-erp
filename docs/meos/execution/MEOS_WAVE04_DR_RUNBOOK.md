# MEOS Wave 04 — Backup & Disaster Recovery Runbook

**Status:** PARTIAL (scripts landed; offsite + monitored SLO still required for PASS) · **Date:** 2026-08-17

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

## Current gap to PASS

| Item | Status |
|------|--------|
| Backup script `meos-postgres-backup.sh` | **LANDED** |
| Restore drill script `meos-postgres-restore-drill.sh` | **LANDED** |
| Offsite object storage configured in every env (`MEOS_BACKUP_S3_URI`) | **PENDING ops** |
| Scheduled job + alert on backup failure | **PENDING ops** |
| Quarterly monitored restore SLO recorded | **PENDING ops** |
