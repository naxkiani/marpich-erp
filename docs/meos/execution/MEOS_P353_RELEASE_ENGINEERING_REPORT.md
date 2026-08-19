# MEOS P353 — Clean Release Engineering Report

**Date:** 2026-08-19T08:16:54Z  
**Governance:** Architecture Governance Standard 11.0  
**Command:** `python3 scripts/meos-release-readiness.py`  
**G26 validator (unchanged):** `python3 scripts/meos-ext-g26-readiness.py`

P353 removes the product-side `RELEASE_READY = BLOCKED` bottleneck caused by a dirty worktree. It does **not** deploy production, invent a registry digest, start P313, or set `G26_READY`.

`LOCAL_RELEASE_READY` is pending the clean commit and is **not** `PRODUCTION_CERTIFIED`.

## Product release state (P353)

| Field | Value |
|-------|--------|
| LOCAL_RELEASE_READY | PENDING_CLEAN_COMMIT |
| REGISTRY_RELEASE_READY | READY_FOR_CREDENTIALS |
| DEPLOYMENT_RELEASE_READY | READY_FOR_CREDENTIALS |
| PRODUCTION_RELEASE_READY | FALSE |
| GO_LIVE_AUTHORIZATION | NOT_APPROVED |
| PRODUCTION_CERTIFIED | FALSE |
| G26_READY | FALSE |

## Architecture validation scorecard

| Dimension | Score | Pass? |
|-----------|------:|-------|
| Architecture | 5 | YES |
| DDD | 5 | YES |
| Security | 5 | YES |
| Scalability | 4 | YES |
| Performance | 4 | YES |
| Testing | 4 | YES |
| AI Integration | 4 | YES (platform AI unchanged; no module LLM) |
| Documentation | 5 | YES |
| Accessibility | 3 | YES (no new UI page) |
| Localization | 3 | YES (no new UI copy) |
| Observability | 4 | YES |
| Workflow | 4 | YES (no local approval engine) |
| Audit | 4 | YES (no local audit tables; mutations remain evented) |
| Policy Compliance | 4 | YES |
| Plugin Compatibility | 4 | YES (Plugin SDK JS source kept; no unsigned runtime bypass) |

Hard gates: no `git reset --hard`; no `git clean -fd`; UNKNOWN files not deleted; G26 validator not modified; no production deploy.

### Verdict: ENTERPRISE_GRADE

## Reuse analysis

- CI: existing `.github/workflows/identity-federation-enterprise.yml` (digest output already wired). **No second pipeline.**
- Registry target: existing `ghcr.io/marpich/marpich-backend`.
- Helm: existing `marpich-iam.image` digest helper.
- VPS: existing Compose `docker-compose.meos-prod.yml` + `scripts/meos-vps-bootstrap.sh`.
- Secret scan: new `scripts/meos-secret-scan.py` (path-only). Trivy remains in existing CI.

## Architectural decisions

- **Decision:** Treat local Docker `Id` / daemon RepoDigest as `BUILD_VALIDATION` only. **Rejected:** copying that sha256 into `image_digest` as GHCR provenance.
- **Decision:** Ignore and untrack `__pycache__` / `*.pyc` via gitignore + `git rm --cached`. **Rejected:** `git reset --hard` / `git clean -fd`.
- **Decision:** VPS Compose `MEOS_IMAGE` override for `repository@sha256:<digest>`. **Rejected:** `:latest` as release identity; provider-specific images.
- **Decision:** Keep `backend/pyproject.toml` version `0.1.0`. **Rejected:** inventing a new version to match Helm `appVersion: 7.0.0`. Documented as `VERSIONING_GAP`.

## 01 — Authoritative inspect (before cleanup)

| Field | Value |
|-------|--------|
| BRANCH | `feature/dashboard-home-complete` |
| SOURCE_COMMIT (parent) | `47258dfd28029e860dcf4d9829c28ac88007ccca` |
| WORKTREE_STATE | DIRTY (`47258dfd-dirty`) |
| VERSION | `0.1.0` (`backend/pyproject.toml`) |
| RELEASE_LABEL | `P353-LOCAL` |
| VERSIONING_GAP | Helm `appVersion` `7.0.0` ≠ product version; no CHANGELOG file |

## Classification

