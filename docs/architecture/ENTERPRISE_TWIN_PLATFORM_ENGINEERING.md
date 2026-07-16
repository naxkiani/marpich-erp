# Enterprise Twin Platform Engineering & DevSecOps — Architecture Law

**Prompt:** V03-C02-P199-D1 · Volume 03 · Chapter 02  
**Governance:** Enterprise Architecture Governance 10.0  
**Status:** Canonical — production architecture (not a prototype brief)  
**ADR:** [ADR-209](../adr/209-twin-platform-engineering-devsecops.md)  
**Extends:** ADR-203 · 203a · 207 · 208 · deployment precedent ADR-201d · ADR-202e  
**Companions:** [ENTERPRISE_IDENTITY_DIGITAL_TWIN_PLATFORM.md](ENTERPRISE_IDENTITY_DIGITAL_TWIN_PLATFORM.md) · Sync [ENTERPRISE_TWIN_SYNCHRONIZATION_EVENT_MESH.md](ENTERPRISE_TWIN_SYNCHRONIZATION_EVENT_MESH.md) · Intelligence [ENTERPRISE_TWIN_AI_INTELLIGENCE_PLATFORM.md](ENTERPRISE_TWIN_AI_INTELLIGENCE_PLATFORM.md)

**Law:** Digital Twin production operations run on the **shared Marpich IAM / platform engineering plane**. Twin Sync workers, snapshotters, and intelligence batch jobs are **workloads and catalogs** — never a second CI/CD product, Secrets SoR, Event Bus, or cloud-hardcoded operator. Infrastructure, regions, certificates, secrets, deployment rules, and scaling policies are **configuration- and policy-driven**.

---

## Hard reuse map (anti-duplication)

| Concern | Owner | Twin D1 role |
|---------|-------|--------------|
| IAM release (`marpich-iam` Helm) | Platform Engineering | Extend chart: twin paths, jobs, HPA, metrics |
| Secrets SoR | Core Secrets + Vault/cloud KMS | Path catalog only |
| Feature Flags / Settings | Feature Flag System · Settings | Register `twin.*` |
| Event Mesh / Fabric / Orchestration | ADR-010 / 175 / 178 + 207 | Sync workers consume configured topics |
| AI inference capacity | AI Platform + Governance | Quotas / jobs — no twin GPU chart |
| Observability | OTel / Prometheus / Grafana / Elastic | Twin SRE metrics + dashboards |
| API Gateway | Gateway platform | Register `/api/v1/identity-twins` |
| CI/CD engines | GHA / GitLab / ADO / Argo / Flux (+ adapters) | Twin workflow + GitOps parameters |
| IaC | Terraform/OpenTofu modules + Ansible + Kustomize | Twin submodule or values-only |

```text
Git (trunk / release) ──► CI (test · scan · SBOM · sign) ──► OCI registry
                                      │
                                      ▼
                              GitOps (ArgoCD | Flux)
                                      │
                                      ▼
                    marpich-iam Helm (API + twin workers + CronJobs)
                                      │
              ┌───────────────────────┼───────────────────────┐
              ▼                       ▼                       ▼
         Event Mesh              Postgres                  AI Platform
       (twin topics)           (identity_twin)            (inference)
```

### Forbidden

- Twin-owned Vault fork or second secrets BC  
- Hardcoded AWS/Azure/GCP-only logic in twin domain  
- Module-local Kubernetes operators bypassing GitOps  
- Second Event Bus / local Kafka inside twin  
- Demo Docker Compose as the production topology  

---

## SECTION 1 — Enterprise Platform Engineering

Twin uses **platform-shared** services; twin-specific configuration lives in catalogs.

| Capability | Implementation |
|------------|----------------|
| Platform API | Core + module REST; twin under `/api/v1/identity-twins` |
| Platform Controller / Operator | Shared platform operator; twin lifecycle via application + Workflow, not a proprietary CRD SoR |
| Platform SDK / CLI | `marpich` CLI extensions: `twin sync`, `twin diagnose`, `twin migrate` (calls APIs) |
| Platform Dashboard | Ops Center catalog → Grafana + Admin UI modules |
| Platform Registry | Module registry + twin kind catalog (ADR-203a) |
| Configuration / Metadata / Discovery / Health | Settings + Feature Flags + gateway health + twin health facets |
| Upgrade / Lifecycle / Diagnostics | GitOps chart version + twin version upgrade job + diagnostics API |

