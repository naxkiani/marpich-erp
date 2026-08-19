# MEOS Release Engineering Runbook (P353)

**Dirty SHA is not a certified release.** After P353, release identity is the clean commit recorded in [MEOS_RELEASE_MANIFEST.v1.yaml](./MEOS_RELEASE_MANIFEST.v1.yaml).  
Do not `git reset --hard`. Do not delete user work. Do not invent a GHCR digest.

Local clean SHA ≠ production certification. G26 remains independent.

## Canonical sequence

```
WORKTREE CLEAN
  → COMMIT (authorized)
  → TEST (pytest / existing CI test-federation)
  → BUILD (backend.Dockerfile)
  → IMAGE + IMMUTABLE DIGEST (GHCR; CI records steps.image.outputs.digest)
  → REGISTRY ghcr.io/marpich/marpich-backend
  → DEPLOY Helm --set image.tag=sha-<commit> --set-string image.digest=<digest>
     or VPS Compose MEOS_IMAGE=ghcr.io/marpich/marpich-backend@sha256:<digest>
  → VERIFY probes + G26 validator (production only when EXT-G26 exists)
```

Forbidden as certification evidence: `latest`, dirty describe, local-only image id, compose `:5444`, localhost `/health`.

## Existing CI (do not replace)

`.github/workflows/identity-federation-enterprise.yml`

- Tags `:7.0.0` (mutable) **and** `:sha-${{ github.sha }}`
- Artifact `meos-image-digest`
- Staging/production Helm pass `image.digest`
- Production job still runs `helm rollback marpich-iam 0` on failure (**CONFIGURED**, not PRODUCTION_VERIFIED)
- GHCR push requires GitHub Actions credentials — workstation **READY_FOR_CREDENTIALS**

## VPS / Hostinger VPS

Set `MEOS_IMAGE` to `repository@sha256:<digest>`. Rollback uses `MEOS_PREVIOUS_IMAGE`. See `scripts/meos-vps-bootstrap.sh`.

## Kubernetes

Helm helper `marpich-iam.image` uses `image.digest` when set. Default production values leave digest empty (**NOT_AVAILABLE**) until CI supplies it.

## Demo release path

1. Clean source (`git status --short` empty).
2. Known local image (`meos/backend:p353-local` or Compose build).
3. Demo database: `infrastructure/docker/compose/docker-compose.dev.yml` Postgres `:5433`.
4. No production secrets. No production traffic.

## Identity proof (when deployed)

`DEPLOYED_COMMIT = CLEAN_COMMIT`  
`DEPLOYED_IMAGE_DIGEST = CI_ARTIFACT_DIGEST`
