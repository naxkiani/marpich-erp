# MEOS Application Registry

**Generated:** 2026-08-12 · **Source of truth (machine):** [MEOS_APPLICATION_REGISTRY.v1.yaml](MEOS_APPLICATION_REGISTRY.v1.yaml)  
**P313 (2026-08-18):** Live API Q2C + healthcare **PASS** on Postgres. **No app promoted to ACTIVE.** Overall still `NOT_READY`.  
**P318 (2026-08-18):** Intelligence gate **FOUNDATION** only — no registry promotions.  
**P319 (2026-08-18):** Automation **BLOCK_AUTOMATION** — no ACTIVE automations.  
**P320 (2026-08-18):** Experience **FUNCTIONAL** only — no registry promotions to ACTIVE.  
**P321 (2026-08-18):** Integration fabric **IMPLEMENTED** (code) — **0 ACTIVE** external integrations.  
**P322 (2026-08-18):** Extension ecosystem **GOVERNED** (Plugin Platform + install≠activate). Marketplace seeds are DEMO, **not CERTIFIED**. **No app promoted to ACTIVE.**  
**P323 (2026-08-18):** Developer platform **DOCUMENTED/DEVELOPABLE** (manifest SDK). **Not PUBLISHABLE.** No app promoted to ACTIVE.  
**P324 (2026-08-18):** Release engineering **NOT_RELEASE_CANDIDATE**. **No production deploy.** No app promoted to ACTIVE.  
**P325 (2026-08-18):** Continuous evolution **BLOCKED** (no production). No app promoted to ACTIVE.  
**P326 (2026-08-18):** Business value **NOT_MEASURED** (outcomes IDENTIFIED only). No app promoted to ACTIVE.  
**P327 (2026-08-18):** Strategy **NOT_DECLARED** (PLATFORM_GATE drafts only). No app promoted to ACTIVE. `projects` remains SCAFFOLDED.  
**P328 (2026-08-18):** Risk **RISK_AWARE** (R-01…R-07). Production resilience **NOT_VERIFIED**. No app promoted to ACTIVE.  
**P329 (2026-08-18):** Continuity **DOCUMENTED**. Production IR **not active**. No app promoted to ACTIVE.  
**P330 (2026-08-18):** Closed-loop ops **GATED** at L0. `BLOCK_AUTOMATION` held. No app promoted to ACTIVE.  
**P331 (2026-08-18):** Optimization **BLOCKED** (cannot MEASURE). Local p95 not reused as prod SLO. No app promoted to ACTIVE.  
**P332 (2026-08-18):** Knowledge **INVENTORIED**. Lessons DRAFT (`validated_count: 0`). No app promoted to ACTIVE.  
**P333 (2026-08-18):** Capability overlay **MAPPED**. `operational_count: 0` · skills **0** · readiness **NOT_MEASURED**. No app promoted to ACTIVE. HR remains employment SoR — not HCM/LMS/talent.  
**P334 (2026-08-18):** Change overlay **INVENTORIED**. `production_change_count: 0` · **ADOPTED = false**. No app promoted to ACTIVE. `projects` remains SCAFFOLDED.  
**P335 (2026-08-19):** Portfolio overlay **INVENTORIED**. No budget/ROI. No app promoted to ACTIVE. `projects` remains SCAFFOLDED.  
**P336 (2026-08-19):** Architecture overlay **INVENTORIED**. Registry remains SoR (47 apps, 0 ACTIVE). No CMDB/ITSM. See [MEOS_P336_ARCHITECTURE_RATIONALIZATION.md](./MEOS_P336_ARCHITECTURE_RATIONALIZATION.md).  
**P337 (2026-08-19):** Data overlay **INVENTORIED**. **0** published data products. No warehouse/mesh/catalog/MDM product. See [MEOS_P337_DATA_ARCHITECTURE.md](./MEOS_P337_DATA_ARCHITECTURE.md).  
**P338 (2026-08-19):** Decision overlay **FOUNDATION**. **0** executed decisions. KPI trust **NOT_MEASURED**. No BI/KPI/AI product. See [MEOS_P338_DECISION_INTELLIGENCE.md](./MEOS_P338_DECISION_INTELLIGENCE.md).  
**P339 (2026-08-19):** Execution overlay **INVENTORIED**. **0** authorized actions. **0** realized benefits. `projects` remains SCAFFOLDED. See [MEOS_P339_DECISION_EXECUTION.md](./MEOS_P339_DECISION_EXECUTION.md).  
**P340 (2026-08-19):** G26 enablement **OUTCOME_B**. G26 **BLOCKED**. No production execution. See [MEOS_P340_G26_EXECUTION_ENABLEMENT.md](./MEOS_P340_G26_EXECUTION_ENABLEMENT.md).  
**P341 (2026-08-19):** Infrastructure **OUTCOME_B**. PRODUCTION_CERTIFIED **NO**. P0 = **1**. See [MEOS_P341_PRODUCTION_INFRASTRUCTURE_READINESS.md](./MEOS_P341_PRODUCTION_INFRASTRUCTURE_READINESS.md).  
**P342 (2026-08-19):** Recert **OUTCOME_B**. **P313_RE_CERTIFICATION_READY = false**. No ACTIVE promotions. See [MEOS_P342_PRODUCTION_GATE_CLOSURE.md](./MEOS_P342_PRODUCTION_GATE_CLOSURE.md).  
**P343 (2026-08-19):** Final gate **OUTCOME_B**. **PRODUCTION_CERTIFIED = NO**. **GO_LIVE_READY = NO**. No ACTIVE promotions. See [MEOS_P343_FINAL_PRODUCTION_CERTIFICATION.md](./MEOS_P343_FINAL_PRODUCTION_CERTIFICATION.md).  
**P344 (2026-08-19):** Launch **STOPPED**. No ACTIVE promotions. See [MEOS_P344_GO_LIVE_EXECUTION.md](./MEOS_P344_GO_LIVE_EXECUTION.md).  
**P345 (2026-08-19):** G26 provisioning **BLOCKED**. No ACTIVE promotions. See [MEOS_P345_G26_PROVISIONING.md](./MEOS_P345_G26_PROVISIONING.md).  
**P346 (2026-08-19):** G26 evidence **STOPPED**. No ACTIVE promotions. See [MEOS_P346_G26_BLOCKER_CLOSURE.md](./MEOS_P346_G26_BLOCKER_CLOSURE.md).  
**P347 (2026-08-19):** **EXT-G26 UNRESOLVED**. No ACTIVE promotions. See [MEOS_P347_EXTERNAL_HANDOFF.md](./MEOS_P347_EXTERNAL_HANDOFF.md).  
**P348 (2026-08-19):** **G26_READY = FALSE**. No ACTIVE promotions. See [MEOS_EXT_G26_INFRASTRUCTURE_HANDOFF.md](./MEOS_EXT_G26_INFRASTRUCTURE_HANDOFF.md).  
**Rule:** `ACTIVE` only when login-scoped create/read/update/search works end-to-end. Docs-only / empty scaffolds are never ACTIVE.

