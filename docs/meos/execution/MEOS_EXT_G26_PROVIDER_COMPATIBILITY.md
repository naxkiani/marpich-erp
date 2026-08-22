# MEOS EXT-G26 — Provider Compatibility Matrix (P349)

**Date:** 2026-08-19  
**Phase:** P349 discovery. **Not** provisioning. **Not** G26 PASS.  
**Machine:** [MEOS_P349_INFRASTRUCTURE_DISCOVERY.v1.yaml](./MEOS_P349_INFRASTRUCTURE_DISCOVERY.v1.yaml)  
**Validator:** `python3 scripts/meos-ext-g26-readiness.py` (do not set `G26_READY`).  
**OWNER:** NOT_AVAILABLE  

**P349_STATUS:** REQUIREMENTS_IDENTIFIED  
**EXT-G26:** UNRESOLVED · **G26:** BLOCKED · **G26_READY:** FALSE · **P0:** 1  
**CURRENT_PROVIDER:** NOT_AVAILABLE  
**PROVIDER_SELECTION:** BLOCKED  
**COST:** NOT_AVAILABLE (EXTERNAL_RESEARCH_REQUIRED)  

This matrix evaluates infrastructure against the **existing** MEOS deployment architecture. It does not create a second cluster, CI, or workflow engine.

## Authoritative deployment path (repository evidence)

Verified files, not memory:

| Layer | Path | Status |
|-------|------|--------|
| CI | `.github/workflows/identity-federation-enterprise.yml` | DESIGNED |
| Also CI | `.github/workflows/digital-twin-enterprise.yml` (same GHCR + Helm rollback) | DESIGNED |
| Registry | `ghcr.io/marpich/marpich-backend` | DESIGNED (`:7.0.0` mutable + `:sha-${{ github.sha }}`) |
| Image | `infrastructure/docker/images/backend.Dockerfile` | DESIGNED |
| Helm | `infrastructure/kubernetes/helm/marpich-iam/` Chart 1.1.0 / app 7.0.0 | DESIGNED |
| Flux | `infrastructure/fluxcd/marpich-iam-helmrelease.yaml` | DESIGNED (not live) |
| Compose | `infrastructure/docker/compose/docker-compose.meos-prod.yml` | **NON_PRODUCTION** (self-signed TLS, Postgres `:5444`) |
| Demo Postgres | `docker-compose.dev.yml` host `:5433` | **NON_PRODUCTION** |
| Terraform | `infrastructure/terraform/environments/development/main.tf` | **STUB** (modules commented) |
| Ansible | — | **MISSING** |

**Exact path found:**

```
CLEAN SHA
  → GitHub Actions (identity-federation-enterprise.yml)
  → GHCR ghcr.io/marpich/marpich-backend (:sha-<commit>)
  → Helm upgrade --install marpich-iam  (CI imperative)
     and/or Flux HelmRelease marpich-iam (GitOps)
  → Kubernetes namespace marpich
```

Both Helm-from-CI and Flux are **DESIGNED**. Neither has a live production cluster. Do **not** add a third path. Operational SoR after a cluster exists: keep CI for **build + digest**; use existing Helm **or** Flux for **apply**. Do not invent ArgoCD as a new platform (runbook mentions ArgoCD as an optional rollback UI; **no Argo manifests** exist in this repository).

**Chart scope:** `marpich-iam` deploys the **backend image** with IAM/federation ingress paths. It is the existing production chart. It is **not** a separately sized full-MEOS cluster profile. Full-platform sizing = **NOT_MEASURED**.

## Provider-neutral requirements

