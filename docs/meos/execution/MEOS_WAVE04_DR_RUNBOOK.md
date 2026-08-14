# MEOS Wave 04 — Backup & Disaster Recovery Runbook

**Status:** PARTIAL (runbook + drill checklist) · **Date:** 2026-08-13

## Scope

Postgres (SoR) · object storage for Document Exchange blobs · Redis (cache — reconstructible) · Event outbox / broker offsets.

## RPO / RTO targets (demo → production)

| Tier | RPO | RTO |
|------|-----|-----|
| Demo / staging | 24h | 4h |
| Production (target) | ≤15m | ≤1h |

## Backup

1. **Postgres:** nightly `pg_dump` (logical) + continuous WAL archive when streaming replication is enabled.
2. **Migrations:** store applied versions (`platform.schema_migrations`); restore requires replay via `scripts/run-migrations.sh` only after base restore if schema lag.
3. **Documents:** bucket versioning + cross-region replica (Integration / file_storage platform — not module FS).
4. **Secrets:** never in DB dumps committed to git; restore from Secrets Manager / env only.

## Restore drill (quarterly)

```bash
# 1. Provision empty Postgres
# 2. Restore dump
# 3. Apply any missing migrations
./scripts/run-migrations.sh
# 4. Start API with DATABASE_URL pointing at restored instance
# 5. Smoke:
./scripts/meos-wave01-user-loop.sh
./scripts/meos-wave02-q2c-loop.sh
./scripts/meos-healthcare-loop.sh
```

## Failover notes

- Ephemeral filesystem (Render/containers): **do not** rely on local disk for SoR.
- Bind services to `0.0.0.0:$PORT`.
- Document last successful drill date in `MEOS_PRODUCTION_READINESS.md`.

## Current gap to PASS

Automated offsite backup job + monitored restore SLO — track as production hardening (still FAIL until ops automation lands).
