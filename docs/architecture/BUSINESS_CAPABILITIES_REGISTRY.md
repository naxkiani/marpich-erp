# Business Capabilities Registry

**Status:** Canonical — identify capabilities before modules  
**Audience:** Chief Enterprise Architect, product, engineers, AI agents  
**Companions:** [CHIEF_ARCHITECT_MANDATE.md](CHIEF_ARCHITECT_MANDATE.md) · [CORE_PLATFORM_DESIGN.md](CORE_PLATFORM_DESIGN.md) · [MODULE_STRUCTURE_STANDARD.md](MODULE_STRUCTURE_STANDARD.md)

**Rules:**
1. **Identify capabilities first — never create modules first.**
2. **Never duplicate capabilities** — one capability → one bounded context owner.
3. Each capability eventually becomes: Application Service · Domain Service · Events · Reports · Permissions · UI Components · API Contracts.

**Machine-readable catalog:** `backend/shared/contracts/business_capabilities.json`

---

## Design order (mandatory)

```
Capability → Bounded context → Aggregates → Events → Application services → API → Persistence → Module manifest
```

Modules are the **packaging** of a capability — not the starting point.

---

## Three tiers

| Tier | What it is | Examples | Document |
|------|------------|----------|----------|
| **Platform** | Reusable enterprise plumbing — no industry logic | Auth, audit, workflow, search | [CORE_PLATFORM_DESIGN.md](CORE_PLATFORM_DESIGN.md) |
| **Enterprise** | Cross-industry ERP capabilities | CRM, payroll, procurement, GL | This registry — Section B |
| **Industry** | Vertical lifecycles & specialized rules | Patient lifecycle, student lifecycle | This registry — Section C |

**Do not re-implement Platform capabilities as business modules.** Consume Core via REST + events.

---

## Capability deliverables (every capability)

When a capability is implemented, it **must** produce:

| # | Deliverable | Location / contract |
|---|-------------|---------------------|
| 1 | **Application Service** | `application/service.py` — use cases, transaction boundaries |
| 2 | **Domain Service** | `domain/services/` — rules spanning aggregates (when needed) |
| 3 | **Events** | `domain/events/` + `docs/architecture/events/*.json` |
| 4 | **Reports** | Report templates registered with Report Engine |
| 5 | **Permissions** | `{context}.{resource}.{action}` in module manifest |
| 6 | **UI Components** | `frontend/modules/{module}/` — pages, hooks, locales |
| 7 | **API Contracts** | `presentation/router.py` + OpenAPI + `presentation/schemas.py` |

---

## Section A — Platform capabilities (reference only)

Listed once in [CORE_PLATFORM_DESIGN.md](CORE_PLATFORM_DESIGN.md). **Not business capabilities.**

| Capability | Owner |
|------------|-------|
| Authentication · Authorization · Identity · User · Role · Permission | `identity` |
| Tenant Management | `core_platform` |
| Organization Management | `organization` |
| Configuration (Settings) · Localization · Secrets | `settings`, `localization`, `secrets` |
| Notification · Workflow · Search · Audit · Document · Media | respective contexts |
| AI Platform · Analytics · Integration | `ai`, `analytics`, `integration` |
| Scheduling · Workers · File Storage · Reports | planned contexts |
| API Gateway · Health · Logging · Monitoring · Caching | `core/`, `shared/` |

User examples **Workflow Management**, **Document Lifecycle**, **Notification Lifecycle**, **AI Assistance**, **Analytics** → **Platform**, not duplicated here.

---

## Section B — Enterprise capabilities (cross-industry)

### B1 — Commercial & customer

| ID | Capability | Owning context | Lifecycle | Not duplicated by |
|----|------------|----------------|-----------|-------------------|
| `CAP-ENT-001` | **Customer Management** | `crm` | — | Sales, marketing modules |
| `CAP-ENT-002` | **Sales Lifecycle** | `sales` | Quote → order → fulfill | CRM, POS checkout |
| `CAP-ENT-003` | **Quote & Proposal Management** | `sales` | — | *(part of sales — same context)* |

### B2 — Human capital

| ID | Capability | Owning context | Lifecycle | Not duplicated by |
|----|------------|----------------|-----------|-------------------|
| `CAP-ENT-010` | **Employee Management** | `human_resources` | Hire → transfer → exit | Payroll, identity users |
| `CAP-ENT-011` | **Recruitment Management** | `human_resources` | Applicant → offer | Employee management |
| `CAP-ENT-012` | **Attendance Management** | `human_resources` | — | Education attendance |
| `CAP-ENT-013` | **Leave Management** | `human_resources` | — | — |
| `CAP-ENT-014` | **Performance Management** | `human_resources` | Review cycles | — |
| `CAP-ENT-015` | **Payroll Lifecycle** | `payroll` | Accrue → pay → file | Employee management |
| `CAP-ENT-016` | **Benefits Administration** | `human_resources` | — | Payroll |

