# Marpich Infrastructure

Cloud-native deployment artifacts — separate from application code.

```
infrastructure/
├── docker/               # Images, compose, migrations, container policies
│   ├── compose/          # docker-compose.yml (dev), docker-compose.prod.yml
│   ├── images/
│   ├── policies/         # OCI signing / scan / promotion policy
│   └── migrations/       # 002–028 (incl. adaptive_auth + identity_federation)
├── observability/        # Prometheus, Grafana, OTel Collector
├── nginx/                # NGINX reverse proxy (IAM + federation)
├── traefik/              # Traefik dynamic routing
├── secrets/              # Secrets catalogs (paths only — never values)
├── service-mesh/         # Istio / Linkerd / Consul policies
├── argocd/               # GitOps application manifests
├── ansible/              # Deployment playbooks
├── azure-pipelines/      # Azure DevOps pipelines
├── terraform/            # IaC
│   ├── modules/          # networking, database, cache, messaging, adaptive-auth, identity-federation, monitoring
│   └── environments/     # development | staging | production
└── kubernetes/
    ├── base/             # namespace + federation CronJobs / NetworkPolicy / VPA
    ├── overlays/         # staging | production Kustomize
    └── helm/marpich-iam/ # Enterprise IAM Helm chart (P197-D + P198-D1 federation)
```

## Local development

```bash
# Infra only (Postgres, Redis, Kafka)
pnpm docker:up
./scripts/run-migrations.sh

# Or one command (start + wait + migrate)
pnpm dev:infra

# With observability overlay (OTel, Prometheus, Grafana)
pnpm docker:up:obs
```

Canonical compose file: `docker/compose/docker-compose.dev.yml`

- One Terraform module per infrastructure concern (not one giant `main.tf`)
- K8s base + overlays per environment (Kustomize)
- Backend and frontend images built from `docker/images/`
- Backend image installs **`argon2-cffi`** (Argon2id password hashing, ADR-197) and fails the build if unavailable
- Identity Federation (P198-D1) extends shared `marpich-iam` — see ADR-202e

## Identity Federation Ops (P198-D1)

| Concern | Path |
|---------|------|
| Helm values / ingress | `kubernetes/helm/marpich-iam/` |
| Prometheus alerts | `observability/prometheus/alerts/identity-federation.yml` |
| Grafana | `observability/grafana/dashboards/identity-federation*.json` |
| CI | `.github/workflows/identity-federation-enterprise.yml` |
| Terraform | `terraform/modules/identity-federation/` |
| Deploy docs | `docs/deployment/IDENTITY_FEDERATION_DEPLOYMENT_GUIDE.md` |