## Status legend

`DESIGNED` → `SCAFFOLDED` → `IMPLEMENTED` → `INTEGRATED` → `TESTED` → `HARDENED` → `PRODUCTION_READY` → `ACTIVE`

## Wave 01 — Platform Core

| App ID | Name | Status | FE | BE | Notes |
|--------|------|--------|----|----|-------|
| `identity` | Identity & Access | INTEGRATED | login + account | JWT APIs | Core SoR |
| `authorization` | Authorization | IMPLEMENTED | via shell | check APIs | Deny-by-default server-side |
| `core_platform` | Tenant / Module activation | INTEGRATED | Dashboard | platform APIs | |
| `notifications` | Notification Platform | INTEGRATED* | desk + shell | inbox APIs | *shell auth wired in Wave 01 |
| `search` | Enterprise Search | INTEGRATED* | shell | query APIs | *auth headers required |
| `audit` | Audit Platform | INTEGRATED | Audit desk | entries APIs | |
| `workflow` | Workflow Engine | IMPLEMENTED→INTEGRATED | Task Center | tasks/definitions | UI added Wave 01 |
| `ai` | AI Platform | IMPLEMENTED | shell copilot | `/ai/assist` | Auth session headers |
| `documents` | Document Exchange | IMPLEMENTED | Document Studio | documents APIs | blob SoR |
| `organization` | Organization | IMPLEMENTED | partial | APIs | |
| `settings` | Settings | IMPLEMENTED | partial | APIs | |
| `application_registry` | MEOS App Registry | IMPLEMENTED | nav/palette | docs+TS | metadata-driven nav |