### B3 — Finance & accounting

| ID | Capability | Owning context | Lifecycle | Not duplicated by |
|----|------------|----------------|-----------|-------------------|
| `CAP-ENT-020` | **Financial Management** | `finance` | Budget → period → close | Accounting GL |
| `CAP-ENT-021` | **Accounting & General Ledger** | `accounting` | Post → reconcile | Finance budgets |
| `CAP-ENT-022` | **Accounts Payable** | `accounting` | Invoice → pay | Procurement |
| `CAP-ENT-023` | **Accounts Receivable** | `accounting` | Invoice → collect | Sales, healthcare billing |
| `CAP-ENT-024` | **Billing & Invoicing** | `accounting` | — | Industry-specific billing |
| `CAP-ENT-025` | **Treasury Management** | `treasury` | Liquidity → transfer | Banking ledger |
| `CAP-ENT-026` | **Tax Processing** | `tax` | Calculate → file → pay | Municipal local tax |
| `CAP-ENT-027` | **Financial Compliance** | `finance` | AML, KYC, regulatory | Platform audit |
| `CAP-ENT-028` | **Statutory Financial Audit** | `accounting` | — | Platform audit engine |

### B4 — Banking & specialized finance

| ID | Capability | Owning context | Lifecycle | Not duplicated by |
|----|------------|----------------|-----------|-------------------|
| `CAP-ENT-030` | **Banking Operations** | `banking` | Account → transaction | Treasury, FX |
| `CAP-ENT-031` | **Lending & Credit** | `banking` | Apply → disburse → repay | Islamic products |
| `CAP-ENT-032` | **Islamic Banking Products** | `islamic_banking` | Murabaha, Sukuk, … | Conventional interest |
| `CAP-ENT-033` | **Sharia Compliance** | `islamic_banking` | — | General compliance |
| `CAP-ENT-034` | **Currency Exchange Operations** | `currency_exchange` | Deal → settle | Exchange rates |
| `CAP-ENT-035` | **Exchange Rate Management** | `currency_exchange` | Quote → publish | FX deals |
| `CAP-ENT-036` | **Collections Management** | `banking` | Delinquent → recover | AR |
| `CAP-ENT-037` | **Trade Finance** | `banking` | LC, guarantee, … | Core banking |
| `CAP-ENT-038` | **Mobile Money** | `banking` | Wallet → transfer | POS |

### B5 — Supply chain & operations

| ID | Capability | Owning context | Lifecycle | Not duplicated by |
|----|------------|----------------|-----------|-------------------|
| `CAP-ENT-040` | **Procurement Lifecycle** | `procurement` | Requisition → PO → receive | Inventory, AP |
| `CAP-ENT-041` | **Vendor Management** | `procurement` | Onboard → evaluate | CRM |
| `CAP-ENT-042` | **Inventory Lifecycle** | `inventory` | Stock → adjust → count | Warehouse ops |
| `CAP-ENT-043` | **Warehouse Operations** | `warehouse` | Receive → pick → ship | Inventory state |
| `CAP-ENT-044` | **Manufacturing & Production** | `manufacturing` | Plan → produce → complete | MRP |
| `CAP-ENT-045` | **MRP Planning** | `manufacturing` | — | Production execution |
| `CAP-ENT-046` | **Quality Management** | `manufacturing` | Inspect → quarantine | Lab QC |
| `CAP-ENT-047` | **Project Management** | `projects` | Initiate → deliver → close | Construction BOQ |
| `CAP-ENT-048` | **Fleet Management** | `warehouse` *or future `logistics`* | Asset → maintain | Transportation routing |
| `CAP-ENT-049` | **Shipment Management** | `warehouse` | Create → dispatch → deliver | Inventory |
| `CAP-ENT-050` | **Route & Dispatch** | `warehouse` | Plan → assign | Fleet |

> **Note:** `logistics` namespace in industry packs maps to capabilities 048–050; bounded context may split to `logistics` when implemented.

---

## Section C — Industry capabilities (vertical lifecycles)

### C1 — Education

