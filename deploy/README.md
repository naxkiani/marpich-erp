# MEOS Deployment Factory (index)

**Law:** ONE product · ONE image (`infrastructure/docker/images/backend.Dockerfile`) · ONE config contract · MULTIPLE adapters.

This directory does **not** contain a second application, CI, or Kubernetes controller. Every path below **reuses** `infrastructure/` and `scripts/`.

| Adapter | Canonical artifact | Class |
|---------|--------------------|-------|
| docker/ | `infrastructure/docker/images/backend.Dockerfile` | NON_PRODUCTION until GHCR digest |
| compose/ | `docker-compose.dev.yml` + `docker-compose.meos-prod.yml` | LOCAL / DEMO |
| vps/ | `scripts/meos-vps-bootstrap.sh` + Compose | READY_FOR_CREDENTIALS |
| hostinger/ | same as vps/; shared hosting INCOMPATIBLE | READY_FOR_CREDENTIALS |
| aws/ | EC2 + Compose (simplest); EKS uses kubernetes/ | READY_FOR_CREDENTIALS |
| azure/ | Azure VM + Compose; AKS uses kubernetes/ | READY_FOR_CREDENTIALS |
| gcp/ | Compute Engine + Compose; GKE uses kubernetes/ | READY_FOR_CREDENTIALS |
| kubernetes/ | `infrastructure/kubernetes/helm/marpich-iam` (+ optional Flux) | READY_FOR_CREDENTIALS |
| environments/ | profiles + CONTRACT — placeholders only | no secrets |
| scripts/ | one-command DEMO/LOCAL wrappers | NON_PRODUCTION |

`ENV_PRODUCTION` is a **profile**, not a certified environment. G26 remains independent.

Operator: `python3 scripts/meos-platform-readiness.py`
