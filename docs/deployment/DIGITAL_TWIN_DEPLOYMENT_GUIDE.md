# Digital Twin — Production Deployment Guide

**Prompt:** V03-C02-P199-D1 · **ADR:** 209  
**Chart:** `infrastructure/kubernetes/helm/marpich-iam`  
**CI:** `.github/workflows/digital-twin-enterprise.yml`

## Prerequisites

1. Postgres with `identity_twin` migrations applied (`029` / `031`)  
2. Event Mesh topics `marpich.twin.*.v1` provisioned (ADR-207)  
3. Secrets seeded at `marpich/${env}/iam/twin/*` (see `TWIN_SECRETS_CATALOG.yaml`)  
4. Feature Flags: `twinEnabled`, `twinSyncEnabled`, `twinIntelligenceEnabled`  
5. API Gateway route profile `TWIN_API_GATEWAY.v1.yaml` active  

## Deploy (GitOps preferred)

### ArgoCD

Parameters already include twin flags in `infrastructure/argocd/marpich-iam-application.yaml`. Sync Application `marpich-iam`.

### FluxCD

`infrastructure/fluxcd/marpich-iam-helmrelease.yaml` values enable twin workers.

### Helm (manual / CI)

```bash
helm upgrade --install marpich-iam infrastructure/kubernetes/helm/marpich-iam \
  --namespace marpich --create-namespace \
  -f infrastructure/kubernetes/helm/marpich-iam/values-production.yaml \
  --set image.tag=sha-<gitsha> \
  --set featureFlags.twinEnabled=true \
  --set twinWorkers.enabled=true \
  --wait --timeout 15m
```

## Verification

| Check | Command / Signal |
|-------|------------------|
| Helm | `helm lint` · `helm status marpich-iam -n marpich` |
| Pods | `kubectl -n marpich get deploy -l app.kubernetes.io/component=digital-twin-sync` |
| API | `GET /api/v1/identity-twins` (auth) |
| Metrics | `/api/v1/identity-twins/metrics` scraped by ServiceMonitor |
| Sync lag | Prometheus `twin_sync_lag_seconds` p95 ≤ 30s |

## Progressive delivery

1. Staging full traffic  
2. Production canary 5% (`canary.enabled=true`)  
3. Continuous Verification (SLO burn)  
4. Promote or automatic `helm rollback`  

## Rollback

```bash
helm rollback marpich-iam 0 --namespace marpich
```

Also disable flags via Feature Flag System if AI/sync plane must fail closed without redeploy.

## Multi-cloud / edge

Select topology from `TWIN_DEPLOYMENT_TOPOLOGY.v1.yaml`. Cloud provider is IaC profile only — twin domain has no cloud SDKs.

## Related

- [ENTERPRISE_TWIN_PLATFORM_ENGINEERING.md](../architecture/ENTERPRISE_TWIN_PLATFORM_ENGINEERING.md)  
- [DIGITAL_TWIN_OPERATOR_GUIDE.md](../operations/DIGITAL_TWIN_OPERATOR_GUIDE.md)  
- [DIGITAL_TWIN_DR_BCP.md](../operations/DIGITAL_TWIN_DR_BCP.md)