| Need | Neutral requirement |
|------|---------------------|
| Compute | Kubernetes-compatible production runtime with Helm 3 and kubectl |
| Database | Production PostgreSQL (not localhost / `:5433` / `:5444`), SSL, automated backup |
| Network | Public ingress + private database connectivity |
| DNS | Public hostname under operator-owned zone |
| TLS | Public CA (cert-manager `letsencrypt-prod` is the Helm expectation) |
| Secrets | Production secret store that can materialize Kubernetes Secrets (no values in git) |
| Registry | Immutable image identity (digest preferred; `:sha-<commit>` is the existing tag contract) |
| CI | Authenticated deploy to the cluster using the **existing** workflow |
| Rollback | Versioned Helm release rollback (`helm rollback marpich-iam 0 --namespace marpich`) |
| Observability | Production logs + metrics + alerts (G23 currently FAIL) |
| Backup / restore | Production PostgreSQL backup/restore, not workstation MinIO |

## Provider class evaluation (no vendor lock)

Pricing is **not** in the repository. **PRICE = NOT_AVAILABLE.** Do not invent numbers.

| Class | Compatibility with existing Helm/Flux/GHCR | Complexity | Security / ops | Database | TLS | Secrets | CI | Rollback | Observability | Recommendation |
|-------|--------------------------------------------|------------|----------------|----------|-----|---------|----|----------|---------------|----------------|
| **Managed Kubernetes** (EKS/GKE/AKS-class) | High — kubectl/Helm/Flux native | Lower ops than self-build | Cloud IAM + private subnets possible | Pair with **managed PostgreSQL** | cert-manager + public DNS | Cloud secret manager + External Secrets **or** CSI | GitHub Environments kubeconfig | Helm history native | Cloud + in-cluster Prometheus DESIGNED | **RECOMMENDED_PROVIDER_CLASS** |
| **Cloud Kubernetes** (same as managed; named separately in mandate) | High | Same | Same | Same | Same | Same | Same | Same | Same | Treat as alias of managed K8s |
| **VPS + K3s** | Compatible if Helm/Flux/nginx/cert-manager installed | Higher ops (OS, etcd, upgrades) | Operator-owned hardening | Need separate managed PG or carefully isolated PG **not** on the API node as SoR | cert-manager still required | Vault or cloud SM still required | Same CI if kubeconfig in GitHub | Helm still works | Self-operate Prometheus/Grafana | **ALTERNATIVE** if budget/control requires it |
| **Bare-metal Kubernetes** | Compatible | Highest | Highest operator burden | External PG still required for G26-02 | Same | Same | Same | Same | Same | **ALTERNATIVE** only with dedicated platform ops |
| Compose / local k3d / kind treated as G26 | **Forbidden** by validator | Low | Not production | `:5433`/`:5444` NON_PRODUCTION | Self-signed invalid | `.env` files invalid | N/A | N/A | Local scrape ≠ G23 | **REJECTED** |

**Why recommended class = managed Kubernetes + managed PostgreSQL:** the existing artifacts assume Ingress-NGINX, cert-manager ClusterIssuer `letsencrypt-prod`, Kubernetes Secrets, Helm, optional Flux, and `postgresql.enabled: false` with an **external** database. A managed control plane plus managed PostgreSQL matches that contract with the least new architecture.

**Why not selected now:** no authorized hosting account, no kubeconfig, no production DNS ownership evidence, no secret-manager availability flag. **PROVIDER_SELECTION = BLOCKED** until those exist.

**Risks (all classes):** Helm Secret `{release}-secrets` is **referenced but not templated**; ExternalSecrets flags are **values-only** (no CRD templates). Flux GitRepository URL `https://github.com/marpich/marpich-erp.git` is DESIGNED; remote match to this clone is **NOT_VERIFIED**. CI tags mutable `:7.0.0` — G26 identity must use `sha-` **and** digest.

## Category matrix (01–16)

For each row: **REQUIRED** · **EXISTING MEOS EXPECTATION** · **PROVIDER CAPABILITY REQUIRED** · **CURRENT EVIDENCE** · **GAP** · **BLOCKER** · **VALIDATION METHOD**.

### 01 COMPUTE / CLUSTER

