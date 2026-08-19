# MEOS Multi-Platform Launch Matrix (P351)

**G26_READY remains FALSE** until EXT-G26 resources exist. Adapter ≠ production.

Statuses: IMPLEMENTED · CONFIGURED · READY_FOR_CREDENTIALS · READY_FOR_DEPLOYMENT · PRODUCTION_VERIFIED · BLOCKED · PARTIALLY_COMPATIBLE · INCOMPATIBLE · EXTERNAL_DEPENDENCY

| Target | Method | Status | External dependency |
|--------|--------|--------|---------------------|
| A LOCAL DEVELOPMENT | `scripts/dev-up.sh` + compose.dev | CONFIGURED | Docker optional for DB |
| B SINGLE SERVER / VPS | Compose meosprod + `scripts/meos-vps-bootstrap.sh` | READY_FOR_CREDENTIALS | Linux VPS, Docker, DNS |
| C DOCKER HOST | same Compose | CONFIGURED | Docker Engine |
| D HOSTINGER VPS | VPS package | PARTIALLY_COMPATIBLE | Hostinger **VPS** (not shared) |
| D HOSTINGER SHARED | — | INCOMPATIBLE | no Docker/K8s on typical shared |
| E AWS | Helm or VPS on EC2; managed RDS later | READY_FOR_CREDENTIALS | AWS account |
| F Azure | Helm or VM + Compose | READY_FOR_CREDENTIALS | Azure account |
| G GCP | Helm or GCE + Compose | READY_FOR_CREDENTIALS | GCP account |
| H Kubernetes | existing Helm/Flux | READY_FOR_CREDENTIALS | kubeconfig |
| I Managed Kubernetes | same Helm | READY_FOR_CREDENTIALS | managed cluster |

No target is PRODUCTION_VERIFIED.

## Hostinger

| Offer | Verdict |
|-------|---------|
| VPS with Docker | PARTIALLY_COMPATIBLE — use PROFILE_VPS / PROFILE_HOSTINGER_VPS |
| Shared hosting (PHP/FTP) | INCOMPATIBLE — MEOS is Python + Postgres + containers |

Do not force MEOS onto shared hosting.

Machine: [MEOS_PLATFORM_ADAPTER_STATUS.v1.yaml](./MEOS_PLATFORM_ADAPTER_STATUS.v1.yaml)
