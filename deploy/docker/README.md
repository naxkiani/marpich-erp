# Canonical Docker image (NON_PRODUCTION until GHCR digest exists)

**Dockerfile:** `infrastructure/docker/images/backend.Dockerfile`  
**Context:** `backend/`  
**Do not use `:latest` as release identity.**

```bash
docker build -f infrastructure/docker/images/backend.Dockerfile -t meos/backend:local-build backend
```

Local `Id` is BUILD_VALIDATION, not REGISTRY_PROVENANCE. Health: `/api/v1/health`. Readiness: `/api/v1/ready`.
