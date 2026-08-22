# MEOS P352 — Product Infrastructure Hardening

**Date:** 2026-08-19T08:05:00Z  
**P352_STATUS:** PRODUCT_INFRASTRUCTURE_HARDENED  
**COMPOSE_IS_PRODUCTION:** FALSE  
**G26_READY:** FALSE · **P0:** 1 · **P313:** NOT_CERTIFIED · **GO_LIVE:** NOT_APPROVED  

P352 executed P351 packages. It did not provision cloud, fake a registry digest, deploy `47258dfd-dirty`, start P313, or GO-LIVE.

## Canonical runtime (one)

| Item | Evidence |
|------|----------|
| Runtime | Python 3.12 FastAPI (`core.presentation.api.main:app`) |
| Port | 8000 (Compose demo maps 8080) |
| Database | PostgreSQL 16; local `:5433` / compose `:5444` NON_PRODUCTION |
| Cache | Redis (compose) |
| Events | Outbox (`EVENT_BUS_MODE=outbox` in demo/prod profile); Kafka optional |
| Storage | MinIO interface (workstation) |
| Proxy | Caddy (self-signed = DEVELOPMENT ONLY) |
| Health | `GET /api/v1/health` process ok |
| Live | `GET /api/v1/live` |
| Ready | `GET /api/v1/ready` dependency (Postgres SELECT 1 when persistence=postgres) |

Helm readiness probe now uses `/api/v1/ready` (was incorrectly `/health`).

## Executed evidence

| Check | Result |
|-------|--------|
| Docker build `meos/backend:p352-local` | **PASS** (image_id recorded; registry digest NOT_AVAILABLE) |
| Migration check (55 SQL, no apply) | **PASS** |
| Local backup `:5433` | **PASS** (740566 bytes) — **not** PRODUCTION_BACKUP |
| Restore → `marpich_platform_p352_restore` | **PASS** — production restore **NOT_VERIFIED** |
| pytest health/ready/live + tenant isolation + settings | **40 passed** |
| Helm CLI | **MISSING** (chart templates validated in-repo) |
| GHCR push | **READY_FOR_CREDENTIALS** |
| Dirty SHA deploy | **FORBIDDEN** |

## Product vs production

LOCAL_READY / DEMO_READY / DOCKER_BUILD_READY may be TRUE while G26_READY remains FALSE. That is the intended split.
