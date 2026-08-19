# MEOS P354 — Universal Installation

**Date:** 2026-08-19  
**Status:** `DEPLOYMENT_MECHANISM_READY` — **not** `PRODUCTION_CERTIFIED`  
**G26_READY:** FALSE · **P0:** 1 · **P313:** NOT_CERTIFIED · **GO_LIVE_AUTHORIZATION:** NOT_APPROVED

P354 turns P353 packages into one operator path. It reuses Docker, Compose, Helm, Flux, existing CI, GHCR, migrations, backup/restore, and runbooks. It does **not** create a second CI, Kubernetes controller, or cloud fabricator.

## Operator path

```
1. python3 scripts/meos-release.py inspect
2. python3 scripts/meos-install.py --platform LOCAL          # PLAN_ONLY
3. python3 scripts/meos-install-readiness.py LOCAL
4. Select platform (DEMO | LOCAL | VPS | HOSTINGER_VPS | AWS | AZURE | GCP | KUBERNETES)
5. Configure from infrastructure/launch/env.production.example (gitignored copy)
6. python3 scripts/meos-release.py verify
7. Deploy only with --execute --apply on LOCAL/DEMO, or credentials on other targets
8. Migration: scripts/meos-migration-check.sh then scripts/run-migrations.sh (explicit)
9. Verify PROCESS_HEALTH /api/v1/health ≠ APPLICATION_READINESS /api/v1/ready
   ≠ PRODUCTION_READINESS (G26 validator)
10. Backup via existing scripts (local backup ≠ production backup)
11. Record release in MEOS_RELEASE / MEOS_RELEASE_PACKAGE
12. Certification remains P313 after G26 — not started here
```

## Commands

```bash
python3 scripts/meos-release.py inspect|build|test|package|verify
python3 scripts/meos-release.py publish --confirm-publish   # refuses without credentials; never silent
python3 scripts/meos-install.py --platform VPS              # default PLAN_ONLY
python3 scripts/meos-install.py --platform LOCAL --execute --apply   # LOCAL/DEMO only
python3 scripts/meos-install-readiness.py KUBERNETES
```

`--production` or `MARPICH_ENVIRONMENT=production` does **not** make a laptop PRODUCTION.

## Hostinger VPS (not shared hosting)

SSH → Docker Engine → `MEOS_IMAGE=ghcr.io/marpich/marpich-backend@sha256:<digest>` → Compose meosprod → Postgres not published publicly → Caddyfile.vps.example + public DNS/CA → existing backup scripts. Shared hosting: **INCOMPATIBLE**. Missing SSH/Docker: **READY_FOR_CREDENTIALS**.

## Frozen

G26_READY = FALSE · PRODUCTION_CERTIFIED = FALSE · GO_LIVE_READY = FALSE · ACTIVE_APPLICATIONS = 0 · PRODUCTION_TRAFFIC = NOT_ENABLED

See [MEOS_RELEASE_OPERATIONS.md](./MEOS_RELEASE_OPERATIONS.md) · [MEOS_INSTALLATION_MATRIX.v1.yaml](./MEOS_INSTALLATION_MATRIX.v1.yaml) · [MEOS_P353_RELEASE_ENGINEERING_REPORT.md](./MEOS_P353_RELEASE_ENGINEERING_REPORT.md) · [MEOS_P354_LAUNCH_CONTROL_REPORT.md](./MEOS_P354_LAUNCH_CONTROL_REPORT.md)

Unified launch CLI (orchestration only; same mechanisms):

```bash
python3 scripts/meos-launch.py list
python3 scripts/meos-launch.py preflight --env local
python3 scripts/meos-launch.py plan --env demo
python3 scripts/meos-launch.py deploy --env demo --confirm yes
```