| Field | Value |
|-------|--------|
| REQUIRED | Authorized production Kubernetes-compatible cluster |
| EXISTING MEOS EXPECTATION | Namespace `marpich`; Helm release `marpich-iam`; optional Flux; kubeconfig for CI `azure/setup-kubectl` |
| PROVIDER CAPABILITY REQUIRED | Managed or self-hosted K8s with Helm 3, RBAC, workload identity optional |
| CURRENT EVIDENCE | G26-01 **BLOCKED**. `KUBECONFIG` missing; `~/.kube/config` absent |
| GAP | No cluster |
| BLOCKER | Authorized production hosting account + cluster |
| VALIDATION | `test -n "$KUBECONFIG" -o -f "$HOME/.kube/config"` then `kubectl get ns marpich` |

### 02 DATABASE

| Field | Value |
|-------|--------|
| REQUIRED | Real production / managed PostgreSQL |
| EXISTING MEOS EXPECTATION | `postgresql.enabled: false`; `externalDatabase.host: postgres.marpich.svc.cluster.local`; secret `marpich-db-credentials` / `database-url`; `PERSISTENCE_BACKEND=postgres`; production settings reject `marpich:marpich` and memory |
| PROVIDER CAPABILITY REQUIRED | PostgreSQL 16-compatible (compose evidence uses `postgres:16-alpine`), private network, SSL, automated backup |
| CURRENT EVIDENCE | G26-02 **BLOCKED**. Workstation `:5433` / compose `:5444` / localhost = **NON_PRODUCTION** |
| GAP | No non-local production DSN |
| BLOCKER | Managed PostgreSQL host that is not localhost/:5433/:5444 |
| VALIDATION | `MEOS_PRODUCTION_PGHOST` / `PGHOST` not in {localhost,127.0.0.1}; port not 5433/5444; SSL evidenced |

### 03 NETWORK

| Field | Value |
|-------|--------|
| REQUIRED | Public ingress + private database path |
| EXISTING MEOS EXPECTATION | Ingress class `nginx`; ClusterIP service port 8000; `networkPolicy.enabled: true` |
| PROVIDER CAPABILITY REQUIRED | Load balancer or equivalent for Ingress-NGINX; private DB endpoint |
| CURRENT EVIDENCE | G26-07 **NOT_AVAILABLE**. No production DNS/ingress observed |
| GAP | No cluster, no LB, no DNS |
| BLOCKER | Production network + ingress controller |
| VALIDATION | Non-localhost `MEOS_PRODUCTION_DNS`; ingress ADDRESS assigned |

### 04 DNS

| Field | Value |
|-------|--------|
| REQUIRED | Public DNS for the production hostname |
| EXISTING MEOS EXPECTATION | Helm production host **`auth.marpich.io`** (DESIGNED). Dev host `auth.dev.marpich.io`. |
| PROVIDER CAPABILITY REQUIRED | Authoritative DNS for the zone that will serve the hostname |
| CURRENT EVIDENCE | Live **PRODUCTION_HOSTNAME = NOT_DEFINED**. Designed name is not DNS evidence. Zone ownership **NOT_VERIFIED** |
| GAP | No public record, no zone proof |
| BLOCKER | DNS zone + record to ingress |
| VALIDATION | Public A/AAAA or CNAME not pointing at localhost |

### 05 TLS

| Field | Value |
|-------|--------|
| REQUIRED | Public-CA TLS; HTTPS redirect |
| EXISTING MEOS EXPECTATION | `cert-manager.io/cluster-issuer: letsencrypt-prod`; `ssl-redirect: true`; prod TLS secret `marpich-iam-prod-tls` |
| PROVIDER CAPABILITY REQUIRED | Public HTTP-01 or DNS-01 to a public CA; cert-manager on cluster |
| CURRENT EVIDENCE | G26-03 **BLOCKED**. Compose self-signed is **not** production |
| GAP | No public hostname, no issued cert |
| BLOCKER | Public DNS + public CA certificate |
| VALIDATION | `MEOS_PUBLIC_CA_TLS=1` **only after** a real public-CA cert exists (do not set to force PASS) |

### 06 SECRET MANAGEMENT

