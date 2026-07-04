# ADR-036: Integration Platform — Sole External Bridge

## Status

Accepted

## Context

Marpich connects to banks, payment gateways, government APIs, LMS systems, directories, ERP/CRM, and cloud storage. Without a canonical integration layer, business modules embed HTTP clients, duplicate retry logic, leak secrets, and bypass audit. The existing `integration` context provides connectors, webhooks, sync jobs, and logs — but lacks a unified enterprise design covering all provider categories, polling, ingress, DLQ, retry policies, contracts, and monitoring.

Product leadership mandated: **external systems connect ONLY through the Integration Platform.**

## Decision

Adopt **`docs/architecture/INTEGRATION_PLATFORM.md`** as canonical external connectivity law.

### Sole bridge

- All outbound third-party calls via Integration connectors/adapters
- All inbound partner callbacks via API Gateway → Integration ingress
- Business modules use ports/events — never vendor SDKs or raw HTTP in domain/application

### Supported integration categories

Bank APIs, payment gateways, SMS/email providers (adapter for Notification Service), government/tax/currency APIs, Moodle, Google Classroom, Microsoft 365, Google Workspace, LDAP, Active Directory, ERP/CRM connectors, cloud storage, custom REST.

### Platform capabilities

| Capability | Artifact |
|------------|----------|
| Connectors | `Connector` aggregate + per-vendor adapters |
| Webhooks | Outbound event fan-out + inbound ingress |
| Polling | Scheduling Platform + watermark cursors |
| Sync jobs | `SyncJob` + normalized record contracts |
| Error recovery | Retry with exponential backoff + circuit breaker |
| DLQ | `integration.dead_letter` + replay API |
| API contracts | `docs/architecture/integration/**/*.json` |
| Monitoring | Logs, metrics, alerts, connector health |

### Catalog

`docs/architecture/integration/CONNECTOR_CATALOG.yaml` — canonical connector type registry.

## Consequences

- New external systems require catalog entry + adapter + contract before module consumption
- Notification Service uses Integration adapters for SMS/email providers
- Identity consumes `integration.directory.synced` — not direct LDAP from identity module
- Ingress routes added to API Gateway route registry under `/integrations/ingress`

## Alternatives considered

- Per-module integrations — rejected (duplication, secret sprawl)
- iPaaS only (Zapier) — insufficient for enterprise bank/government/tax
- Direct module HTTP with shared library — rejected (violates bounded context isolation)
