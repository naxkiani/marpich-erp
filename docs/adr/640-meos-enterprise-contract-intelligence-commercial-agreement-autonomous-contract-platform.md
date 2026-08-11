# ADR 640 — MEOS Enterprise Contract Intelligence, Commercial Agreement & Autonomous Contract Management Platform (MECIAP)

- **Status:** Accepted
- **Date:** 2026-08-11
- **Deciders:** Chief Enterprise Architect · MEOS Architecture Board
- **Tags:** meos · p283 · meciap · contract · agreement · obligation · sla · renewal · negotiation · productization
- **Related:** [ADR 639](639-meos-enterprise-pricing-intelligence-revenue-optimization-autonomous-pricing-platform.md) · [ADR 638](638-meos-enterprise-management-accounting-cost-profitability-intelligence-platform.md) · [ADR 635](635-meos-enterprise-revenue-billing-quote-to-cash-intelligence-platform.md) · [ADR 634](634-meos-enterprise-sales-intelligence-autonomous-revenue-operations-platform.md) · [ADR 628](628-meos-enterprise-financial-intelligence-autonomous-finance-platform.md) · [ADR 641](641-meos-enterprise-commercial-compliance-obligation-contract-performance-intelligence-platform.md) · [Law P283](../architecture/ENTERPRISE_MEOS_CONTRACT_INTELLIGENCE_COMMERCIAL_AGREEMENT_AUTONOMOUS_CONTRACT_PLATFORM.md) · Governance Standard 11.0

## Context

MEOS needs a specialized **Contract Intelligence / Commercial Agreement / Autonomous Contract Management** productization layer — without replacing Sales (P277), Quote-to-Cash (P278), Pricing (P282), Cost/Profitability (P281), Planning (P280), Treasury (P279), Financial Control (P271), or Document Exchange, and without ungated binding contractual commitments.

## Decision

1. Establish SoR **`contract_operating`** as MECIAP fabric under API **`/api/v1/contract-operating*`**, schema **`contract_operating_*`**.
2. Capability **`CAP-PLT-MECIAP-001`**; fabric id **`meos_enterprise_contract_intelligence_commercial_agreement_autonomous_contract_platform_framework`**.
3. **Boundary law (hard):**
   - **P277** = Sales Intelligence / RevOps
   - **P278** = Quote-to-Cash
   - **P279** = Treasury / Liquidity / Cash
   - **P280** = Planning / Budgeting / Performance
   - **P281** = Cost / Profitability
   - **P282** = Pricing Intelligence
   - **P271** = Financial Accounting / Financial Control (**authoritative**)
   - **Documents** = Document binaries, versions, e-sign (**authoritative for file content**)
   - **P283** = Contract Intelligence / Agreement Lifecycle / Commercial Terms / Obligations / Contract Governance
4. Federate-by-contract: P277–P282, P271, Documents — never fork peer APIs; never dual-write peer ledgers; never store PDF/binary in contract tables (`document_id` only).
5. Contracts, templates, clauses and policies are **versioned, explainable, reproducible, auditable**. Material create/amend/terminate/renew commits require **Policy + DoA + Human Governance + Audit** (or published Autonomy Threshold).
6. **No AI Agent may create, change, or terminate binding contractual commitments outside Policy + Delegation Authority.**
7. Inference → **P214-Z** only; no module-local LLM.
8. Twin contract scenarios via P265 are non-actuating unless Policy + Workflow + DoA (or autonomy threshold) approve.

## Consequences

- Unlocks Phase 1–4 MECIAP roadmap (P283-A…D) and **P284** Commercial Compliance / Obligation & Contract Performance series (delivered as normative law + ADR 641).
- P277 remains Sales; P278 remains Q2C; P282 remains Pricing; Documents remain file SoR; MECIAP owns contract campaigns, structured terms/obligations and governed lifecycle overlays.
- Ungated binding commitment or local document blob storage is an architecture failure.

## Alternatives considered

| Alternative | Rejected because |
|-------------|------------------|
| Embed contracts inside P277 Sales OS | Violates Sales vs Contract Intelligence depth split |
| Embed inside P278 Q2C | Violates Q2C execution vs agreement lifecycle |
| Store PDF/binary in contract tables | Violates Document Exchange law |
| Ungated agent execute/amend/terminate | Violates human contract governance |
| Dual-write orders/AR from contract OS | Violates P278/P271 SoR boundaries |

## Compliance checklist

- [x] DDD · CQRS · events · hexagonal boundaries documented
- [x] Peer federation matrix (P277 · P278 · P282 · P281 · Documents · Policy · Workflow · Audit)
- [x] Versioned contracts/templates/policies · `document_id` only
- [x] P277–P282 and P271/Documents boundaries preserved explicitly
- [x] No ungated binding contractual commitments
- [x] P284 delivered — [ADR 641 / MECCPI](641-meos-enterprise-commercial-compliance-obligation-contract-performance-intelligence-platform.md)
