# Shared Kernel

**Status:** Canonical — reusable enterprise primitives only  
**Audience:** All service authors, AI agents  
**Code root:** `backend/shared/`  
**Companions:** [SERVICE_BOUNDARIES.md](SERVICE_BOUNDARIES.md) · [CORE_PLATFORM_DESIGN.md](CORE_PLATFORM_DESIGN.md)

**Law: Never place business logic inside Shared Kernel. Only reusable enterprise components.**

---

## What Shared Kernel is

The Shared Kernel is the **only** code that multiple bounded contexts may import. It contains **no industry rules** — no patients, invoices, permits, or loan calculations.

```
┌─────────────────────────────────────────────────────────────┐
│                    SHARED KERNEL                             │
│  Value objects · Primitives · Context · Pagination · DTOs   │
│  NO business rules · NO service-specific aggregates          │
└───────────────────────────┬─────────────────────────────────┘
                            │ import allowed
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
   hospital            finance              identity
   (business)          (business)           (platform)
```

**Forbidden in Shared Kernel:**
- Hospital admission rules, tax brackets, payroll formulas
- Imports from `contexts.*`
- Database ORM models for business entities
- Workflow definitions, permission catalogs for specific modules

---

## Component catalog

| Component | Package path | Purpose |
|-----------|--------------|---------|
| **Money** | `shared.domain.value_objects.money` | Amount + currency, safe arithmetic |
| **Currency** | `shared.domain.value_objects.currency` | ISO 4217 code validation |
| **Address** | `shared.domain.value_objects.address` | Structured postal address |
| **Country** | `shared.domain.value_objects.country` | ISO 3166-1 alpha-2 |
| **Language** | `shared.domain.value_objects.language` | BCP 47 / ISO 639 tag |
| **Time Zone** | `shared.domain.value_objects.timezone` | IANA timezone id |
| **Measurement Units** | `shared.domain.value_objects.measurement` | Quantity + unit enum |
| **Date Utilities** | `shared.kernel.date_utils` | UTC helpers, parsing — no fiscal rules |
| **Audit Models** | `shared.domain.audit.models` | Audit metadata primitives |
| **Pagination** | `shared.application.pagination` | Page request / result |
| **Sorting** | `shared.application.sorting` | Sort field + order |
| **Filtering** | `shared.application.filtering` | Filter operators + specs |
| **Validation** | `shared.kernel.validation` | Format validators (email, slug) |
| **Permissions** | `shared.domain.permissions` | RBAC evaluator (wildcard) |
| **User Context** | `shared.domain.context.user_context` | Request-scoped user identity |
| **Tenant Context** | `shared.domain.context.tenant_context` | Request-scoped tenant |
| **Localization helpers** | `shared.kernel.localization` | Locale tag normalize, RTL map |
| **Common Exceptions** | `shared.domain.exceptions` | Domain / application error types |
| **Response Models** | `shared.presentation.responses` | API envelope |
| **Base Repository** | `shared.domain.ports.repository` | Generic repository port |
| **Base Entity** | `shared.domain.aggregates.entity` | Identity equality |
| **Aggregate Root** | `shared.domain.aggregates.aggregate_root` | Event collection |
| **Base Service** | `shared.application.base_service` | Service marker + context access |
| **Base DTO** | `shared.presentation.dto` | Pydantic base for APIs |
| **Result** | `shared.application.result` | `Result[T]` success/fail |
| **UniqueId** | `shared.domain.value_objects.unique_id` | UUID identity |
| **TenantId** | `shared.domain.value_objects.tenant_id` | Tenant slug VO |
| **IntegrationEvent** | `shared.domain.events.integration_event` | Cross-service events |
| **DomainEvent** | `shared.domain.events.domain_event` | In-context events |

---

## Import rules

| From | To | Allowed |
|------|-----|---------|
| `contexts.{any}` | `shared.*` | Yes |
| `shared.*` | `contexts.{any}` | **No** |
| `shared.*` | FastAPI, SQLAlchemy in **domain** | **No** |
| `shared.infrastructure.*` | Used by adapters only | Infra is not kernel domain |

---

## Usage examples

```python
from decimal import Decimal
from shared.domain.value_objects.money import Money
from shared.domain.value_objects.currency import Currency
from shared.application.pagination import PageRequest, PageResult
from shared.application.result import Result
from shared.presentation.responses import success_response

price = Money(amount=Decimal("19.99"), currency=Currency("USD"))
page = PageRequest(page=1, page_size=50)
return success_response(data=items, meta={"page": page.page, "total": 100})
```

---

## Extension protocol

New kernel types require:
1. No business semantics — must be usable by hospital **and** banking
2. Unit tests in `backend/shared/tests/`
3. Entry in this document
4. ADR if the type changes cross-cutting contracts

---

## Related

| Document | Role |
|----------|------|
| [SERVICE_BOUNDARIES.md](SERVICE_BOUNDARIES.md) | Services own business logic |
| [DDD_DOMAIN_ARCHITECTURE.md](DDD_DOMAIN_ARCHITECTURE.md) | Domain vs shared |
| ADR-030 | Shared Kernel |
