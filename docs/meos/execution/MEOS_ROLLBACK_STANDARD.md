# MEOS Rollback Standard

**Date:** 2026-08-18T11:50:00Z  
**Production live rollback:** **BLOCKED** (P313 G27) — nothing is deployed to a production cluster.

## What exists

| Mechanism | Path | Scope | Status |
|-----------|------|-------|--------|
| Postgres restore drill | `scripts/meos-postgres-restore-drill.sh` | Workstation / isolated DB | **TESTED** historically (P313 G08) |
| Offsite restore drill | `scripts/meos-offsite-restore-drill.sh` | MinIO listing + restore | **TESTED** historically (P313 G09) |
| Backup | `scripts/meos-postgres-backup.sh` | Dump + WAL tar | **TESTED** historically (P313 G07) |
| Plugin version rollback API | Plugin Platform | Tenant install version | **NOT_IMPLEMENTED** |
| Automatic traffic rollback | Canary controller | Production | **NOT_IMPLEMENTED** |
| Compose stack recreate | docker compose | LOCAL / meos-prod profile | Workstation only — **not** production |

## Rules

1. Do not auto-rollback financial or clinical data paths if that could worsen integrity — restore from backup with an explicit operator decision.  
2. Every rollback must record actor, release id, reason, time, environment, result. Production audit of rollback: **NOT_AVAILABLE** (no production deploy).  
3. Forward recovery (restore drill) **is not** evidence of rolling back a live production release.  
4. Dirty working tree **cannot** be the unique source of a rolled-back production artifact.

## Artifact identity (P353)

| Slot | Identity | Status |
|------|----------|--------|
| CURRENT_ARTIFACT | `MEOS_IMAGE` / Helm `image.repository@image.digest` | **NOT_AVAILABLE** until GHCR digest exists |
| PREVIOUS_ARTIFACT | `MEOS_PREVIOUS_IMAGE` (previous digest) | **NOT_AVAILABLE** |
| ROLLBACK_TESTED | Production rollback of a live release | **FALSE** |
| LOCAL_ROLLBACK_TEST | Workstation compose recreate / restore drill | Record separately; **not** G27 |

Rollback must reference an immutable digest (`repository@sha256:…`). Tags `:latest` and `:7.0.0` are **not** rollback identity.

Do not claim **ROLLBACK_TESTED** unless a production rollback was actually executed.

## Manual rollback (when production exists)

Authorized operators: restore from a named backup, redeploy the previous **immutable SHA**, verify health + a real business smoke (not HTTP 200 alone), then record the change per [MEOS_CHANGE_MANAGEMENT.md](./MEOS_CHANGE_MANAGEMENT.md).

Until G26 is cleared, this procedure is **documentary**.
