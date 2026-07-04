# Marpich DDD Domain Architecture

**Status:** Canonical — full Domain-Driven Design for Marpich Enterprise Platform  
**Audience:** Chief Enterprise Architect, engineers, AI agents  
**Companions:** [CHIEF_ARCHITECT_MANDATE.md](CHIEF_ARCHITECT_MANDATE.md) · [DDD_ARCHITECTURE.md](DDD_ARCHITECTURE.md) · [MODULE_STRUCTURE_STANDARD.md](MODULE_STRUCTURE_STANDARD.md)

**Rule: Every domain is isolated. Business logic lives inside the domain. Communication is contracts only.**

---

## Strategic Classification — Three Domain Types

```
┌─────────────────────────────────────────────────────────────────┐
│  SUPPORTING DOMAINS (Platform)                                   │
│  Enable every tenant — not industry-specific                     │
│  Identity · Tenant · Audit · Workflow · Documents · AI · Search  │
└────────────────────────────┬────────────────────────────────────┘
                             │ Events + Public APIs
┌────────────────────────────▼────────────────────────────────────┐
│  GENERIC DOMAINS (Commodity ERP)                                 │
│  Reused across all industries — finance, HR, inventory, …      │
└────────────────────────────┬────────────────────────────────────┘
                             │ Events + Public APIs
┌────────────────────────────▼────────────────────────────────────┐
│  CORE DOMAINS (Industry / Competitive)                           │
│  Hospital · Banking · University · Retail · Government · …       │
│  Where industry advantage and specialized rules live               │
└─────────────────────────────────────────────────────────────────┘
```

| Type | DDD role | Marpich examples | Schema pattern |
|------|----------|------------------|----------------|
| **Core Domain** | Competitive advantage; specialized business rules | `hospital`, `banking`, `university`, `currency_exchange`, `government` | `{context}_*` |
| **Supporting Domain** | Platform capabilities; custom-built enablers | `identity`, `core_platform`, `audit`, `workflow`, `documents`, `ai`, `search`, `notifications` | `platform_*`, `identity_*`, … |
| **Generic Domain** | Commodity ERP; shared across packs | `finance`, `accounting`, `hr`, `crm`, `inventory`, `procurement`, `payroll`, `tax` | `{context}_*` |

Registry: `backend/contexts/registry.py` · detail: [BOUNDED_CONTEXTS.md](BOUNDED_CONTEXTS.md)

> **Per tenant:** the activated **industry pack** determines which core domains run; supporting + selected generic domains compose the solution.

---

## Every domain owns (complete ownership)

Each bounded context under `backend/contexts/{domain}/` **must** own all assets defined in [SERVICE_BOUNDARIES.md](SERVICE_BOUNDARIES.md):

| Asset | Location | Notes |
|-------|----------|-------|
| **Database** | `{schema}_*` migrations, ORM | No shared tables; no cross-schema access |
| **Business rules** | `domain/` aggregates, domain services | Invariants — **only here** |
| **Entities** | `domain/aggregates/` | Aggregate roots + child entities |
| **Value objects** | `domain/value_objects/` | Immutable, validated |
| **Repositories** | `domain/ports/` + `infrastructure/persistence/` | This service's tables only |
| **Application services** | `application/` | Use cases, orchestration, transactions |
| **Events** | `domain/events/` | Domain + integration event definitions |
| **API** | `presentation/router.py` | Public REST under `/api/v1/{domain}/` |
| **Permissions** | manifest + router guards | `{domain}.*` registered at activation |
| **Background jobs** | `infrastructure/workers/` | Scoped to this service's data |
| **Reports** | templates → Report Engine | Definitions owned here |
| **AI models & prompts** | `context.yaml` `ai:` block | Platform AI executes |
| **Configuration** | settings schema in `context.yaml` | Module keys — not in peer services |
| **UI components** | `frontend/modules/{domain}/` | Module-scoped presentation |

**Never place business rules in presentation, infrastructure, or another service.**

---

## Hard Rules (non-negotiable)

### Database isolation

| Rule | Detail |
|------|--------|
| **Never share database tables between domains** | One schema prefix per context (`hospital_*`, `finance_*`) |
| **Never access another domain's database directly** | No cross-schema JOINs, no shared ORM models |
| **Every table has `tenant_id`** | Row-level isolation |
| **Cross-domain reference** | Foreign key as **ID only** in application layer — not shared table ownership |
| **Shared Kernel** | Reusable primitives in `backend/shared/` — [SHARED_KERNEL.md](SHARED_KERNEL.md); **no business logic** |