| Field | Value |
|-------|--------|
| REQUIRED | Real production secret manager |
| EXISTING MEOS EXPECTATION | Helm `secrets.vault.enabled: true`, `externalSecrets.enabled: true` (**values only** — **no** ExternalSecret/Vault templates). Pods `envFrom.secretRef` name `{fullname}-secrets`. DB `existingSecret: marpich-db-credentials`. Platform Secrets BC is an API catalog, not a live cloud vault. |
| PROVIDER CAPABILITY REQUIRED | Cloud SM / Vault / equivalent that can create those Kubernetes Secrets without committing values |
| CURRENT EVIDENCE | G26-04 **BLOCKED**. `MEOS_SECRET_MANAGER_AVAILABLE` unset. Interface **DESIGNED**. Live store **NOT_CONFIGURED** |
| GAP | No production secret backend; Helm Secret object not in chart |
| BLOCKER | Secret manager + injection into `{fullname}-secrets` and `marpich-db-credentials` |
| VALIDATION | Availability flag only (`MEOS_SECRET_MANAGER_AVAILABLE=1`). **Never print values.** |

### 07 CONTAINER REGISTRY

| Field | Value |
|-------|--------|
| REQUIRED | Immutable container images |
| EXISTING MEOS EXPECTATION | GHCR `ghcr.io/marpich/marpich-backend`; CI `packages: write` + `GITHUB_TOKEN` |
| PROVIDER CAPABILITY REQUIRED | GHCR (existing) or equivalent OCI registry with digest |
| CURRENT EVIDENCE | Workflow DESIGNED. Production digest **NOT_AVAILABLE**. Mutable `:7.0.0` **insufficient** for G26-09 |
| GAP | No CI digest artifact / `MEOS_IMAGE_DIGEST` |
| BLOCKER | Successful CI build of a **clean** SHA emitting digest |
| VALIDATION | Image digest equals deployed digest |

### 08 CI/CD

| Field | Value |
|-------|--------|
| REQUIRED | Authenticated deploy of immutable digest via **existing** workflow |
| EXISTING MEOS EXPECTATION | test → Trivy → SBOM → build-push → `helm upgrade` staging → optional production canary; GitHub `environment: staging` / `production` |
| PROVIDER CAPABILITY REQUIRED | GitHub Environment secrets: kubeconfig (or OIDC to cloud). **Do not create a new pipeline.** |
| CURRENT EVIDENCE | G26-06 **BLOCKED**. Workflow DESIGNED; deploy credentials not evidenced |
| GAP | No kube credentials in CI; digest not exported |
| BLOCKER | CI deploy credentials + clean SHA + cluster |
| VALIDATION | Existing workflow run + `MEOS_IMAGE_DIGEST` + Helm release |

### 09 OBSERVABILITY

| Field | Value |
|-------|--------|
| REQUIRED | Production logs, metrics, health, alerting |
| EXISTING MEOS EXPECTATION | Helm `serviceMonitor.enabled: true`; `OTEL_ENABLED=true`; `infrastructure/observability/prometheus/prometheus.yml`; Alertmanager commented as optional |
| PROVIDER CAPABILITY REQUIRED | Metrics + log store + alert routing on the production cluster |
| CURRENT EVIDENCE | **CONFIGURED** in repo. G23 **FAIL**. **Not PRODUCTION_VERIFIED** |
| GAP | No production scrape, no on-call, no alert fire test |
| BLOCKER | Production telemetry (does not upgrade G23 in this phase) |
| VALIDATION | Production alert test after runtime exists. P349 must **not** set G23 PASS |

### 10 BACKUP

| Field | Value |
|-------|--------|
| REQUIRED | Production database backup (encrypted, retained) |
| EXISTING MEOS EXPECTATION | `scripts/meos-postgres-backup.sh` defaults `PGHOST=127.0.0.1` `PGPORT=5433`; workstation MinIO offsite drill is **not** production |
| PROVIDER CAPABILITY REQUIRED | Managed PG automated backups or WAL+object store **of the production instance** |
| CURRENT EVIDENCE | Workstation backup **NON_PRODUCTION**. Production backup **NOT_VERIFIED** |
| GAP | No production backup job against managed PG |
| BLOCKER | Production backup configuration |
| VALIDATION | Backup artifact of the production database (not `:5433`) |

