# Strict Service Boundaries

**Status:** Canonical — non-negotiable isolation law for every service  
**Audience:** Chief Enterprise Architect, platform engineers, module authors, AI agents  
**Companions:** [DDD_DOMAIN_ARCHITECTURE.md](DDD_DOMAIN_ARCHITECTURE.md) · [BUSINESS_CAPABILITIES_REGISTRY.md](BUSINESS_CAPABILITIES_REGISTRY.md) · [CORE_PLATFORM_DESIGN.md](CORE_PLATFORM_DESIGN.md) · [COMMUNICATION_ARCHITECTURE.md](COMMUNICATION_ARCHITECTURE.md)

**A service = one bounded context = one deployable unit of ownership** (`backend/contexts/{service_id}/` or grouped logical service with explicit contract).

---

## The law

```
Each service owns its world completely.
Services never share mutable state.
Services never query each other's databases.
Services never duplicate business logic.
Services communicate only through contracts.
```

---

## What each service owns (exclusive)

Every service **exclusively owns** all nine dimensions below. No other service may write to or implement these for that domain.

| # | Asset | Owner location | Rule |
|---|-------|----------------|------|
| 1 | **Database** | `{schema}_*` tables, migrations, ORM rows | No shared tables; no cross-schema writes |
| 2 | **Business rules** | `domain/aggregates/`, `domain/services/` | Invariants live only here |
| 3 | **Events** | `domain/events/` + published schemas | Service defines its integration language |
| 4 | **API** | `presentation/router.py` → `/api/v1/{prefix}/` | Public surface is versioned OpenAPI |
| 5 | **Permissions** | `{service_id}.{resource}.{action}` catalog | Registered at module activation |
| 6 | **Background jobs** | `infrastructure/workers/` or scheduler registrations | Jobs process **this** service's data only |
| 7 | **Reports** | Report templates + data sources for **this** domain | Report Engine executes; service owns definitions |
| 8 | **AI models & prompts** | `context.yaml` `ai:` block + tenant model config | Platform AI runs inference; service owns domain prompts/embeddings config |
| 9 | **Configuration** | Settings schema + tenant overrides for **this** module | No other service stores this module's config keys |

### Ownership diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    SERVICE (bounded context)                 │
│  ┌─────────┐ ┌──────────────┐ ┌────────┐ ┌─────────────┐  │
│  │Database │ │Business Rules│ │ Events │ │     API     │  │
│  └─────────┘ └──────────────┘ └────────┘ └─────────────┘  │
│  ┌─────────────┐ ┌────────┐ ┌─────────┐ ┌──────────────┐  │
│  │ Permissions │ │  Jobs  │ │ Reports │ │ AI config    │  │
│  └─────────────┘ └────────┘ └─────────┘ └──────────────┘  │
│  ┌─────────────────────────────────────────────────────┐  │
│  │              Configuration (module settings)         │  │
│  └─────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
         │                    │                    │
         ▼                    ▼                    ▼
    REST API          Integration Events     App Contracts
```

---

## Never allow

### 1. Shared mutable state

| Forbidden | Why | Correct |
|-----------|-----|---------|
| Global in-memory dict shared across services | Race conditions, untestable coupling | Service-local memory store or Redis key with `{tenant}:{service}:` prefix |
| Shared Python singleton holding domain entities | Hidden coupling | DI container per service |
| Shared cache entry mutated by two services | Split-brain | Writer owns key; others read via API/event projection |
| Shared database row updated by two services | Ownership violation | One writer service; others hold ID + eventual consistency |

```python
# ❌ FORBIDDEN — cross-service mutable singleton
class SharedPatientCache:
    patients: dict[str, Patient] = {}  # hospital AND clinic writing here

# ✅ ALLOWED — service-scoped store
class HospitalMemoryStore:
    patients: dict[str, Patient] = {}