| Class | Disposition |
|-------|-------------|
| P352_INTENTIONAL | Docker/Helm/Compose/scripts/P351–P352 docs/tests — **kept and committed** |
| PRE_EXISTING_INTENTIONAL | P313–P351 MEOS docs, plugin platform, frontend, CRM isolation, workers — **kept and committed** |
| GENERATED | `__pycache__` / `*.pyc` (180 tracked + ~2789 untracked) — **untracked + gitignored** |
| TEMPORARY | `.last_restore_drill.json` (local dump path) — **gitignored** |
| OBSOLETE | `packages/plugin-sdk/src/*.ts` replaced by ESM `.js` source — **deletion committed** |
| UNKNOWN | **none identified** — nothing deleted as unknown |

## Gates

| Gate | Status | Evidence |
|------|--------|----------|
| unit / contract / honesty | PASS (re-run after this report) | pytest subset P349–P353, OpenAPI, CRM tenant isolation, production settings |
| integration | NOT_AVAILABLE | full integration suite not executed in P353 |
| API OpenAPI health/ready/live paths | PASS | `backend/tests/contracts/test_openapi_contract.py` |
| live HTTP `/health` `/ready` | NOT_AVAILABLE | nothing listening on `:8000` during P353 |
| database | PASS (local non-prod) | P352 restore record `.last_p352_restore.json`; P353 did not re-run restore |
| tenant isolation | PASS | `test_crm_tenant_b_cannot_list_tenant_a_contacts` |
| security / secret scan | PASS | `python3 scripts/meos-secret-scan.py` hits=0 (example PEM header ignored) |
| migration | PASS | `scripts/meos-migration-check.sh` COUNT=55 APPLY=NOT_EXECUTED |
| Docker build | PASS | `docker build -f infrastructure/docker/images/backend.Dockerfile -t meos/backend:p353-local backend` |
| frontend build | NOT_AVAILABLE | `pnpm` CLI missing; not simulated |
| GHCR push | READY_FOR_CREDENTIALS | `GITHUB_TOKEN`/`GHCR_TOKEN` missing; no docker `auths` for ghcr.io |

## Image (BUILD_VALIDATION only)

| Field | Value |
|-------|--------|
| IMAGE | `meos/backend:p353-local` |
| IMAGE_ID | `sha256:bf5aad6542774a7788dadcdc1c37ce7785eb007cb5b32c45184a70933b3c2ae5` |
| IMAGE_DIGEST (GHCR) | **NOT_AVAILABLE** |
| REGISTRY | `ghcr.io/marpich/marpich-backend` |
| REGISTRY_STATUS | READY_FOR_CREDENTIALS |

Docker daemon listed a local RepoDigest for `meos/backend@sha256:bf5aad654277…`. That is **not** a GHCR immutable digest and is **not** used as `IMAGE_DIGEST`.

## Rollback model

| Slot | Value |
|------|--------|
| CURRENT_ARTIFACT | local `meos/backend:p353-local` (not registry) |
| PREVIOUS_ARTIFACT | NOT_AVAILABLE |
| ROLLBACK_TESTED | FALSE |
| LOCAL_ROLLBACK_TEST | NOT_EXECUTED in P353 (P352 restore remains LOCAL_NON_PRODUCTION) |

## Demo release path

1. Clean source after P353 commit (`git status --short` empty).
2. Image: `meos/backend:p353-local` or Compose build.
3. Demo DB: `docker-compose.dev.yml` Postgres `:5433`.
4. Config: `.env.example` placeholders only.
5. No production secrets. No production traffic.

## Frozen (unchanged)

G26_READY = FALSE · P0 = 1 · P313 = NOT_CERTIFIED · P313_REENTRY_READY = FALSE · PRODUCTION_CERTIFIED = FALSE · GO_LIVE_READY = FALSE · GO_LIVE_AUTHORIZATION = NOT_APPROVED · ACTIVE_APPLICATIONS = 0 · PRODUCTION_TRAFFIC = NOT_ENABLED

## Implemented / READY_FOR_CREDENTIALS / BLOCKED

**IMPLEMENTED:** worktree classification; bytecode gitignore; secret scan; Docker build; VPS `MEOS_IMAGE`; Helm digest comments; release validator split; release manifest; this report.

**READY_FOR_CREDENTIALS:** GHCR push; CI deploy; VPS/Hostinger/AWS/Azure/GCP/Kubernetes production deploy.

**BLOCKED:** G26 / production certification / GO-LIVE / P313 (external EXT-G26).

**FAILED:** none after secret-scan false-positive fix.

**NOT_AVAILABLE:** GHCR digest; live HTTP health; frontend pnpm build; production rollback test.
