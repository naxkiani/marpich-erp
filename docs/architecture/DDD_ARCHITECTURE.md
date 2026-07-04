# Marpich ERP — Domain Driven Design Architecture

> **Canonical DDD law:** [DDD_DOMAIN_ARCHITECTURE.md](DDD_DOMAIN_ARCHITECTURE.md) — Core / Supporting / Generic domains, isolation, ownership.

## Strategic Design

Marpich ERP implements **Strict Bounded Context isolation**. Each business domain is an independent deployable unit with its own:

- Ubiquitous language
- Aggregate model
- Database schema (`{context}_*` tables, always `tenant_id`)
- API surface
- Event publications and subscriptions

**Forbidden:** Direct imports, shared ORM models, or synchronous HTTP calls between business domains.

**Required:** Integration events via Kafka + outbox pattern + idempotent consumers.

---

## Context Classification

See [DDD_DOMAIN_ARCHITECTURE.md](DDD_DOMAIN_ARCHITECTURE.md) for **Core Domain**, **Supporting Domain**, and **Generic Domain** definitions and ownership rules.

```
┌─────────────────────────────────────────────────────────────────────┐
│                    SUPPORTING / PLATFORM CONTEXTS                    │
│  Core Platform · Identity · Workflow · Documents · Notifications    │
│  Media · Search · Settings · Analytics · AI                         │
└───────────────────────────────┬─────────────────────────────────────┘
                                │ Integration Events
┌───────────────────────────────▼─────────────────────────────────────┐
│                    GENERIC SUBDOMAINS (Shared ERP)                   │
│  Finance · Accounting · Tax · Treasury · Payroll · HR · CRM · Sales│
│  Procurement · Inventory · Warehouse · Manufacturing · Projects      │
└───────────────────────────────┬─────────────────────────────────────┘
                                │ Integration Events
┌───────────────────────────────▼─────────────────────────────────────┐
│                    SPECIALIZED / INDUSTRY CONTEXTS                   │
│  Banking · Islamic Banking · Currency Exchange                       │
│  University · School · Hospital · Laboratory · Pharmacy              │
│  Hotel · Restaurant · Real Estate · Construction · Government · NGO  │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Tactical Patterns (every context)

| Pattern | Implementation |
|---------|----------------|
| **Aggregate** | Single consistency boundary; one repository per aggregate |
| **Domain Event** | Internal state change notification |
| **Integration Event** | Cross-context contract (published language) |
| **Repository** | Port in domain; adapter in infrastructure |
| **Anti-Corruption Layer** | Event consumer translates external payloads to local models |
| **Outbox** | At-least-once delivery; no dual-write |
| **Saga** | Cross-context workflows via event choreography |
| **CQRS** | Commands mutate; queries use read models/projections |

---

## Layer Structure (per context)

```
backend/contexts/{context_name}/
├── domain/           # Pure Python — zero infrastructure imports
│   ├── aggregates/
│   ├── value_objects/
│   ├── events/       # Domain events (internal)
│   ├── ports/        # Repository & service interfaces
│   └── services/     # Domain services (stateless logic)
├── application/      # Use cases, command/query handlers
├── infrastructure/   # ORM, Kafka consumers, external APIs
├── presentation/     # FastAPI routers
├── tests/
└── docs/             # Ubiquitous language glossary
```

---

## Dependency Rules

```python
# ✅ ALLOWED
from shared.domain.aggregates import AggregateRoot
from shared.domain.events import IntegrationEvent

# ❌ FORBIDDEN — never import another bounded context's domain
from contexts.finance.domain.aggregates.invoice import Invoice  # NO
from contexts.hospital.domain.aggregates.patient import Patient  # NO
```

Cross-context reference: **ID only** (e.g. `patient_id: UniqueId`, not `Patient` object).

---

## Event Flow

```
Context A (Hospital)
  PatientAdmitted (domain event)
    → Outbox
      → Kafka: hospital.patient.admitted.v1 (integration event)
        → Context B (Billing) ACL consumer
          → CreateAdmissionBillingCommand (local)
        → Context C (Analytics) projection
          → Update occupancy metrics
