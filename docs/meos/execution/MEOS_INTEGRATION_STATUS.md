# MEOS Integration Status

**Date:** 2026-08-12

## Channels in use

| Channel | Status |
|---------|--------|
| REST `/api/v1/*` | Primary; many routers live |
| Integration events + outbox | Present in identity/platform patterns; not fully proven E2E for all modules |
| ACL consumers | Partial |
| Document Exchange | `document_id` refs in desks |
| Search indexing | Event-driven design; memory index by default |
| Notifications | API + inbox; shell must send JWT |
| Workflow | Definitions/tasks APIs exist; FE Task Center Wave 01 |

## Blockers

1. Shell clients omitting auth → 401 → fake UX  
2. Missing packages still listed in startup registry  
3. Default memory → no durable cross-process event consumers  

## Wave 01 actions

- Auth headers on shell integrations  
- Gate missing routers  
- Document Postgres activation for identity, notifications, search, audit, workflow  
- Workflow Task Center consumes existing APIs only (no new engine)