```

### 2. Cross-service database queries

| Forbidden | Why | Correct |
|-----------|-----|---------|
| `JOIN hospital.patients ON finance.invoice ...` | Breaks deployment independence | Store `patient_id` in finance; fetch via API if needed |
| Importing another service's ORM row class | Compile-time DB coupling | ACL maps event payload → local aggregate |
| Reading another schema in repository | Hidden dependency | Integration event builds local read model |
| Shared connection writing two schemas in one transaction | Distributed monolith | Saga via events; outbox per service |

```python
# ❌ FORBIDDEN
from shared.infrastructure.database.orm import HospitalPatientRow  # in accounting context
select(InvoiceRow).join(HospitalPatientRow, ...)

# ✅ ALLOWED
billing.patient_ref = payload["patient_id"]  # ID from event only
```

### 3. Business logic duplication

| Forbidden | Why | Correct |
|-----------|-----|---------|
| Copy auth stack into hospital module | Core Platform exists | `require_permissions` + Identity |
| Duplicate tax calculation in payroll and accounting | Single capability owner | `tax` service; others subscribe |
| Reimplement workflow engine in procurement | Platform Workflow | Emit event → workflow task |
| Industry-specific rule in `shared/` or `core/` | Wrong layer | Move to owning bounded context |

See [PLATFORM_CHARTER.md](PLATFORM_CHARTER.md) forbidden-duplication table and [BUSINESS_CAPABILITIES_REGISTRY.md](BUSINESS_CAPABILITIES_REGISTRY.md) anti-duplication matrix.

---

## Communication — five channels

> **Full law:** [COMMUNICATION_ARCHITECTURE.md](COMMUNICATION_ARCHITECTURE.md) — diagrams, eight requirements, rejection rules.

```
 Service A                                              Service B
     │                                                       ▲
     │  ① REST APIs (sync, contract-first)                  │
     ├───────────────────────────────────────────────────────┤
     │  ② Internal Application Contracts (DTOs, schemas)    │
     ├───────────────────────────────────────────────────────┤
     │  ③ Domain / Integration Events (async)                │
     ├───────────────────────────────────────────────────────┤
     │  ④ Message Broker (Kafka / outbox transport)        │
     ├───────────────────────────────────────────────────────┤
     │  ⑤ Scheduled Synchronization (batch via API/events)   │
     └───────────────────────────────────────────────────────┘

 ✗ Direct database access to peer service
 ✗ Import peer domain layer
 ✗ Shared mutable state
 ✗ Private internal APIs (undocumented service-to-service)
 ✗ Synchronous in-process calls to peer application service
