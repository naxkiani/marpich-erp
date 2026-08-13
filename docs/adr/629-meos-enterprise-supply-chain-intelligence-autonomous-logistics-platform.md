# ADR 629 — MEOS Enterprise Supply Chain Intelligence & Autonomous Logistics Platform (P272)

## Status
Accepted

## Context
P271 established MEFIAF over P231/Financial Kernel. P272 productizes Supply Chain Intelligence & Autonomous Logistics as the MEOS Enterprise Supply Network Operating Layer. P232 already owns `supply_chain_intelligence`; inventory, warehouse, procurement and logistics own operational truth. MESCIAL must federate those SoRs — never fork `/api/v1/supply-chain-intelligence*`, never dual-write stock/shipment/PO ledgers, and never ungated material procure/replenish/ship. P273 is planned for Customer Experience, CRM Intelligence & Autonomous Relationship.

## Decision
1. SoR `supply_network_operating`; fabric `meos_enterprise_supply_chain_intelligence_autonomous_logistics_platform_framework`; API `/api/v1/supply-network-operating*`; capability `CAP-PLT-MESCIAL-001`; acronym **MESCIAL**.
2. Logical BCs inside one SoR: Procurement Operating, Supplier Intelligence Operating, Inventory Optimization Operating, Logistics Operating, Supply Planning Operating, Control Tower/Risk Operating.
3. Federate with P232, inventory, warehouse, procurement, logistics, P271, P221, P267, Workflow, Policy, Audit, Integration, P214-Z — never replace them; never dual-write peer operational catalogs; never merge unrelated domain lifecycles.
4. Inference only via P214-Z; material procure/replenish/ship require Workflow + human approval and owning SoR APIs; simulation ≠ execute; carriers/WMS/TMS via Integration Platform only.
5. Roadmap: P272 foundation → P272-A…D; unblocks P273.

## Consequences
Positive: governed Supply Network OS (Control Tower, forecast/procure/inventory/logistics campaigns, gated execution) over canonical supply peers.  
Negative: stock/PO/shipment truth remains peer-owned — MESCIAL stores operating campaigns and peer refs only.

## Links
Law: `ENTERPRISE_MEOS_SUPPLY_CHAIN_INTELLIGENCE_AUTONOMOUS_LOGISTICS_PLATFORM.md` · Prior: ADR 628 · Next: P272-A · Peer: ADR 630 (P273 MECXARP) · Canonical: P232 · inventory · warehouse · procurement · logistics
