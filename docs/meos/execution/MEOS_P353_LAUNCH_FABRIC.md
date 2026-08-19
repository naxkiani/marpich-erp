# MEOS P353 — Multi-platform launch fabric

**Date:** 2026-08-19  
**Layer:** packaging / overlays / release engineering only  
**Not:** a second ERP, CI, Helm, or G26 bypass

ONE CODEBASE → ONE RELEASE ARTIFACT → TARGET OVERLAY → TARGET DEPLOYMENT (when credentials exist).

Existing structure remains `deploy/` (not a parallel `deployment/` tree). Target overlays live in `deploy/targets/`.

```
BASE (deploy/targets/base.yaml)
  + TARGET OVERLAY (vps|hostinger-vps|aws|azure|gcp|kubernetes|local)
  + ENVIRONMENT CONFIG (deploy/environments/ENV_*.env.example)
  + SECRET REFERENCES (env.production.example / ExternalSecret)
```

## Frozen certification (unchanged)

G26_READY = FALSE · P0 = 1 · P313 = NOT_CERTIFIED · P313_REENTRY_READY = FALSE  
PRODUCTION_CERTIFIED = FALSE · GO_LIVE_READY = FALSE · GO_LIVE_AUTHORIZATION = NOT_APPROVED  
ACTIVE_APPLICATIONS = 0 · PRODUCTION_TRAFFIC = NOT_ENABLED

## What P353 prepares offline

| Package | Overlay | Canonical mechanism |
|---------|---------|---------------------|
| LOCAL | `deploy/targets/local.yaml` | `scripts/dev-up.sh` |
| DEMO / Docker | `deploy/targets/local-demo.yaml` | `deploy/scripts/meos-demo.sh` |
| VPS | `deploy/targets/vps.yaml` | `scripts/meos-vps-bootstrap.sh` |
| Hostinger VPS | `deploy/targets/hostinger-vps.yaml` | same as VPS; shared **INCOMPATIBLE** |
| AWS | `deploy/targets/aws.yaml` | EC2+Compose (simplest) |
| Azure | `deploy/targets/azure.yaml` | VM+Compose |
| GCP | `deploy/targets/gcp.yaml` | GCE+Compose |
| Kubernetes | `deploy/targets/kubernetes.yaml` | existing Helm; Flux optional |

Cloud **provisioning** stays READY_FOR_CREDENTIALS. That is not a packaging failure.

## Validators (do not replace G26)

```bash
python3 scripts/meos-platform-target-readiness.py
python3 scripts/meos-secret-scan.py
python3 scripts/meos-ext-g26-readiness.py
```

States are not collapsed: PACKAGE_READY ≠ CREDENTIALS_AVAILABLE ≠ DEPLOYED ≠ PRODUCTION_VERIFIED.

This phase **stops** after offline preparation. It does not create a new P354 because credentials are missing. Existing launch CLI may be used later; G26 remains the production gate.