## Wave 02 — Business Core (first Functional)

| App ID | Name | Status | FE | BE | Notes |
|--------|------|--------|----|----|-------|
| `crm` | CRM (CAP-ENT-001) | TESTED | `/crm` desk | contacts + opportunities | create/list/win/lose + events + Postgres schema |
| `sales` | Sales (CAP-ENT-002) | TESTED | `/sales` desk | quotations + orders | CRM win → draft quote → send → order + events + Postgres schema |
| `inventory` | Inventory (CAP-ENT-042) | TESTED | `/inventory` desk | stock levels + reservations | sales.order.placed → reserve SKU + events + migration 048 |
| `accounting` | Accounting AR (CAP-ENT-023) | TESTED | `/accounting` desk | AR invoices | sales.order.placed → draft → issue → receive-payment → accounting.payment.received + migration 052 |
| `procurement` | Procurement (CAP-ENT-040) | TESTED | `/procurement` desk | requisitions + goods receipt | reorder → draft → approve → receive → inventory restock + migration 051 |
| `human_resources` | HR (CAP-ENT-010) | TESTED | `/hr` desk | employees | hire → list → terminate + events + migration 053 |
| `payroll` | Payroll (CAP-ENT-015) | TESTED | `/payroll` desk | employee projection + runs | HR hire ACL → pay run → payroll.run.completed + migration 054 |
| `tax` | Tax (CAP-ENT-026) | TESTED | `/tax` desk | liabilities + returns | payroll.run.completed → liability → file return + migration 055 |

**Harden:** `scripts/meos-wave02-q2c-loop.sh` + `.github/workflows/meos-wave02-smoke.yml` — full closed loop on Postgres.

| `hospital` | Hospital (CAP-HLT-001+) | TESTED | `/healthcare/hospital` | patients/admissions/encounters + care-events | Hospital→Lab→Pharmacy loop + `meos-healthcare-loop.sh` |
| `clinic` | Clinic (CAP-HLT-002+) | TESTED | `/healthcare/clinic` | outpatient + lab result notes | `clinic.encounter.completed` → lab/pharmacy ACL |
| `pharmacy` | Pharmacy (CAP-HLT-008) | TESTED | `/healthcare/pharmacy` | Rx + dispense | events → hospital care-events |
| `laboratory` | Laboratory (CAP-HLT-007) | TESTED | `/healthcare/laboratory` | order→sample→result | events → hospital care-events |

**Harden:** `scripts/meos-wave02-q2c-loop.sh` + `.github/workflows/meos-wave02-smoke.yml` — full closed loop on Postgres.  
**Healthcare:** `scripts/meos-healthcare-loop.sh` + `.github/workflows/meos-healthcare-smoke.yml`.  
**Money-path:** migrations 038–045 via `run-migrations.sh` + `.github/workflows/meos-money-path-smoke.yml`.

## Domain apps with UI (demo / partial)

