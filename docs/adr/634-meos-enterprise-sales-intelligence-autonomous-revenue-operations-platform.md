# ADR 634 — MEOS Enterprise Sales Intelligence & Autonomous Revenue Operations Platform (MESIARO)

- **Status:** Accepted
- **Date:** 2026-08-10
- **Deciders:** Chief Enterprise Architect · MEOS Architecture Board
- **Tags:** meos · p277 · mesiaro · sales · revenue-operations · lead-to-revenue · pipeline · forecasting · pricing · quotes · productization
- **Related:** [ADR 633](633-meos-enterprise-procurement-intelligence-autonomous-sourcing-platform.md) · [ADR 630](630-meos-enterprise-customer-experience-crm-intelligence-autonomous-relationship-platform.md) · [ADR 628](628-meos-enterprise-financial-intelligence-autonomous-finance-platform.md) · [ADR 635](635-meos-enterprise-revenue-billing-quote-to-cash-intelligence-platform.md) · [ADR 639](639-meos-enterprise-pricing-intelligence-revenue-optimization-autonomous-pricing-platform.md) · [Law P277](../architecture/ENTERPRISE_MEOS_SALES_INTELLIGENCE_AUTONOMOUS_REVENUE_OPERATIONS_PLATFORM.md) · Governance Standard 11.0

## Context

MEOS needs a specialized **Sales Intelligence / Revenue Operations** productization layer for Lead-to-Revenue — without merging Customer Experience (P273), Financial Intelligence (P271), or forking CRM/Sales systems of record.

## Decision

1. Establish SoR **`sales_revenue_operating`** as MESIARO fabric under API **`/api/v1/sales-revenue-operating*`**, schema **`sales_revenue_operating_*`**.
2. Capability **`CAP-PLT-MESIARO-001`**; fabric id **`meos_enterprise_sales_intelligence_autonomous_revenue_operations_platform_framework`**.
3. **Boundary law (hard):**
   - **P273** = CX / CRM / Relationship Intelligence OS
   - **P277** = Sales Execution / RevOps / Sales Intelligence OS
   - **P271** = Financial Intelligence / Revenue Financial Control
4. Federate-by-contract: CRM (leads/opportunities), Sales (quotes/orders), P273, P271, P272–P276 — never dual-write peer schemas; never fork `/api/v1/crm*`, `/api/v1/sales*`, or `/api/v1/customer-relationship-operating*`.
5. Material pricing, discount, quote, and commercial commitments require **Policy + Delegation-of-Authority + Human Governance + Audit**; agents recommend; simulation ≠ execute.
6. Inference → **P214-Z** only; no module-local LLM.
7. Twin revenue scenarios via P265 are non-actuating unless Policy + Workflow + DoA approve commit to Sales/Finance peers.

## Consequences

- Unlocks Phase 1–4 MESIARO roadmap (P277-A…D) and **P278** Quote-to-Cash / Billing series (delivered as normative law + ADR 635).
- CRM and Sales remain canonical for opportunity and quote/order truth; MESIARO owns operating campaigns and intelligence overlays.
- Commercial auto-commit without DoA is an architecture failure.

## Alternatives considered

| Alternative | Rejected because |
|-------------|------------------|
| Embed RevOps inside P273 CX OS | Violates P273 vs P277 boundary |
| Fork CRM/Sales APIs into MESIARO | Dual SoR / dual-write risk |
| Local GL or revenue recognition in Sales OS | P271 / Financial Kernel owns financial control |
| Ungated agent quote/order commit | Violates human commercial governance |

## Compliance checklist

- [x] DDD · CQRS · events · hexagonal boundaries documented
- [x] Peer federation matrix (CRM · Sales · P273 · P271 · Policy · Workflow · Audit)
- [x] Material commercial gate law
- [x] AI explainability + bias monitoring on scoring/prediction
- [x] P278 delivered — [ADR 635 / MEQTCIP](635-meos-enterprise-revenue-billing-quote-to-cash-intelligence-platform.md)