Catalog: `identity/TWIN_OPS_CENTER.v1.yaml`.

---

## SECTION 2 — DevSecOps foundation

### Continuous * everything

| Loop | Engine (catalog-selectable) |
|------|----------------------------|
| CI / CD / Deploy | GitHub Actions · GitLab CI · Azure DevOps · Jenkins · Tekton · Spinnaker (adapters) |
| GitOps | ArgoCD · FluxCD |
| Verification | Continuous Verification (smoke + SLO burn) |
| Compliance | Policy gates + Audit + SBOM attestation |
| Monitoring / Security / Docs / Testing | OTel + Trivy + ADR/docs CI + pytest contracts |

Canonical twin pipeline: `.github/workflows/digital-twin-enterprise.yml`  
Parity: extend `.gitlab-ci.yml` · `infrastructure/azure-pipelines/digital-twin.yml`.

---

## SECTION 3 — Source control strategy

| Practice | Marpich twin default |
|----------|----------------------|
| Trunk-based | Default for main; short-lived feature branches |
| Git Flow | Optional for regulated release trains (policy) |
| Hotfix | `hotfix/*` → main + release branch; semantic version bump |
| SemVer / Conventional Commits | Required for chart + migration tags |
| Monorepo | Primary (`Marpich ERP`) |
| Polyrepo | Allowed for edge agents via Integration Platform packages |
| CODEOWNERS | `backend/contexts/identity_digital_twin/` · twin infra paths |

Never hardcode branch protection — repository governance as org policy.

---

## SECTION 4 — Infrastructure as Code

| Tool | Role |
|------|------|
| Terraform / OpenTofu | Environment modules (network, DB, cache, messaging, monitoring) |
| Pulumi | Optional alternate IaC backend (same module contracts) |
| Ansible | Helm deploy playbooks |
| Helm | Canonical K8s packaging (`marpich-iam`) |
| Kustomize | Env overlays `staging` / `production` |

Module: `infrastructure/terraform/modules/identity-digital-twin/` (topics ACLs, Redis prefix, optional RDS params) — prefer shared messaging/database modules when possible.  
Immutable + versioned: image digest pins; chart appVersion; Terraform state locked.

---

## SECTION 5 — Kubernetes platform

Twin workloads on shared cluster:

| Resource | Twin use |
|----------|----------|
| Namespace | `marpich` (+ observability / ingress / security) |
| Deployment | `marpich-iam` (API) + `twin-sync-workers` (+ optional) |
| StatefulSet | Optional local edge cache (topology `edge`) |
| DaemonSet | Runtime security agents (platform-shared) |
| CronJob | Snapshot · retention · drift scan · kind catalog reconcile |
| Job | Migrations `029`/`031` |
| HPA / VPA / Cluster Autoscaler | API + workers; cluster via Karpenter/CA (env) |
| Ingress / Gateway API | Twin API paths |
| NetworkPolicy / Admission | Deny-by-default; Kyverno/OPA policies catalog |
| PVC / StorageClass | Snapshot offload only if needed — prefer object storage via platform |

Templates: `infrastructure/kubernetes/helm/marpich-iam/templates/twin-*.yaml`.

---

## SECTION 6 — Service mesh

Support **Istio · Linkerd · Consul** via `infrastructure/service-mesh/*/twin-*.yaml`.

| Capability | Twin profile |
|------------|--------------|
| mTLS | Required between IAM pods and mesh |
| Traffic split / mirror / canary / blue-green | Progressive delivery flags |
| Circuit breaker / retry / timeout / rate limit | DestinationRule / ServiceProfile catalogs |
| Authorization policies | Path `/api/v1/identity-twins` |
| Telemetry | Mesh metrics + twin app metrics |

Mesh choice = cluster profile, not twin domain dependency.

---

## SECTION 7 — Container platform

