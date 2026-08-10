# ADR 632 — MEOS Enterprise Asset Intelligence & Autonomous Asset Management Platform (P275)

## Status
Accepted

## Context
P274 established MEHCAWP over P235/HR peers. P275 productizes Asset Intelligence & Autonomous Asset Management as the MEOS Enterprise Asset & Physical Operations Layer. P236 already owns manufacturing/industrial intelligence (including PdM depth); P227/P265 own digital twins; inventory owns spare-parts stock; Manufacturing/Robotics own OT actuation. MEAIAMP must federate those SoRs — never fork `/api/v1/manufacturing-intelligence*` or twin APIs, never dual-write stock/asset ledgers, and never ungated physical/OT actuation. P276 is planned for Procurement Intelligence & Autonomous Sourcing over P272 / procurement.

## Decision
1. SoR `enterprise_asset_operating`; fabric `meos_enterprise_asset_intelligence_autonomous_asset_management_platform_framework`; API `/api/v1/enterprise-asset-operating*`; capability `CAP-PLT-MEAIAMP-001`; acronym **MEAIAMP**.
2. Logical BCs inside one SoR: Asset Registry Operating, Asset Lifecycle Operating, Maintenance Operating, Asset Condition Operating, Field Service Operating, Performance/Risk/Twin Operating.
3. Federate with P236, P227/P265, inventory/warehouse, Manufacturing/Robotics, P274, P272, P271, P268, P267, Workflow, Policy, Audit, Integration, P214-Z — never replace them; never dual-write peer catalogs.
4. Inference only via P214-Z; critical maintenance/actuation require Workflow + human approval; twin simulation ≠ actuate; IoT vendors via Integration Platform only; cyber-physical via P268.
5. Roadmap: P275 foundation → P275-A…D; unblocks P276.

## Consequences
Positive: governed Asset OS (registry, 360, PdM, field service, TCO/risk campaigns, gated work orders) over canonical industrial/twin/inventory peers.  
Negative: manufacturing intel, twin models, stock and OT truth remain peer-owned — MEAIAMP stores operating campaigns and peer refs only.

## Links
Law: `ENTERPRISE_MEOS_ASSET_INTELLIGENCE_AUTONOMOUS_ASSET_MANAGEMENT_PLATFORM.md` · Prior: ADR 631 · Next: P275-A · Peer: ADR 633 (P276 MEPIASP) · Canonical: P236 · P265 · inventory · Manufacturing/OT
