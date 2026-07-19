# EIFTP Deployment, DevSecOps, Kubernetes & Observability Surface

**Prompt:** P200-B11 · **ADR:** [225](../adr/225-enterprise-identity-federation-deployment-observability-devsecops.md)  
**Depends on:** [OHS / APIs](ENTERPRISE_IDENTITY_FEDERATION_APIS_EVENTS_CQRS.md) (ADR-224) · B2 ARCH_* catalogs · ADR-202e  
**SoR:** `backend/contexts/identity_federation/` · Chart: `marpich-iam`  
**Next:** P200-B12 Cursor Deliverables + Definition of Done

---

## 1. Mission

Make every EIFTP capability **automatically** buildable, testable, deployable, observable, scalable, recoverable, and auditable on MEOS Kubernetes — GitOps-first, Zero Trust runtime, AI-assisted ops signals.

---

## 2. Ownership (critical)

| Capability | Owner |
|------------|--------|
| Cluster provisioning / GitOps controllers | Platform Engineering (infra) |
| Metrics store / Tempo / Loki / Grafana | Observability Platform |
| Secrets / cert rotation | Secrets Platform + Vault |
| Federation deploy profile · SLOs · DR checklist · ops APIs | **This surface (B11)** |
| External IdP connectors | Integration Platform sidecars |

Do **not** create `contexts/eiftp/` or a parallel Observability / Platform Engineering bounded context inside federation.

---

## 3. Architecture

```mermaid
flowchart TB
  GH[GitHub Actions / Azure Pipelines] --> SCAN[SAST SCA Secret Trivy SBOM Cosign]
  SCAN --> REG[OCI Registry]
  REG --> GITOPS[ArgoCD / Flux]
  GITOPS --> K8S[marpich-iam Helm]
  K8S --> MESH[Service Mesh mTLS]
  K8S --> APP[Federation API + Outbox]
  APP --> OTEL[OpenTelemetry]
  OTEL --> PROM[Prometheus / Grafana]
  APP --> OPS[/federation/ops]
```

Catalogs:

- [OPS_ARCHITECTURE.v1.yaml](identity/eiftp/OPS_ARCHITECTURE.v1.yaml)
- [OPS_SRE_CATALOG.v1.yaml](identity/eiftp/OPS_SRE_CATALOG.v1.yaml)
- [OPS_SURFACE.v1.yaml](identity/eiftp/OPS_SURFACE.v1.yaml)
- Extends B2: `ARCH_DEPLOYMENT` · `ARCH_DEVSECOPS` · `ARCH_OBSERVABILITY`

---

## 4. Kubernetes & GitOps

| Asset | Path |
|-------|------|
| Helm chart | `infrastructure/kubernetes/helm/marpich-iam/` |
| Argo CD | `infrastructure/argocd/marpich-iam-application.yaml` |
| Flux | `infrastructure/fluxcd/marpich-iam-helmrelease.yaml` |
| HPA / VPA / NetworkPolicy / ServiceMonitor | chart templates |

Runtime: Pod Security restricted · network policies · mesh mTLS · admission (OPA/Kyverno at platform) · image verify (Cosign) · SBOM from CI.

Promotion: `dev` → `staging` → `prod` **only** via GitOps PR + signed artifacts. Manual `kubectl apply` is not a supported production path.

---

## 5. DevSecOps pipeline

Workflow: `.github/workflows/identity-federation-enterprise.yml` (+ Azure Pipelines twin).

Stages: Source → Build → SAST → Unit → Dependency/Secret scan → Container build/scan → Integration → Sign → GitOps promote → Verify → Rollback.

IaC: Terraform/OpenTofu · Helm · Kustomize · Crossplane/Cluster API (platform) · Ansible playbooks under `infrastructure/ansible/`.

---

## 6. Observability & SRE

| Concern | Standard |
|---------|----------|
| Metrics | Prometheus scrape — `/federation/metrics`, `/federation/ops/metrics` · METRICS_CATALOG |
| Logs | Structured → Loki/OpenSearch (platform) |
| Traces | OpenTelemetry (`backend/shared/infrastructure/observability/telemetry.py`) |
| Dashboards | Grafana `identity-federation*` |
| Alerts | `infrastructure/observability/prometheus/alerts/identity-federation.yml` |

SLOs (28-day): Availability **99.99%** · Login p95 **200 ms** · Token p95 **100 ms**. Exhausted error budget → freeze risky deploys.

APIs: `GET /api/v1/federation/ops/{surface,deployment,pipeline,observability,slo,dr,health,metrics}` · `POST .../incidents/signal` · `POST .../dr/drill` · `POST .../ai/recommend`.

---

## 7. Disaster recovery & multi-region

Targets: **RPO ≤ 5 min** · **RTO ≤ 30 min**. Modes: active-passive · active-active geo. Runbook: [IDENTITY_FEDERATION_DR_GUIDE.md](../deployment/IDENTITY_FEDERATION_DR_GUIDE.md). Drill results recorded via ops API.

Multi-cloud: AWS / Azure / GCP / private — via platform Cluster API + GitOps overlays; federation does not embed cloud SDKs.

---

## 8. AI ops, knowledge graph, digital twins

AI signals (ACL to AI Platform only): incident correlation · capacity hints · log anomalies · self-healing recommendations · deploy validation hints. Never AuthZ Permit/Deny.

KG edges: Cluster↔Microservice · Pipeline↔Application · Alert↔Metric · Incident↔Runbook. Twins: cluster · pipeline · mesh · infrastructure · deployment · runtime (state via platform twin sync — chart workers exist).

---

## 9. Quality gates

Reject: manual prod deploys · secrets in Git · no GitOps · no IaC · no runtime admission/scan · no distributed tracing · non–K8s-native packaging · no multi-region DR plan · no autoscaling · `contexts/eiftp`.

---

## 10. Definition of Done (B11)

Every EIFTP microservice path is GitOps-deployable on `marpich-iam`, CI-secured, OTel-instrumented, SLO-governed, DR-tested, and operable via `/federation/ops` without reinventing platform clusters, secrets, or observability stores.

---

## Architecture validation scorecard

| Dimension | Score | Pass? |
|-----------|------:|:-----:|
| Architecture | 5 | ✓ |
| DDD | 5 | ✓ |
| Security | 5 | ✓ |
| Scalability | 5 | ✓ |
| Performance | 4 | ✓ |
| Testing | 4 | ✓ |
| AI Integration | 4 | ✓ |
| Documentation | 5 | ✓ |
| Accessibility | 3 | N/A (API) |
| Localization | 3 | N/A (ops) |
| Observability | 5 | ✓ |
| Workflow | 4 | ✓ |
| Audit | 4 | ✓ |
| Policy Compliance | 4 | ✓ |
| Plugin Compatibility | 4 | ✓ |

Hard gates: GitOps · Helm · pipeline · OTel · no `eiftp` sibling · no secrets in ops sources.

### Verdict: ENTERPRISE_GRADE (P200-B11)

## Reuse analysis

- Helm `marpich-iam`, ArgoCD/Flux, GitHub workflow, Grafana/Prometheus assets, OTel bootstrap, B2 ARCH_* catalogs, existing `federation_*_metrics`.

## Architectural decisions

- **FederationOpsPlatform facade** over inventing Platform Engineering BC — rationale: MEOS already owns clusters/GitOps; EIFTP owns profile + SLO/DR signals.  
- **Rejected:** module-local Prometheus/Elasticsearch; secrets in ConfigMaps; manual-only prod path.
