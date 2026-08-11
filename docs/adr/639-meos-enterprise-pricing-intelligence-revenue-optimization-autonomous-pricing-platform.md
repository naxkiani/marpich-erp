# ADR 639 — MEOS Enterprise Pricing Intelligence, Revenue Optimization & Autonomous Pricing Management Platform (MEPRIAP)

- **Status:** Accepted
- **Date:** 2026-08-11
- **Deciders:** Chief Enterprise Architect · MEOS Architecture Board
- **Tags:** meos · p282 · mepriap · pricing · revenue-optimization · elasticity · discount · promotion · margin-aware · productization
- **Related:** [ADR 638](638-meos-enterprise-management-accounting-cost-profitability-intelligence-platform.md) · [ADR 637](637-meos-enterprise-financial-planning-budgeting-autonomous-performance-management-platform.md) · [ADR 635](635-meos-enterprise-revenue-billing-quote-to-cash-intelligence-platform.md) · [ADR 634](634-meos-enterprise-sales-intelligence-autonomous-revenue-operations-platform.md) · [ADR 628](628-meos-enterprise-financial-intelligence-autonomous-finance-platform.md) · [ADR 640](640-meos-enterprise-contract-intelligence-commercial-agreement-autonomous-contract-platform.md) · [Law P282](../architecture/ENTERPRISE_MEOS_PRICING_INTELLIGENCE_REVENUE_OPTIMIZATION_AUTONOMOUS_PRICING_PLATFORM.md) · Governance Standard 11.0

## Context

MEOS needs a specialized **Pricing Intelligence / Revenue Optimization / Autonomous Pricing** productization layer — without replacing Sales (P277), Quote-to-Cash (P278), Treasury (P279), FP&A (P280), Management Accounting (P281), or Financial Control (P271), and without ungated price commits.

## Decision

1. Establish SoR **`pricing_operating`** as MEPRIAP fabric under API **`/api/v1/pricing-operating*`**, schema **`pricing_operating_*`**.
2. Capability **`CAP-PLT-MEPRIAP-001`**; fabric id **`meos_enterprise_pricing_intelligence_revenue_optimization_autonomous_pricing_platform_framework`**.
3. **Boundary law (hard):**
   - **P277** = Sales Intelligence / RevOps
   - **P278** = Quote-to-Cash
   - **P279** = Treasury / Liquidity / Cash
   - **P280** = Planning / Budgeting / Performance
   - **P281** = Cost / Profitability / Unit Economics
   - **P271** = Financial Accounting / Financial Control (**authoritative**)
   - **P282** = Pricing Intelligence / Price Optimization / Revenue Optimization / Pricing Governance
4. Federate-by-contract: P277–P281, P271 — never fork Sales/Q2C/Planning/Cost/Finance APIs; never dual-write price lists into peer ledgers without ACL; never local GL.
5. Pricing models, price books and pricing policies are **versioned, explainable, reproducible, auditable**. Material price/discount/promotion commits require **Policy + DoA + Human Governance + Audit** (or published Autonomy Threshold).
6. **No AI Agent may bypass Pricing Policy.** When P281 data is available, revenue optimization **must** evaluate profitability / margin context.
7. Inference → **P214-Z** only; no module-local LLM; no ungated agent price mutation.
8. Twin price/demand scenarios via P265 are non-actuating unless Policy + Workflow + DoA (or autonomy threshold) approve.

## Consequences

- Unlocks Phase 1–4 MEPRIAP roadmap (P282-A…D) and **P283** Contract Intelligence / Commercial Agreement series (delivered as normative law + ADR 640).
- P277 remains Sales; P278 remains Q2C execution; P281 remains cost/profitability; MEPRIAP owns pricing campaigns, versioned books and governed pricing decision overlays.
- Uncontrolled price mutation or policy bypass is an architecture failure.

## Alternatives considered

| Alternative | Rejected because |
|-------------|------------------|
| Embed pricing inside P277 Sales OS | Violates Sales vs Pricing Intelligence depth split |
| Embed inside P278 Q2C | Violates Q2C execution vs pricing optimization |
| Optimize revenue without P281 margin context | Violates margin-aware pricing law |
| Ungated agent price commits | Violates human pricing governance + autonomy thresholds |
| Dual-write price books into Sales/Q2C without ACL | Violates SoR boundaries |

## Compliance checklist

- [x] DDD · CQRS · events · hexagonal boundaries documented
- [x] Peer federation matrix (P277 · P278 · P281 · P280 · P271 · Policy · Workflow · Audit)
- [x] Versioned pricing models/books/policies · deterministic/reproducible decisions
- [x] P277–P281 and P271 boundaries preserved explicitly
- [x] Margin-aware pricing when P281 available
- [x] P283 delivered — [ADR 640 / MECIAP](640-meos-enterprise-contract-intelligence-commercial-agreement-autonomous-contract-platform.md)
