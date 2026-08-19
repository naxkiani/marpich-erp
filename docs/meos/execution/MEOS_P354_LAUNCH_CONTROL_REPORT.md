# MEOS P354 — Unified Launch Control Report

**Date:** 2026-08-19  
**CLI:** `python3 scripts/meos-launch.py`  
**Installer (unchanged):** [MEOS_P354_UNIVERSAL_INSTALLATION.md](./MEOS_P354_UNIVERSAL_INSTALLATION.md)  
**Registry:** [MEOS_ENVIRONMENT_REGISTRY.v1.yaml](./MEOS_ENVIRONMENT_REGISTRY.v1.yaml)  
**Dashboard overlay:** [MEOS_LAUNCH_CONTROL.v1.yaml](./MEOS_LAUNCH_CONTROL.v1.yaml)

P354 launch control is an **orchestration layer**. It reuses P353 adapters, Compose, VPS bootstrap, Helm/Flux, existing CI, backup/restore, and the G26 validator. It does **not** create a second deployment platform.

## Operator flow

1. SELECT PLATFORM — `python3 scripts/meos-launch.py list`
2. CHECK PREFLIGHT — `preflight --env <env>`
3. VIEW BLOCKERS — JSON `blockers` / `credentials.missing`
4. GENERATE PLAN — `plan --env <env>` (no deploy)
5. CONFIRM — `--confirm yes` (no confirmation → `NOT_EXECUTED`)
6. DEPLOY — LOCAL/DEMO execute existing scripts; cloud is not simulated
7. VERIFY — probes + independent G26 (not inferred from exit code)
8. RECEIVE REPORT — this document + CLI JSON

Forbidden: `--force` · `--skip-g26` · `--production-anyway` · `--ignore-certification`

## Matrix

| PLATFORM | PREFLIGHT | PLAN | DEPLOYMENT | VERIFICATION | BLOCKERS | NEXT_ACTION |
|----------|-----------|------|------------|--------------|----------|-------------|
| LOCAL | READY (if Docker) | PLAN_READY | executable NON_PRODUCTION | `/health` + `/ready` on :8000 | dirty SHA ≠ release | `deploy --env local --confirm yes` |
| DEMO | READY (if Docker) | PLAN_READY | executable NON_PRODUCTION | :8080 probes | compose ≠ production | `deploy --env demo --confirm yes` |
| VPS | READY_FOR_CREDENTIALS | plan only | NOT_EXECUTED | n/a | SSH | supply host |
| HOSTINGER_VPS | READY_FOR_CREDENTIALS | plan only | NOT_EXECUTED | n/a | SSH; shared **INCOMPATIBLE** | Hostinger VPS only |
| AWS | READY_FOR_CREDENTIALS | plan only | NOT_EXECUTED | n/a | AWS keys | EC2+Compose path |
| AZURE | READY_FOR_CREDENTIALS | plan only | NOT_EXECUTED | n/a | Azure identity | VM+Compose path |
| GCP | READY_FOR_CREDENTIALS | plan only | NOT_EXECUTED | n/a | GCP identity | GCE+Compose path |
| KUBERNETES | READY_FOR_CREDENTIALS | plan only | NOT_EXECUTED | n/a | kubeconfig, digest | existing Helm |
| PRODUCTION | DEPLOYMENT_BLOCKED | blocked | BLOCKED | G26 FALSE | G26, P313, GO-LIVE | do not start P313 |

`READY_FOR_CREDENTIALS` is not `READY`. Localhost/Compose databases are not production.

## Frozen gates

```
G26_READY = FALSE
P0 = 1
P313 = NOT_CERTIFIED
PRODUCTION_CERTIFIED = FALSE
GO_LIVE_READY = FALSE
GO_LIVE_AUTHORIZATION = NOT_APPROVED
ACTIVE_APPLICATIONS = 0
PRODUCTION_TRAFFIC = NOT_ENABLED
```

Dirty tree: release deploy **BLOCKED**. Do not `git reset --hard`. `47258dfd-dirty` remains **FORBIDDEN_FOR_RELEASE**.

## Commands

```bash
python3 scripts/meos-launch.py list
python3 scripts/meos-launch.py preflight --env demo
python3 scripts/meos-launch.py plan --env aws
python3 scripts/meos-launch.py deploy --env demo --confirm yes
python3 scripts/meos-launch.py verify --env demo
python3 scripts/meos-launch.py status
python3 scripts/meos-launch.py rollback --env demo --confirm yes
python3 scripts/meos-ext-g26-readiness.py
```