### 11 RESTORE

| Field | Value |
|-------|--------|
| REQUIRED | Proven restore of production backups |
| EXISTING MEOS EXPECTATION | `scripts/meos-postgres-restore-drill.sh`; P313 workstation restore is **not** G26 |
| PROVIDER CAPABILITY REQUIRED | Restore into an isolated production-class instance |
| CURRENT EVIDENCE | Workstation restore only. Production restore **NOT_VERIFIED**. RTO/RPO production **NOT_VERIFIED** |
| GAP | No production restore evidence |
| BLOCKER | Restore drill on production backup |
| VALIDATION | Restore report against production backup ID |

### 12 ROLLBACK

| Field | Value |
|-------|--------|
| REQUIRED | Real production Helm rollback evidence |
| EXISTING MEOS EXPECTATION | CI `helm rollback marpich-iam 0 --namespace marpich` on production job failure; Flux `rollback.cleanupOnFail: true`; runbook `docs/operations/runbooks/digital-twin-rollback.md` |
| PROVIDER CAPABILITY REQUIRED | Helm history retained on the cluster |
| CURRENT EVIDENCE | G26-10 **BLOCKED**. **CONFIGURED**, not **TESTED**, not **PRODUCTION_VERIFIED** |
| GAP | No N→N+1→N on production |
| BLOCKER | First production release then exercised rollback |
| VALIDATION | `MEOS_ROLLBACK_EXERCISED=1` only after a real rollback (do not set to force PASS) |

### 13 SECURITY

| Field | Value |
|-------|--------|
| REQUIRED | AuthN/Z, TLS, RBAC, network policy, image immutability, CI auth, audit |
| EXISTING MEOS EXPECTATION | JWT + permissions; Helm `runAsNonRoot`, drop ALL caps, readOnlyRootFilesystem; `networkPolicy.enabled`; Trivy in CI; Audit platform via events |
| PROVIDER CAPABILITY REQUIRED | Private nodes/subnets; no public DB; image pull from GHCR |
| CURRENT EVIDENCE | Code/CI **CONFIGURED**. Production controls **NOT_VERIFIED** |
| GAP | No production cluster to attach policies to |
| BLOCKER | Cluster + TLS + secrets + non-local DB |
| VALIDATION | G26 gates + existing security pytest (workstation tests ≠ production) |

### 14 IDENTITY

| Field | Value |
|-------|--------|
| REQUIRED | Deployed commit = clean SHA; deployed digest = CI digest |
| EXISTING MEOS EXPECTATION | `--set image.tag=sha-${{ github.sha }}`; probes `/api/v1/health` |
| PROVIDER CAPABILITY REQUIRED | Ability to read deployed image ID/digest from the cluster |
| CURRENT EVIDENCE | G26-08 **BLOCKED**, G26-09 **NOT_AVAILABLE**. Local `/health` = **NOT PRODUCTION** |
| GAP | Nothing deployed |
| BLOCKER | Production runtime + clean SHA |
| VALIDATION | `MEOS_DEPLOYED_COMMIT` + `MEOS_DEPLOYED_DIGEST` match HEAD and CI |

### 15 STORAGE

