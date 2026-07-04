# Module Architecture — Identical Structure for Every Module

**Status:** Canonical — non-negotiable module consistency  
**Audience:** Engineers, AI agents, module authors  
**Implementation root:** `backend/contexts/{module_id}/`  
**Frontend root:** `frontend/modules/{module_id}/`  
**Scaffold:** `backend/contexts/_template/`  
**Companions:** [MODULE_STRUCTURE_STANDARD.md](MODULE_STRUCTURE_STANDARD.md) · [DEPENDENCY_GRAPH.md](DEPENDENCY_GRAPH.md) · [SERVICE_BOUNDARIES.md](SERVICE_BOUNDARIES.md) · [SHARED_KERNEL.md](SHARED_KERNEL.md)

**Law: Every module must follow identical architecture. Never violate module consistency.**

---

## Module = Bounded Context

One **business capability** → one **module** → one folder under `backend/contexts/{module_id}/`.

```
Capability (CAP-xxx)  →  Module  →  backend/contexts/{module_id}/
```

Platform services are also modules (`identity`, `audit`, `workflow`, …) and use the **same tree**.

---

## Identical module tree (mandatory)

Every module **must** contain this structure. Missing folders are filled with `__init__.py` (and `.gitkeep` only when a doc file is required).

```
backend/contexts/{module_id}/
├── application/                    # APPLICATION LAYER
│   ├── commands/                   # Write intents (CQRS)
│   ├── queries/                    # Read intents (CQRS)
│   ├── dto/                        # Application DTOs (not HTTP schemas)
│   ├── validators/                 # Input validation (application rules)
│   └── use_cases/                  # Use case handlers / application services
├── domain/                         # DOMAIN LAYER
│   ├── entities/                   # Entities (incl. aggregates under aggregates/ or here)
│   ├── aggregates/                 # Aggregate roots (preferred location)
│   ├── value_objects/              # Module-specific value objects
│   ├── services/                   # Domain services (stateless rules)
│   ├── ports/                      # Repository interfaces (repositories)
│   ├── events/                     # Domain + integration events
│   └── specifications/             # Query specifications / business predicates
├── infrastructure/                 # INFRASTRUCTURE LAYER
│   ├── persistence/                # ORM adapters, memory_store, postgres_store
│   ├── messaging/                  # Outbox, event handlers, ACL
│   ├── caching/                    # Module-scoped cache adapters
│   ├── storage/                    # File/blob adapters (via platform storage)
│   └── external_apis/              # Third-party API clients
├── presentation/                   # PRESENTATION LAYER
│   ├── rest/                       # FastAPI router + HTTP schemas
│   ├── websocket/                  # WebSocket handlers (if applicable)
│   ├── reports/                    # Report template hooks / export endpoints
│   └── dashboard/                  # Dashboard data endpoints (BFF-style reads)
├── tests/                          # TESTS
│   ├── unit/                       # Domain + application unit tests
│   ├── integration/                # API + event flow tests
│   └── performance/                # Load/latency tests (when required)
├── docs/                           # DOCUMENTATION
│   ├── api/                        # OpenAPI extensions, endpoint matrix
│   └── architecture/               # Ubiquitous language, diagrams, ADR links
├── container.py                    # DI, subscriptions, lifecycle
└── context.yaml                    # Module manifest
```

### Frontend mirror (when UI exists)

```
frontend/modules/{module_id}/
├── components/
├── pages/
├── hooks/
├── dashboard/                      # Module dashboard widgets
├── reports/                        # Report viewer components
├── locales/
└── README.md
```

---

## Layer responsibilities

### Application

| Folder | Contains | Rules |
|--------|----------|-------|
| `commands/` | `CreateXCommand`, `UpdateXCommand` dataclasses | One command per write use case |
| `queries/` | `GetXQuery`, `ListXQuery` | No side effects |
| `dto/` | Application-layer data carriers | Not HTTP — not domain entities |
| `validators/` | Command/query validation | No FastAPI imports |
| `use_cases/` | Handlers orchestrating domain + ports | Transaction boundary here |

**Legacy:** existing modules may use `application/service.py` — new code **must** use `use_cases/` (+ optional thin `service.py` facade).

### Domain

| Folder | Contains | Rules |
|--------|----------|-------|
| `aggregates/` / `entities/` | Aggregate roots, entities | Invariants inside aggregates |
| `value_objects/` | Module-specific VOs | Use Shared Kernel for Money, Address, etc. |
| `services/` | Domain services | Pure Python — no I/O |
| `ports/` | `IRepository` ABCs | Implemented only in infrastructure |
| `events/` | Domain + integration event classes | Versioned integration events |
| `specifications/` | `PatientIsActiveSpec`, etc. | Reusable predicates |

### Infrastructure

| Folder | Contains | Rules |
|--------|----------|-------|
| `persistence/` | `memory_store.py`, `postgres_store.py` | Own schema only |
| `messaging/` | Outbox writers, ACL `on_*` handlers | Subscribe in `container.py` |
| `caching/` | Redis keys `{tenant}:{module}:*` | No cross-module cache mutation |
| `storage/` | Presigned upload adapters | Delegate to platform file storage |
| `external_apis/` | HTTP clients to third parties | Map to domain via ACL |

