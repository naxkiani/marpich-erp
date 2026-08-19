# MEOS EXT-G26 — Production Infrastructure Bill of Materials (P349)

**Date:** 2026-08-19  
**Law:** Include only requirements supported by repository evidence. Do not invent capacity or prices.  
**Companion:** [MEOS_EXT_G26_PROVIDER_COMPATIBILITY.md](./MEOS_EXT_G26_PROVIDER_COMPATIBILITY.md) · [MEOS_EXT_G26_EXTERNAL_DEPENDENCIES.v1.yaml](./MEOS_EXT_G26_EXTERNAL_DEPENDENCIES.v1.yaml)  
**OWNER:** NOT_AVAILABLE  
**STATUS of this BOM:** REQUIREMENTS_IDENTIFIED — **not provisioned**  
**COST:** NOT_AVAILABLE  

Compose, demo Postgres `:5433`, and workstation backups are **excluded** as production items.

| ITEM | MINIMUM REQUIREMENT | PURPOSE | DEPENDENCY | VALIDATION | STATUS |
|------|---------------------|---------|------------|------------|--------|
| Kubernetes-compatible cluster | Helm 3 + kubectl; namespace `marpich`; enough capacity for IAM chart floor below | G26-01 compute | Hosting account | kubeconfig present; `kubectl get ns` | BLOCKED |
| IAM API replicas | 6 (Helm `values-production.yaml` `replicaCount`) | Serve backend/IAM ingress | Cluster | `kubectl get deploy -n marpich` | BLOCKED |
| Twin worker replicas | 6 (Helm production `twinWorkers.replicaCount`) | Identity-twin jobs | Cluster | `kubectl get deploy -n marpich` | BLOCKED |
| CPU request floor | 4500m (6×500m API + 6×250m twin) | Scheduler fit | Cluster size | Node allocatable ≥ requests | DESIGNED / NOT_MEASURED |
| Memory request floor | 4608Mi (6×512Mi + 6×256Mi) | Scheduler fit | Cluster size | Node allocatable ≥ requests | DESIGNED / NOT_MEASURED |
| CPU/memory limits | API 2000m/2Gi; twin 1000m/1Gi per pod | Isolation | Cluster | Helm values | DESIGNED |
| Managed PostgreSQL | PostgreSQL 16-compatible; not localhost; not `:5433`/`:5444`; SSL | G26-02 system of record | Private network | Non-local PGHOST; production settings gates | BLOCKED |
| DB name / secret contract | Database `marpich_platform`; secret `marpich-db-credentials` key `database-url` | App DSN | Secret manager | Secret exists (no value print) | BLOCKED |
| Ingress-NGINX | IngressClass `nginx` | G26-07 HTTP(S) entry | Cluster + LB | `kubectl get ingressclass` | BLOCKED |
| Public DNS | Live hostname; Helm DESIGNED `auth.marpich.io` | G26-07 / G26-03 | DNS zone | Resolve ≠ localhost | NOT_AVAILABLE |
| Public-CA TLS | cert-manager ClusterIssuer `letsencrypt-prod`; secret `marpich-iam-prod-tls` | G26-03 HTTPS | DNS + cert-manager | Public CA; not compose self-signed | BLOCKED |
| Kubernetes Secrets | `{release}-secrets` envFrom; **not** in Helm templates | G26-04 runtime env | Secret manager | `kubectl get secret` without `-o yaml` values | NOT_AVAILABLE |
| Secret manager | Production SM/Vault/ES capable of filling those Secrets; Helm flags vault+externalSecrets **values-only** | G26-04 | Identity to SM | `MEOS_SECRET_MANAGER_AVAILABLE` after real backend | BLOCKED |
| GHCR | `ghcr.io/marpich/marpich-backend` | Image supply | GitHub Packages | CI push | BLOCKED |
| Image tag contract | `sha-<git sha>` (not `latest`; `:7.0.0` mutable) | G26-09 | Clean SHA + CI | Deployed tag/digest | BLOCKED |
| Image digest | OCI digest recorded from CI | G26-06/09 | CI build | `MEOS_IMAGE_DIGEST` | NOT_AVAILABLE |
| GitHub Actions | Existing `identity-federation-enterprise.yml` | Build/test/deploy | GHCR + kube credentials | Workflow run on clean SHA | BLOCKED |
| GitHub Environments | `staging` and `production` | CI deploy auth | Cluster kubeconfig | Environment protection | BLOCKED |
| Flux (optional) | `infrastructure/fluxcd/marpich-iam-helmrelease.yaml` | GitOps apply | GitRepository URL | `flux get helmreleases` | NOT_AVAILABLE |
| Redis | Host `redis.marpich.svc.cluster.local:6379` (`redis.enabled: false`) | Helm env contract | Cluster or managed Redis | Connectivity | NOT_AVAILABLE |
| Kafka | `kafka.marpich.svc.cluster.local:9092`; `KAFKA_ENABLED=true` | Outbox/events path | Cluster or managed Kafka | Connectivity | NOT_AVAILABLE |
| ServiceMonitor / Prometheus | Helm `serviceMonitor.enabled: true`; repo `infrastructure/observability/prometheus/` | Metrics | Cluster observability | Production scrape | CONFIGURED / FAIL (G23) |
| OpenTelemetry | `OTEL_ENABLED=true` in Helm env | Traces/metrics export | OTLP endpoint | Production export | CONFIGURED / NOT_VERIFIED |
| Alerting | Alert rules in repo; Alertmanager commented optional in prometheus.yml | G23 | On-call route | Production alert test | FAIL |
| Production backup | Automated backup of **production** PostgreSQL | Durability | Managed PG | Backup artifact | NOT_VERIFIED |
| Production restore | Restore drill of production backup | Recoverability | Backup | Restore report | NOT_VERIFIED |
| Helm rollback | `helm rollback marpich-iam 0 --namespace marpich` | G26-10 | Helm history | Exercised N→N+1→N | CONFIGURED / BLOCKED |
| NetworkPolicy | Helm `networkPolicy.enabled: true` | Segmentation | Cluster CNI | Policy applied | CONFIGURED / BLOCKED |
| Pod security | runAsNonRoot 1000; drop ALL; readOnlyRootFilesystem | Container security | Cluster | Live pod spec | CONFIGURED / BLOCKED |
| CI Trivy + SBOM | Existing workflow jobs | Image/fs scan | GitHub Actions | Job logs | DESIGNED |
| Production settings | `MARPICH_ENVIRONMENT=production`; postgres persistence; non-default JWT/DB | App hard gates | Secrets | Settings validator | CONFIGURED in code / not live |

**Not in this BOM (insufficient or non-production evidence):** Terraform modules (STUB), Ansible (MISSING), Compose `meosprod`, demo `:5433`, self-signed compose certs, workstation MinIO dumps, SLA/RPO/RTO numbers, dollar costs, full-MEOS node counts.

**HPA maxima (100 API / 200 twin) are DESIGNED caps, not minimum BOM items.**