| Field | Value |
|-------|--------|
| REQUIRED | Persistent storage for PostgreSQL (managed) and optional redis/kafka if in-cluster |
| EXISTING MEOS EXPECTATION | Chart disables in-cluster Bitnami postgresql/redis. External Redis `redis.marpich.svc.cluster.local`. Kafka `kafka.marpich.svc.cluster.local:9092` |
| PROVIDER CAPABILITY REQUIRED | Managed disk for data services **or** managed Redis/Kafka. Sizes **NOT_MEASURED** |
| CURRENT EVIDENCE | No production volumes. Redis/Kafka **NOT_AVAILABLE** |
| GAP | External Redis/Kafka not provisioned; sizes unknown |
| BLOCKER | Data-plane storage for PG (required). Redis/Kafka required by Helm env flags (`KAFKA_ENABLED=true`) unless explicitly disabled in a future authorized values change — **do not change architecture in P349** |
| VALIDATION | PG storage healthy; Redis/Kafka reachability if still enabled |

### 16 DISASTER RECOVERY

| Field | Value |
|-------|--------|
| REQUIRED | Production DR distinct from workstation Wave 04 |
| EXISTING MEOS EXPECTATION | WAL archive in compose; offsite MinIO drill on workstation |
| PROVIDER CAPABILITY REQUIRED | Multi-AZ or snapshot restore of managed PG. RTO/RPO **NOT_VERIFIED** (do not invent SLA) |
| CURRENT EVIDENCE | Workstation DR ≠ production DR |
| GAP | No production DR plan executed |
| BLOCKER | Production backup + restore |
| VALIDATION | Production restore drill after G26-02 exists |

## Minimum production profile (evidence only)

Derived **only** from `values-production.yaml` + default `resources` / `twinWorkers` (DESIGNED, not load-tested).

| Resource | Designed minimum (IAM chart) | Status |
|----------|------------------------------|--------|
| API replicas | 6 | DESIGNED |
| Twin worker replicas | 6 | DESIGNED |
| API request | 500m CPU / 512Mi each | DESIGNED |
| Twin request | 250m CPU / 256Mi each | DESIGNED |
| **Cluster request floor (IAM+twin min)** | **4500m CPU / 4608Mi memory** | DESIGNED, **NOT_MEASURED** load |
| API limit (per pod) | 2000m / 2Gi | DESIGNED |
| HPA max API | 100 | DESIGNED (not a minimum) |
| HPA max twin | 200 | DESIGNED (not a minimum) |
| Database CPU/RAM/disk | — | **NOT_MEASURED** |
| Backup storage | — | **NOT_MEASURED** |
| Ingress / LB | nginx + public IP | DESIGNED, not provisioned |
| TLS | letsencrypt-prod | DESIGNED |
| Secrets | Vault + ExternalSecrets flags | DESIGNED / NOT_CONFIGURED |
| Registry | GHCR | DESIGNED |
| Observability | ServiceMonitor + OTEL | CONFIGURED, G23 FAIL |
| SLA / RPS | Helm `authLatencyTargetMs: 150` is a **target**, not a measured capacity | **NOT_MEASURED** |

Full MEOS (all modules, Kafka, Redis, observability stack) **NOT_MEASURED**. Do not treat the IAM chart floor as a certified capacity plan.

## Security control verification (production)

| Control | Repo expectation | Production status |
|---------|------------------|-------------------|
| Zero Trust | Helm `zeroTrustEnabled: true` | CONFIGURED, not PRODUCTION_VERIFIED |
| TLS | cert-manager public CA | BLOCKED |
| Secret management | Vault/ES flags + K8s Secret | NOT_CONFIGURED |
| IAM | GitHub + cluster RBAC + app JWT | Cluster IAM NOT_AVAILABLE |
| RBAC | Helm ServiceAccount create | CONFIGURED in chart |
| Network segmentation | `networkPolicy.enabled: true` | CONFIGURED in chart |
| Database security | External PG + RLS env `MARPICH_RLS_ENABLED=true` | NON_PRODUCTION DSN |
| Container security | non-root, drop ALL, Trivy CI | CONFIGURED |
| Image immutability | `sha-` tag; digest GAP | BLOCKED |
| CI authentication | `GITHUB_TOKEN` + Environments | DESIGNED |
| Audit | Platform audit via events | Not production-verified |
| Logging | OTEL / Prometheus | CONFIGURED, not production |
| Backup protection | Production backup encryption | NOT_VERIFIED |

