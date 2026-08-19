# MEOS EXT-G26 — Infrastructure Implementation Plan (P349)

**Date:** 2026-08-19  
**Status:** PLAN ONLY. P349 **must not** provision, deploy, create DNS/TLS/secrets/databases, enable traffic, or start P313.  
**Reuse:** existing Helm `marpich-iam`, Flux HelmRelease, CI `identity-federation-enterprise.yml`, GHCR. **No second deployment, CI, or workflow system.**  
**Machine:** [MEOS_P349_INFRASTRUCTURE_DISCOVERY.v1.yaml](./MEOS_P349_INFRASTRUCTURE_DISCOVERY.v1.yaml)  
**Validator after real infra:** `python3 scripts/meos-ext-g26-readiness.py` — do **not** set `G26_READY=TRUE` manually.  
**OWNER** for every phase: **NOT_AVAILABLE**  
**PROVIDER_SELECTION:** BLOCKED until Phase 01 account exists.  
**Recommended class (not selected):** MANAGED_KUBERNETES_PLUS_MANAGED_POSTGRESQL  

Re-entry after this plan is executed in the real world:

```
REAL INFRASTRUCTURE PROVISIONED
        ↓
G26 VALIDATOR
        ↓
G26_READY = TRUE
        ↓
EXPLICIT P313 RE-ENTRY
        ↓
P313 RECERTIFICATION
        ↓
P0 = 0 ONLY IF CERTIFIED
        ↓
GO_LIVE_READY
        ↓
SEPARATE HUMAN APPROVAL
        ↓
GO-LIVE
```

---

## PHASE 01 — Provider / Hosting

| Field | Content |
|-------|---------|
| OBJECTIVE | Obtain an authorized production hosting account compatible with Kubernetes + managed PostgreSQL |
| PREREQUISITES | Human authorization to spend/operate; P349 complete |
| ACTION | Select a provider **class** (recommended: managed K8s + managed PG). Do not invent pricing. Record account **existence** only — never print keys |
| EVIDENCE | Account identifier (non-secret); provider class named |
| VALIDATION | Account can create cluster + database APIs |
| ROLLBACK | Close unused trial accounts; do not leave orphan credentials |
| OWNER | NOT_AVAILABLE |

---

## PHASE 02 — Cluster / Runtime

| Field | Content |
|-------|---------|
| OBJECTIVE | Kubernetes-compatible production cluster for Helm/Flux |
| PREREQUISITES | Phase 01 account |
| ACTION | Create cluster; install Ingress-NGINX; enable NetworkPolicy CNI; create namespace `marpich`; issue kubeconfig to operators and GitHub Environments. **Do not** treat kind/k3d/compose as this cluster |
| EVIDENCE | kubeconfig file present; `kubectl get nodes` Ready |
| VALIDATION | G26-01 path: `KUBECONFIG` or `~/.kube/config` |
| ROLLBACK | Destroy cluster only with authorization; revoke kubeconfigs |
| OWNER | NOT_AVAILABLE |

---

## PHASE 03 — Managed PostgreSQL

| Field | Content |
|-------|---------|
| OBJECTIVE | Production PostgreSQL satisfying G26-02 |
| PREREQUISITES | Phase 02 private network |
| ACTION | Provision managed PostgreSQL 16-compatible; private endpoint; SSL; database `marpich_platform`; **not** published as localhost/:5433/:5444. Store DSN in secret manager only |
| EVIDENCE | Host/port class ≠ LOCAL; automated backup enabled by provider |
| VALIDATION | Validator PGHOST/PGPORT not local/5433/5444; app `PERSISTENCE_BACKEND=postgres`; reject default `marpich:marpich` |
| ROLLBACK | Provider snapshot restore; do not fall back to compose `:5444` as production |
| OWNER | NOT_AVAILABLE |

---

## PHASE 04 — Secrets

| Field | Content |
|-------|---------|
| OBJECTIVE | Production secret manager filling Helm-expected Secrets |
| PREREQUISITES | Phase 02 cluster |
| ACTION | Enable cloud SM or Vault; External Secrets or equivalent to create `{fullname}-secrets` and `marpich-db-credentials` (`database-url`). Helm currently **does not** template these. Do **not** commit values. Rotate per platform Secrets law |
| EVIDENCE | Secret **names** exist; `MEOS_SECRET_MANAGER_AVAILABLE` only after the backend is real |
| VALIDATION | G26-04; pods can start without git-hosted `.env` |
| ROLLBACK | Revoke leases; rotate; do not print old values |
| OWNER | NOT_AVAILABLE |

---

## PHASE 05 — DNS / TLS

| Field | Content |
|-------|---------|
| OBJECTIVE | Public DNS + public-CA TLS for G26-03/G26-07 |
| PREREQUISITES | Ingress ADDRESS from Phase 02 |
| ACTION | Point a public hostname at ingress. Helm DESIGNED host is `auth.marpich.io`; live hostname remains **NOT_DEFINED** until a record exists. Install cert-manager; ClusterIssuer `letsencrypt-prod`; issue `marpich-iam-prod-tls`. Enforce HTTPS redirect (already in Helm annotations) |
| EVIDENCE | Public resolution; certificate chain from a public CA |
| VALIDATION | `MEOS_PRODUCTION_DNS` non-local; `MEOS_PUBLIC_CA_TLS=1` only after issuance |
| ROLLBACK | Remove DNS; cert-manager deletes Certificate as configured |
| OWNER | NOT_AVAILABLE |

---