OCI images via `infrastructure/docker/images/backend.Dockerfile`  
Registry GHCR (or ECR/ACR/GCR via config)  
Promotion: digest → staging → production  
Signing + SBOM + Trivy + provenance (SLSA) in CI  
Trusted image admission via cluster policy  

---

## SECTION 8 — Secrets management

Providers: Vault · Azure Key Vault · AWS Secrets Manager · GCP Secret Manager  

Catalog: `infrastructure/secrets/TWIN_SECRETS_CATALOG.yaml`  
Path prefix: `marpich/${environment}/iam/twin/*`  

Rotation: External Secrets + cert-manager; dynamic DB/API credentials; never secrets in Git.

---

## SECTION 9 — Configuration management

| Layer | Owner |
|-------|-------|
| Central config | Settings service |
| Feature flags | Feature Flag System (`twin.sync.enabled`, `twin.intelligence.enabled`, …) |
| Helm values | Environment + GitOps parameters |
| Tenant / policy config | Policy Engine + tenant packs |
| Dynamic runtime | Flag evaluate API — no `os.getenv` feature gates in domain |

---

## SECTION 10 — Network architecture

Catalog: `identity/TWIN_DEPLOYMENT_TOPOLOGY.v1.yaml`

Private · Public · Management · DMZ · VPN · Private endpoints · Global/Regional LB · API Gateway · Ingress · DNS · Service discovery (mesh + Core discovery).

Zero Trust: unauthenticated twin APIs forbidden; management plane isolated.

---

## SECTION 11 — Edge computing

Topologies: regional nodes · bank branches · campuses · hospitals · retail · IoT gateways  

Edge twin cache: projections only; offline sync via Sync Engine + Integration connectors (ADR-207).  
Edge AI: AI Platform edge profile — twin never embeds models.  
Catalog nodes declare RPO/RTO and allowed twin kinds.

---

## SECTION 12 — Multi-cloud

Supported: AWS · Azure · GCP · Oracle · OpenStack · VMware · Bare metal  

**Cloud abstraction:** Terraform providers + Helm values + Event Mesh transport registry — twin application code has **zero** cloud SDK imports for infra.

---

## SECTION 13 — Deployment strategies

Rolling (default) · Blue/Green · Canary · Shadow · Progressive delivery  

Automatic rollback on SLO burn or failed Continuous Verification  
Health validation: readiness/liveness + twin sync lag SLO  
Deployment approval: Workflow / environment protection (GitHub Environments)

---

## SECTION 14 — Automation

Infrastructure · deployment · provisioning · configuration · scaling (HPA/KEDA) · certificates (cert-manager) · backup · recovery · testing — all GitOps/CI scheduled jobs.  
Twin provisioning automation = tenant module activation + kind catalog seed (API), not DDL scripts per tenant.

---

## SECTION 15 — Platform security

Supply chain: signed images, SBOM, provenance verification  
Runtime: Falco/agent DaemonSet (platform)  
Hardening: CIS K8s + PSA restricted + container drop-caps  
Admission: OPA/Kyverno deny untrusted images  
Network isolation: NetworkPolicy + mesh AuthZ  

---

## SECTION 16 — Digital Twin operations

| Operation | Mechanism |
|-----------|-----------|
| Provision / Activate / Suspend | Twin API + Policy + Feature Flags |
| Migration | Sync full mode + version bump job |
| Synchronization | Sync Engine workers (ADR-207) |
| Recovery | Snapshot + event replay + SoR full sync |
| Archiving / Retirement | Lifecycle Workflow + retention Policy |
| Version upgrade | Chart/appVersion + migration Job |
| Diagnostics | Twin diagnostics API + Ops Center runbooks |

---

## SECTION 17 — Scalability

| Plane | Scale lever |
|-------|-------------|
| API | HPA + regional LB |
| Sync workers | HPA/KEDA on consumer lag |
| Queue / events | Mesh partitions + Orchestration concurrency |
| Graph | Query hop budgets + Directory hydrate pools |
| AI | AI Platform async jobs + quotas |
| Database | Partition by `tenant_id`; read replicas; archive cold snapshots |
| Storage | Object store for large snapshot blobs (Document/Object platform) |
| Regional | Active-active with conflict Policy |

