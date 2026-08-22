# MEOS P354 — Release Candidate Engineering

**Date:** 2026-08-19  
**Governance:** Architecture Governance Standard 11.0  
**Command:** `python3 scripts/meos-release-candidate-readiness.py`  
**Reused (not bypassed):** `meos-launch-readiness.py` · `meos-release-readiness.py` · `meos-ext-g26-readiness.py`

P354 turns the existing MEOS codebase into a **reproducible release-candidate factory**. It does **not** GO-LIVE.

**RELEASE_CANDIDATE ≠ PRODUCTION_CERTIFIED.**  
**RELEASE_READY ≠ PRODUCTION_READY.**

## Release identity (actual)

| Field | Value |
|-------|--------|
| VERSION | `0.1.0` (`backend/pyproject.toml`) — Helm `appVersion` `7.0.0` is a documented VERSIONING_GAP |
| RELEASE_ID | `MEOS-0.1.0-dd967051` |
| COMMIT_SHA | `dd967051ab05c6ff57262502b456ad51b7d748fd` |
| git describe | `dd967051-dirty` |
| WORKTREE_STATUS | **DIRTY** |
| RELEASE_SOURCE | **NOT_ELIGIBLE** |
| RELEASE_CANDIDATE | **FALSE** |
| BUILD_ID | `NOT_AVAILABLE` (no CI run id) |
| image | `meos/backend:p353-local` |
| image_id | `sha256:bf5aad6542774a7788dadcdc1c37ce7785eb007cb5b32c45184a70933b3c2ae5` (BUILD_VALIDATION) |
| image_digest | **NOT_AVAILABLE** |
| REGISTRY_ARTIFACT | READY_FOR_CREDENTIALS |

Forbidden identity `47258dfd-dirty` remains forbidden. The current dirty identity is `dd967051-dirty` and is also **not** a release candidate.

## Changes in this phase

- Release-candidate validator that **rejects dirty trees**, `:latest`, missing version, missing commit, and missing migration identity.
- Nested `MEOS_RELEASE_MANIFEST.v1.yaml` contract (`release` / `application` / `validation` / `targets` / `certification`) without dropping P353 top-level keys.
- Declared-dependency SBOM (`DECLARED_DEPENDENCIES_ONLY`). Syft/CycloneDX were **not** on PATH.
- Migration inventory manifest (55 SQL files, latest prefix `055`). Apply **NOT_EXECUTED** against production.
- Honesty tests for dirty rejection, mutable tags, missing digest, G26/P0 protection, local vs production.

No second application, CI, Kubernetes, database, workflow, or governance system was created.

## Clean-source gate

`git status` is dirty. Files are classified **INTENTIONAL** or **REQUIRED** (P353 launch fabric + this P354 factory). None are TEMPORARY or OBSOLETE.

**Safe procedure (do not execute destructively):**

1. Do **not** `git reset --hard`.
2. Do **not** `git clean -fd`.
3. Commit classified INTENTIONAL/REQUIRED files after operator review.
4. Re-run `python3 scripts/meos-release-candidate-readiness.py`.
5. Only then `RELEASE_SOURCE = ELIGIBLE`.

Until that commit exists, `meos-release.py build` stays **BLOCKED** (`DIRTY_RELEASE`).

## Tests

Inspected and executed where available. Failures are not hidden.

| Suite | Result |
|-------|--------|
| P354/P353 honesty + health/live/ready contracts | **PASS** (22 tests) |
| CRM tenant isolation (`test_crm_tenant_b_cannot_list_tenant_a_contacts`) | **PASS** (Tenant B cannot list/GET Tenant A contacts) |
| Secret scan `scripts/meos-secret-scan.py` | **PASS** (hits=0) |
| Migration inventory `scripts/meos-migration-check.sh` | **PASS** COUNT=55 APPLY=NOT_EXECUTED |
| Local backup `:5433` | **PASS** 741468 bytes — **LOCAL_EVIDENCE**, not PRODUCTION_BACKUP |
| Restore → `marpich_platform_p354_restore` | **PASS** — production restore **NOT_VERIFIED** |
| Demo compose `/live` `/health` `/ready` on `:8080` | **PASS** — LOCAL_EVIDENCE, not production |
| Integration / full suite | NOT_AVAILABLE as a single green gate in this phase |
| Frontend build | NOT_AVAILABLE |
| Workflow / documents / audit isolation | NOT_APPLICABLE as dedicated RC modules (existing platform tests remain) |
| Docker rebuild of current dirty SHA | **BLOCKED** (DIRTY_RELEASE) |
| Docker prior local image inspect | PASS (`p353-local`) |

## Health / readiness contract

| Endpoint | Class |
|----------|--------|
| `GET /live` and `GET /api/v1/live` | PROCESS ALIVE |
| `GET /api/v1/health` | APPLICATION PROCESS ok (not DB) |
| `GET /api/v1/ready` | DATABASE READY (`SELECT 1` when Postgres) |
| `python3 scripts/meos-ext-g26-readiness.py` | PRODUCTION VERIFIED (independent; currently FAIL) |

