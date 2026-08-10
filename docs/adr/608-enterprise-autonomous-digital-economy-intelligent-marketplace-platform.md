# ADR 608 — Enterprise Autonomous Digital Economy & Intelligent Marketplace Platform (P249)

## Status
Accepted

## Context
P248 established EAEIPSP (environmental–planetary intelligence). P249 opens the Enterprise Autonomous Digital Economy & Intelligent Marketplace Platform (EADEIMP) for marketplace intelligence, matching/pricing, trust-scored commerce networks and gated value exchange under MEOS 11.0. Sales, POS and CRM remain commerce execution SoRs (POS ≠ sales); Financial Kernel remains settlement SoR; Plugin Platform remains third-party extension marketplace — EADEIMP is marketplace intelligence only and must never post local journals or capture ungated payments.

## Decision
1. SoR `marketplace_intelligence`; fabric `meos_enterprise_autonomous_digital_economy_intelligent_marketplace_platform_framework`; API `/api/v1/marketplace-intelligence*`; capability `CAP-PLT-EADEIMP-001`.
2. Ten logical BCs inside one SoR: Marketplace Management, Commerce Intelligence, Customer Intelligence, Seller Management, Transaction Management, Pricing Intelligence, Trust Management, Digital Economy Analytics, Network Management, Marketplace Governance.
3. Federate with sales, pos, crm, Financial Kernel, P231/P244, P232, P243, P230, P223, P227, P228, P229, P224, Plugin Platform via ACL/events — never replace them; never merge POS and sales; never conflate Plugin Marketplace with commerce marketplace.
4. Inference only via P214-Z; exchange via Workflow + sales/POS/Financial Kernel; trust/consent via P230; simulation ≠ execute transaction.
5. Never local JournalEntry/GL; never payment SDKs in domain; never local buyer/seller PII vaults; never module-local LLM; never opaque unexplainable pricing/match recommendations; never silent consent override.
6. Roadmap: P249 foundation → P249-A…D (marketplace domain → AI/KG/twin → autonomous assist → civilization-scale gated digital economy intel).

## Consequences
Positive: governed marketplace control-tower intelligence federated with sales/POS/finance/supply peers.  
Negative: orders, checkouts, customers and journals remain peer-owned — EADEIMP stores marketplace models, matching/pricing intel and peer refs only.

## Links
Law: `ENTERPRISE_AUTONOMOUS_DIGITAL_ECONOMY_INTELLIGENT_MARKETPLACE_PLATFORM.md` · Prior: ADR 607 · Next: P249-A · Peer: ADR 609 (P250 EAKEGINP)
