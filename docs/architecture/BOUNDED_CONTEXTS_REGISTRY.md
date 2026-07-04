# Marpich Bounded Contexts Registry

**Status:** Canonical — master catalog of all bounded contexts  
**Audience:** Chief Enterprise Architect, engineers, AI agents  
**Code registry:** `backend/contexts/registry.py`  
**Companions:** [DDD_DOMAIN_ARCHITECTURE.md](DDD_DOMAIN_ARCHITECTURE.md) · [BOUNDED_CONTEXTS.md](BOUNDED_CONTEXTS.md)

**Rules: Never merge unrelated domains. Every context evolves independently.**

---

## Independence Contract (every context)

| Dimension | Must be independent |
|-----------|---------------------|
| **Terminology** | Ubiquitous language in `contexts/{id}/docs/` |
| **Database models** | Schema `{schema_name}_*` — never shared tables |
| **Business rules** | `domain/` only |
| **Permissions** | `{context_id}.*` catalog |
| **Workflows** | Process definitions owned or subscribed via events |
| **Events** | Versioned integration events in `docs/architecture/events/` |
| **Documentation** | `contexts/{id}/docs/` + BOUNDED_CONTEXTS entry |

**Communication:** integration events · public APIs · application contracts only.

---

## Master Catalog (42 + Organization + Audit = 44 contexts)

| # | Context | ID | DDD type | Schema | Path |
|---|---------|-----|----------|--------|------|
| 1 | Core Platform | `core_platform` | Supporting | `platform` | `contexts/core_platform/` |
| 2 | Identity | `identity` | Supporting | `identity` | `contexts/identity/` |
| 3 | Finance | `finance` | Generic | `finance` | `contexts/finance/` |
| 4 | Accounting | `accounting` | Generic | `accounting` | `contexts/accounting/` |
| 5 | Treasury | `treasury` | Generic | `finance`/`treasury` | `contexts/treasury/` |
| 6 | Banking | `banking` | Core | `banking` | `contexts/banking/` |
| 7 | Islamic Banking | `islamic_banking` | Core | `islamic_banking` | `contexts/islamic_banking/` |
| 8 | Currency Exchange | `currency_exchange` | Core | `currency_exchange` | `contexts/currency_exchange/` |
| 9 | Tax | `tax` | Generic | `tax` | `contexts/tax/` |
| 10 | University | `university` | Core | `university` | `contexts/university/` |
| 11 | School | `school` | Core | `school` | `contexts/school/` |
| 12 | Hospital | `hospital` | Core | `hospital` | `contexts/hospital/` |
| 13 | Clinic | `clinic` | Core | `clinic` | `contexts/clinic/` |
| 14 | Laboratory | `laboratory` | Core | `laboratory` | `contexts/laboratory/` |
| 15 | Pharmacy | `pharmacy` | Core | `pharmacy` | `contexts/pharmacy/` |
| 16 | CRM | `crm` | Generic | `crm` | `contexts/crm/` |
| 17 | Sales | `sales` | Generic | `sales` | `contexts/sales/` |
| 18 | Procurement | `procurement` | Generic | `procurement` | `contexts/procurement/` |
| 19 | Warehouse | `warehouse` | Generic | `warehouse` | `contexts/warehouse/` |
| 20 | Inventory | `inventory` | Generic | `inventory` | `contexts/inventory/` |
| 21 | Manufacturing | `manufacturing` | Generic | `manufacturing` | `contexts/manufacturing/` |
| 22 | Construction | `construction` | Core | `construction` | `contexts/construction/` |
| 23 | Projects | `projects` | Generic | `projects` | `contexts/projects/` |
| 24 | Human Resources | `human_resources` | Generic | `human_resources` | `contexts/human_resources/` |
| 25 | Payroll | `payroll` | Generic | `payroll` | `contexts/payroll/` |
| 26 | Government | `government` | Core | `government` | `contexts/government/` |
| 27 | Municipality | `municipality` | Core | `municipality` | `contexts/municipality/` |
| 28 | Real Estate | `real_estate` | Core | `real_estate` | `contexts/real_estate/` |
| 29 | Hotel | `hotel` | Core | `hotel` | `contexts/hotel/` |
| 30 | Restaurant | `restaurant` | Core | `restaurant` | `contexts/restaurant/` |
| 31 | POS | `pos` | Core | `pos` | `contexts/pos/` |
| 32 | NGO | `ngo` | Core | `ngo` | `contexts/ngo/` |
| 33 | Analytics | `analytics` | Supporting | `analytics` | `contexts/analytics/` |
| 34 | Documents | `documents` | Supporting | `documents` | `contexts/documents/` |
| 35 | Workflow | `workflow` | Supporting | `workflow` | `contexts/workflow/` |
| 36 | Search | `search` | Supporting | `search` | `contexts/search/` |
| 37 | Notifications | `notifications` | Supporting | `notifications` | `contexts/notifications/` |
| 38 | Media | `media` | Supporting | `media` | `contexts/media/` |
| 39 | AI Platform | `ai` | Supporting | `ai` | `contexts/ai/` |
| 40 | Integrations | `integration` | Supporting | `integration` | `contexts/integration/` |
| 41 | Settings | `settings` | Supporting | `settings` | `contexts/settings/` |
| 42 | Localization | `localization` | Supporting | `localization` | `contexts/localization/` |

