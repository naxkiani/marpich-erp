# ADR-209: Enterprise Digital Twin — Platform Engineering & DevSecOps (P199-D1)

## Status

Accepted

## Context

Prompts 199-A/B/C delivered Twin Platform domain law (ADR-203/203a), Sync Engine & Event Mesh (ADR-207), and Twin AI Intelligence (ADR-208). Production operation at multi-industry scale requires Platform Engineering, DevSecOps, GitOps, multi-cloud/edge topology, quality gates, and Twin-specific SRE — without inventing a second IAM release plane or Secrets SoR.

**Prompt ID:** V03-C02-P199-D1 · **ADR number:** 209  
**Precedent:** ADR-201d (Adaptive Auth) · ADR-202e (Federation)

## Decision

1. **Ship twin inside shared `marpich-iam` Helm release** — additional Deployments/HPA/CronJobs/NetworkPolicy/ServiceMonitor for sync workers, snapshotters, intelligence batch jobs; not a parallel backend binary or orphan chart.  
2. **Platform Engineering** for twin is a **profile** over Core Platform APIs (registry, config, metadata, discovery, health, feature flags, secrets refs) — twin does not own a second Platform Controller/Operator SoR.  
3. **DevSecOps** reuses GHA / GitLab / Azure Pipelines / ArgoCD / Flux patterns from federation; add twin path filters and quality gates. Jenkins/Tekton/Spinnaker/GitLab are **adapters** via catalog — never hardcoded as sole CI.  
4. **IaC** extends Terraform modules + Ansible + Helm + Kustomize; OpenTofu/Pulumi are interchangeable backends behind module contracts. Cloud provider choice is environment configuration.  
5. **Kubernetes / mesh / containers / secrets / network / edge / multi-cloud** follow federation topology catalogs with twin-specific worker planes (sync, graph query budgets, AI job quotas via AI Platform).  
6. **Twin Operations** (provision/activate/suspend/migrate/recover/archive/retire) are **application + GitOps + policy** — Worker autoscaling is KEDA/HPA on Event Mesh lag, not ad-hoc scripts.  
7. **Performance targets** (100M+ twins, 10M+ concurrent users, billions events/day, sub-second sync, 99.99%) are **SLO catalog + capacity plans** — achieved via sharding, async workers, regional meshes; not by embedding thresholds in domain code.  
8. Everything configurable: regions, clusters, scaling rules, deployment strategies, certificates, secrets paths, policies.

## Consequences

- Production twin requires migrations (`029`/`031`), Postgres + Event Mesh + Redis (cache), Feature Flags `twin.*`, Secrets path `marpich/${env}/iam/twin/*`.  
- AI GPU capacity stays on AI Platform plane — not in twin Helm.  
- Operators use Twin Deployment / Operator / DR guides under `docs/deployment` and `docs/operations`.

## References

- [ENTERPRISE_TWIN_PLATFORM_ENGINEERING.md](../architecture/ENTERPRISE_TWIN_PLATFORM_ENGINEERING.md)  
- ADR-203 · 203a · 207 · 208 · 201d · 202e
