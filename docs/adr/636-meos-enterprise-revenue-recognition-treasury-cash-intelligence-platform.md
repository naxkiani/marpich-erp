# ADR 636 — MEOS Enterprise Revenue Recognition, Treasury & Cash Intelligence Platform (METRCIP)

- **Status:** Accepted
- **Date:** 2026-08-10
- **Deciders:** Chief Enterprise Architect · MEOS Architecture Board
- **Tags:** meos · p279 · metrcip · treasury · cash · liquidity · revenue-recognition · fx · working-capital · bank-connectivity · productization
- **Related:** [ADR 635](635-meos-enterprise-revenue-billing-quote-to-cash-intelligence-platform.md) · [ADR 634](634-meos-enterprise-sales-intelligence-autonomous-revenue-operations-platform.md) · [ADR 628](628-meos-enterprise-financial-intelligence-autonomous-finance-platform.md) · [Law P279](../architecture/ENTERPRISE_MEOS_REVENUE_RECOGNITION_TREASURY_CASH_INTELLIGENCE_PLATFORM.md) · Governance Standard 11.0

## Context

MEOS needs a specialized **Revenue Recognition / Treasury / Cash Intelligence** productization layer — without replacing Financial Intelligence (P271), merging Quote-to-Cash (P278), or forking Treasury/Banking systems of record.

## Decision

1. Establish SoR **`treasury_cash_operating`** as METRCIP fabric under API **`/api/v1/treasury-cash-operating*`**, schema **`treasury_cash_operating_*`**.
2. Capability **`CAP-PLT-METRCIP-001`**; fabric id **`meos_enterprise_revenue_recognition_treasury_cash_intelligence_platform_framework`**.
3. **Boundary law (hard):**
   - **P277** = Sales / RevOps OS
   - **P278** = Quote-to-Cash execution OS
   - **P279** = Revenue Recognition / Treasury / Liquidity / Cash Intelligence OS
   - **P271** = Enterprise Financial Intelligence / Accounting / Financial Control (**authoritative; not replaced**)
4. Federate-by-contract: Treasury, Banking, Accounting, P278, P271, P272–P277, Integration (bank rails) — never dual-write peer schemas; never fork `/api/v1/treasury*`, `/api/v1/quote-to-cash-operating*`, or `/api/v1/autonomous-finance-operating*`; never local GL.
5. Material bank transfers, investments, funding, FX hedges, high-value payments, and write-offs/adjustments require **Policy + Delegation-of-Authority + Human Governance + Dual Control + Audit**; agents recommend; simulation ≠ execute; payments are **idempotent**.
6. Inference → **P214-Z** only; no module-local LLM; no bank SDKs in domain (Integration Platform only); Zero Trust bank connectivity via P268.
7. Twin liquidity stress via P265 is non-actuating unless Policy + Workflow + Dual Control + DoA approve commit to Treasury/Finance peers.

## Consequences

- Unlocks Phase 1–4 METRCIP roadmap (P279-A…D) and **P280** FP&A / Budgeting / Performance series.
- Treasury and Banking remain canonical for cash/bank truth; P271 remains final accounting/control; METRCIP owns operating campaigns and intelligence overlays.
- Treasury auto-commit without Dual Control/DoA is an architecture failure.

## Alternatives considered

| Alternative | Rejected because |
|-------------|------------------|
| Embed Treasury OS inside P271 Finance OS | Violates operational treasury vs financial control split |
| Embed Treasury OS inside P278 Q2C | Violates Q2C vs treasury/liquidity boundary |
| Fork Treasury/Banking APIs into METRCIP | Dual SoR / dual-write risk |
| Local GL or final recognition posting without P271 | P271 / Financial Kernel owns financial control |
| Ungated agent transfer/hedge/fund | Violates Dual Control + human treasury governance |
| Embed bank SDKs in domain | Violates Integration Platform law |

## Compliance checklist

- [x] DDD · CQRS · events · hexagonal boundaries documented
- [x] Peer federation matrix (Treasury · Banking · P278 · P271 · Integration · Policy · Workflow · Audit)
- [x] Material treasury gate law + Dual Control + idempotent payment law
- [x] P271 financial boundary preserved explicitly
- [x] P280 stub announced
