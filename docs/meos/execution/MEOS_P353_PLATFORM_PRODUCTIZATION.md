# MEOS P353 — Multi-platform productization & deployment factory

**Date:** 2026-08-19  
**Governance:** 11.0  
**Companion (release identity):** [MEOS_P353_RELEASE_ENGINEERING_REPORT.md](./MEOS_P353_RELEASE_ENGINEERING_REPORT.md)  
**Factory:** [MEOS_DEPLOYMENT_FACTORY.md](./MEOS_DEPLOYMENT_FACTORY.md)  
**Matrix:** [MEOS_PLATFORM_READINESS.v1.yaml](./MEOS_PLATFORM_READINESS.v1.yaml)  
**Customer:** [MEOS_CUSTOMER_DEPLOYMENT_GUIDE.md](./MEOS_CUSTOMER_DEPLOYMENT_GUIDE.md)

This document is the **deployment factory** narrative. It does **not** replace the clean-release report. It does **not** change G26, P0, P313, or GO-LIVE.

## Objective

Remove the “single production provider” bottleneck **without fabricating production**. One canonical application and one canonical deployment architecture, with environment adapters for Linux/VPS, Hostinger VPS, AWS, Azure, GCP, Kubernetes, Docker Compose DEMO, and local development.

## Frozen gates (unchanged)

```
G26_STATUS                = BLOCKED
G26_READY                 = FALSE
P0                        = 1
P313                      = NOT_CERTIFIED
P313_REENTRY_READY        = FALSE
PRODUCTION_CERTIFIED      = FALSE
GO_LIVE_READY             = FALSE
GO_LIVE_AUTHORIZATION     = NOT_APPROVED
ACTIVE_APPLICATIONS       = 0
PRODUCTION_TRAFFIC        = NOT_ENABLED
```

`READY_FOR_CREDENTIALS` is not `READY`. Localhost is not production. Compose is not production. Dirty SHA is not a release. Configured is not verified.

## What was built (no second architecture)

| Item | Location | Class |
|------|----------|-------|
| Factory index | `deploy/` | adapters only |
| Env profiles | `deploy/environments/` | placeholders, no secrets |
| Config contract | `deploy/environments/CONTRACT.v1.yaml` | CONFIGURED ≠ VERIFIED |
| DEMO commands | `deploy/scripts/meos-demo.sh` | NON_PRODUCTION |
| VPS / Hostinger | `deploy/vps/` · `deploy/hostinger/` | READY_FOR_CREDENTIALS |
| AWS / Azure / GCP | `deploy/aws/` · `azure/` · `gcp/` | READY_FOR_CREDENTIALS |
| Kubernetes | `deploy/kubernetes/` → existing Helm | READY_FOR_CREDENTIALS |
| CI matrix | `deploy/ci/DEPLOYMENT_MATRIX.v1.yaml` | no auto production |
| Validator | `scripts/meos-platform-readiness.py` | no mock PASS |
| Packages | `deploy/packages/` + `infrastructure/launch/commercial/` | no forks |

Canonical image remains `infrastructure/docker/images/backend.Dockerfile`. Release identity is digest, never `:latest`. Local image class: **NON_PRODUCTION**.

## Cloud path selection (simplest compatible)

- **AWS:** EC2 + Compose. EKS = Kubernetes adapter (same Helm).
- **Azure:** VM + Compose. AKS = Kubernetes adapter.
- **GCP:** GCE + Compose. GKE = Kubernetes adapter.

No competing AWS/Azure/GCP architectures. No provision without credentials.

## SaaS / marketplace (preparation only)

Hosted SaaS is **not** activated. Tenant model = Identity/Organization. Isolation = `tenant_id` in owning schemas (no cross-schema queries). Billing = existing license contract (`payment_execution: READY_FOR_CREDENTIALS`). Marketplace requirements remain design-only. No fake customers, payments, or production tenants.

## Clean release vs factory

Worktree dirt after productization files is expected until a human commit. Classify files; do not `git reset --hard`. `47258dfd-dirty` remains **FORBIDDEN_FOR_RELEASE**. Factory success does not require a clean SHA; **release** still does.

## Honesty

| Claim | Truth |
|-------|--------|
| LOCAL / DEMO READY | product packages exist |
| Cloud READY | **no** — READY_FOR_CREDENTIALS |
| Docker READY | Dockerfile + prior local build evidence |
| G26 | BLOCKED |
| Production | FALSE |

## Commands

```bash
python3 scripts/meos-platform-readiness.py
python3 scripts/meos-ext-g26-readiness.py
python3 scripts/meos-install.py --platform DEMO
./deploy/scripts/meos-demo.sh help
```

P313 is **not** started. GO-LIVE is **not** approved.
