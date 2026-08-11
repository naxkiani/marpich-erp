# ADR 641 — MEOS Enterprise Commercial Compliance, Obligation & Contract Performance Intelligence Platform (MECCPI)

- **Status:** Accepted
- **Date:** 2026-08-11
- **Deciders:** Chief Enterprise Architect · MEOS Architecture Board
- **Tags:** meos · p284 · meccpi · commercial-compliance · obligation · sla · kpi · penalty · service-credit · productization
- **Related:** [ADR 640](640-meos-enterprise-contract-intelligence-commercial-agreement-autonomous-contract-platform.md) · [ADR 639](639-meos-enterprise-pricing-intelligence-revenue-optimization-autonomous-pricing-platform.md) · [ADR 635](635-meos-enterprise-revenue-billing-quote-to-cash-intelligence-platform.md) · [ADR 634](634-meos-enterprise-sales-intelligence-autonomous-revenue-operations-platform.md) · [ADR 628](628-meos-enterprise-financial-intelligence-autonomous-finance-platform.md) · [ADR 642](642-meos-enterprise-service-management-sla-operations-intelligent-service-delivery-platform.md) · [Law P284](../architecture/ENTERPRISE_MEOS_COMMERCIAL_COMPLIANCE_OBLIGATION_CONTRACT_PERFORMANCE_INTELLIGENCE_PLATFORM.md) · Governance Standard 11.0

## Context

MEOS needs a specialized **Commercial Compliance / Obligation Assurance / Contract Performance** productization layer — without replacing Contract Lifecycle (P283), Sales (P277), Q2C (P278), Pricing (P282), Cost (P281), or Financial Control (P271), and without ungated penalty/service-credit enforcement.

## Decision

1. Establish SoR **`commercial_performance_operating`** as MECCPI fabric under API **`/api/v1/commercial-performance-operating*`**, schema **`commercial_performance_operating_*`**.
2. Capability **`CAP-PLT-MECCPI-001`**; fabric id **`meos_enterprise_commercial_compliance_obligation_contract_performance_intelligence_platform_framework`**.
3. **Boundary law (hard):**
   - **P283** = Contract Intelligence / Agreement Lifecycle / Terms (**definition**)
   - **P284** = Commercial Compliance / Obligation Assurance / Performance (**execution assurance**)
   - **P284 does not replace P283**
4. Federate-by-contract: P283, P277–P282, P271, Documents — never fork peer APIs; never dual-write peer ledgers; evidence binaries via `document_id` only.
5. Performance/SLA/KPI/compliance policies are **versioned, explainable, reproducible, auditable**. Material penalty, service credit and binding corrective actions require **Policy + DoA + Human Governance + Audit** (or published Autonomy Threshold).
6. **No AI Agent may create/execute binding commercial actions outside Policy + Delegation Authority.**
7. Inference → **P214-Z** only; no module-local LLM.
8. Twin performance scenarios via P265 are non-actuating unless Policy + Workflow + DoA (or autonomy threshold) approve.

## Consequences

- Unlocks Phase 1–4 MECCPI roadmap (P284-A…D) and **P285** Service Management / SLA Operations series (delivered as normative law + ADR 642).
- P283 remains contract definition SoR; MECCPI owns performance campaigns, measurements, exceptions and gated assurance overlays.
- Ungated penalty/credit enforcement or merging P283+P284 SoRs is an architecture failure.

## Alternatives considered

| Alternative | Rejected because |
|-------------|------------------|
| Embed performance assurance inside P283 | Violates definition vs execution-assurance split |
| Enforce penalties by dual-writing GL locally | P271 / Financial Kernel owns financial control |
| Store evidence PDFs in performance tables | Violates Document Exchange law |
| Ungated agent penalty/credit execution | Violates human commercial governance |

## Compliance checklist

- [x] DDD · CQRS · events · hexagonal boundaries documented
- [x] Peer federation matrix (P283 · P278 · P277 · P281 · Documents · Policy · Workflow · Audit)
- [x] Versioned performance/SLA/KPI/compliance policies · `document_id` evidence refs
- [x] P283 boundary preserved explicitly (definition ≠ assurance)
- [x] No ungated binding commercial actions
- [x] P285 delivered — [ADR 642 / MESMIP](642-meos-enterprise-service-management-sla-operations-intelligent-service-delivery-platform.md)