| ID | Capability | Owning context | Lifecycle stages |
|----|------------|----------------|------------------|
| `CAP-EDU-001` | **Student Lifecycle** | `university` / `school` | Prospect → enroll → graduate |
| `CAP-EDU-002` | **Admissions Management** | `university` | Apply → admit |
| `CAP-EDU-003` | **Academics Management** | `university` | Course → section → grade |
| `CAP-EDU-004` | **Grading & Assessment** | `school` | Assign → score → report |
| `CAP-EDU-005` | **School Attendance** | `school` | Daily → absent → notify |
| `CAP-EDU-006` | **Research Management** | `university` | Proposal → publish |
| `CAP-EDU-007` | **Library Management** | `university` | Catalog → lend → return |

### C2 — Healthcare

| ID | Capability | Owning context | Lifecycle stages |
|----|------------|----------------|------------------|
| `CAP-HLT-001` | **Patient Lifecycle (acute)** | `hospital` | Register → admit → discharge |
| `CAP-HLT-002` | **Outpatient Care Lifecycle** | `clinic` | Register → visit → follow-up |
| `CAP-HLT-003` | **Appointment Management** | `clinic` | Schedule → check-in → complete |
| `CAP-HLT-004` | **Admission & Bed Management** | `hospital` | Admit → transfer → discharge |
| `CAP-HLT-005` | **Clinical Encounter Management** | `hospital` | Start → document → complete |
| `CAP-HLT-006` | **Referral Management** | `clinic` | Create → send → accept |
| `CAP-HLT-007` | **Laboratory / LIMS** | `laboratory` | Order → sample → result |
| `CAP-HLT-008` | **Pharmacy & Dispensing** | `pharmacy` | Prescribe → dispense → counsel |
| `CAP-HLT-009` | **Healthcare Billing** | `hospital` *integrates* `accounting` | Encounter → claim → pay |
| `CAP-HLT-010` | **Radiology Management** | `hospital` | Order → image → report |

**Never merge:** `CAP-HLT-001` (hospital) ≠ `CAP-HLT-002` (clinic) ≠ `CAP-HLT-007` (lab) ≠ `CAP-HLT-008` (pharmacy).

### C3 — Construction & engineering

| ID | Capability | Owning context | Lifecycle stages |
|----|------------|----------------|------------------|
| `CAP-CNS-001` | **Construction Lifecycle** | `construction` | Tender → build → handover |
| `CAP-CNS-002` | **Bill of Quantities (BOQ)** | `construction` | Estimate → revise → award |
| `CAP-CNS-003` | **Engineering Project Delivery** | `projects` | Design → deliver → bill |

### C4 — Real estate & property

| ID | Capability | Owning context | Lifecycle stages |
|----|------------|----------------|------------------|
| `CAP-RE-001` | **Property Lifecycle** | `real_estate` | List → transact → close |
| `CAP-RE-002` | **Listing & Transaction Management** | `real_estate` | Listing → offer → settlement |
| `CAP-RE-003` | **Property Management** | `real_estate` | Lease → maintain → renew |

### C5 — Hospitality & retail

| ID | Capability | Owning context | Lifecycle stages |
|----|------------|----------------|------------------|
| `CAP-HSP-001` | **Hotel Reservation Lifecycle** | `hotel` | Book → stay → checkout |
| `CAP-HSP-002` | **Housekeeping Operations** | `hotel` | Assign → clean → inspect |
| `CAP-HSP-003` | **Food & Beverage Operations** | `restaurant` | Order → prepare → serve |
| `CAP-RTL-001` | **Retail Catalog Management** | `sales` | SKU → price → publish |
| `CAP-RTL-002` | **POS & In-Store Checkout** | `pos` | Shift → sale → receipt |

**Never merge:** `CAP-RTL-002` (POS terminal) ≠ `CAP-ENT-002` (back-office sales) ≠ `CAP-RTL-001` (catalog).

### C6 — Government, municipality & NGO

| ID | Capability | Owning context | Lifecycle stages |
|----|------------|----------------|------------------|
| `CAP-GOV-001` | **Citizen Services** | `government` | Request → process → resolve |
| `CAP-GOV-002` | **Government Permit Management** | `government` | Apply → review → issue |
| `CAP-GOV-003` | **Municipal Permit Management** | `municipality` | Apply → inspect → issue |
| `CAP-GOV-004` | **Municipal Utility Management** | `municipality` | Account → bill → collect |
| `CAP-GOV-005` | **Municipal Service Requests** | `municipality` | Open → work → close |
| `CAP-GOV-006` | **Public Sector Procurement** | `government` | Tender → award → contract |
| `CAP-NGO-001` | **Grant Lifecycle** | `ngo` | Apply → award → report |
| `CAP-NGO-002` | **Program Management** | `ngo` | Plan → execute → measure |
| `CAP-NGO-003` | **Donor Management** | `ngo` | *(extends CRM)* | Steward → donate → receipt |