```

---

## Context Map Relationships

| Relationship | Contexts | Mechanism |
|--------------|----------|-----------|
| **Customer-Supplier** | Hospital → Billing | Events: `hospital.encounter.completed` |
| **Conformist** | All → Identity | Events: `identity.user.created` |
| **Published Language** | All contexts | Shared integration event schema registry |
| **Anti-Corruption Layer** | Every consumer | `infrastructure/acl/` per subscription |
| **Separate Ways** | Banking ↔ Restaurant | No direct relationship |
| **Open Host Service** | Core Platform | Tenant provisioning API |

See [CONTEXT_MAP.md](./CONTEXT_MAP.md) for full diagram.

---

## 44 Bounded Contexts

| # | Context | Type | Schema |
|---|---------|------|--------|
| 1 | Core Platform | Platform | `platform_*` |
| 2 | Identity | Platform | `identity_*` |
| 3 | Finance | Generic | `finance_*` |
| 4 | Accounting | Generic | `accounting_*` |
| 5 | Banking | Specialized | `banking_*` |
| 6 | Islamic Banking | Specialized | `islamic_banking_*` |
| 7 | Treasury | Generic | `treasury_*` |
| 8 | Currency Exchange | Specialized | `currency_exchange_*` |
| 9 | Tax | Generic | `tax_*` |
| 10 | Payroll | Generic | `payroll_*` |
| 11 | Human Resources | Generic | `hr_*` |
| 12 | CRM | Generic | `crm_*` |
| 13 | Sales | Generic | `sales_*` |
| 14 | Procurement | Generic | `procurement_*` |
| 15 | Inventory | Generic | `inventory_*` |
| 16 | Warehouse | Generic | `warehouse_*` |
| 17 | Manufacturing | Generic | `manufacturing_*` |
| 18 | Construction | Industry | `construction_*` |
| 19 | Projects | Generic | `projects_*` |
| 20 | University | Industry | `university_*` |
| 21 | School | Industry | `school_*` |
| 22 | Hospital | Core | `hospital_*` |
| 23 | Clinic | Core | `clinic_*` |
| 24 | Laboratory | Core | `laboratory_*` |
| 25 | Pharmacy | Core | `pharmacy_*` |
| 26 | Hotel | Core | `hotel_*` |
| 27 | Restaurant | Core | `restaurant_*` |
| 28 | POS | Core | `pos_*` |
| 29 | Real Estate | Core | `real_estate_*` |
| 30 | Government | Core | `government_*` |
| 31 | Municipality | Core | `municipality_*` |
| 32 | NGO | Core | `ngo_*` |
| 33 | Workflow | Supporting | `workflow_*` |
| 34 | Documents | Supporting | `documents_*` |
| 35 | Analytics | Supporting | `analytics_*` |
| 36 | AI Platform | Supporting | `ai_*` |
| 37 | Notifications | Supporting | `notifications_*` |
| 38 | Media | Supporting | `media_*` |
| 39 | Search | Supporting | `search_*` |
| 40 | Settings | Supporting | `settings_*` |
| 41 | Localization | Supporting | `localization_*` |
| 42 | Integrations | Supporting | `integration_*` |
| 43 | Organization | Supporting | `organization_*` |
| 44 | Audit | Supporting | `audit_*` |

Full registry: [BOUNDED_CONTEXTS_REGISTRY.md](./BOUNDED_CONTEXTS_REGISTRY.md)  
Detail: [BOUNDED_CONTEXTS.md](./BOUNDED_CONTEXTS.md)  
Events: [DOMAIN_EVENTS_CATALOG.md](./DOMAIN_EVENTS_CATALOG.md)

---

## Industry Pack Activation

Industry packs activate **subsets** of contexts — never duplicate code:

```
Hospital Pack  → hospital + laboratory + pharmacy + finance + accounting + hr + inventory
Islamic Bank   → islamic_banking + banking + treasury + compliance events
University     → university + finance + hr + crm + projects
```

Configuration: `settings` context stores active contexts per tenant.

---

## Governance

1. New aggregate → ADR in `docs/adr/`
2. New integration event → register in `DOMAIN_EVENTS_CATALOG.md` + schema in `docs/architecture/events/`
3. New context → add to `backend/contexts/registry.py` + [BOUNDED_CONTEXTS_REGISTRY.md](./BOUNDED_CONTEXTS_REGISTRY.md)
4. CI lint rule: block cross-context domain imports
