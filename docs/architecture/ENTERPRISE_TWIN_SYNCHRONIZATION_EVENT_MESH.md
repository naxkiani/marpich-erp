# Twin Synchronization Engine & Event Mesh — Architecture Law

**Prompt:** V03-C02-P199-B · Volume 03 · Chapter 02  
**Governance:** Enterprise Architecture Governance 10.0  
**Status:** Canonical — production architecture (not a demo brief)  
**ADR:** [ADR-207](../adr/207-twin-synchronization-engine-event-mesh.md)  
**Extends:** [ADR-203](../adr/203-enterprise-identity-digital-twin.md) · [ADR-203a](../adr/203a-digital-twin-type-catalog.md)  
**Companion:** [ENTERPRISE_IDENTITY_DIGITAL_TWIN_PLATFORM.md](ENTERPRISE_IDENTITY_DIGITAL_TWIN_PLATFORM.md)

**Law:** Twin synchronization is a **projection pipeline**. The Enterprise Event Mesh is a **binding profile** over Event Fabric + Message Orchestration — never a second bus. External systems enter only through the **Integration Platform**. Sync modes, topics, routing, retries, and conflict rules are **catalog- and policy-driven**.

---

## Hard reuse map (anti-duplication)

| Layer | Owner | 199-B role |
|-------|-------|------------|
| Twin Sync Engine | `identity_digital_twin` (logical pack) | Coordinator, workers, delta, conflict, modes, metrics |
| Event Mesh | Event Fabric (ADR-010) + Enterprise Event Bus (ADR-175) + Message Orchestration (ADR-178) | Topics, schema registry, DLQ, replay, priority |
| External connectors | Integration Platform (ADR-036) | REST/SOAP/GraphQL/gRPC/CDC/LDAP/SCIM/SFTP/… |
| Job timing | Enterprise Scheduler | Batch / scheduled sync ticks |
| Gates | Policy Engine | Sync policies per source domain |
| Durable audit | Audit Platform | Consume sync/conflict events |

```text
Source SoR / Partner / IoT
        │ (external only)
        ▼
Integration Platform ──► integration.* events
        │
        ▼
Event Fabric / Mesh profile ──► twin sync topics + DLQ
        │
        ▼
Twin Sync Engine (workers) ──► Twin BC aggregates (projection)
        │
        ▼
identity_twin.* events ──► Analytics / AuthZ facets / Search / AI
```

---

## SECTION 1 — Twin Synchronization Engine

### 1.1 Components

| Component | Responsibility |
|-----------|----------------|
| **Synchronization Coordinator** | Accepts sync intents; selects mode; partitions work by `(tenant_id, kind, subject_ref)`; tracks `SyncRun` lifecycle |
| **Synchronization Scheduler** | Emits ticks via Enterprise Scheduler (`twin.sync.schedule.*`); never embeds cron in domain |
| **Synchronization Workers** | Execute unit of work; pull from sync queue; idempotent per `(tenant_id, sync_run_id, work_item_id)` |
| **Conflict Detection Engine** | Detects concurrent facet writes / source-version collisions / LWW vs vector-clock mismatches |
| **Conflict Resolution Engine** | Applies **policy-selected** strategy (source_wins, twin_wins, merge_json, manual_escalate, workflow) |
| **Version Manager** | Monotonic `TwinVersion`; records `source_versions` map per upstream event |
| **State Manager** | Applies facet merges to `twin_states` / `DigitalTwin` |
| **Delta Processor** | Computes JSON Patch / facet-level deltas for incremental sync |
| **Snapshot Generator** | Creates immutable snapshots on schedule or significant sync |
| **Recovery Manager** | Replay from snapshots + event cursor; rebuild from SoR full sync when corrupted |
| **Synchronization Queue** | Logical queue on Message Orchestration (priority queues); not an ad-hoc Redis list in domain |
| **Synchronization Policies** | Policy Engine keys (Section 6) |
| **Synchronization Metrics** | OTel metrics + Analytics business metrics (Section 9) |

### 1.2 Sync modes (configurable)

| Mode | Trigger | Typical use |
|------|---------|-------------|
| Real-time | Integration / domain event | Identity login, risk score |
| Near real-time | Buffered micro-batch (≤ N seconds) | High-churn attributes |
| Batch | Scheduler window | Nightly industry packs |
| Scheduled | Cron expression via Scheduler | Compliance snapshots |
| Manual | `POST .../sync` | Operator repair |
| Incremental | Delta Processor | Partial facet update |
| Full | Full projection replace | Recovery / onboarding |
| Cross-tenant | Shared-scope grant + policy | Partner twin visibility |
| Cross-region | Region router + residency policy | Multi-region active-active |