### Presentation

| Folder | Contains | Rules |
|--------|----------|-------|
| `rest/` | `router.py`, `schemas.py` | Maps HTTP → commands/queries |
| `websocket/` | `ws_router.py` | Auth + tenant on connect |
| `reports/` | Report registration, download routes | Data from own read models |
| `dashboard/` | Aggregated read endpoints | No business rules — query only |

**Legacy:** `presentation/router.py` at root — migrate to `presentation/rest/router.py`.

### Tests

| Folder | Minimum |
|--------|---------|
| `unit/` | Domain invariants, validators, specifications |
| `integration/` | REST + event flows (`httpx` + test app) |
| `performance/` | Required for high-traffic modules (POS, search ingest) |

### Documentation

| Folder | Minimum |
|--------|---------|
| `docs/api/` | Permission matrix, route list |
| `docs/architecture/` | Ubiquitous language, aggregates, events |

---

## Consistency rules (never violate)

| # | Rule |
|---|------|
| 1 | **Same folder names** in every module — no renaming `handlers/` vs `use_cases/` |
| 2 | **Same layer boundaries** — domain never imports infrastructure or presentation |
| 3 | **Commands mutate; queries read** — no writes in queries |
| 4 | **REST maps to application** — routers call use cases, not repositories |
| 5 | **Repositories are ports** — interfaces in `domain/ports/`, impl in `infrastructure/persistence/` |
| 6 | **Events cross modules** — never direct service calls to peer domain |
| 7 | **Tests mirror layers** — `tests/unit/domain/`, `tests/integration/api/` |
| 8 | **Docs required** — module incomplete without `docs/architecture/README.md` |
| 9 | **Shared Kernel for primitives** — Money, pagination, responses from `shared/` |
| 10 | **Platform for cross-cutting** — auth, audit, workflow, AI from Core |

---

## Request flow (identical in every module)

```
HTTP / WS Client
      │
      ▼
presentation/rest/router.py  ──►  validators/
      │                              │
      ▼                              ▼
application/use_cases/  ◄──  commands/ or queries/
      │
      ├──► domain/aggregates + domain/services
      │
      ├──► domain/ports/ ──► infrastructure/persistence/
      │
      └──► infrastructure/messaging/ ──► integration events
```

---

## Module manifest (`context.yaml`)

Unchanged requirements — plus architecture version:

```yaml
context: clinic
architecture_version: "1.0"
display_name: Clinic
type: industry
aggregates: [Patient, Appointment, OutpatientEncounter, Referral]
publishes: [clinic.appointment.scheduled]
subscribes: [identity.user.created]
schema: clinic
```

---

## N/A folders

If a module has no WebSocket, `presentation/websocket/` still exists with `__init__.py` and `README.md` stating **N/A**.

Same for `performance/`, `external_apis/`, `dashboard/` when not applicable.

**Never delete mandatory folders** — consistency beats minimal trees.

---

## Migration from legacy layout

| Legacy | Standard |
|--------|----------|
| `application/service.py` | Split into `application/use_cases/` |
| `presentation/router.py` | Move to `presentation/rest/router.py` |
| `presentation/schemas.py` | Move to `presentation/rest/schemas.py` |
| `domain/aggregates/` only | Keep; add empty `entities/` if unused |
| Flat `tests/test_*.py` | Move to `tests/integration/` |

Existing modules (hospital, clinic, …) may migrate incrementally; **new modules must use full tree**.

---

## Checklist (copy per module)

```markdown
## Module architecture consistency

### Application
- [ ] commands/
- [ ] queries/
- [ ] dto/
- [ ] validators/
- [ ] use_cases/

### Domain
- [ ] aggregates/ or entities/
- [ ] value_objects/
- [ ] services/
- [ ] ports/
- [ ] events/
- [ ] specifications/

### Infrastructure
- [ ] persistence/
- [ ] messaging/
- [ ] caching/
- [ ] storage/
- [ ] external_apis/

### Presentation
- [ ] rest/
- [ ] websocket/ (or N/A doc)
- [ ] reports/
- [ ] dashboard/

### Tests
- [ ] unit/
- [ ] integration/
- [ ] performance/ (or N/A doc)

### Documentation
- [ ] docs/api/
- [ ] docs/architecture/

### Root
- [ ] container.py
- [ ] context.yaml
```

---

## Enforcement

| Mechanism | Location |
|-----------|----------|
| Scaffold template | `backend/contexts/_template/` |
| Cursor rule | `.cursor/rules/marpich-module-architecture.mdc` |
| ADR-031 | Module architecture consistency |
| Code review | Reject PRs with non-standard layout |

**Module consistency violations are architecture rejections.**

---

## Related

| Document | Role |
|----------|------|
| [MODULE_STRUCTURE_STANDARD.md](MODULE_STRUCTURE_STANDARD.md) | Integrations + sizing |
| [BUSINESS_CAPABILITIES_REGISTRY.md](BUSINESS_CAPABILITIES_REGISTRY.md) | Capability before module |
| [SERVICE_BOUNDARIES.md](SERVICE_BOUNDARIES.md) | Nine ownership dimensions |
