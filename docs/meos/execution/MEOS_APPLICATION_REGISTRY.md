# MEOS Application Registry

**Generated:** 2026-08-12 · **Source of truth (machine):** [MEOS_APPLICATION_REGISTRY.v1.yaml](MEOS_APPLICATION_REGISTRY.v1.yaml)  
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
| `accounting` | Accounting AR (CAP-ENT-023) | TESTED | `/accounting` desk | AR invoices | sales.order.placed → draft → issue + journal intent + migration 049 |
| `procurement` | Procurement (CAP-ENT-040) | TESTED | `/procurement` desk | requisitions | inventory.reorder.triggered → draft → submit → approve + migration 050 |

## Domain apps with UI (demo / partial)

| App ID | Status | Route |
|--------|--------|-------|
| `hospital` | IMPLEMENTED | `/healthcare/hospital` |
| `clinic` | IMPLEMENTED | `/healthcare/clinic` |
| `crm` | TESTED | `/crm` |
| `sales` | TESTED | `/sales` |
| `inventory` | TESTED | `/inventory` |
| `accounting` | TESTED | `/accounting` |
| `procurement` | TESTED | `/procurement` |
| `pharmacy` | IMPLEMENTED | `/healthcare/pharmacy` |
| `laboratory` | IMPLEMENTED | `/healthcare/laboratory` |
| `university` | IMPLEMENTED | `/education/university` |
| `banking` | IMPLEMENTED | `/banking/analytics` |
| `messenger` | IMPLEMENTED | `/enterprise/messenger` |
| `plugins` | IMPLEMENTED | `/enterprise/plugins` |
| `identity_federation` | IMPLEMENTED | `/enterprise/federation` |
| `enterprise_observability` | IMPLEMENTED | `/enterprise/observability` |
| `enterprise_scheduler` | IMPLEMENTED | `/enterprise/scheduler` |
| `enterprise_connector_framework` | IMPLEMENTED | `/enterprise/connector-framework` |
| `enterprise_integration_studio` | IMPLEMENTED | `/enterprise/integration-studio` |

## Empty scaffolds (not ACTIVE)

`construction`, `currency_exchange`, `government`, `hotel`, `human_resources`, `islamic_banking`, `manufacturing`, `ngo`, `payroll`, `projects`, `real_estate`, `restaurant`, `school`, `tax`, `warehouse` — status **SCAFFOLDED** / empty tree.

## Missing packages referenced by ROUTER_SPECS (gated)

`mfa`, `adaptive_authentication`, `reporting`, `fraud_detection`, `data_protection`, `ai_governance`, `ai_security`, `ai_cfo_assistant`, `enterprise_*` extras, `grc`, `security`, financial AI extras — see Architecture Status. Status **DESIGNED** (no package).

## Score summary (honest)

| Layer | Score (0–100) |
|-------|---------------|
| Architecture docs | 90 |
| Platform core APIs | 72 |
| ONE shell UX | 78 (Wave 01 auth-wired) |
| Persistence (default memory) | 65 (Postgres :5433 + CRM + Sales + Inventory + AR invoices) |
| CI / tests gate | 80 (Wave 01 smoke + CRM + Sales + Inventory + AR + Procurement flow tests) |
| Production readiness | 35 |