## PHASE 06 — CI/CD

| Field | Content |
|-------|---------|
| OBJECTIVE | Existing workflow deploys an immutable image |
| PREREQUISITES | Clean git (Phase 07 prerequisite overlapping); GHCR; kube credentials in GitHub `staging`/`production` Environments |
| ACTION | **Do not create a new pipeline.** Configure secrets for `.github/workflows/identity-federation-enterprise.yml`. Prefer recording image **digest** from `docker/build-push-action` (today the workflow tags `sha-${{ github.sha }}` and mutable `7.0.0` but does not export digest). Deploy with `--set image.tag=sha-<clean-sha>` as already written |
| EVIDENCE | Workflow run ID; `MEOS_IMAGE_DIGEST`; GHCR package |
| VALIDATION | G26-05 empty tree + G26-06 digest + credentials |
| ROLLBACK | Re-run previous SHA workflow; Helm rollback in production job already on failure |
| OWNER | NOT_AVAILABLE |

---

## PHASE 07 — Deployment

| Field | Content |
|-------|---------|
| OBJECTIVE | First production Helm (or Flux) release of a **clean** SHA |
| PREREQUISITES | Phases 02–06; **CLEAN** working tree; **FORBIDDEN** to deploy `47258dfd-dirty` |
| ACTION | `helm upgrade --install marpich-iam … -f values-production.yaml --set image.tag=sha-<clean>` **or** apply existing Flux HelmRelease. Do not activate applications. Do not enable production traffic beyond what Ingress necessarily exposes — GO-LIVE remains **NOT APPROVED** |
| EVIDENCE | Helm revision; pod image ID; deployed commit annotation if added later |
| VALIDATION | G26-08/G26-09: `DEPLOYED_COMMIT = CLEAN_COMMIT`; `DEPLOYED_IMAGE_DIGEST = CI_ARTIFACT_DIGEST` |
| ROLLBACK | `helm rollback marpich-iam 0 --namespace marpich` |
| OWNER | NOT_AVAILABLE |

**Explicit non-production:** local `/health`, Compose `meosprod`, development, test, demo.

---

## PHASE 08 — Observability

| Field | Content |
|-------|---------|
| OBJECTIVE | Production logs, metrics, health, alerting (G23 remains FAIL until verified) |
| PREREQUISITES | Phase 07 runtime |
| ACTION | Scrape ServiceMonitors; enable Alertmanager (currently commented in `prometheus.yml`); OTLP endpoint for `OTEL_ENABLED`. Do **not** mark G23 PASS in this document |
| EVIDENCE | Production dashboards/alerts firing in a test |
| VALIDATION | CONFIGURED vs PRODUCTION_VERIFIED — only the latter can later change G23 |
| ROLLBACK | Keep scrape configs; disable noisy routes |
| OWNER | NOT_AVAILABLE |

---

## PHASE 09 — Backup

| Field | Content |
|-------|---------|
| OBJECTIVE | Production PostgreSQL backup (not workstation `scripts/meos-postgres-backup.sh` against `:5433`) |
| PREREQUISITES | Phase 03 |
| ACTION | Enable managed backup + encryption + retention **as provided by the database service**. Retention/RPO/RTO remain **NOT_VERIFIED** until measured |
| EVIDENCE | Backup job ID / snapshot ID |
| VALIDATION | Artifact is of the production instance |
| ROLLBACK | N/A for backup enablement; keep last good snapshot |
| OWNER | NOT_AVAILABLE |

---

## PHASE 10 — Rollback

| Field | Content |
|-------|---------|
| OBJECTIVE | Exercise Helm rollback on production (G26-10) |
| PREREQUISITES | At least two Helm revisions on production |
| ACTION | Deploy N+1 then `helm rollback marpich-iam 0 --namespace marpich`; verify probes. Flux `rollback.cleanupOnFail` remains secondary |
| EVIDENCE | Helm history; health after rollback |
| VALIDATION | CONFIGURED ≠ TESTED ≠ PRODUCTION_VERIFIED. Set `MEOS_ROLLBACK_EXERCISED=1` only after the real exercise |
| ROLLBACK | Roll forward to last good digest if rollback itself fails |
| OWNER | NOT_AVAILABLE |

---

## PHASE 11 — G26 Validation

| Field | Content |
|-------|---------|
| OBJECTIVE | Run the real validator against real evidence |
| PREREQUISITES | Phases 01–10 evidence; clean SHA deployed |
| ACTION | `python3 scripts/meos-ext-g26-readiness.py` with **no** env manipulation to force PASS |
| EVIDENCE | Validator JSON: `g26_ready` true only if G26-01…10 all PASS |
| VALIDATION | Exit 0 only when ready. Expected **now** (P349): `G26_READY = FALSE` |
| ROLLBACK | If FAIL/BLOCKED, return to the failing phase; **do not** start P313 |
| OWNER | NOT_AVAILABLE |

P313 starts **only** by explicit re-entry after `G26_READY = TRUE`. P349 does not change P0, P313, PRODUCTION_CERTIFIED, or GO_LIVE_AUTHORIZATION.

---

## Clean-release sequence (blocks Phase 06–07)

See compatibility doc. Summary: do not reset; do not auto-commit; ignore or stop tracking `__pycache__`; commit only authorized files; empty `git status --short`; then CI.

## Stop conditions (still in force)

- Fake kubeconfig / fake TLS / fake Postgres / fake secrets  
- Dirty SHA deploy  
- Second CI or Helm system  
- Automatic P313 or GO-LIVE  