```python
# ✅ ALLOWED — store ID reference
admission.patient_id: UniqueId

# ❌ FORBIDDEN — shared table or cross-context ORM
from shared.infrastructure.database.orm import HospitalPatientRow  # in finance context
JOIN finance.invoice ON hospital.patient ...  # cross-schema join
```

### Business logic isolation

| Rule | Detail |
|------|--------|
| **Never allow business logic outside the domain** | No rules in routers, ORM, frontend, or `shared/` (except kernel primitives) |
| **Application layer** | Coordinates — does not replace domain invariants |
| **Infrastructure** | Persistence & adapters only |

### Communication — five channels

See [COMMUNICATION_ARCHITECTURE.md](COMMUNICATION_ARCHITECTURE.md) and [SERVICE_BOUNDARIES.md](SERVICE_BOUNDARIES.md) for full law.

```
Domain A                              Domain B
   │                                      ▲
   │  ① REST APIs (sync)                  │
   ├──────────────────────────────────────┤
   │  ② Application Contracts (schemas)    │
   ├──────────────────────────────────────┤
   │  ③ Domain / Integration Events       │
   ├──────────────────────────────────────┤
   │  ④ Message Broker (Kafka / outbox)   │
   ├──────────────────────────────────────┤
   │  ⑤ Scheduled Synchronization       │
   └──────────────────────────────────────┘

   ✗ Direct database access
   ✗ Domain layer imports
   ✗ Shared mutable state
   ✗ Business logic duplication
   ✗ Direct coupling (in-process peer calls)
```

Every communication: **Authenticated · Authorized · Logged · Audited · Versioned · Traceable · Retryable · Observable**

| Channel | Mechanism | Example |
|---------|-----------|---------|
| **REST APIs** | Versioned OpenAPI | `GET /api/v1/hospital/encounters/{id}` |
| **Events** | Outbox → broker → idempotent ACL | `hospital.encounter.completed.v1` |
| **Message broker** | Kafka / in-process bus | `marpich.hospital.encounter.completed.v1` |
| **Application contracts** | DTOs + JSON schemas | `docs/architecture/events/*.json` |
| **Scheduled sync** | Cron → owner REST or events | Search/analytics projection |

**Anti-Corruption Layer (ACL):** every event consumer translates external payload to local commands — `infrastructure/acl/` or handler in `container.py`.

---

## Tactical Layer Structure (per domain)

```
backend/contexts/{domain}/
├── domain/
│   ├── aggregates/          # Entities + invariants
│   ├── value_objects/
│   ├── events/              # Domain + integration events
│   ├── ports/               # Repository interfaces
│   └── services/            # Domain services (stateless rules)
├── application/
│   └── service.py           # Application services (use cases)
├── infrastructure/
│   ├── persistence/         # Repository implementations — THIS domain's tables only
│   └── acl/                 # Anti-corruption for inbound events
├── presentation/
│   ├── router.py            # Public API
│   └── schemas.py           # Application contracts (request/response)
├── container.py
├── context.yaml
├── tests/
└── docs/                    # Ubiquitous language
```

---

## Domain Checklist (new or changed domain)

```markdown
## DDD domain checklist

### Classification
- [ ] Type: Core | Supporting | Generic
- [ ] Registered in `contexts/registry.py`

### Ownership
- [ ] Business rules in domain layer only
- [ ] Entities & value objects defined
- [ ] Repositories (port + adapter)
- [ ] Application services
- [ ] Integration events + schemas
- [ ] Permissions registered
- [ ] Reports/dashboards hooks
- [ ] Public API (OpenAPI)
- [ ] UI module (if applicable)
- [ ] AI extensions declared

### Isolation
- [ ] Own schema `{domain}_*` — no shared tables
- [ ] No imports from other contexts' domain/
- [ ] No cross-domain DB access
- [ ] Cross-domain via events/API/contracts only
- [ ] ACL on all event subscriptions
```

---

## Governance

| Action | Requirement |
|--------|-------------|
| New aggregate | ADR + update BOUNDED_CONTEXTS |
| New integration event | Schema in `docs/architecture/events/` + contract test |
| New context | `registry.py` + migration `{domain}_*` schema |
| Cross-domain need | Event or public API design review — **not** shared table |

---

## Enforcement

| Mechanism | Location |
|-----------|----------|
| Cursor rule | `.cursor/rules/marpich-ddd-domains.mdc` |
| Tactical reference | [DDD_ARCHITECTURE.md](DDD_ARCHITECTURE.md) |
| Import boundary | CI / review — no `contexts.X.domain` cross-imports |

**Violation of database or logic boundaries is an architecture rejection — not a style issue.**
