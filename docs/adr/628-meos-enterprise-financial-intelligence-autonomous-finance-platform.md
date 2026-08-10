# ADR 628 — MEOS Enterprise Financial Intelligence & Autonomous Finance Platform (P271)

## Status
Accepted

## Context
P270 established MEGRSC over P240/GRC peers. P271 productizes Financial Intelligence & Autonomous Finance as the MEOS Enterprise Value Intelligence Operating Layer. P231 already owns `financial_intelligence`; Financial Kernel owns GL/journals/COA; accounting and treasury own documents and cash operations. MEFIAF must federate those SoRs — never fork `/api/v1/financial-intelligence*`, never duplicate ledger truth, and never ungated material post/pay/invest. P272 is planned for Supply Chain Intelligence & Autonomous Logistics over P232.

## Decision
1. SoR `autonomous_finance_operating`; fabric `meos_enterprise_financial_intelligence_autonomous_finance_platform_framework`; API `/api/v1/autonomous-finance-operating*`; capability `CAP-PLT-MEFIAF-001`; acronym **MEFIAF**.
2. Logical BCs inside one SoR: Accounting Intelligence Operating, Financial Planning Operating, Treasury Intelligence Operating, Revenue Intelligence Operating, Cost Intelligence Operating, Financial Risk/Investment Operating.
3. Federate with P231, Financial Kernel, accounting, treasury, banking, P270, P269, P268, P261, Workflow, Audit, P214-Z — never replace them; never dual-write GL/journal or peer finance catalogs.
4. Inference only via P214-Z; material post/pay/invest require Workflow + human approval and Kernel/treasury APIs; simulation ≠ execute; no opaque auto-post.
5. Roadmap: P271 foundation → P271-A…D; unblocks P272.

## Consequences
Positive: governed Finance OS (CFO workspace, forecast/treasury/revenue campaigns, gated automation) over canonical financial peers.  
Negative: ledger/cash/doc truth remains peer-owned — MEFIAF stores operating campaigns and peer refs only.

## Links
Law: `ENTERPRISE_MEOS_FINANCIAL_INTELLIGENCE_AUTONOMOUS_FINANCE_PLATFORM.md` · Prior: ADR 627 · Next: P271-A · Peer: ADR 629 (P272 MESCIAL) · Peer: [ADR 634 / P277 MESIARO](634-meos-enterprise-sales-intelligence-autonomous-revenue-operations-platform.md) (Sales/RevOps — never local GL) · Peer: [ADR 635 / P278 MEQTCIP](635-meos-enterprise-revenue-billing-quote-to-cash-intelligence-platform.md) (Q2C — never dual-write AR; P271 remains Financial Control) · Peer: [ADR 636 / P279 METRCIP](636-meos-enterprise-revenue-recognition-treasury-cash-intelligence-platform.md) (Treasury/RevRec — does not replace P271) · Canonical: P231 · Financial Kernel · accounting · treasury
