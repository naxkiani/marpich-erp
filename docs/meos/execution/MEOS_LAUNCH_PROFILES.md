# MEOS Launch Profiles (P351)

All profiles run the **same** application/domain. Only adapters change. None is GO-LIVE.

## PROFILE_LOCAL — CONFIGURED

- **Requirements:** Docker (Postgres) or existing `:5433`; Python 3.12 venv  
- **Config:** `backend/.env.example` (`MARPICH_ENVIRONMENT=development`)  
- **Deploy:** `./scripts/dev-up.sh` then `cd backend && uvicorn core.presentation.api.main:app --reload --port 8000`  
- **Verify:** `pg_isready -h 127.0.0.1 -p 5433`; `curl -fsS http://127.0.0.1:8000/api/v1/health`  
- **Rollback:** stop uvicorn; `docker compose -f infrastructure/docker/compose/docker-compose.dev.yml down` (does not delete unless `-v`)  
- **External:** none  
- **Class:** LOCAL ≠ PRODUCTION  

## PROFILE_DOCKER — IMPLEMENTED

- **Requirements:** Docker Engine + Compose v2  
- **Config:** gitignored env from `infrastructure/launch/env.production.example` or `scripts/meos-prod-env-init.sh`  
- **Deploy:** `docker compose -p meosprod --env-file infrastructure/docker/compose/.env.meos-prod -f infrastructure/docker/compose/docker-compose.meos-prod.yml up -d`  
- **Verify:** Postgres `:5444`; API `:8080`; Caddy `:8443` self-signed  
- **Rollback:** `MEOS_IMAGE=$MEOS_PREVIOUS_IMAGE` then `compose up -d`; not `:latest` as certification  
- **Class:** DEMO / workstation ≠ PRODUCTION  

## PROFILE_VPS / PROFILE_HOSTINGER_VPS — READY_FOR_CREDENTIALS

- **Requirements:** Linux VPS, Docker, ports 80/443, **do not publish Postgres publicly**  
- **Config:** `env.production.example`; `Caddyfile.vps.example`  
- **Deploy:** `./scripts/meos-vps-bootstrap.sh` then Compose on the VPS  
- **TLS:** public hostname + Caddy/Let’s Encrypt; localhost certs DEVELOPMENT ONLY  
- **Backup:** `scripts/meos-postgres-backup.sh` on that instance  
- **Upgrade / rollback:** Compose image digest pin  
- **Hostinger shared:** INCOMPATIBLE  

## PROFILE_AWS / AZURE / GCP — READY_FOR_CREDENTIALS

Do not provision. Credentials remain NOT_AVAILABLE until supplied.

| Need | AWS | Azure | GCP |
|------|-----|-------|-----|
| Compute | EKS or EC2 Docker | AKS or VM | GKE or GCE |
| Database | RDS PostgreSQL | Azure Database for PostgreSQL | Cloud SQL |
| Secrets | Secrets Manager | Key Vault | Secret Manager |
| DNS/TLS | Route53 + ACM or cert-manager | Front Door/AppGW or cert-manager | Cloud DNS + cert-manager |
| Registry | GHCR (existing) or ECR | GHCR or ACR | GHCR or Artifact Registry |
| Observability | OTEL → vendor or in-cluster Prometheus | same | same |
| Backup | RDS snapshots | Azure backups | Cloud SQL backups |
| Rollback | Helm history | Helm history | Helm history |

Deploy sequence (when credentials exist): clean SHA → existing CI → GHCR digest → Helm `marpich-iam` with `image.digest`. **No second CI.**

## PROFILE_KUBERNETES — READY_FOR_CREDENTIALS

- **Method:** existing Helm + optional Flux  
- **Image:** `ghcr.io/marpich/marpich-backend` `@digest` preferred over `:7.0.0`  
- **Secrets:** ExternalSecret (production values)  
- **TLS:** Ingress `letsencrypt-prod`  
- **Rollback:** `helm rollback marpich-iam 0 --namespace marpich`  
- **Verify:** non-local health URL; G26 validator  

## Verification (all profiles)

```bash
python3 scripts/meos-launch-readiness.py
python3 scripts/meos-ext-g26-readiness.py
```
