# Marpich Module Structure Standard

**Status:** Canonical — every business capability is one module  
**Audience:** Engineering, AI agents, module authors  
**Companions:** [MODULE_ARCHITECTURE.md](MODULE_ARCHITECTURE.md) · [MODULE_SYSTEM.md](MODULE_SYSTEM.md) · [PLATFORM_CHARTER.md](PLATFORM_CHARTER.md) · [DEVELOPMENT_PROTOCOL.md](DEVELOPMENT_PROTOCOL.md) · [DEPENDENCY_GRAPH.md](DEPENDENCY_GRAPH.md)

**Rules:** Every business capability → one module. **Every module follows identical architecture** — see [MODULE_ARCHITECTURE.md](MODULE_ARCHITECTURE.md). Never violate module consistency.

---

## One Capability = One Module

| Principle | Meaning |
|-----------|---------|
| **Every business capability must become a module** | Admissions, invoicing, bed management — each is a separate `{namespace}.{capability}` module |
| **Never build monolithic modules** | No “hospital-everything” or “finance-all-in-one” contexts — split by aggregate boundary and ubiquitous language |
| **Modules extend Core** | Platform provides permissions, events, search, etc. — modules **integrate**, never reimplement |

### Monolithic vs modular (examples)

| ❌ Monolithic (forbidden) | ✅ Modular (required) |
|---------------------------|----------------------|
| `hospital` owns EMR + lab + pharmacy + billing | `healthcare.patient-management`, `healthcare.clinical`, `healthcare.billing`, … |
| `retail` owns POS + inventory + ecommerce | `retail.pos`, `retail.inventory`, `retail.catalog` |
| One 50-file `service.py` | One application service per aggregate / use-case group |

**Split signal:** More than one aggregate root with unrelated lifecycles → separate modules.

---

## Required Layers (every module)

**Canonical tree:** [MODULE_ARCHITECTURE.md](MODULE_ARCHITECTURE.md) — identical folders in every module.

Each module under `backend/contexts/{context}/` **must** contain the full tree (Application · Domain · Infrastructure · Presentation · Tests · Documentation). Scaffold from `backend/contexts/_template/`.

Summary (see MODULE_ARCHITECTURE for complete list):

```
backend/contexts/{context}/
├── application/commands|queries|dto|validators|use_cases/
├── domain/aggregates|value_objects|services|ports|events|specifications/
├── infrastructure/persistence|messaging|caching|storage|external_apis/
├── presentation/rest|websocket|reports|dashboard/
├── tests/unit|integration|performance/
├── docs/api|architecture/
├── container.py
└── context.yaml
```

**Legacy modules** may still use `application/service.py` and `presentation/router.py` until migrated. **New modules** must use the full tree.

| Layer | Responsibility | Forbidden imports |
|-------|----------------|-------------------|
| **Domain** | Aggregates, invariants, domain events | No FastAPI, SQLAlchemy, HTTP |
| **Application** | Commands, queries, transaction boundaries | No FastAPI routers |
| **Infrastructure** | ORM, messaging adapters, external APIs | Implements domain ports only |
| **Presentation / API** | HTTP mapping, validation, auth decorators | No business rules |
| **API Layer** | Same as presentation — REST under `/api/v1/` | OpenAPI-documented |

Frontend mirror (when UI exists):

```
frontend/modules/{module}/
├── components/
├── pages/
├── hooks/
├── dashboard/        # Module dashboard widgets
├── reports/          # Report viewer components
├── locales/
└── README.md
```

---

## Required Module Integrations (every module)

Modules **wire into** Core Platform services — they do not duplicate them.

| Integration | Module must provide | Platform owner |
|-------------|---------------------|----------------|
| **Permissions** | Register `module.resource.action` at activation; guard every route | Permission / Identity |
| **Events** | Publish versioned integration events; subscribe via `container.py` | Event fabric / outbox |
| **Tests** | Unit tests in `tests/`; integration tests for API + event flows | CI / pytest |
| **Documentation** | `context.yaml`, `docs/` glossary, OpenAPI descriptions | — |
| **Settings** | JSON Schema config block; tenant overrides | Settings Service |
| **AI (Platform Service)** | All [14 AI surfaces](AI_PLATFORM_STANDARD.md); `context.yaml` `ai:` block | AI Service `/api/v1/ai` |