No production credentials, secret values, or private keys are recorded in this document.

## Clean release (G26-05)

`git status --short` is **not** empty. `GIT_DESCRIBE = 47258dfd-dirty`. **FORBIDDEN_DIRTY = TRUE**.

Observed composition (counts; nothing deleted by P349):

| Class | Count |
|-------|--------|
| Untracked `??` | 909 |
| Modified `M` | 73 |
| Deleted `D` | 2 |
| `__pycache__` among dirty | 730 |
| Untracked under `docs/` | 139 |
| Paths touching `scripts/` | 11 |

`.gitignore` does **not** currently ignore `__pycache__` / `*.pyc`.

**CLEAN_RELEASE_BLOCKERS**

1. Untracked `__pycache__` / `.pyc` (generated).  
2. Uncommitted MEOS docs and implementation files (user work — **do not delete**).  
3. Modified tracked files (including `.gitignore`).  
4. No authorized commit.  
5. Mutable image tag `:7.0.0` must not be the G26 identity even after a clean SHA.

**SAFE_CLEAN_RELEASE_SEQUENCE** (do not execute without authorization)

1. Do **not** `git reset` / force-clean.  
2. Do **not** commit unless the user explicitly authorizes.  
3. Optionally add `__pycache__/` and `*.pyc` to `.gitignore` (hygiene) — only if authorized.  
4. User selects which docs/code are in-scope; leave the rest uncommitted or stash with consent.  
5. `git status --short` empty.  
6. `git describe --always --dirty` has **no** `-dirty`.  
7. Existing CI builds that SHA; record **digest** (workflow today does not export digest).  
8. Only that SHA is eligible for G26-05/09.

Until then `47258dfd-dirty` remains **FORBIDDEN**.

## Production runtime contract (G26-08)

Required evidence when a runtime exists (none of this is present now):

| Field | Required |
|-------|----------|
| PRODUCTION_IDENTITY | Not LOCAL / COMPOSE / DEVELOPMENT / TEST / DEMO |
| DEPLOYED_COMMIT | Clean SHA |
| DEPLOYED_IMAGE | `ghcr.io/marpich/marpich-backend` |
| IMAGE_DIGEST | CI artifact digest (not `latest`, not `:7.0.0` alone) |
| DATABASE | Non-local managed PostgreSQL |
| HEALTH / READINESS | Production ingress URL (not `127.0.0.1:8000`) |
| ENVIRONMENT | `MARPICH_ENVIRONMENT=production` |
| INGRESS | `auth.marpich.io` **or** another operator-declared hostname after DNS exists |
| LOGGING | Production log pipeline |

**LOCAL /health = NOT PRODUCTION. COMPOSE = NOT PRODUCTION.**

## Rollback distinction (G26-10)

| State | Helm/Flux/CI rollback |
|-------|------------------------|
| CONFIGURED | YES |
| TESTED | NO |
| PRODUCTION_VERIFIED | NO |

Do **not** claim G26-10 PASS.

## Cost

**COST = NOT_AVAILABLE.** Repository contains no current price list. **EXTERNAL_RESEARCH_REQUIRED** before any budget number.

## Decision

```
PROVIDER_SELECTION          = BLOCKED
CURRENT_PROVIDER            = NOT_AVAILABLE
RECOMMENDED_PROVIDER_CLASS  = MANAGED_KUBERNETES_PLUS_MANAGED_POSTGRESQL
ALTERNATIVE_PROVIDER_CLASSES = VPS_PLUS_K3S_PLUS_MANAGED_OR_EXTERNAL_POSTGRESQL
                               BARE_METAL_KUBERNETES
WHY                         = Matches existing Helm/Flux/GHCR/cert-manager contract
COMPATIBILITY               = HIGH for recommended class
RISKS                       = No account; Helm secrets not templated; Flux URL unverified
OPERATIONAL_COMPLEXITY      = LOWEST for managed K8s+PG; HIGHER for K3s/bare metal
```
