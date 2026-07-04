# ADR-010: Enterprise Event Fabric

## Status

Accepted

## Context

Cross-context communication in Marpich uses versioned **integration events**. The initial implementation used an in-process event bus suitable for development and tests, but production requires:

- **Transactional outbox** so domain commits and event publication are atomic
- **At-least-once delivery** with **idempotent consumers**
- Optional **Kafka fan-out** for external systems and future microservice extraction
- **Dead-letter** storage for failed dispatches

## Decision

Introduce an **Event Fabric** layer with three modes:

| Mode | Use case |
|------|----------|
| `direct` | Local dev and unit/integration tests — in-process delivery |
| `outbox` | Production modular monolith — durable enqueue + dispatcher |
| Kafka (optional) | External consumers when `kafka_enabled=true` |

### Components

1. **`EventFabric.publish()`** — single entry point for all contexts
2. **`OutboxRepository`** — memory (tests) or PostgreSQL (`platform.outbox`)
3. **`OutboxDispatcher`** — polls unpublished rows, publishes to Kafka, delivers to in-process subscribers
4. **`ProcessedEventStore`** — deduplication ledger (`platform.processed_events`)
5. **`InProcessEventBus.deliver()`** — wraps handlers with idempotency keys `(tenant_id, event_id, consumer_id)`

### Schema

Migration `013_event_fabric.sql` extends `platform.outbox` and adds:

- `platform.processed_events` — consumer deduplication
- `platform.dead_letter_events` — failed dispatch audit trail

### Configuration

```env
EVENT_BUS_MODE=direct|outbox
OUTBOX_POLL_INTERVAL_MS=500
OUTBOX_BATCH_SIZE=100
OUTBOX_DISPATCH_IMMEDIATE=true
KAFKA_ENABLED=false
KAFKA_BOOTSTRAP_SERVERS=
```

### Rules

- Contexts MUST publish via `publish_integration_event()` / `EventFabric.publish()` — never call handlers directly
- Handlers MUST be idempotent; the ledger guards against duplicate delivery
- No bounded context imports another context's domain layer

## Consequences

- Production deployments set `event_bus_mode=outbox` and run the dispatcher in the API lifespan
- Tests reset fabric state via `EventFabric.reset_dev_state()`
- Kafka is optional; without `aiokafka` the transport no-ops safely
- Future work: transactional outbox in same DB session as domain writes (unit of work pattern)
