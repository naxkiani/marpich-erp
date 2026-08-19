# MEOS Customer Deployment Guide

Enterprise product install for operators. **No internal credentials.** The same application image is used for every package. Compose and localhost are **not** production.

## README

Marpich Enterprise Operating System (MEOS) is one product with multiple deployment adapters:

| Package | Typical use |
|---------|-------------|
| MEOS DEMO | Evaluation on a workstation |
| MEOS SINGLE-TENANT | One organization, local or VPS |
| MEOS VPS | Ubuntu VM + Docker Compose |
| MEOS CLOUD | AWS / Azure / GCP (credentials required) |
| MEOS KUBERNETES | Existing Helm chart |

Installer (plan only until you apply a non-production target):

```bash
python3 scripts/meos-install.py --platform LOCAL
python3 scripts/meos-install.py --platform DEMO
python3 scripts/meos-install.py --platform VPS
```

`--apply` is allowed only for LOCAL/DEMO. Production apply is blocked until G26 + P313 + human GO-LIVE.

## INSTALLATION

1. Copy this repository (or a release commit — never `47258dfd-dirty`).
2. Install Docker Engine + Compose v2 (VPS/DEMO) **or** Helm 3 (Kubernetes).
3. Copy `infrastructure/launch/env.production.example` to a gitignored env file. Replace every `CHANGE_ME`.
4. DEMO: `./deploy/scripts/meos-demo.sh start`
5. LOCAL: `./scripts/dev-up.sh` then run the backend (`uvicorn` as documented by that script).
6. VPS: `scripts/meos-vps-bootstrap.sh` after SSH access exists.
7. Kubernetes: `helm upgrade --install marpich-iam infrastructure/kubernetes/helm/marpich-iam` with `image.digest` from CI. Do not use `:latest` as release identity.

## SYSTEM REQUIREMENTS

- Ubuntu 22.04+ (VPS) or a Kubernetes cluster 1.27+
- 4 vCPU / 8 GiB RAM minimum for DEMO; size production from capacity evidence (not invented here)
- PostgreSQL 16 (Compose image or managed)
- Redis 7
- Outbound HTTPS for image pull (GHCR) when using the registry
- A public hostname + public CA for any production TLS claim

Hostinger **shared hosting is incompatible**. Use a Hostinger **VPS**.

## ENVIRONMENT VARIABLES

Canonical contract: `deploy/environments/CONTRACT.v1.yaml`. Examples (placeholders only): `deploy/environments/ENV_*.env.example`.

Required categories: `APP_ENV`, `DATABASE_URL`, `DATABASE_SSL`, `REDIS_URL`, `SECRET_PROVIDER`, `STORAGE_PROVIDER`, `PUBLIC_BASE_URL`, `TLS_MODE`, `EMAIL_PROVIDER`, `OBSERVABILITY_PROVIDER`, `BACKUP_PROVIDER`, `REGISTRY`, `IMAGE`, `IMAGE_DIGEST`.

Never commit real secrets. `CONFIGURED` is not `VERIFIED`. `VERIFIED` is not `PRODUCTION_VERIFIED`.

## DATABASE SETUP

Compose DEMO/LOCAL create PostgreSQL automatically. For VPS/cloud, provision PostgreSQL, do not publish port 5432 to the public internet, set `DATABASE_SSL=require` for production claims. Apply migrations with `scripts/run-migrations.sh` / `scripts/meos-migration-check.sh` (check does not apply).

## DOMAIN SETUP

Set `PUBLIC_BASE_URL` to the public hostname. Localhost and RFC-1918 addresses are not production domains.

## TLS SETUP

DEMO: HTTP on `127.0.0.1:8080` (no public CA).  
VPS: Caddy example `infrastructure/docker/compose/Caddyfile.vps.example`.  
Kubernetes: Ingress + cert-manager (chart templates).  
Production TLS is **not** verified until G26 evidence exists.

## BACKUP

```bash
./deploy/scripts/meos-demo.sh backup
# or
PGPORT=5433 ./scripts/meos-postgres-backup.sh
```

Local dumps are **LOCAL_NON_PRODUCTION**. Production requires offsite backup evidence.

## RESTORE

```bash
./deploy/scripts/meos-demo.sh restore
# or
./scripts/meos-postgres-restore-drill.sh
```

Restore drill defaults to a separate database (`marpich_platform_restore`). Do not restore over production without an authorized change.

## UPGRADE

1. Record current `MEOS_IMAGE` / `image.digest`.
2. Pull the new immutable digest (never `:latest` as identity).
3. Run migration check, then apply with authorization.
4. Roll forward Compose or `helm upgrade`.

## ROLLBACK

- Compose: set `MEOS_PREVIOUS_IMAGE` and recreate the backend service.
- Helm: `helm rollback marpich-iam 0 --namespace marpich`

## TROUBLESHOOTING

| Symptom | Check |
|---------|--------|
| API not up | `docker compose -p meosprod ps` or `./deploy/scripts/meos-demo.sh health` |
| Process up, app not ready | `/api/v1/health` vs `/api/v1/ready` |
| Migration mismatch | `./scripts/meos-migration-check.sh` |
| Image pull denied | GHCR credentials (READY_FOR_CREDENTIALS) |
| Shared Hostinger | Incompatible — use VPS |

## HEALTH CHECK

- Process: `GET /api/v1/health`
- Application: `GET /api/v1/ready`
- Kubernetes: liveness `/api/v1/live`, readiness `/api/v1/ready`
- Production: `python3 scripts/meos-ext-g26-readiness.py` (currently **G26_READY = FALSE**)

## ADMIN ACCESS

Create the first admin through the Identity module after the API is ready. Do not use demo passwords in production. Onboarding planner: `python3 scripts/meos-onboard.py` (PLAN_ONLY).

## SECURITY CHECKLIST

- [ ] Secrets only in gitignored env or a secret manager
- [ ] PostgreSQL not published publicly
- [ ] JWT and signing secrets are unique per environment
- [ ] TLS public CA for any internet hostname
- [ ] Tenant isolation tests pass (`crm` tenant B cannot list tenant A)
- [ ] Backup and restore drill recorded
- [ ] Image identified by digest, not `:latest`
- [ ] Production GO-LIVE not assumed from a demo start

Production certification and GO-LIVE remain **not approved**.
