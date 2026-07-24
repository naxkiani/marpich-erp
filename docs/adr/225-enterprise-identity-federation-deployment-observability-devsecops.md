# ADR-225: EIFTP Deployment, DevSecOps, Kubernetes & Observability Surface (P200-B11)

## Status

Accepted — Official EIFTP Ops / Deploy / Observability baseline (V03-C03)

## Context

P200-B10 packaged the Open Host Service. P200-B11 standardizes how EIFTP is **built, deployed, observed, recovered, and operated** on the MEOS Kubernetes/GitOps platform — without inventing a parallel Observability BC, secret store, or deploy toolchain.

## Decision

1. Law: `docs/architecture/ENTERPRISE_IDENTITY_FEDERATION_DEPLOYMENT_OBSERVABILITY_DEVSECOPS.md`
2. Catalogs: `docs/architecture/identity/eiftp/OPS_*.v1.yaml` extending B2 `ARCH_DEPLOYMENT|DEVSECOPS|OBSERVABILITY`
3. Runtime SoR remains `identity_federation`; Helm chart SoR: `infrastructure/kubernetes/helm/marpich-iam/`
4. GitOps via existing ArgoCD/Flux applications — no manual-only deploy path
5. Observability reuses platform OTel + METRICS_CATALOG (`identity_federation_metrics`) + existing scrape paths
6. Facade: `FederationOpsPlatform` — deploy profile, SRE SLO/error budget, DR checklist, AI ops signals (facts)
7. REST: `/api/v1/federation/ops/*` — discovery + health + SLO + DR drill registry
8. Secrets only via Vault/platform secret injection — never in Git
9. Deep multi-cloud cost platforms remain infra team ownership; B11 catalogs federation constraints

## Consequences

- B12 DoD validates deploy/obs/security gates against these catalogs
- CI must remain GitHub Actions `identity-federation-enterprise.yml` + Helm smoke

## References

ADR-202e · 216 · 224 · ENTERPRISE_OBSERVABILITY_PLATFORM · SECURITY_STANDARD · PERFORMANCE_STANDARD
