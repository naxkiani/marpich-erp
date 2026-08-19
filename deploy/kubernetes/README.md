# Kubernetes adapter (existing Helm is authoritative)

**Chart:** `infrastructure/kubernetes/helm/marpich-iam`  
**Optional GitOps:** `infrastructure/fluxcd/marpich-iam-helmrelease.yaml`  
Flux is **not** required for every environment. Direct Helm is an approved path.

```bash
helm lint infrastructure/kubernetes/helm/marpich-iam
helm upgrade --install marpich-iam infrastructure/kubernetes/helm/marpich-iam \
  --set-string image.digest=<ci-digest>
helm rollback marpich-iam 0 --namespace marpich
```

Probes: liveness `/api/v1/live`, readiness `/api/v1/ready`. ExternalSecret template exists; production values enable it. Digest empty = **NOT_AVAILABLE**. Never `:latest` as certification identity.

KUBERNETES_STATUS = **READY_FOR_CREDENTIALS** (no kubeconfig).