```

Every communication must be: **Authenticated · Authorized · Logged · Audited · Versioned · Traceable · Retryable · Observable**

| Channel | Purpose | Marpich implementation |
|---------|---------|------------------------|
| **REST APIs** | Commands, queries, request/response | FastAPI routers `/api/v1/{prefix}/`, OpenAPI |
| **Application contracts** | Stable payloads — no domain model sharing | `presentation/schemas.py`, `docs/architecture/events/*.json`, `shared/contracts/` |
| **Domain events** | Internal aggregate facts (same service) | `domain/events/domain_event.py` |
| **Integration events** | Cross-service published language | Outbox → broker → ACL consumer |
| **Message broker** | Durable async transport | Kafka (prod) / `InProcessEventBus` (dev) |
| **Scheduled sync** | Batch projections, reconciliation | Scheduling Platform → REST or event replay — never cross-schema |

### REST rules

- Version prefix: `/api/v1/`
- Standard envelope: `{ data, meta, errors }`
- Auth: JWT + `X-Tenant-ID` on tenant-scoped routes
- **Consumers use HTTP client + contract DTO** — never import peer routers

### Event rules

- Envelope: `event_id`, `event_name`, `event_version`, `tenant_id`, `correlation_id`, `payload`
- Topic: `marpich.{event_name}.v{version}`
- Producers: transactional **outbox** in same DB transaction as mutation
- Consumers: **idempotent** `(tenant_id, event_id)` + **ACL** in `infrastructure/acl/`

### Contract rules

- Event schemas: `docs/architecture/events/{name}.v{n}.json`
- Industry packs: `shared/contracts/industry_packs.json`
- Capabilities: `shared/contracts/business_capabilities.json`
- **Contracts are the only shared code** between services — never aggregates

---

## Anti-Corruption Layer (mandatory for consumers)

Every inbound event or external API payload passes through ACL:

```
Integration Event → infrastructure/acl/{source}_events.py → Application Command → Domain
```

ACL translates **external schema → local language**. Never import peer aggregates.

---

## Background jobs

| Rule | Detail |
|------|--------|
| **Job owns** | One service's schema and rules |
| **Enqueue** | Via scheduler service or outbox — include `tenant_id`, `correlation_id` |
| **Cross-service effect** | Publish integration event when done — do not write peer tables |
| **Forbidden** | Cron in hospital that updates `finance.*` tables directly |

---

## Reports & AI

| Asset | Owner | Platform role |
|-------|-------|---------------|
| **Report definitions** | Service | Report Engine renders |
| **Report data queries** | Service read models only | No cross-schema SQL |
| **AI prompt templates** | Service manifest | AI Platform executes |
| **Model deployment config** | Service tenant settings | AI Platform hosts runtime |
| **Forbidden** | Hospital embedding OpenAI SDK for billing rules | Use `/api/v1/ai` |

---

## Configuration

| Scope | Owner | Example |
|-------|-------|---------|
| Platform config | `settings` service | Branding, feature flags |
| Module config | Each service's settings schema | `healthcare.billing.defaultCodes` |
| Secrets | `secrets` service + vault | API keys by `secret_ref` |
| **Forbidden** | Hospital storing finance keys in local table | Register in Settings/Secrets |

---

## Service boundary checklist

```markdown
## Service boundary review

### Ownership (all nine)
- [ ] Database — own schema only
- [ ] Business rules — domain layer only
- [ ] Events — published schemas registered
- [ ] API — public router documented
- [ ] Permissions — catalog registered
- [ ] Background jobs — scoped to this service
- [ ] Reports — templates owned here
- [ ] AI — manifest block, no embedded models
- [ ] Configuration — JSON schema in context.yaml

### Prohibitions
- [ ] No shared mutable state with other services
- [ ] No cross-service SQL / ORM imports
- [ ] No duplicated business logic (Core or peer service)

### Communication
- [ ] Outbound: REST or integration events only
- [ ] Inbound: ACL on all subscriptions
- [ ] Contracts versioned in docs/architecture/events/
```

---

## Enforcement

| Mechanism | Location |
|-----------|----------|
| Architecture review | Reject PRs violating ownership |
| Import lint (planned) | Block `contexts.{A}.domain` from `contexts.{B}` |
| Contract tests | `tests/contracts/test_integration_event_contracts.py` |
| Cursor rules | `marpich-service-boundaries.mdc`, `marpich-ddd-domains.mdc` |
| ADR-008, ADR-029 | Bounded context + strict service boundaries |

**Boundary violations are architecture rejections — not style issues.**

---

## Related documents

| Document | Role |
|----------|------|
| [DDD_DOMAIN_ARCHITECTURE.md](DDD_DOMAIN_ARCHITECTURE.md) | DDD classification + tactical layers |
| [BOUNDED_CONTEXTS_REGISTRY.md](BOUNDED_CONTEXTS_REGISTRY.md) | Context catalog |
| [CORE_PLATFORM_DESIGN.md](CORE_PLATFORM_DESIGN.md) | Platform services — no business logic |
| [DEVELOPMENT_PROTOCOL.md](DEVELOPMENT_PROTOCOL.md) | Reuse before code |
| ADR-008 | Bounded context isolation |
| ADR-029 | Strict service boundaries |