| App ID | Status | Route |
|--------|--------|-------|
| `hospital` | TESTED | `/healthcare/hospital` |
| `clinic` | TESTED | `/healthcare/clinic` |
| `crm` | TESTED | `/crm` |
| `sales` | TESTED | `/sales` |
| `inventory` | TESTED | `/inventory` |
| `accounting` | TESTED | `/accounting` |
| `procurement` | TESTED | `/procurement` |
| `human_resources` | TESTED | `/hr` |
| `payroll` | TESTED | `/payroll` |
| `tax` | TESTED | `/tax` |
| `pharmacy` | TESTED | `/healthcare/pharmacy` |
| `laboratory` | TESTED | `/healthcare/laboratory` |
| `university` | IMPLEMENTED | `/education/university` |
| `banking` | IMPLEMENTED | `/banking/analytics` |
| `messenger` | IMPLEMENTED | `/enterprise/messenger` |
| `plugins` | IMPLEMENTED | `/enterprise/plugins` |
| `identity_federation` | IMPLEMENTED | `/enterprise/federation` |
| `enterprise_observability` | IMPLEMENTED | `/enterprise/observability` |
| `enterprise_scheduler` | IMPLEMENTED | `/enterprise/scheduler` |
| `enterprise_connector_framework` | IMPLEMENTED | `/enterprise/connector-framework` |
| `enterprise_integration_studio` | IMPLEMENTED | `/enterprise/integration-studio` |

## Empty scaffolds (not ACTIVE) — P2 keep coming_soon

`construction`, `currency_exchange`, `government`, `hotel`, `islamic_banking`, `manufacturing`, `ngo`, `projects`, `real_estate`, `restaurant`, `school`, `warehouse` — status **SCAFFOLDED** / empty tree. Frozen in `EMPTY_INDUSTRY_SCAFFOLD_IDS` + `DEFERRED_CONTEXT_IDS`. **Do not expand** without a Functional vertical slice.

## Blueprint fabrics (not Functional) — P2 stop catalog inflation

| App ID | Status | Notes |
|--------|--------|-------|
| `quantum` | BLUEPRINT | P215 catalogs/docs; APIs off unless `MARPICH_ENABLE_BLUEPRINT_APIS` or `profile=blueprint` |
| `robotics` | BLUEPRINT | P216 |
| `biotechnology` | BLUEPRINT | P217 |
| `space` | BLUEPRINT | P218 |
| `civilization` | BLUEPRINT | P219 |

Law: `docs/adr/p2-blueprint-scaffold-honesty.md`. Blueprint ≠ TESTED / PRODUCTION_READY / ACTIVE.

## Missing packages referenced by ROUTER_SPECS (gated) — P3 contract

`mfa`, `adaptive_authentication`, `reporting`, `fraud_detection`, `data_protection`, `ai_governance`, `ai_security`, `ai_cfo_assistant`, `enterprise_*` extras, `grc`, `security`, financial AI extras — see Architecture Status. Status **DESIGNED** (no package).

**P3:** module-path baseline `backend/tests/architecture/missing_router_packages_baseline.json` + contracts `tests/contracts/test_router_package_contracts.py` + CI `meos-p3-router-contracts.yml`. New missing ROUTER/SERVICE specs fail CI; landing a package requires shrinking the baseline (ADR: `docs/adr/p3-router-package-contracts.md`).

## Score summary (honest)

| Layer | Score (0–100) |
|-------|---------------|
| Architecture docs | 90 |
| Platform core APIs | 72 |
| ONE shell UX | 78 (Wave 01 auth-wired) |
| Persistence (default memory) | 65 (Postgres :5433 + CRM + Sales + Inventory + AR invoices) |
| CI / tests gate | 82 (Wave 01 smoke + Wave 02 Q2C memory/postgres loop) |
| Production readiness | 35 |

## Status legend (extended)

`DESIGNED` → `SCAFFOLDED` → **`BLUEPRINT`** (catalog/docs only) → `IMPLEMENTED` → … → `ACTIVE`  
`BLUEPRINT` never counts toward production readiness scores.
