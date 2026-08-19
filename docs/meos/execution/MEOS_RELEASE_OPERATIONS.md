# MEOS Release Operations (P354)

Reuse P353 identity rules. Dirty SHA `47258dfd-dirty` remains **FORBIDDEN**. Local image id is **not** a GHCR digest.

## MEOS_RELEASE

Immutable fields: `release_version`, `source_commit`, `build_id`, `image`, `image_digest`, `schema_version`, `config_version`, `created_at`, `artifacts`, `supported_platforms`, `verification_status`.

Inspect: `python3 scripts/meos-release.py inspect`

## Build / test / package / verify / publish

| Command | Behavior |
|---------|----------|
| `meos-release build` | Existing `backend.Dockerfile` → `meos/backend:p354-local` (BUILD_VALIDATION) |
| `meos-release test` | Existing pytest subset + secret scan + migration-check |
| `meos-release package` | `infrastructure/launch/MEOS_RELEASE_PACKAGE/` checksums, no secrets |
| `meos-release verify` | Rejects dirty tree and `:latest`-only identity |
| `meos-release publish --confirm-publish` | Requires GHCR credentials; never silent; no invented digest |

## Installer

Default **PLAN_ONLY**. `--apply` is LOCAL/DEMO only. Production apply is **FORBIDDEN** until EXT-G26.

Health classes (not interchangeable):

| Class | Probe |
|-------|--------|
| PROCESS_HEALTH | `/api/v1/health` |
| APPLICATION_READINESS | `/api/v1/ready` |
| PRODUCTION_READINESS | `python3 scripts/meos-ext-g26-readiness.py` |

## Kubernetes (existing Helm + Flux)

```bash
helm lint infrastructure/kubernetes/helm/marpich-iam
helm upgrade --install marpich-iam infrastructure/kubernetes/helm/marpich-iam --set-string image.digest=<ci-digest>
helm rollback marpich-iam 0 --namespace marpich
```

Flux overlay example: `infrastructure/fluxcd/marpich-iam-digest.values.example.yaml`. No second controller.

## Migration

1. Preflight: `scripts/meos-migration-check.sh`  
2. Backup: `scripts/meos-postgres-backup.sh`  
3. Apply: `scripts/run-migrations.sh` only with explicit operator intent  
4. Destructive: **BLOCKED** (`--authorize-destructive` remains blocked)

## Rollback

`CURRENT_ARTIFACT` / `PREVIOUS_ARTIFACT` (`MEOS_IMAGE` / `MEOS_PREVIOUS_IMAGE` or Helm revision). `ROLLBACK_TESTED=FALSE` until exercised.

P351/P353 runbooks remain canonical for adapters: [MEOS_LAUNCH_PROFILES.md](./MEOS_LAUNCH_PROFILES.md) · [MEOS_RELEASE_ENGINEERING_RUNBOOK.md](./MEOS_RELEASE_ENGINEERING_RUNBOOK.md)