### 1.3 SyncRun aggregate (new)

| Field | Notes |
|-------|-------|
| `sync_run_ref` | Unique per tenant |
| `mode` | From catalog |
| `twin_ref` / `scope` | Single twin or kind-wide |
| `status` | `queued|running|completed|failed|conflict|cancelled` |
| `stats` | items, lag_ms, conflicts |
| `correlation_id` | Propagated end-to-end |

Emits: `identity_twin.synchronization.started|completed|failed`, `identity_twin.conflict.detected|resolved`.

### 1.4 Industry coverage (event packs — not twin connectors)

Identity, ERP, Financial, Banking, FX, Treasury, Tax, HR, Payroll, CRM, Procurement, Inventory, Healthcare, University, Government, Construction, Retail, Manufacturing, AI, IoT, Mobile/Desktop apps, Partners, Third-party APIs — each **publishes** normalized integration/domain events. Twin Sync Engine **subscribes** with ACL mappers registered in catalog. **No** `httpx` to banks from twin workers.

---

## SECTION 2 — Enterprise Event Mesh

### 2.1 Definition

**Event Mesh** = multi-transport **binding + governance plane** over:

- Event Fabric (outbox, publish API, envelope)
- Enterprise Event Bus (topic catalog, schema registry UI/API)
- Message Orchestration (priority, delayed, DLQ, replay, exactly-once governance)

Transports (registry-configured): Apache Kafka · Apache Pulsar · NATS · RabbitMQ · Azure Event Grid · AWS EventBridge · Google Pub/Sub. Pulsar/Event Grid added by **extending** transport registry (ADR-175 amendment via ADR-207) — not a new BC.

### 2.2 Topics (twin profile — names from catalog)

| Topic | Purpose | Partitions guidance |
|-------|---------|---------------------|
| `marpich.twin.lifecycle.v1` | create/update/delete/activate/… | Hash `tenant_id` |
| `marpich.twin.sync.v1` | sync started/completed/failed + synchronized | Hash `tenant_id:twin_ref` |
| `marpich.twin.intelligence.v1` | predict/simulate/drift/anomaly | Hash `tenant_id` |
| `marpich.twin.security.v1` | trust/risk/compromise | Hash `tenant_id` |
| `marpich.twin.graph.v1` | relationships | Hash `tenant_id` |
| `marpich.twin.compliance.v1` | compliance facet | Hash `tenant_id` |
| `marpich.twin.dlq.v1` | dead letters | Low partition count |

Consumer groups (examples): `twin-sync-workers`, `twin-snapshotters`, `twin-metrics`, `audit-ingest`, `search-indexer`.

### 2.3 Reliability patterns

| Pattern | Implementation |
|---------|----------------|
| Schema Registry | Bus registry + YAML contracts; Avro/JSON Schema per event |
| DLQ | Orchestration DLQ → `marpich.twin.dlq.v1` |
| Retry | Exponential backoff catalog; max attempts policy |
| Outbox | Producer in same TX as twin persist |
| Inbox | Consumer ledger `(tenant_id, event_id, consumer_id)` |
| Saga | Only for multi-step recovery/delete — Workflow/Saga platform, not twin-local |
| Idempotent processing | Inbox + deterministic work_item keys |
| Exactly-once | Governance: outbox + idempotent handler (ADR-178) |
| Replay | Orchestration replay API + cursor |
| Retention | Topic retention policy catalog (e.g. 7d hot / 90d compact) |

### 2.4 Forbidden

Local Kafka in twin module · module DLQ tables · unsigned payloads in production · skipping outbox.

---

## SECTION 3 — Digital Twin events

### 3.1 Catalog (publish)

| Event | Topic family |
|-------|--------------|
| `identity_twin.created` | lifecycle |
| `identity_twin.updated` | lifecycle |
| `identity_twin.deleted` | lifecycle |
| `identity_twin.activated` | lifecycle |
| `identity_twin.suspended` | lifecycle |
| `identity_twin.recovered` | lifecycle |
| `identity_twin.merged` | lifecycle |
| `identity_twin.split` | lifecycle |
| `identity_twin.snapshot.created` | sync/intelligence |
| `identity_twin.predicted` | intelligence |
| `identity_twin.trust.changed` | security |
| `identity_twin.risk.changed` | security |
| `identity_twin.health.changed` | intelligence |
| `identity_twin.relationship.changed` | graph |
| `identity_twin.compliance.changed` | compliance |
| `identity_twin.anomaly.detected` | intelligence |
| `identity_twin.synchronization.started` | sync |
| `identity_twin.synchronization.completed` | sync |
| `identity_twin.synchronization.failed` | sync |
| `identity_twin.conflict.detected` | sync |
| `identity_twin.conflict.resolved` | sync |
| `identity_twin.synchronized` | sync (projection applied) |
| `identity_twin.simulation.completed` | intelligence |
| `identity_twin.drift.detected` | intelligence |
| `identity_twin.compromised` | security |
| `identity_twin.archived` | lifecycle |

