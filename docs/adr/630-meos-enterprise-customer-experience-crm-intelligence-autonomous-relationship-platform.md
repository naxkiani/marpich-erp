# ADR 630 — MEOS Enterprise Customer Experience, CRM Intelligence & Autonomous Relationship Platform (P273)

## Status
Accepted

## Context
P272 established MESCIAL over P232/supply peers. P273 productizes Customer Experience, CRM Intelligence & Autonomous Relationship as the MEOS Customer Experience & Relationship Operating Layer. CRM already owns contacts/leads/opportunities/accounts; Sales owns quotations/orders; Identity owns subject identity; P230/P269 own consent/privacy. MECXARP must federate those SoRs — never fork `/api/v1/crm*` or `/api/v1/sales*`, never dual-write customer ledgers, and never ungated critical engagement without Policy + Consent + human authority. P274 is planned for Human Capital Intelligence & Autonomous Workforce over P235 / HR peers.

## Decision
1. SoR `customer_relationship_operating`; fabric `meos_enterprise_customer_experience_crm_intelligence_autonomous_relationship_platform_framework`; API `/api/v1/customer-relationship-operating*`; capability `CAP-PLT-MECXARP-001`; acronym **MECXARP**.
2. Logical BCs inside one SoR: Customer Identity Operating, Sales Intelligence Operating, Customer Service Operating, Customer Journey Operating, Customer Value/Retention Operating, Engagement Governance.
3. Federate with CRM, Sales, Identity, P230/P269, P268, P271, P272, Notifications, Workflow, Policy, Audit, P214-Z — never replace them; never dual-write CRM/Sales catalogs; never merge CRM and Sales lifecycles.
4. Inference only via P214-Z; material engagement/retention/case-close require Workflow + human approval when critical; outreach fail-closed on missing consent; simulation ≠ execute; notifications via Notification Platform only.
5. Roadmap: P273 foundation → P273-A…D; unblocks P274.

## Consequences
Positive: governed Customer Relationship OS (360, journey, sales/service intelligence, gated engagement) over canonical CRM/Sales peers.  
Negative: contact/opportunity/order truth remains peer-owned — MECXARP stores operating campaigns and peer refs only.

## Links
Law: `ENTERPRISE_MEOS_CUSTOMER_EXPERIENCE_CRM_INTELLIGENCE_AUTONOMOUS_RELATIONSHIP_PLATFORM.md` · Prior: ADR 629 · Next: P273-A · Peer: ADR 631 (P274 MEHCAWP) · Peer: [ADR 634 / P277 MESIARO](634-meos-enterprise-sales-intelligence-autonomous-revenue-operations-platform.md) (CX vs Sales/RevOps boundary) · Peer: [ADR 635 / P278 MEQTCIP](635-meos-enterprise-revenue-billing-quote-to-cash-intelligence-platform.md) (CX vs Q2C) · Canonical: CRM · Sales · Identity · P230
