# MEOS Deployment Factory

**Phase:** P353 multi-platform productization  
**Law:** one MEOS product, one container image, one configuration contract, multiple environment adapters.  
**Not production:** localhost, Compose, dirty SHA, and `READY_FOR_CREDENTIALS` are not production.  
**GO_LIVE_AUTHORIZATION = NOT_APPROVED.** G26_READY = FALSE. P0 = 1. P313 = NOT_CERTIFIED.

Canonical index: [`deploy/README.md`](../../../deploy/README.md).

## Canonical artifacts (do not fork)

| Concern | Path |
|---------|------|
| Image | `infrastructure/docker/images/backend.Dockerfile` |
| LOCAL Compose | `infrastructure/docker/compose/docker-compose.dev.yml` |
| DEMO Compose | `infrastructure/docker/compose/docker-compose.meos-prod.yml` (`COMPOSE_IS_PRODUCTION = FALSE`) |
| VPS | `scripts/meos-vps-bootstrap.sh` + `Caddyfile.vps.example` |
| Kubernetes | `infrastructure/kubernetes/helm/marpich-iam` |
| GitOps (optional) | `infrastructure/fluxcd/marpich-iam-helmrelease.yaml` |
| CI | `.github/workflows/identity-federation-enterprise.yml` |
| Installer | `python3 scripts/meos-install.py` (PLAN_ONLY) |
| Backup / restore | `scripts/meos-postgres-backup.sh` · `scripts/meos-postgres-restore-drill.sh` |
| Contract | `deploy/environments/CONTRACT.v1.yaml` |
| Profiles | `deploy/environments/ENV_*.env.example` · `profiles.v1.yaml` |

`deploy/` is an **index of adapters**. It does not contain a second backend, frontend, database, CI, or Kubernetes controller.

## One-command DEMO (NON_PRODUCTION)

```bash
./deploy/scripts/meos-demo.sh start
./deploy/scripts/meos-demo.sh health
./deploy/scripts/meos-demo.sh backup
./deploy/scripts/meos-demo.sh restore
./deploy/scripts/meos-demo.sh stop
./deploy/scripts/meos-demo.sh reset   # destroys meosprod volumes
```

Process health: `/api/v1/health`. Application readiness: `/api/v1/ready`. Production readiness: `python3 scripts/meos-ext-g26-readiness.py` (independent; currently FALSE).

## Cloud adapters (one path each)

| Provider | Chosen path | Kubernetes path |
|----------|-------------|-----------------|
| AWS | EC2 + Compose | EKS uses Helm package |
| Azure | Linux VM + Compose | AKS uses Helm package |
| GCP | Compute Engine + Compose | GKE uses Helm package |

Missing credentials → **READY_FOR_CREDENTIALS**. Packages still exist. No provision in this phase.

Hostinger **shared hosting = INCOMPATIBLE**. Hostinger **VPS** = generic VPS package.

## CI matrix

Documented in `deploy/ci/DEPLOYMENT_MATRIX.v1.yaml`. Production job requires `workflow_dispatch` + GitHub `production` environment. The pipeline does **not** auto-deploy production. G26, P313, and human GO-LIVE remain gates.

## Launch checklist factory (reuse this list)

| # | Stage | DEMO | STAGING | PRODUCTION |
|---|--------|------|---------|------------|
| 1 | BUILD | local image | CI image | CI image + digest |
| 2 | TEST | pytest | pytest + helm lint | pytest + G26 |
| 3 | SECURITY | secret scan | secret scan | secret manager VERIFIED |
| 4 | DATABASE | :5444 | managed Postgres | managed Postgres PRODUCTION_VERIFIED |
| 5 | BACKUP | local script | target backup | offsite VERIFIED |
| 6 | RESTORE | local drill | target drill | production drill |
| 7 | TLS | none/HTTP | public CA | public CA VERIFIED |
| 8 | SECRETS | env file | secret manager | PRODUCTION_VERIFIED |
| 9 | DEPLOY | compose | helm/compose | G26 + authorization |
| 10 | HEALTH | `/health` | `/health` | production `/health` |
| 11 | READINESS | `/ready` | `/ready` | production `/ready` |
| 12 | OBSERVABILITY | CONFIGURED | OTLP | PRODUCTION_VERIFIED |
| 13 | ROLLBACK | compose down | previous digest | helm rollback |
| 14 | TENANT ISOLATION | CRM unit test | same | production evidence |
| 15 | BUSINESS SMOKE | wave scripts | staging smoke | production smoke |
| 16 | CERTIFICATION | N/A | N/A | P313 + GO-LIVE |

DEMO launch ≠ STAGING launch ≠ PRODUCTION launch.

## Clean-release chain (do not `git reset --hard`)

`CLEAN TREE → COMMIT → TEST → BUILD → IMAGE → DIGEST → DEPLOYMENT`

Classify uncommitted files (SOURCE / GENERATED / TEMPORARY / DOCUMENTATION / TEST / BUILD_ARTIFACT / OBSOLETE). `47258dfd-dirty` remains **FORBIDDEN_FOR_RELEASE**. A dirty worktree is not a release identity.

## SaaS / hosted (preparation only)

Not activated. Tenant and domain models remain Identity + Organization. Storage/database isolation stay per-tenant `tenant_id` in owning schemas. Billing integration point is the existing license contract (`payment_execution: READY_FOR_CREDENTIALS`). Email/notifications/audit stay platform services. No production tenants, no SaaS billing enablement.

## Product packages (same application)

MEOS DEMO · MEOS SINGLE-TENANT · MEOS VPS · MEOS CLOUD · MEOS KUBERNETES — see `deploy/packages/` and `infrastructure/launch/commercial/`. No forks.

## Validator

```bash
python3 scripts/meos-platform-readiness.py
python3 scripts/meos-ext-g26-readiness.py
```