---

## Anti-duplication matrix

| If you need… | Use this capability | Do NOT create… |
|--------------|---------------------|----------------|
| Login / JWT / MFA | Platform Authentication | `hospital.auth` |
| Audit trail | Platform Audit Engine | `finance.audit-log` |
| Approvals | Platform Workflow | `procurement.approvals` duplicate engine |
| Email / SMS | Platform Notifications | Custom mailer in module |
| Full-text search | Platform Search | Module-specific Elasticsearch |
| AI chat / insights | Platform AI | Embedded OpenAI in hospital |
| Customer contacts | `CAP-ENT-001` Customer Management | Duplicate CRM in every industry |
| Stock levels | `CAP-ENT-042` Inventory Lifecycle | Warehouse owning inventory rules |
| GL posting | `CAP-ENT-021` Accounting | Finance owning journal entries |
| Hospital patient | `CAP-HLT-001` Patient Lifecycle | Merged `healthcare` monolith |
| Clinic patient | `CAP-HLT-002` Outpatient Lifecycle | Shared `patients` table with hospital |
| Exchange deals | `CAP-ENT-034` FX Operations | Treasury absorbing FX |
| FX rate tables | `CAP-ENT-035` Exchange Rate Management | Settings JSON for rates |
| Employee record | `CAP-ENT-010` Employee Management | Identity user = login only |
| Pay run | `CAP-ENT-015` Payroll Lifecycle | HR calculating net pay |

---

## Capability → bounded context map

One capability has **one owning context**. Related capabilities may share a context only when they share aggregates and ubiquitous language.

```
crm          ← CAP-ENT-001
sales        ← CAP-ENT-002, CAP-RTL-001
human_resources ← CAP-ENT-010..014, 016
payroll      ← CAP-ENT-015
finance      ← CAP-ENT-020, 027
accounting   ← CAP-ENT-021..024, 028
treasury     ← CAP-ENT-025
tax          ← CAP-ENT-026
banking      ← CAP-ENT-030, 031, 036..038
islamic_banking ← CAP-ENT-032, 033
currency_exchange ← CAP-ENT-034, 035
procurement  ← CAP-ENT-040, 041
inventory    ← CAP-ENT-042
warehouse    ← CAP-ENT-043, 048..050
manufacturing ← CAP-ENT-044..046
projects     ← CAP-ENT-047, CAP-CNS-003
university   ← CAP-EDU-001..003, 006, 007
school       ← CAP-EDU-001, 004, 005
hospital     ← CAP-HLT-001, 004, 005, 009, 010
clinic       ← CAP-HLT-002, 003, 006
laboratory   ← CAP-HLT-007
pharmacy     ← CAP-HLT-008
construction ← CAP-CNS-001, 002
real_estate  ← CAP-RE-001..003
hotel        ← CAP-HSP-001, 002
restaurant   ← CAP-HSP-003
pos          ← CAP-RTL-002
government   ← CAP-GOV-001, 002, 006
municipality ← CAP-GOV-003, 004, 005
ngo          ← CAP-NGO-001, 002, 003
```

---

## From capability to module (when ready)

Only **after** capability is registered here:

1. Assign `{namespace}.{capability-id}` module ID ([MODULE_SYSTEM.md](MODULE_SYSTEM.md))
2. Register bounded context in `backend/contexts/registry.py`
3. Implement seven deliverables ([MODULE_STRUCTURE_STANDARD.md](MODULE_STRUCTURE_STANDARD.md))
4. Add to `industry_packs.json` required/optional modules
5. Publish event schemas in `docs/architecture/events/`

---

## Summary counts

| Tier | Count |
|------|-------|
| Platform (reference) | 29 — see CORE_PLATFORM_DESIGN |
| Enterprise | 38 |
| Industry | 35 |
| **Total business capabilities** | **73** |

---

## Related documents

| Document | Role |
|----------|------|
| [CHIEF_ARCHITECT_MANDATE.md](CHIEF_ARCHITECT_MANDATE.md) | Capabilities before CRUD |
| [CORE_PLATFORM_DESIGN.md](CORE_PLATFORM_DESIGN.md) | Platform tier |
| [BOUNDED_CONTEXTS_REGISTRY.md](BOUNDED_CONTEXTS_REGISTRY.md) | Context independence |
| [MODULE_STRUCTURE_STANDARD.md](MODULE_STRUCTURE_STANDARD.md) | Seven deliverables per module |
| ADR-028 | Business capabilities registry |
