# ADR 638 — MEOS Enterprise Management Accounting, Cost & Profitability Intelligence Platform (MEMACPI)

- **Status:** Accepted
- **Date:** 2026-08-11
- **Deciders:** Chief Enterprise Architect · MEOS Architecture Board
- **Tags:** meos · p281 · memacpi · management-accounting · cost · profitability · abc · unit-economics · cost-to-serve · productization
- **Related:** [ADR 637](637-meos-enterprise-financial-planning-budgeting-autonomous-performance-management-platform.md) · [ADR 636](636-meos-enterprise-revenue-recognition-treasury-cash-intelligence-platform.md) · [ADR 628](628-meos-enterprise-financial-intelligence-autonomous-finance-platform.md) · [ADR 639](639-meos-enterprise-pricing-intelligence-revenue-optimization-autonomous-pricing-platform.md) · [Law P281](../architecture/ENTERPRISE_MEOS_MANAGEMENT_ACCOUNTING_COST_PROFITABILITY_INTELLIGENCE_PLATFORM.md) · Governance Standard 11.0

## Context

MEOS needs a specialized **Management Accounting / Cost / Profitability** productization layer — without replacing Financial Control (P271), Treasury (P279), or FP&A (P280), and without mutating the authoritative ledger.

## Decision

1. Establish SoR **`management_accounting_operating`** as MEMACPI fabric under API **`/api/v1/management-accounting-operating*`**, schema **`management_accounting_operating_*`**.
2. Capability **`CAP-PLT-MEMACPI-001`**; fabric id **`meos_enterprise_management_accounting_cost_profitability_intelligence_platform_framework`**.
3. **Boundary law (hard):**
   - **P271** = Financial Accounting / Financial Control (**authoritative**)
   - **P279** = Treasury / Liquidity / Cash
   - **P280** = Planning / Budgeting / Forecasting / Performance
   - **P281** = Management Accounting / Cost / Profitability / Unit Economics
4. Federate-by-contract: P271, P280, P279, Accounting, P272–P278 — never dual-write cost/allocation into GL; never fork Finance/Planning/Treasury APIs; never local GL.
5. Allocation rules and cost/profitability models are **versioned, explainable, reproducible, auditable**. Material cost reallocations, significant optimizations, and intercompany pricing *context* changes require **Policy + DoA + Human Governance + Audit**.
6. Transfer pricing **context** only — Legal/Tax final determination remains P269 + P271 + external rules.
7. Inference → **P214-Z** only; no module-local LLM; no agent ledger mutation outside Policy Boundary.
8. Twin cost/pricing scenarios via P265 are non-actuating unless Policy + Workflow + DoA approve.

## Consequences

- Unlocks Phase 1–4 MEMACPI roadmap (P281-A…D) and **P282** Pricing Intelligence / Revenue Optimization series (delivered as normative law + ADR 639).
- P271 remains ledger/control; P280 remains planning; P279 remains cash; MEMACPI owns management accounting campaigns and interpretive profitability overlays.
- Uncontrolled ledger mutation or unversioned allocation publish is an architecture failure.

## Alternatives considered

| Alternative | Rejected because |
|-------------|------------------|
| Embed cost/profitability inside P280 FP&A | Violates planning vs management accounting depth split |
| Embed inside P271 Finance OS | Violates accounting control vs management accounting interpretation |
| Mutate GL from allocation publish | P271 / Financial Kernel owns financial control |
| Tax determination in MEMACPI | P269 + P271 + external regulatory rules |
| Ungated agent cost restructuring | Violates human cost governance |

## Compliance checklist

- [x] DDD · CQRS · events · hexagonal boundaries documented
- [x] Peer federation matrix (P271 · P280 · P279 · Accounting · Policy · Workflow · Audit)
- [x] Versioned allocation/cost models · deterministic/reproducible calc
- [x] P271/P279/P280 boundaries preserved explicitly
- [x] P282 delivered — [ADR 639 / MEPRIAP](639-meos-enterprise-pricing-intelligence-revenue-optimization-autonomous-pricing-platform.md)
