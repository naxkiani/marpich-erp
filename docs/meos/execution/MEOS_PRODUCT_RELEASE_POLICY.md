# MEOS Product Release Policy (P355)

Commercial identity is `MEOS_PRODUCT` plus `MEOS_RELEASE`. Dirty SHA is not a commercial artifact.

## Channels

DEV → ALPHA → BETA → RC → STABLE → LTS  

Silent promotion is **FORBIDDEN**. Each promotion requires explicit channel, version, `source_commit`, artifact, digest, release notes, and migration state.

Current channel while the worktree is dirty: **DEV** / `FORBIDDEN_DIRTY` (not STABLE).

## Versioning

Reuse `backend/pyproject.toml` `0.1.0`. Helm `appVersion` `7.0.0` is a **VERSIONING_GAP**, not a new product version.

## Packages

`infrastructure/launch/commercial/{DEMO,SELF_HOSTED,VPS,KUBERNETES,CLOUD_READY}/`  
No secrets. Distribution (GHCR/download) requires explicit authorization. Publish remains P354 `--confirm-publish`.

See [MEOS_VERSION_COMPATIBILITY.v1.yaml](./MEOS_VERSION_COMPATIBILITY.v1.yaml) · [MEOS_RELEASE_OPERATIONS.md](./MEOS_RELEASE_OPERATIONS.md)