Contracts: `docs/architecture/identity/DIGITAL_TWIN_EVENT_CONTRACTS.v1.yaml` (extended)  
AsyncAPI: generated later from same catalog (align ADR-198 generation pipeline) — **single source of truth = YAML contracts**.

### 3.2 Versioning strategy

- Event name immutable; bump `event_version`  
- Additive optional fields only within version  
- Breaking change → new topic suffix `.v2` + dual-publish window  
- Consumers must ignore unknown fields  

---

## SECTION 4 — API platform

Base path remains **/api/v1/identity-twins** (gateway). Protocols: REST (mandatory) · GraphQL/gRPC via ADR-198 generation · AsyncAPI derived from event catalog · OpenAPI 3.1 as source for REST.

### 4.1 Endpoints (REST)

| Method | Path | Permission |
|--------|------|------------|
| POST | `/twins` | `twin.write` |
| GET | `/twins` | `twin.read` |
| GET | `/twins/{twin_ref}` | `twin.read` |
| PUT | `/twins/{twin_ref}` | `twin.write` |
| DELETE | `/twins/{twin_ref}` | `twin.admin` |
| POST | `/twins/{twin_ref}/sync` | `twin.write` |
| POST | `/twins/{twin_ref}/snapshot` | `twin.write` |
| POST | `/twins/{twin_ref}/predict` | `twin.ai.infer` |
| POST | `/twins/{twin_ref}/simulate` | `twin.write` |
| POST | `/twins/{twin_ref}/relationships` | `twin.write` |
| GET | `/twins/{twin_ref}/history` | `twin.read` |
| GET | `/twins/{twin_ref}/health` | `twin.read` |
| GET | `/twins/{twin_ref}/risk` | `twin.read` |
| GET | `/twins/{twin_ref}/trust` | `twin.read` |
| GET | `/twins/{twin_ref}/events` | `twin.read` |
| GET | `/sync-runs` · `/sync-runs/{ref}` | `twin.read` |
| POST | `/sync-runs` (scoped batch/manual) | `twin.admin` |

Alias note: existing routes use `/api/v1/identity-twins/...`; OpenAPI documents both resource shapes with `{twin_ref}` as `{id}`.

### 4.2 DTOs & validation (summary)

- `CreateTwinRequest`: `kind` (catalog), `subject_ref` (required), `attributes` object, no secrets  
- `SyncTwinRequest`: `mode` enum from catalog, optional `facets[]`, `full` boolean  
- `PredictTwinRequest`: `horizon`, facts bag; confidence returned from AI Platform  
- List queries: pagination `limit≤100` + cursor  

### 4.3 Errors — RFC 9457 Problem Details

```json
{
  "type": "https://marpich.example/problems/twin-sync-conflict",
  "title": "Twin synchronization conflict",
  "status": 409,
  "detail": "Facet 'risk' source_version collision",
  "instance": "/api/v1/identity-twins/{twin_ref}/sync",
  "correlation_id": "...",
  "tenant_id": "...",
  "code": "twin.errors.conflict"
}
```

All 4xx/5xx twin APIs use `application/problem+json`.

---

## SECTION 5 — Event routing

| Component | Role |
|-----------|------|
| Event Router | Message Orchestration route tables |
| Event Gateway | EIEAP / API Gateway ingress for inbound webhooks → Integration |
| Filters | CEL/JSONPath filters in catalog |
| Priority Queues | critical > high > normal > low |
| Topic Routing | `event_name` → topic binding catalog |
| Tenant Routing | Partition key `tenant_id`; isolation mandatory |
| Regional Routing | Region attribute → regional mesh binding |
| Organization Routing | Optional header `organization_id` for shared scope |
| Policy-Based Routing | Policy Engine may force DLQ / delay / drop |

Routing policies are **data** in Bus/Orchestration catalogs — never hardcoded switch statements in twin workers.

---

## SECTION 6 — Synchronization policies

All evaluated via Policy Engine (`domain=platform` or industry domain).

