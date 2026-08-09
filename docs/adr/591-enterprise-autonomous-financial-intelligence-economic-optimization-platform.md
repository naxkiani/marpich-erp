# ADR 591 — Enterprise Autonomous Financial Intelligence & Economic Optimization Platform (P231)

## Status
Accepted

## Context
P230 established EPDRTIP (privacy, digital rights & trust). P231 opens the Enterprise Autonomous Financial Intelligence & Economic Optimization Platform (EAFIEOP) for financial intelligence, economic modeling, autonomous optimization, financial risk intelligence and value creation under MEOS 11.0. Financial Kernel remains the sole GL/journal/COA/posting foundation; Accounting/Treasury/Banking remain document and product SoRs — EAFIEOP is intelligence/optimization only.

## Decision
1. SoR `financial_intelligence`; fabric `meos_enterprise_autonomous_financial_intelligence_economic_optimization_platform_framework`; API `/api/v1/financial-intelligence*`; capability `CAP-PLT-EAFIEOP-001`.
2. Ten logical BCs inside one SoR: Financial Management, Economic Intelligence, Investment, Risk, Capital Optimization, Budget Governance, Value Management, Economic Simulation, Compliance, Financial Strategy.
3. Federate with Financial Kernel, Accounting, Treasury, Banking, P224, P227–P230, P221 via ACL/events — never replace them.
4. Inference only via P214-Z; execute via Workflow; ledger via `IFinancialKernel` only; policy via Policy Engine; audit via Audit; market data via Integration Platform.
5. Never local JournalEntry/GL/COA; never hardcoded account codes; never ungated capital/budget/investment execute; never module-local LLM.
6. Roadmap: P231 foundation → P231-A…D (core models → AI/simulation → optimization → civilization-scale gated economics).

## Consequences
Positive: governed CFO-grade intelligence and economic simulation without forking the ledger.  
Negative: balances and journals remain Kernel-owned — EAFIEOP stores models, scenarios, recommendations and allocation plans with posting-intent refs only.

## Links
Law: `ENTERPRISE_AUTONOMOUS_FINANCIAL_INTELLIGENCE_ECONOMIC_OPTIMIZATION_PLATFORM.md` · Prior: ADR 590 · Next: P231-A · Peer: ADR 592 (P232 EASCLIP)
