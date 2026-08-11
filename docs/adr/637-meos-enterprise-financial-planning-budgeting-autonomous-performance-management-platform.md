# ADR 637 — MEOS Enterprise Financial Planning, Budgeting & Autonomous Performance Management Platform (MEFPAPM)

- **Status:** Accepted
- **Date:** 2026-08-11
- **Deciders:** Chief Enterprise Architect · MEOS Architecture Board
- **Tags:** meos · p280 · mefpapm · fpa · budgeting · forecasting · scenario · performance · capital-planning · productization
- **Related:** [ADR 636](636-meos-enterprise-revenue-recognition-treasury-cash-intelligence-platform.md) · [ADR 635](635-meos-enterprise-revenue-billing-quote-to-cash-intelligence-platform.md) · [ADR 628](628-meos-enterprise-financial-intelligence-autonomous-finance-platform.md) · [ADR 638](638-meos-enterprise-management-accounting-cost-profitability-intelligence-platform.md) · [Law P280](../architecture/ENTERPRISE_MEOS_FINANCIAL_PLANNING_BUDGETING_AUTONOMOUS_PERFORMANCE_MANAGEMENT_PLATFORM.md) · Governance Standard 11.0

## Context

MEOS needs a specialized **Financial Planning / Budgeting / Performance Management** productization layer — without replacing Financial Intelligence (P271), Treasury/Cash Intelligence (P279), or forking Accounting systems of record.

## Decision

1. Establish SoR **`financial_planning_operating`** as MEFPAPM fabric under API **`/api/v1/financial-planning-operating*`**, schema **`financial_planning_operating_*`**.
2. Capability **`CAP-PLT-MEFPAPM-001`**; fabric id **`meos_enterprise_financial_planning_budgeting_autonomous_performance_management_platform_framework`**.
3. **Boundary law (hard):**
   - **P271** = Enterprise Financial Intelligence / Accounting / Financial Control (**authoritative**)
   - **P279** = Revenue Recognition / Treasury / Liquidity / Cash Intelligence
   - **P280** = Planning / Budgeting / Forecasting / Performance Management
4. Federate-by-contract: P271, P279, Accounting, P272–P278 — never dual-write peer schemas; never fork `/api/v1/autonomous-finance-operating*` or `/api/v1/treasury-cash-operating*`; never local GL; never mutate ledger from planning fabric.
5. Material budget reallocation, capital allocation, major target changes, and strategic plan changes require **Policy + Delegation-of-Authority + Human Governance + Audit**; agents recommend; scenarios are **isolated** and **versioned**; simulation ≠ publish.
6. Inference → **P214-Z** only; no module-local LLM; deterministic financial calculations.
7. Twin/scenario via P265 is non-actuating unless Policy + Workflow + DoA approve plan publish/revision.

## Consequences

- Unlocks Phase 1–4 MEFPAPM roadmap (P280-A…D) and **P281** Management Accounting / Cost & Profitability series (delivered as normative law + ADR 638).
- P271 remains final accounting/control; P279 remains cash/treasury; MEFPAPM owns planning campaigns, versions and performance overlays.
- Uncontrolled plan mutation or ledger write from FP&A is an architecture failure.

## Alternatives considered

| Alternative | Rejected because |
|-------------|------------------|
| Embed FP&A inside P271 Finance OS | Violates planning vs financial control split |
| Embed FP&A inside P279 Treasury OS | Violates planning vs liquidity/cash split |
| Mutate GL from budget publish | P271 / Financial Kernel owns financial control |
| Ungated agent budget/capital commit | Violates human planning governance |
| Non-versioned / non-isolated scenarios | Violates reproducibility and auditability |

## Compliance checklist

- [x] DDD · CQRS · events · hexagonal boundaries documented
- [x] Peer federation matrix (P271 · P279 · Accounting · Policy · Workflow · Audit)
- [x] Material planning gate law + versioning + scenario isolation
- [x] P271 and P279 financial/treasury boundaries preserved explicitly
- [x] P281 delivered — [ADR 638 / MEMACPI](638-meos-enterprise-management-accounting-cost-profitability-intelligence-platform.md)