Localhost `/health` on `:8080` is **LOCAL_EVIDENCE**. It is not production evidence.

Helm probes (static): liveness `/api/v1/live`, readiness `/api/v1/ready`. `helm`/`kubectl` were **not** on PATH → `STATIC_VALIDATION_LIMITED`.

## Database / backup / restore

| Item | Result |
|------|--------|
| Current migration | `055` |
| Production database | **NOT_VERIFIED** |
| Backup | PASS — **LOCAL_EVIDENCE** (not PRODUCTION_BACKUP) |
| Restore | PASS — **LOCAL_NON_PRODUCTION** (`docs/meos/execution/.last_p352_restore.json`) |
| Rollback | CONFIGURED (`MEOS_IMAGE=$MEOS_PREVIOUS_IMAGE` / `helm rollback`) — **not** production-tested |

`:5433` / `:5444` remain NON_PRODUCTION.

## Security

| Check | Result |
|-------|--------|
| Secret scan (path) | executed via `meos-secret-scan.py` |
| Dockerfile | `USER app`, `STOPSIGNAL SIGTERM`, bind `0.0.0.0:8000` |
| `:latest` as release identity | rejected |
| TLS | template only; public CA **not** invented |
| JWT/session/CORS/RBAC | existing Identity/AuthZ; not weakened |
| Trivy / pip-audit / Syft | **NOT_AVAILABLE** on PATH |
| SBOM | DECLARED_DEPENDENCIES_ONLY — **not** a security certification |

## Tenant isolation

Existing CRM test: Tenant B cannot list or GET Tenant A contacts. Other modules were **not** invented for this gate.

## Cross-platform packages (static)

| Target | PACKAGE | CONFIG | SECRETS | DEPLOYMENT | RUNTIME | PRODUCTION |
|--------|---------|--------|---------|------------|---------|------------|
| VPS | READY | READY | READY_FOR_CREDENTIALS | NOT_VERIFIED | NOT_VERIFIED | NOT_VERIFIED |
| HOSTINGER_VPS | READY | READY | READY_FOR_CREDENTIALS | NOT_VERIFIED | NOT_VERIFIED | NOT_VERIFIED |
| AWS | READY | READY | READY_FOR_CREDENTIALS | NOT_VERIFIED | NOT_VERIFIED | NOT_VERIFIED |
| AZURE | READY | READY | READY_FOR_CREDENTIALS | NOT_VERIFIED | NOT_VERIFIED | NOT_VERIFIED |
| GCP | READY | READY | READY_FOR_CREDENTIALS | NOT_VERIFIED | NOT_VERIFIED | NOT_VERIFIED |
| KUBERNETES | READY | READY | READY_FOR_CREDENTIALS | NOT_VERIFIED | NOT_VERIFIED | NOT_VERIFIED |

Hostinger **shared hosting** remains INCOMPATIBLE. No package is PRODUCTION_READY.

Architecture remains: **one release + target config + target secrets = deployment**.

## Known limitations

- Dirty worktree → `RELEASE_CANDIDATE = FALSE`.
- No GHCR push → digest `NOT_AVAILABLE`. Local Docker Id is not a registry digest.
- Helm/kubectl/Syft/Trivy not installed → static/limited validation.
- Cloud credentials missing → provider deploy `READY_FOR_CREDENTIALS` (does not block local engineering).
- VERSIONING_GAP (0.1.0 vs Helm 7.0.0) unchanged — version not invented.
- G26 remains BLOCKED. P313 remains NOT_CERTIFIED.

## External dependencies

GHCR credentials · public CA TLS · secret manager · offsite backup · production cluster (EXT-G26). Missing credentials do **not** block source validation, local image evidence, tests, SBOM, or package validation.

## Certification (unchanged)

| Field | Value |
|-------|--------|
| G26 | BLOCKED |
| G26_READY | FALSE |
| P0 | 1 |
| P313 | NOT_CERTIFIED |
| P313_REENTRY_READY | FALSE |
| PRODUCTION_CERTIFIED | FALSE |
| GO_LIVE_READY | FALSE |
| GO_LIVE_AUTHORIZATION | NOT_APPROVED |
| ACTIVE_APPLICATIONS | 0 |
| PRODUCTION_TRAFFIC | NOT_ENABLED |

P354 does not start P313 and does not create P355 because credentials are missing.

## Rollback

See `infrastructure/launch/MEOS_RELEASE_PACKAGE/ROLLBACK.md` and `MEOS_RELEASE_OPERATIONS.md`. Previous registry artifact: **NOT_AVAILABLE**. Rollback is configured, not production-tested.

## Package

Existing `infrastructure/launch/MEOS_RELEASE_PACKAGE/` (no second `release/` tree): manifest, checksums, declared SBOM, deployment pointers, rollback notes. No passwords, tokens, kubeconfig, or private keys.
