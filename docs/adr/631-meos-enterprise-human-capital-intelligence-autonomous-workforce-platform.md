# ADR 631 — MEOS Enterprise Human Capital Intelligence & Autonomous Workforce Platform (P274)

## Status
Accepted

## Context
P273 established MECXARP over CRM/Sales peers. P274 productizes Human Capital Intelligence & Autonomous Workforce as the MEOS Human Capital & Workforce Operating Layer. P235 already owns `workforce_intelligence`; P251 owns `human_capability_intelligence`; P234 owns learning/capability journey depth; HR owns employment; Payroll owns compensation. MEHCAWP must federate those SoRs — never fork `/api/v1/workforce-intelligence*` or `/api/v1/human-capability-intelligence*`, never dual-write employment/payroll ledgers, and never ungated hire/terminate/pay/promote/comp. P275 is planned for Asset Intelligence & Autonomous Asset Management.

## Decision
1. SoR `human_capital_operating`; fabric `meos_enterprise_human_capital_intelligence_autonomous_workforce_platform_framework`; API `/api/v1/human-capital-operating*`; capability `CAP-PLT-MEHCAWP-001`; acronym **MEHCAWP**.
2. Logical BCs inside one SoR: Employee Management Operating, Recruitment Operating, Talent Operating, Skills Operating, Performance Operating, Learning/Experience/Risk Operating.
3. Federate with P235, P251, P234, HR, Payroll, Identity, P230/P269, P268, P271, P273, P272, Documents, Workflow, Policy, Audit, Integration, P214-Z — never replace them; never dual-write peer employment/payroll/capability catalogs.
4. Inference only via P214-Z; high-impact employment actions require Workflow + human approval + explainability + audit; bias monitoring on recruitment/talent/performance; simulation ≠ execute; ATS/HRIS/LMS via Integration Platform only.
5. Roadmap: P274 foundation → P274-A…D; unblocks P275.

## Consequences
Positive: governed Human Capital OS (Employee 360, talent/skills/recruit campaigns, gated workforce optimization) over canonical workforce peers.  
Negative: employment/pay/capability truth remains peer-owned — MEHCAWP stores operating campaigns and peer refs only.

## Links
Law: `ENTERPRISE_MEOS_HUMAN_CAPITAL_INTELLIGENCE_AUTONOMOUS_WORKFORCE_PLATFORM.md` · Prior: ADR 630 · Next: P274-A · Peer: ADR 632 (P275 MEAIAMP) · Canonical: P235 · P251 · HR · Payroll