Domains must follow [DDD_DOMAIN_ARCHITECTURE.md](DDD_DOMAIN_ARCHITECTURE.md) — own schema, isolated logic.
| **Analytics** | Metrics events or analytics subscription hooks | Analytics Service |
| **Workflow** | Process definitions / task hooks | Workflow Service |
| **Reports** | Report template + data source registration | Report Engine |
| **Notifications** | Emit events that trigger notifications | Notification Service |
| **Search** | Indexable entities + event for index updates | [ENTERPRISE_SEARCH_ENGINE.md](ENTERPRISE_SEARCH_ENGINE.md) |
| **Documents** | Store `document_id` ref only — register via Document Exchange | [ENTERPRISE_DOCUMENT_EXCHANGE.md](ENTERPRISE_DOCUMENT_EXCHANGE.md) |
| **Policies** | No hardcoded business rules — evaluate via Policy Engine | [ENTERPRISE_POLICY_ENGINE.md](ENTERPRISE_POLICY_ENGINE.md) |
| **Compliance** | Declare domains; violations via Compliance Framework | [ENTERPRISE_COMPLIANCE_FRAMEWORK.md](ENTERPRISE_COMPLIANCE_FRAMEWORK.md) |
| **Localization** | Externalized strings; locale keys in frontend | Localization Service |

### Integration checklist (copy per module)

```markdown
## Module integration (all required)

- [ ] Domain Layer
- [ ] Application Layer
- [ ] Infrastructure Layer
- [ ] Presentation Layer
- [ ] API Layer (`presentation/router.py`, `/api/v1/…`)
- [ ] Permissions (registered + enforced)
- [ ] Events (publish + subscribe declared in context.yaml)
- [ ] Tests (unit + integration)
- [ ] Documentation (context.yaml + docs/)
- [ ] Settings (config schema)
- [ ] AI Platform — all 14 surfaces ([checklist](AI_PLATFORM_STANDARD.md))
- [ ] Analytics (hooks or event subscriptions)
- [ ] Policies (domain + keys in context.yaml; evaluate via Policy Engine)
- [ ] Workflow (hooks or definitions)
- [ ] Reports (template registration)
- [ ] Notifications (via events)
- [ ] Search (index events / entity metadata)
- [ ] Localization (locale keys / Accept-Language)
```

---

## Module Manifest (extended)

`context.yaml` + registry entry must declare:

```yaml
context: healthcare.clinical
display_name: Clinical Encounters
type: industry
description: Encounters, orders, clinical documentation
aggregates:
  - Encounter
  - ClinicalOrder
publishes:
  - hospital.encounter.started
  - hospital.encounter.completed
subscribes:
  - platform.module.activated
  - healthcare.patient-management.patient.registered
schema: hospital
permissions:
  - healthcare.encounter.read
  - healthcare.encounter.write
settings_schema: configs/healthcare.clinical.schema.json
ai_hooks:
  - clinical.documentation.assist
workflow_hooks:
  - encounter.discharge.approval
report_templates:
  - encounter.summary
search_entities:
  - Encounter
localization_namespace: healthcare.clinical
```

TypeScript manifest (registry): see [MODULE_SYSTEM.md](MODULE_SYSTEM.md).

---

## Sizing Rules — Avoid Monoliths

| Metric | Guideline |
|--------|-----------|
| Aggregate roots | **1–3 per module**; more → split |
| `application/service.py` | Split by aggregate when > ~400 lines |
| Router | Group by resource; split routers if > ~15 endpoints |
| Event publications | Cohesive domain only — no “god event” |
| Dependencies | Declare in manifest; no hidden cross-imports |

When a module grows beyond guidelines → **extract** a new `{namespace}.{capability}` module and integrate via events.

---

## Enforcement

| Mechanism | Location |
|-----------|----------|
| Cursor rule | `.cursor/rules/marpich-module-structure.mdc` |
| Context registry | `backend/contexts/registry.py` |
| Module system | [MODULE_SYSTEM.md](MODULE_SYSTEM.md) |
| Scaffolding reference | `backend/contexts/hospital/` (industry example) |

**Review rejection:** New capabilities added as files inside unrelated contexts, or modules missing layers/integrations, are incomplete.