| Source change class | Example policy key |
|---------------------|-------------------|
| Identity | `twin.sync.identity.enabled` |
| Role / Permission | `twin.sync.permission.enabled` |
| Device / Certificate | `twin.sync.device.enabled` |
| Account / Organization / Branch | `twin.sync.organization.enabled` |
| Bank / University / Hospital / Tax / FX | `twin.sync.pack.{pack}.enabled` |
| AI Agent / IoT | `twin.sync.ai_agent.enabled` / `twin.sync.iot.enabled` |
| Mode selection | `twin.sync.mode.default` |
| Conflict strategy | `twin.sync.conflict.strategy` |
| Cross-tenant | `twin.sync.cross_tenant.allowed` |
| Cross-region | `twin.sync.cross_region.allowed` |
| Max lag | `twin.sync.max_lag_seconds` |
| Full sync cooldown | `twin.sync.full.cooldown_seconds` |

Catalog: `docs/architecture/identity/TWIN_SYNC_POLICY_CATALOG.yaml`

---

## SECTION 7 — Connectors

**Owned exclusively by Integration Platform.** Twin Sync Engine consumes only:

1. Normalized `integration.*` / domain integration events, or  
2. Documented SoR REST/contracts for **recovery full sync** through Integration adapters (never direct vendor SDKs in twin).

Connector types (REST, SOAP, GraphQL, gRPC, CDC, LDAP, AD, SCIM, queues, file/CSV/Excel/SFTP, webhook) → Integration connector catalog + SDK (`packages` / Integration docs). Twin ships **ACL mapper SDK** (event → `SynchronizeTwin` command), not a parallel connector SDK.

---

## SECTION 8 — Event security

| Control | Mechanism |
|---------|-----------|
| Authentication | mTLS / SASL between mesh nodes; service JWT for in-cluster |
| Authorization | Consumer ACLs per topic + tenant |
| Encryption | TLS in transit; payload encryption for sensitive facets via Data Protection |
| Payload signing | Optional detached signature in envelope `security_context` |
| Replay protection | `event_id` inbox + timestamp skew window |
| Validation | Schema registry reject on produce/consume |
| Certificate validation | Transport layer |
| Tenant isolation | Envelope `tenant_id` + partition key + RLS on twin DB |
| Audit trail | All sync/conflict events → Audit Platform |

Zero Trust: unauthenticated mesh traffic forbidden in production profiles.

---

## SECTION 9 — Observability

### 9.1 Metrics (OTel + Prometheus)

| Metric | Type |
|--------|------|
| `twin_sync_runs_total{mode,status}` | counter |
| `twin_sync_lag_seconds{kind}` | histogram |
| `twin_sync_failures_total{reason}` | counter |
| `twin_sync_retries_total` | counter |
| `twin_event_throughput` | counter |
| `twin_consumer_lag` | gauge (from mesh) |
| `twin_health_score` | gauge |
| `twin_freshness_seconds` | histogram |
| `twin_drift_open` | gauge |
| `twin_conflicts_total{strategy}` | counter |

### 9.2 Dashboards

Grafana: Sync Overview · Consumer Lag · Conflict Rate · Twin Freshness  
Elastic: structured logs (`request_id`, `tenant_id`, `sync_run_ref`)  
OTel traces: Coordinator → Worker → State Manager → Outbox publish

---

## SECTION 10 — Principles checklist

DDD · CQRS · Hexagonal · Event-driven · Cloud native · API first · Plugin first · Configuration · Metadata · Policy · Twin-native · Zero Trust · AI native  

**Never hardcode:** topics · queues · events · routing · sync rules · retry · connector logic.

---

## Delivery roadmap (architecture → production)

| Phase | Deliverable |
|-------|-------------|
| B0 | SyncRun aggregate + started/completed/failed events + metrics |
| B1 | Workers on orchestration queue + conflict policy |
| B2 | Delta incremental mode + snapshot generator job |
| B3 | Cross-tenant/region policy paths |
| B4 | Full mesh topic bindings in production Kafka profile |
| B5 | OpenAPI 3.1 + Problem Details hardening + GraphQL/gRPC gen |

## Related

- [ENTERPRISE_EVENT_BUS.md](ENTERPRISE_EVENT_BUS.md)  
- [INTEGRATION_PLATFORM.md](INTEGRATION_PLATFORM.md)  
- [ENTERPRISE_OBSERVABILITY_PLATFORM.md](ENTERPRISE_OBSERVABILITY_PLATFORM.md)  
- ADR-010 · ADR-036 · ADR-175 · ADR-178 · ADR-198 · ADR-203 · ADR-203a · ADR-207 · [ADR-208 Twin Intelligence](../adr/208-twin-ai-intelligence-platform.md) · [ENTERPRISE_TWIN_AI_INTELLIGENCE_PLATFORM.md](ENTERPRISE_TWIN_AI_INTELLIGENCE_PLATFORM.md)
