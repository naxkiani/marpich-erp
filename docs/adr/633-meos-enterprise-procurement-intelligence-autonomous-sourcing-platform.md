# ADR 633 — MEOS Enterprise Procurement Intelligence & Autonomous Sourcing Platform (P276)

## Status
Accepted

## Context
P275 established MEAIAMP over P236/asset peers. P276 productizes Procurement Intelligence & Autonomous Sourcing as the MEOS Enterprise Source-to-Pay Intelligence Layer. P272 already owns supply-network OS; P271 owns financial intelligence; Procurement owns PO/requisition truth; Documents owns contract blobs. MEPIASP must federate those SoRs with a hard boundary — never fork `/api/v1/supply-network-operating*` or `/api/v1/procurement*`, never dual-write PO ledgers, and never ungated material purchase commits. P277 (ADR 634 / MESIARO) productizes Sales Intelligence & Autonomous Revenue Operations over P273/CRM/Sales with a hard CX vs Sales/RevOps vs Finance boundary.

## Decision
1. SoR `procurement_operating`; fabric `meos_enterprise_procurement_intelligence_autonomous_sourcing_platform_framework`; API `/api/v1/procurement-operating*`; capability `CAP-PLT-MEPIASP-001`; acronym **MEPIASP**.
2. Logical BCs inside one SoR: Procurement Requisition Operating, Spend Intelligence Operating, Strategic Sourcing Operating, Supplier Intelligence Operating, Contract Intelligence Operating, Purchase/Governance Operating.
3. Federate with Procurement, P272, P271, Documents, inventory, P275, P273, P274, Policy, Workflow, Audit, P214-Z — never replace them; never merge P272 supply-network and P276 S2P lifecycles; never local GL.
4. Inference only via P214-Z; material financial/contractual commitments require Policy + Delegation-of-Authority + human approval; negotiation recommendations are human-governed; twin scenario ≠ commit; contract binaries via Document Exchange only.
5. Roadmap: P276 foundation → P276-A…D; unblocks P277 (delivered as normative law + ADR 634).

## Consequences
Positive: governed Source-to-Pay OS (spend/sourcing/supplier/contract campaigns, gated purchase recommendations) over canonical procurement/supply/finance peers.  
Negative: PO/budget/supply-network truth remains peer-owned — MEPIASP stores operating campaigns and peer refs only.

## Links
Law: `ENTERPRISE_MEOS_PROCUREMENT_INTELLIGENCE_AUTONOMOUS_SOURCING_PLATFORM.md` · Prior: ADR 632 · Next: P276-A · Peer: [ADR 634 / P277 MESIARO](634-meos-enterprise-sales-intelligence-autonomous-revenue-operations-platform.md) · Canonical: Procurement · P272 · P271 · Documents
