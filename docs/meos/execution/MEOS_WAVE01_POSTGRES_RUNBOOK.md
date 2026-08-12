# MEOS Wave 01 Postgres Persistence Runbook

## Default

`PERSISTENCE_BACKEND=memory` (or unset) — suitable for local UI demos only. Data does not survive process restart or multi-instance.

## Enable Postgres for Wave 01 cores

```bash
export PERSISTENCE_BACKEND=postgres
export DATABASE_URL=postgresql+asyncpg://USER:PASS@HOST:5432/marpich
# plus any project-specific DB settings already in shared/infrastructure/settings.py
```

## Wave 01 contexts that must be durable for Functional demos

- `identity`  
- `notifications`  
- `search`  
- `audit`  
- `workflow`  
- `organization` / `settings`  
- `core_platform`  

Reuse existing `postgres_store` adapters — **do not** invent a second persistence engine.

## Verify

1. Start API with Postgres backend  
2. Register/login  
3. Create notification / index document / workflow task  
4. Restart API → data still present  
5. Confirm tenant isolation (`X-Tenant-ID`)

## Non-goals

Industry scaffolds (CRM/tax/HR) are out of scope until Wave 02. Do not enable Postgres for missing packages.
