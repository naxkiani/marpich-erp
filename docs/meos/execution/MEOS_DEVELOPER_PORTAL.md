# MEOS Developer Portal

**Date:** 2026-08-18T11:30:00Z  
**Law:** Use existing MEOS UX and docs. **Do not invent a second portal product.**

## Authoritative surfaces (actual)

| Need | Where | Auth |
|------|--------|------|
| API reference | FastAPI `/api/docs` · `/api/redoc` · `/api/openapi.json` | Public schema; **calls** still need JWT/tenant |
| Plugin marketplace | `/enterprise/plugins` (P320 AppShell) | `plugins.marketplace.read` |
| Event contracts | `docs/architecture/events/` | Repo |
| Manifest / SDK | `packages/plugin-sdk` · `PLUGIN_MANIFEST.v1.json` | Repo |
| Connector types | `docs/architecture/integration/CONNECTOR_CATALOG.yaml` | Repo |
| Certification | [MEOS_PLUGIN_CERTIFICATION.md](./MEOS_PLUGIN_CERTIFICATION.md) | Honesty: **0 CERTIFIED** |
| Global search | Enterprise Search `/api/v1/search` | JWT + per-hit ACL |

Royal blue / AppShell / Task Center / Notification Center remain the shell. No separate visual language.

## Not SoR

| Surface | Why |
|---------|-----|
| EIS “Developer Portal” panel | Integration Studio seed UI — not Plugin SDK, not OpenAPI SoR |
| Architecture essays naming `DeveloperPortalService` | Catalog/design docs — **not** a live portal app |
| Imaginary `https://developers.marpich.com` | **NOT_IMPLEMENTED** |

## Search

Do not add a second developer search engine. Indexing of API/event docs in Enterprise Search: **not evidenced** as a dedicated developer corpus. Operators use repo + OpenAPI.

## Certification / testing pages

Marketplace UI can install/enable DEMO seeds. It does **not** run CVE scans or mark CERTIFIED. Portal copy must keep `plugins.notCertified`.
