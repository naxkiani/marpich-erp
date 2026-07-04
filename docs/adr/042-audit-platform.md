# ADR-042: Enterprise Audit Platform — Immutable Audit Every Operation

## Status

Accepted

## Context

Platform Charter and Security Standard require audit on every action. The existing `audit` context provides event-driven ingestion via `*`, query, export, retention, and `AuditEntry` aggregate — but lacks canonical design for all tracked categories (API calls, DB changes, medical/academic access, document downloads, AI actions), full canonical envelope (organization, IP, browser, location, old/new value, reason), and tamper-evident immutability.

Compliance requirements: HIPAA, SOX, FERPA, GDPR.

## Decision

Adopt **`docs/architecture/ENTERPRISE_AUDIT_PLATFORM.md`** as canonical audit law.

### Audit every operation

Login, logout, API calls, database changes, permission changes, workflow, financial, medical, academic, document downloads, AI actions.

### Canonical store fields

Timestamp, user, tenant, organization, IP, browser, location, old value, new value, reason — plus severity, resource, integrity chain.

### Immutability

Append-only `AuditEntry`; no updates/deletes except retention policy job (itself audited). Target SHA-256 hash chain.

### Ingestion

1. Integration events (`*` subscription) — primary
2. API Gateway `api.request.completed` — HTTP audit
3. Direct `POST /audit/entries` — sensitive sync paths

Modules never maintain local audit tables.

## Consequences

- Extend `AuditEntry` and event mapper for canonical fields
- Gateway publishes structured API audit events
- Modules must emit access events for PHI/FERPA/document reads
- Integrity hash chain implementation planned

## Alternatives considered

- Per-module audit tables — rejected (compliance fragmentation)
- Mutable audit logs with admin edit — rejected (SOX/HIPAA)
- Log-only without structured store — rejected (query/export requirements)
