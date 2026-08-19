# MEOS Product Infrastructure Blueprint (P351)

**Date:** 2026-08-19  
**P351_STATUS:** PRODUCT_INFRASTRUCTURE_FOUNDATION  
**G26_READY:** FALSE (unchanged). **P0:** 1. **P313:** NOT_CERTIFIED.  
**Law:** Product infrastructure is not production. LOCAL / DEMO / COMPOSE ≠ PRODUCTION.

P351 separates **PRODUCT_INFRASTRUCTURE** (buildable in this repo) from **EXTERNAL_PRODUCTION_RESOURCES** (cluster, managed PG, public DNS/TLS, secret manager, CI kube credentials).

## Reuse (no second platform)

| Concern | Existing SoR |
|---------|----------------|
| Local stack | `infrastructure/docker/compose/docker-compose.dev.yml` + `scripts/dev-up.sh` |
| Demo / workstation prod-profile | `docker-compose.meos-prod.yml` (self-signed TLS, Postgres `:5444`) |
| Image | `infrastructure/docker/images/backend.Dockerfile` (non-root uid 1000) |
| Helm/Flux | `infrastructure/kubernetes/helm/marpich-iam/` + `infrastructure/fluxcd/marpich-iam-helmrelease.yaml` |
| CI | `.github/workflows/identity-federation-enterprise.yml` (digest output wired) |
| Backup/restore | `scripts/meos-postgres-backup.sh` / `scripts/meos-postgres-restore-drill.sh` |
| Observability | `infrastructure/observability/prometheus/` |
| Secrets catalog | `backend/contexts/secrets` (API; not a live vault) |
| Settings gates | `backend/shared/infrastructure/settings.py` |

## Canonical runtime graph (product)

```
Postgres 16  →  backend (FastAPI :8000) + outbox worker
Redis        →  cache (when configured)
MinIO        →  backup object interface (workstation / VPS)
Caddy        →  TLS terminator (self-signed = DEV; public CA = later G26)
Helm IAM     →  same backend image; ExternalSecret → `{release}-secrets`
```

Kafka is **optional**. `docker-compose.meos-prod.yml` sets `KAFKA_ENABLED=false`. Dev compose may start Kafka. Do not invent a second broker.

## Secret interface (provider-neutral)

| Adapter | Mechanism | Status |
|---------|-----------|--------|
| Environment injection | gitignored `.env` / `env.production.example` placeholders | CONFIGURED |
| Docker | Compose `environment:` from env-file (no values in git) | CONFIGURED |
| Kubernetes | ExternalSecret → `{fullname}-secrets` (production values enable it) | CONFIGURED / READY_FOR_CREDENTIALS |
| External SM | Helm `secrets.vault.path` + ClusterSecretStore name | READY_FOR_CREDENTIALS |

Never store values in Git, images, docs, or logs.

## Database strategy (one model)

PostgreSQL 16-compatible. Migrations: `scripts/run-migrations.sh`.  
`localhost:5433` and compose `:5444` remain **NON_PRODUCTION**. Managed PG is G26-02.

## TLS / DNS

| Mode | Mechanism | Class |
|------|-----------|--------|
| Local / demo | `Caddyfile.meos-prod` self-signed | DEVELOPMENT ONLY |
| VPS | `Caddyfile.vps.example` + public hostname | READY_FOR_CREDENTIALS |
| Kubernetes | Ingress + cert-manager `letsencrypt-prod` | READY_FOR_CREDENTIALS |

## Environment contract

| Env | Identity | DB | Secrets | TLS | Deploy |
|-----|----------|----|---------|-----|--------|
| LOCAL | development | `:5433` demo | example | none/http | `dev-up.sh` |
| DEVELOPMENT | development | compose.dev | example | none | compose.dev |
| TEST | test | ephemeral / CI | CI secrets | n/a | pytest |
| STAGING | staging | non-local | GitHub Environment | public or internal CA | existing Helm CI |
| DEMO | demo label | `:5444` meosprod | gitignored env | self-signed | compose meosprod |
| PRODUCTION | production | managed PG | external SM | public CA | Helm/Flux + digest |

LOCAL never satisfies PRODUCTION checks.

## Readiness command

```bash
python3 scripts/meos-launch-readiness.py
python3 scripts/meos-ext-g26-readiness.py   # authoritative G26; do not override
```