### Additional platform contexts (same independence rules)

| Context | ID | Schema | Notes |
|---------|-----|--------|-------|
| Organization | `organization` | `organization` | Org hierarchy — not merged into identity |
| Audit | `audit` | `audit` | Compliance trail — never merged into other domains |

---

## Context Cards (summary by group)

### Platform & supporting

#### Core Platform (`core_platform`)
- **Terminology:** tenant, module, industry pack, activation
- **Permissions:** `platform.tenant.*`, `platform.module.*`
- **Events:** `platform.tenant.provisioned`, `platform.module.activated`
- **API:** `/api/v1/platform`

#### Identity (`identity`)
- **Terminology:** user, role, permission, session, MFA, ABAC policy
- **Permissions:** `identity.user.*`, `identity.role.*`
- **Events:** `identity.user.created`, `identity.login.succeeded`
- **API:** `/api/v1/identity`

#### Localization (`localization`)
- **Terminology:** locale, translation key, namespace, RTL/LTR
- **Permissions:** `localization.locale.*`, `localization.translate.*`
- **Events:** `localization.locale.changed`, `localization.key.missing`
- **API:** `/api/v1/localization`

#### AI Platform (`ai`)
- **Terminology:** inference, insight, prompt template, model deployment
- **Permissions:** `ai.infer`, `ai.insights.read`
- **Events:** `ai.insight.generated`, `ai.prediction.completed`
- **API:** `/api/v1/ai`

*(See [BOUNDED_CONTEXTS.md](BOUNDED_CONTEXTS.md) for full detail on implemented contexts.)*

### Finance cluster — **never merge** (independent contexts)

| Context | Owns | Must not absorb |
|---------|------|-----------------|
| Finance | Budgets, fiscal periods | GL entries |
| Accounting | Journal, COA, AP/AR | Bank transactions |
| Banking | Accounts, loans, cards | Sharia contracts |
| Islamic Banking | Murabaha, Sukuk, profit share | Conventional interest logic |
| Treasury | Liquidity, transfers | FX deals |
| Currency Exchange | Rates, deals, vault | Core banking ledger |
| Tax | Filings, liabilities | Payroll calculation |

### Healthcare cluster — **never merge**

| Context | Relationship |
|---------|--------------|
| Hospital | Acute care, EMR, encounters |
| Clinic | Ambulatory care — **separate** from hospital |
| Laboratory | LIMS — events to hospital/clinic |
| Pharmacy | Dispensing — separate inventory rules |

### Government cluster

| Context | Scope |
|---------|--------|
| Government | National / federal services |
| Municipality | Local permits, utilities — **separate** context from government |

### Retail cluster

| Context | Scope |
|---------|--------|
| Sales / Inventory | Back-office commerce |
| POS | Point-of-sale terminal domain — **separate** from retail catalog |

---

## Adding a context (checklist)

```markdown
- [ ] Unique `id` in `registry.py` — not merged into existing context
- [ ] `context.yaml` manifest
- [ ] Schema migration `{schema}_*`
- [ ] `docs/` ubiquitous language
- [ ] Permissions registered
- [ ] Integration events + JSON schema
- [ ] Entry in BOUNDED_CONTEXTS.md
- [ ] No shared tables with other contexts
```

---

## Anti-patterns

| ❌ Forbidden | ✅ Correct |
|-------------|-----------|
| `hospital_clinic` combined module | `hospital` + `clinic` contexts |
| Shared `patients` table | `hospital_patient` vs `clinic_patient` or ID reference via events |
| Finance logic in accounting router | Accounting domain service only |
| Localization keys in Settings tables only | `localization` context owns translations |

---

## Enforcement

| Mechanism | Location |
|-----------|----------|
| Code registry | `backend/contexts/registry.py` |
| DDD rule | `.cursor/rules/marpich-ddd-domains.mdc` |
| Event catalog | `docs/architecture/DOMAIN_EVENTS_CATALOG.md` |
