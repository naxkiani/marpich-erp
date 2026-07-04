# Marpich Industry Catalog

**Status:** Canonical — unlimited industries on one Core Platform  
**Audience:** Product, sales, engineering, AI agents  
**Companions:** [PLATFORM_CHARTER.md](PLATFORM_CHARTER.md) · [MODULE_SYSTEM.md](MODULE_SYSTEM.md) · [ENTERPRISE_POLICY_ENGINE.md](ENTERPRISE_POLICY_ENGINE.md)

**Rule: Marpich supports unlimited industries. Every industry extends the same Core Platform — never a separate product.**

---

## One Platform, Unlimited Industries

```
                    ┌─────────────────────────┐
                    │     CORE PLATFORM        │
                    │  (always on, shared)     │
                    └───────────┬─────────────┘
                                │
     ┌──────────────────────────┼──────────────────────────┐
     │                          │                          │
 Education              Healthcare                   Banking & Finance
 Retail & POS           Logistics & Mfg              Government & NGO
 Hospitality            Real Estate                  … unlimited more
```

| Principle | Meaning |
|-----------|---------|
| **Unlimited industries** | New `{namespace}.{capability}` modules + industry packs — no forked codebase |
| **Same Core** | Identity, audit, workflow, AI, security — identical for every tenant |
| **Pack = module bundle** | Tenant selects `industry_pack`; registry activates required + optional modules |
| **Extensible** | Add municipality, transportation, or any vertical via manifest — not a new ERP |

**Catalog source of truth (machine-readable):** `backend/shared/contracts/industry_packs.json`

---

## Current Industry Domains

### Education

| Domain | Industry pack ID | Namespace |
|--------|------------------|-----------|
| Education (sector) | `university`, `school` | `education.*` |
| University | `university` | `education.*` |
| School | `school` | `education.*` |

### Healthcare

| Domain | Industry pack ID | Namespace |
|--------|------------------|-----------|
| Healthcare (sector) | hospital, clinic, … | `healthcare.*` |
| Hospital | `hospital` | `healthcare.*` |
| Clinic | `clinic` | `healthcare.*` |
| Laboratory | `laboratory` | `healthcare.*` |
| Pharmacy | `pharmacy` | `healthcare.*` |

### Banking & Finance

| Domain | Industry pack ID | Namespace |
|--------|------------------|-----------|
| Banking | `bank` | `banking.*` |
| Islamic Banking | `islamic_bank` | `banking.*` / `finance.islamic-*` |
| Currency Exchange | `currency_exchange` | `banking.*` |
| Accounting | `accounting_firm` | `accounting.*`, `finance.*` |
| Tax Management | `tax_consulting` | `tax.*`, `finance.*` |

### Public & Social Sector

| Domain | Industry pack ID | Namespace |
|--------|------------------|-----------|
| Government | `government` | `government.*` |
| Municipality | `municipality` | `government.*` |
| NGO | `ngo` | `ngo.*` |

### Construction & Engineering

| Domain | Industry pack ID | Namespace |
|--------|------------------|-----------|
| Construction | `construction` | `construction.*` |
| Engineering | `engineering` | `construction.*`, `engineering.*` |

### Real Estate

| Domain | Industry pack ID | Namespace |
|--------|------------------|-----------|
| Real Estate | `real_estate` | `real-estate.*` |
| Property Management | `property_management` | `real-estate.*` |

### Manufacturing & Supply Chain

| Domain | Industry pack ID | Namespace |
|--------|------------------|-----------|
| Manufacturing | `manufacturing` | `manufacturing.*` |
| Warehouse | `warehouse` | `logistics.*`, `warehouse.*` |
| Inventory | *(shared ERP module)* | `inventory.*` — used across retail, warehouse, manufacturing |
| Logistics | `logistics` | `logistics.*` |
| Transportation | `transportation` | `logistics.*` |

### Retail & Commerce

| Domain | Industry pack ID | Namespace |
|--------|------------------|-----------|
| Retail | `retail` | `retail.*` |
| POS | `pos` | `retail.*` |

### Hospitality

| Domain | Industry pack ID | Namespace |
|--------|------------------|-----------|
| Hotel | `hotel` | `hospitality.*` |
| Restaurant | `restaurant` | `hospitality.*` |

### Professional Services

| Domain | Industry pack ID | Namespace |
|--------|------------------|-----------|
| Professional Services | `hr_company` | `platform.hr`, `platform.crm`, `platform.finance` |

> **Note:** Additional packs in catalog: `microfinance`, `hr_company`. New verticals append to `industry_packs.json` — never a new repository.

---

## Adding a New Industry (protocol)

1. Define `{namespace}.{capability}` modules (bounded contexts)
2. Add industry pack entry to `industry_packs.json`
3. Register contexts in `backend/contexts/registry.py`
4. Wire events in `docs/architecture/DOMAIN_EVENTS_CATALOG.md`
5. Complete [Module Structure Standard](MODULE_STRUCTURE_STANDARD.md) + [AI Platform Standard](AI_PLATFORM_STANDARD.md) checklists

**Forbidden:** Separate repo, duplicate Core, industry-specific auth/audit stack.

---

## Enforcement

| Mechanism | Location |
|-----------|----------|
| Cursor rule | `.cursor/rules/marpich-industry-catalog.mdc` |
| Industry packs | `backend/shared/contracts/industry_packs.json` |
| Context registry | `backend/contexts/registry.py` |
