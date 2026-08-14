# MEOS Wave 01 Postgres Persistence Runbook

## Default

`PERSISTENCE_BACKEND=memory` (or unset) — suitable for local UI demos only. Data does not survive process restart or multi-instance.

## Enable Postgres for Wave 01 cores

Host port **5432 is often already taken**. Compose maps Marpich Postgres to **5433** by default (`MARPICH_PG_HOST_PORT`).

```bash
# 1) Start durable deps (Postgres on host :5433)
docker compose -f infrastructure/docker/compose/docker-compose.dev.yml up -d postgres

# Optional: reuse host Redis if :6379 is already up
export PGHOST=127.0.0.1
export PGPORT=5433
export PGUSER=marpich
export PGPASSWORD=marpich
export PGDATABASE=marpich_platform
# Wave 01 cores only (identity → search/policy/RLS). Federation+ migrations are optional.
export MEOS_WAVE01_ONLY=1
./scripts/wait-for-services.sh   # or: pg_isready -h 127.0.0.1 -p 5433 -U marpich
./scripts/run-migrations.sh

# 2) Backend env (backend/.env)
export PERSISTENCE_BACKEND=postgres
export DATABASE_URL=postgresql+asyncpg://marpich:marpich@127.0.0.1:5433/marpich_platform
```

Override host port if needed: `MARPICH_PG_HOST_PORT=5432 docker compose ... up -d postgres`

## Wave 01 contexts that must be durable for Functional demos

- `identity`  
- `notifications`  
- `search`  
- `audit`  
- `workflow`  
- `organization` / `settings`  
- `core_platform`  

Reuse existing `postgres_store` adapters — **do not** invent a second persistence engine.

## Verify (user loop)

```bash
./scripts/meos-wave01-user-loop.sh
```

Or manually:

1. Start API with Postgres backend  
2. Register/login  
3. Create notification / index document / workflow task  
4. Restart API → data still present  
5. Confirm tenant isolation (`X-Tenant-ID`)

## Non-goals

Industry scaffolds (CRM/tax/HR) are out of scope until Wave 02. Do not enable Postgres for missing packages.
