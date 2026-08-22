# MEOS Environment Contract (P398)

Companion to `MEOS_ENVIRONMENT_CONTRACT.v1.yaml` (P364 field contract). Values remain references only.

## Flow

INPUT → PLAN → VALIDATE → APPROVE → BOOTSTRAP → VERIFY → READY

Every step produces evidence. No step stores secret values.

## Separation

APPLICATION ARTIFACT ≠ INFRASTRUCTURE ≠ ENVIRONMENT CONFIGURATION ≠ SECRETS ≠ PROVIDER ≠ DEPLOYMENT

P397 supplies the immutable release. P398 supplies the deterministic environment. P396 deploys only after both are valid.

## Production

Production bootstrap stays locked until provider, credentials, plan approval, secret manager, DNS, public-CA TLS, backup, observability, G26, P313, and GO-LIVE authorization all exist. This factory cannot set `G26_READY`.
