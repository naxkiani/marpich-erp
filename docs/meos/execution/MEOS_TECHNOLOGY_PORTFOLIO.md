# MEOS Technology Portfolio

**Date:** 2026-08-19T06:15:00Z  
**Evidence:** `package.json`, `backend/pyproject.toml`, `infrastructure/docker/compose/docker-compose.dev.yml`, local runtime 2026-08-18/19.  
**Not** a CMDB or cloud bill.

## Inventory (actual)

| Layer | Technology | Lifecycle now |
|-------|------------|----------------|
| Language | Python ≥3.12, TypeScript 5 | **RETAIN** |
| API | FastAPI, Uvicorn | **RETAIN** |
| UI | Next.js 15, React 19 | **RETAIN** |
| Database | PostgreSQL 16 | **RETAIN** (prod required) |
| Default persistence | SQLAlchemy + **memory** default | **MONITOR** — prod must be postgres |
| Cache | Redis 7 | **RETAIN** |
| Messaging | `apache/kafka-native:3.9.1`; app often `EVENT_BUS_MODE=direct` | **ADOPT** native image locally; **MONITOR** bus mode |
| Object storage | MinIO (S3 API) | **RETAIN** for local/offsite pattern |
| Observability images | OTel, Prometheus, Grafana (compose **profile**) | **MONITOR** — not default `docker:up` |
| CI | GitHub Actions | **RETAIN** |
| Legacy | NestJS `services/*` (gateway 4000, identity 4001, …) | **CONSOLIDATE** toward FastAPI — usage **NOT_MEASURED** |
| Removed | `bitnami/kafka:3.7` | **RETIRED_FROM_HUB** — replaced in compose |

GraphQL: documented intent; runtime **NOT_AVAILABLE**.

## Cost / support

LICENSE / INFRA / OPS / SUPPORT / DEV / INTEGRATION cost: **NOT_MEASURED**. No invoices attached.

## Rules

Do not force framework upgrades for “modernization.” Kafka image change was evidence-backed (Hub 404), not preference.
