# ADR 635 — MEOS Enterprise Revenue, Billing & Quote-to-Cash Intelligence Platform (MEQTCIP)

- **Status:** Accepted
- **Date:** 2026-08-10
- **Deciders:** Chief Enterprise Architect · MEOS Architecture Board
- **Tags:** meos · p278 · meqtcip · quote-to-cash · billing · invoice · receivables · payments · collections · revenue-assurance · productization
- **Related:** [ADR 634](634-meos-enterprise-sales-intelligence-autonomous-revenue-operations-platform.md) · [ADR 630](630-meos-enterprise-customer-experience-crm-intelligence-autonomous-relationship-platform.md) · [ADR 628](628-meos-enterprise-financial-intelligence-autonomous-finance-platform.md) · [ADR 636](636-meos-enterprise-revenue-recognition-treasury-cash-intelligence-platform.md) · [Law P278](../architecture/ENTERPRISE_MEOS_REVENUE_BILLING_QUOTE_TO_CASH_INTELLIGENCE_PLATFORM.md) · Governance Standard 11.0

## Context

MEOS needs a specialized **Quote-to-Cash / Revenue Cycle** productization layer — without merging Sales Intelligence (P277), Financial Intelligence (P271), or forking Sales/Accounting systems of record.

## Decision

1. Establish SoR **`quote_to_cash_operating`** as MEQTCIP fabric under API **`/api/v1/quote-to-cash-operating*`**, schema **`quote_to_cash_operating_*`**.
2. Capability **`CAP-PLT-MEQTCIP-001`**; fabric id **`meos_enterprise_revenue_billing_quote_to_cash_intelligence_platform_framework`**.
3. **Boundary law (hard):**
   - **P273** = CX / CRM / Relationship Intelligence OS
   - **P277** = Sales Execution / RevOps / Sales Intelligence OS
   - **P278** = Quote-to-Cash / Order / Billing / Collection Execution OS
   - **P271** = Financial Intelligence / Accounting / Financial Control
4. Federate-by-contract: Sales (quote/order), Accounting (invoice/AR), P277, P271, P272–P276, Integration (payment rails) — never dual-write peer schemas; never fork `/api/v1/sales*`, `/api/v1/sales-revenue-operating*`, or `/api/v1/autonomous-finance-operating*`; never local GL.
5. Material billing, refund, credit, write-off, commercial adjustment, and high-risk collection require **Policy + Delegation-of-Authority + Human Governance + Audit**; agents recommend; simulation ≠ execute; payment processing is **idempotent**.
6. Inference → **P214-Z** only; no module-local LLM; no payment provider SDKs in domain (Integration Platform only).
7. Twin cash/collection scenarios via P265 are non-actuating unless Policy + Workflow + DoA approve commit to Accounting/Finance peers.

## Consequences

- Unlocks Phase 1–4 MEQTCIP roadmap (P278-A…D) and **P279** Revenue Recognition / Treasury / Cash series (delivered as normative law + ADR 636).
- Sales and Accounting remain canonical for order and invoice/AR truth; MEQTCIP owns operating campaigns and intelligence overlays.
- Financial auto-commit without DoA is an architecture failure.
- P271 remains authoritative Financial Intelligence and Financial Control; P278 provides operational revenue-cycle events and execution context.

## Alternatives considered

| Alternative | Rejected because |
|-------------|------------------|
| Embed Q2C inside P277 Sales OS | Violates P277 vs P278 boundary |
| Embed Q2C inside P271 Finance OS | Violates operational cycle vs financial control split |
| Fork Sales/Accounting APIs into MEQTCIP | Dual SoR / dual-write risk |
| Local GL or revenue recognition posting in Q2C OS | P271 / Financial Kernel owns financial control |
| Ungated agent refund/write-off/payment commit | Violates human financial governance |
| Embed Stripe/Twilio-class SDKs in domain | Violates Integration Platform law |

## Compliance checklist

- [x] DDD · CQRS · events · hexagonal boundaries documented
- [x] Peer federation matrix (Sales · Accounting · P277 · P271 · Integration · Policy · Workflow · Audit)
- [x] Material financial gate law + idempotent payment law
- [x] AI explainability + human gates for high-impact actions
- [x] P279 delivered — [ADR 636 / METRCIP](636-meos-enterprise-revenue-recognition-treasury-cash-intelligence-platform.md)
