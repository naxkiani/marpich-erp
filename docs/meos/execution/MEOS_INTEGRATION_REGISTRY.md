# MEOS Integration Registry

**Date:** 2026-08-18T06:51:00Z  
**Machine:** [MEOS_INTEGRATION_REGISTRY.v1.yaml](./MEOS_INTEGRATION_REGISTRY.v1.yaml)  
**Overall:** `active_count: 0` · **never ACTIVE without runtime evidence**

Catalog **types** (bank_api, payment_gateway, email_provider, …) live in `docs/architecture/integration/CONNECTOR_CATALOG.yaml`. Those are **not** live integrations.

| INTEGRATION_ID | NAME | TYPE | SOURCE | TARGET | PROTOCOL | AUTH | DATA_CLASS | TENANT | STATUS | HEALTH | LAST_SUCCESS | LAST_FAILURE |
|----------------|------|------|--------|--------|----------|------|------------|--------|--------|--------|--------------|--------------|
| `INT-REST-V1` | Platform REST | api | clients | MEOS | HTTPS REST `/api/v1` | JWT + tenant | mixed | header+JWT | **IMPLEMENTED** | NOT_AVAILABLE | NOT_AVAILABLE | NOT_AVAILABLE |
| `INT-OPENAPI` | OpenAPI contract | api | CI | gateway | OpenAPI | n/a | public paths listed | n/a | **TESTED** (contract pytest) | n/a | workstation tests | n/a |
| `INT-EVENT-OUTBOX` | Event fabric outbox | event | aggregates | consumers | outbox | internal | internal | envelope tenant_id | **TESTED** (P313 isolated E2E) | NOT_AVAILABLE (prod) | workstation | NOT_AVAILABLE |
| `INT-WH-CONSOLE` | Console webhook channel | webhook | integration | stdout | in-process | secret flag only | internal | tenant_id | **IMPLEMENTED** (dev) | n/a | test deliveries | n/a |
| `INT-WH-HTTP` | Partner HTTP webhooks | webhook | MEOS | partner URL | HTTPS | HMAC/secret **designed** | varies | tenant_id | **IMPLEMENTED_UNVERIFIED** | NOT_AVAILABLE | NOT_AVAILABLE | NOT_AVAILABLE |
| `INT-WH-INGRESS` | Inbound webhook ingress | webhook | partner | MEOS | HTTPS | designed | varies | must bind to auth context | **NOT_IMPLEMENTED** on `integration` router | — | — | — |
| `INT-SYNC` | Sync jobs | scheduled | connector | peer | job API | JWT | varies | tenant_id | **IMPLEMENTED_UNVERIFIED** | NOT_AVAILABLE | NOT_AVAILABLE | NOT_AVAILABLE |
| `INT-PLUGIN-RT` | Plugin invoke | plugin | host | sandbox | `/plugins/invoke` | JWT + grants | constrained | tenant_id | **TESTED** (unit/API) | NOT_AVAILABLE | tests | n/a |
| `INT-LIVEKIT` | LiveKit adapter | external | messenger | LiveKit | HTTPS | adapter keys | collab | tenant-scoped | **IMPLEMENTED_UNVERIFIED** | NOT_AVAILABLE | NOT_AVAILABLE | NOT_AVAILABLE |
| `INT-PAY` | Payment gateway | payment | finance/POS | PSP | catalog type | api_key/HMAC | financial | tenant | **DESIGNED** | — | — | — |
| `INT-BANK` | Bank API | financial | treasury | bank | catalog type | oauth/mtls | financial | tenant | **DESIGNED** | — | — | — |
| `INT-GOV` | Government/tax rails | regulatory | tax/gov | agency | catalog/docs | — | regulated | tenant | **NOT_IMPLEMENTED** as live | — | — | — |
| `INT-AI-LLM` | External LLM provider | ai | AI service | vendor | HTTPS | env secrets | prompts | tenant | **DISABLED** (stub assist) | — | — | — |
| `INT-WH-ENT` | `enterprise_webhook_platform` BC | webhook | scaffold | — | — | — | — | — | **DESIGNED**/profile-gated | Do not treat as second SoR | — | — |

Owner: **NOT_AVAILABLE** (not invented).  
Fragmentation note: prefer **`integration`** SoR for connectors/webhooks/sync. Do not operate a parallel ESB.
