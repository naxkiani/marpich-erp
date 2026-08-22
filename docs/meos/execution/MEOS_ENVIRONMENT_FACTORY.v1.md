# MEOS Universal Environment Factory (P398)

Coordinates existing P364/P390/P394 environment tools. Not a second Kubernetes, CI/CD, secrets, or observability platform. Not GO-LIVE.

- CLI: `python3 scripts/meos-environment-factory.py status`
- No-arg CLI remains the P364 reference factory
- Control plane: `python3 scripts/meos-environment-control.py`
- Terraform for MEOS: **FORBIDDEN** (identity-digital-twin stub is not MEOS IaC)

## Contract

INPUT → PLAN → VALIDATE → APPROVE → BOOTSTRAP → VERIFY → READY

Destroy requires `destroy-plan` plus separate authorization. Production destroy stays **FORBIDDEN**.

## Commands

`status` · `inspect` · `plan` · `validate` · `bootstrap` · `verify` · `drift` · `destroy-plan`

Without credentials, cloud providers return **AUTHENTICATION_REQUIRED** / **READY_FOR_CREDENTIALS**. Local work is **LOCAL_ONLY**. Cost unknown is **COST_ESTIMATE_UNAVAILABLE**, never a fake zero.

## Status

`P398_STATUS=ENVIRONMENT_FACTORY_READY_EXTERNAL_INFRASTRUCTURE_REQUIRED`
