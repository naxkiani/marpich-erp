# MEOS Integration Gap Report

**Date:** 2026-08-11

## Integration spine status

| Channel | Status | Gap |
|---------|--------|-----|
| REST `/api/v1` | Partial | Many specs; silent ModuleNotFound skips |
| JWT + X-Tenant-ID | Working | Shell widgets often omit headers |
| Integration events / outbox | Incomplete | Console publishers in places |
| Document Exchange (`document_id`) | Partial | Document studio uses Documents |
| Enterprise Search indexing | Partial | Indexing on events not universal |
| Workflow hooks | API-ready | UI + ACL consumers incomplete |
| Notification triggers | API-ready | Modules must not send channels directly |
| AI via `/api/v1/ai` | Partial | Module-local assistants still appear |

## P0/P1 integration actions

- **P0:** Shell → Search / Notifications / AI with same session headers as AuthProvider
- **P0:** Workflow desk calls `/api/v1/workflow/*` with session
- **P1:** Honest ROUTER_SPECS (remove or implement missing packages)
- **P1:** Durable outbox path for identity-critical events
- **P2:** Module activation → nav registry sync

## Forbidden regressions

- No new module-local LLM / SMTP / search engine
- No dual-write of peer domain tables
- No second auth stack in UI pages