---

## SECTION 18 — Performance targets

| Target | Design approach |
|--------|-----------------|
| 100M+ twins | Sharded tenants · kind partitioning · projection-only storage |
| 10M+ concurrent users | Stateless API · edge caches · CDN for static Admin |
| Billions events/day | Kafka/Pulsar scale · async workers · batch ACL |
| Sub-second sync (p95 under normal) | Incremental delta · local hot cache · SLO alert at 2m (ADR-203) |
| 99.99% availability | Multi-AZ · PDB · warm/hot DR per topology |

Optimization: pagination max 100 · never unbounded list · OTel traces on SyncRun.

---

## SECTION 19 — Quality gates

Catalog: `identity/TWIN_QUALITY_GATES.v1.yaml`

| Gate | Blocker examples |
|------|------------------|
| Security | Critical CVE, unsigned image |
| Architecture | Dependency graph / ADR validation |
| Performance | p95 regression vs baseline |
| Deployment | Failed smoke / sync lag burn |
| Compliance | Missing audit/SBOM attestation |
| AI | Unapproved `model_approval_ref` |
| Operational | Missing ServiceMonitor / runbook link |
| Release | SemVer + changelog |

---

## SECTION 20 — Architecture principles checklist

Cloud Native · Platform Engineering · API First · Plugin First · Configuration · Policy · Metadata · DDD · CQRS · Hexagonal · Microservices · Event Driven · Twin Native · KG Native · Zero Trust · AI Native · IaC · GitOps  

**Never hardcode:** infrastructure · cloud providers · certificates · secrets · regions · clusters · deployment rules · scaling rules · configuration · policies · security rules.

---

## Production artifact index

| Artifact | Path |
|----------|------|
| Helm twin jobs | `infrastructure/kubernetes/helm/marpich-iam/templates/twin-cronjobs.yaml` |
| Twin workers | `…/templates/twin-sync-workers.yaml` |
| Values flags | `values.yaml` / `values-production.yaml` |
| ArgoCD / Flux | `infrastructure/argocd/` · `infrastructure/fluxcd/` |
| CI | `.github/workflows/digital-twin-enterprise.yml` |
| Secrets | `infrastructure/secrets/TWIN_SECRETS_CATALOG.yaml` |
| Topology / SRE / GitOps / Gateway | `docs/architecture/identity/TWIN_*.yaml` |
| Deployment guide | `docs/deployment/DIGITAL_TWIN_DEPLOYMENT_GUIDE.md` |
| Operator / DR | `docs/operations/DIGITAL_TWIN_*` |
| Terraform | `infrastructure/terraform/modules/identity-digital-twin/` |

---

## Delivery roadmap

| Phase | Deliverable |
|-------|-------------|
| **D0** | Helm paths + featureFlags + ServiceMonitor + CI twin tests |
| **D1** | Sync worker Deployment + HPA/KEDA + CronJobs |
| **D2** | GitOps twin parameters + mesh twin policies |
| **D3** | SRE dashboards + alerts + runbooks | ✓ completed by ADR-210 / P199-D2.2 |
| **D4** | Multi-region / edge topology profiles |
| **D5** | Quality gates wired in release pipeline |
| **D6** | Chaos + DR drills documented |

---

## Related

- [API_GATEWAY_ARCHITECTURE.md](API_GATEWAY_ARCHITECTURE.md)  
- [ENTERPRISE_OBSERVABILITY_PLATFORM.md](ENTERPRISE_OBSERVABILITY_PLATFORM.md)  
- [ENTERPRISE_TWIN_OBSERVABILITY_IR_BCP_DR.md](ENTERPRISE_TWIN_OBSERVABILITY_IR_BCP_DR.md)  
- [ENTERPRISE_FEATURE_FLAG_SYSTEM.md](ENTERPRISE_FEATURE_FLAG_SYSTEM.md)  
- ADR-201d · ADR-202e · ADR-203 · ADR-207 · ADR-208 · ADR-209 · ADR-210
