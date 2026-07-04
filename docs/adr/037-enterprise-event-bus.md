# ADR-037: Enterprise Event Bus — Domain Events, Immutable Envelopes, Retry

## Status

Accepted

## Context

Marpich uses integration events for cross-module communication (ADR-010 Event Fabric). Product leadership requires a canonical **Enterprise Event Bus** design stating:

- Every business event becomes a **Domain Event**
- Published facts use a mandatory envelope: Tenant, Organization, Correlation ID, Timestamp, User, Security Context
- Events are **immutable**
- Explicit **publisher** and **subscriber** architecture
- **Retry** at dispatch and consumer layers

Existing `_envelope.v1.json` lacked organization, user, and security_context. `IntegrationEvent.envelope()` did not emit them.

## Decision

Adopt **`docs/architecture/ENTERPRISE_EVENT_BUS.md`** as canonical event bus law.

### Event flow

Aggregate → Domain Event → Application mapper → Integration Event → Outbox → EventFabric → Dispatcher → Kafka + InProcessEventBus → ACL subscribers

### Envelope (required)

`tenant_id`, `organization_id`, `user_id`, `correlation_id`, `occurred_at`, `security_context`, plus event identity fields and `payload`.

### Immutability

Frozen dataclasses; append-only outbox; compensating events for corrections; no envelope mutation.

### Publisher

Single entry: `EventFabric.publish()` / `publish_integration_event()`. Outbox in same transaction as aggregate persist.

### Subscriber

ACL in `infrastructure/acl/`; idempotent `(tenant_id, event_id, consumer_id)`; no peer domain imports.

### Retry

- **Dispatch:** outbox `retry_count`, exponential backoff, `platform.dead_letter_events`
- **Consume:** handler retry with idempotency guard; DLQ on exhaustion

### Code changes

- Extend `IntegrationEvent` and `DomainEvent` with `organization_id`, `user_id`, `security_context`
- Update `_envelope.v1.json` contract

## Consequences

- Contract tests validate expanded envelope
- Application services should pass GatewayContext metadata when publishing
- ADR-010 Event Fabric remains implementation layer beneath this design

## Alternatives considered

- Mutable event store with updates — rejected (audit/compliance)
- Direct handler calls — rejected (coupling)
- Optional metadata — rejected; keys required (nullable values for system events)
