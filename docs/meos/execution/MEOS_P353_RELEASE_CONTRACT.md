# MEOS P353 — Release contract

**Authoritative machine manifest:** [MEOS_RELEASE_MANIFEST.v1.yaml](./MEOS_RELEASE_MANIFEST.v1.yaml)

## Required chain

```
SOURCE → CLEAN GIT TREE → COMMIT SHA → TEST → BUILD → IMAGE → IMMUTABLE DIGEST → RELEASE MANIFEST → TARGET DEPLOYMENT
```

`latest` is **FORBIDDEN** as certification identity. Dirty SHA (including `47258dfd-dirty`) is **FORBIDDEN_FOR_RELEASE**. Do not `git reset --hard`.

## Manifest fields

| Field | Rule |
|-------|------|
| release_id | recorded |
| commit_sha | clean commit only for release |
| build_id | CI run id or NOT_AVAILABLE |
| image | repository reference |
| image_digest | GHCR/CI `sha256:…` or **NOT_AVAILABLE** (do not invent) |
| created_at | ISO-8601 |
| application_version | `backend/pyproject.toml` (currently `0.1.0`; Helm `appVersion` `7.0.0` is a VERSIONING_GAP) |
| database_migration_version | latest `infrastructure/docker/migrations` prefix |
| supported_targets | LOCAL DEMO VPS HOSTINGER_VPS AWS AZURE GCP KUBERNETES |
| security_status | secret scan PASS/FAIL |
| test_status | pytest evidence |

Local Docker `Id` is **BUILD_VALIDATION**, not IMAGE_DIGEST.

## Current recorded digest

`image_digest: NOT_AVAILABLE` in the manifest. Registry push remains READY_FOR_CREDENTIALS.

Production deployment additionally requires G26 → P313 → human GO-LIVE. This contract does not certify production.
