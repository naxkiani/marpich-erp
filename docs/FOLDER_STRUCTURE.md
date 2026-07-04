# Marpich ERP — Folder Structure

**1,045 directories** · Clean Architecture · Modular · Not monolithic

## Stack

| Layer | Technology |
|-------|------------|
| Backend | FastAPI, Python 3.12+ |
| Frontend | Next.js, React, TypeScript |
| Infrastructure | Docker, Terraform, Kubernetes |

---

## Top level

```
Marpich ERP/
├── backend/                    # FastAPI — Python Clean Architecture
├── frontend/                   # Next.js — React modular UI
├── infrastructure/             # Docker, Terraform, K8s
├── docs/                       # Platform documentation
├── services/                   # (legacy TypeScript services — migration path)
└── packages/                   # (legacy shared packages — migration path)
```

---

## Backend (`backend/`)

```
backend/
├── pyproject.toml
├── core/                       # Platform kernel — composition only
│   ├── domain/
│   ├── application/
│   ├── infrastructure/
│   └── presentation/
│       ├── api/main.py         # FastAPI entry
│       ├── middleware/
│       ├── routers/
│       ├── schemas/
│       └── dependencies/
├── shared/                     # Cross-cutting primitives
│   ├── domain/
│   ├── application/
│   └── infrastructure/
│       ├── database/
│       ├── cache/
│       ├── messaging/
│       ├── security/
│       ├── logging/
│       └── monitoring/
├── modules/                    # Bounded contexts (never one big app/)
│   ├── platform/
│   ├── finance/
│   ├── healthcare/
│   ├── education/
│   ├── logistics/
│   ├── retail/
│   ├── hospitality/
│   ├── real_estate/
│   ├── construction/
│   ├── government/
│   ├── ngo/
│   ├── manufacturing/
│   ├── hr/
│   ├── crm/
│   ├── inventory/
│   └── ai/
└── tests/
    ├── unit/
    ├── integration/
    └── e2e/
```

### Every backend module

```
modules/{namespace}/{capability}/
├── domain/
├── application/
├── infrastructure/
├── presentation/
├── tests/
└── docs/
```

---

## Backend modules catalog

### `platform/` (9 modules)

| Module | Responsibility |
|--------|----------------|
| `identity` | JWT, RBAC, ABAC, MFA |
| `tenant` | Multi-tenant provisioning |
| `module_registry` | Industry pack activation |
| `workflow` | BPM / approvals |
| `documents` | DMS |
| `notifications` | Email, SMS, push |
| `reporting` | Reports, export |
| `audit` | Immutable audit log |
| `gateway` | API aggregation |

### `finance/` (8)

`accounting`, `core_banking`, `islamic_products`, `treasury`, `tax`, `lending`, `forex`, `compliance`

### `healthcare/` (6)

`patient_management`, `clinical`, `billing`, `pharmacy`, `laboratory`, `appointments`

### `education/` (5)

`student_information`, `academics`, `admissions`, `grading`, `attendance`

### `logistics/` (4)

`fleet`, `warehouse`, `shipments`, `tracking`

### `retail/` (3)

`catalog`, `pos`, `ecommerce`

### `hospitality/` (3)

`reservations`, `housekeeping`, `fnb`

### `real_estate/` (3)

`listings`, `transactions`, `property_management`

### `construction/` (3)

`projects`, `boq`, `subcontractors`

### `government/` (2)

`citizen_services`, `procurement`

### `ngo/` (2)

`grants`, `programs`

### `manufacturing/` (3)

`mrp`, `production`, `quality`

### `hr/` (3)

`payroll`, `recruitment`, `attendance`

### `crm/` (3)

`contacts`, `pipeline`, `campaigns`

### `inventory/` (3)

`stock`, `procurement`, `warehousing`

### `ai/` (4)

`insights`, `fraud_detection`, `clinical_assist`, `document_intelligence`

**Total: 62 backend capability modules × 6 layers = 372 module layer folders**

---

## Frontend (`frontend/`)

```
frontend/
├── package.json
├── core/
│   ├── domain/
│   ├── application/
│   ├── infrastructure/
│   └── presentation/
│       ├── providers/          # Auth, theme, i18n, notifications
│       └── layouts/
├── shared/
│   ├── components/             # Design system
│   ├── hooks/
│   ├── lib/
│   ├── types/
│   ├── i18n/                 # RTL/LTR, fa-IR, ar-SA, en-US
│   └── styles/                 # Dark mode tokens
├── modules/                    # Mirrors backend namespaces
│   └── {namespace}/{capability}/
│       ├── domain/
│       ├── application/
│       ├── infrastructure/
│       ├── presentation/
│       │   ├── components/
│       │   ├── pages/
│       │   └── hooks/
│       ├── tests/
│       └── docs/
└── apps/
    ├── admin_portal/           # Platform admin
    ├── industry_portal/        # Tenant industry UI
    ├── pos/                    # Point of sale
    └── mobile_shell/           # PWA / mobile wrapper
```

Every page module supports: **AI slot · Notifications · Search · Filters · Export · Dark mode · RTL/LTR**

---

## Infrastructure (`infrastructure/`)

```
infrastructure/
├── docker/
│   ├── compose/                # docker-compose stacks
│   ├── images/                 # Dockerfiles (backend, frontend, workers)
│   ├── migrations/             # SQL migrations
│   └── scripts/
├── terraform/
│   ├── modules/
│   │   ├── networking/
│   │   ├── database/
│   │   ├── cache/
│   │   ├── messaging/
│   │   ├── compute/
│   │   ├── storage/
│   │   └── monitoring/
│   └── environments/
│       ├── development/
│       ├── staging/
│       └── production/
└── kubernetes/
    ├── base/
    ├── overlays/
    │   ├── development/
    │   ├── staging/
    │   └── production/
    ├── helm/
    └── operators/
```

---

## Dependency rules

```
┌─────────────────────────────────────────┐
│  core.presentation (FastAPI compose)    │
└─────────────────┬───────────────────────┘
                  │ mounts routers
┌─────────────────▼───────────────────────┐
│  modules.*.presentation                 │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│  modules.*.application                  │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│  modules.*.domain  ←  shared.domain     │
└─────────────────────────────────────────┘
                  ▲
┌─────────────────┴───────────────────────┐
│  modules.*.infrastructure               │
│  shared.infrastructure                  │
└─────────────────────────────────────────┘
```

- Modules communicate via **events** (Kafka), not direct imports
- `tenant_id` on every database table
- Every endpoint: **RBAC**
- Every mutation: **audit log** + **domain event**

---

## New module quick start

1. Copy `backend/modules/_template/MODULE.md` checklist
2. Create `modules/{ns}/{name}/` (already scaffolded)
3. Implement `domain` → `application` → `infrastructure` → `presentation`
4. Register router in `core/presentation/routers/registry.py`
5. Mirror folder under `frontend/modules/{ns}/{name}/`
6. Add Terraform/K8s service entry if separately deployed
