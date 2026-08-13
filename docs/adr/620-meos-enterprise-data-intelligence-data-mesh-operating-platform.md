# ADR 620 — MEOS Enterprise Data Intelligence & Data Mesh Operating Platform (P263)

## Status
Accepted

## Context
P262 established MEIAOI over analytics/insight. P263 productizes Data Mesh operating as the MEOS Data Operating System Layer. P229 EFDMIFP already owns `data_mesh` and `/api/v1/data-mesh*`; P212 owns data governance baseline; P230 owns privacy/trust. MEDIMOP must federate those SoRs — never fork the mesh API or dual-write product catalogs. P264 is planned for Knowledge Graph & Semantic Intelligence productization over P228.

## Decision
1. SoR `data_mesh_operating`; fabric `meos_enterprise_data_intelligence_data_mesh_operating_platform_framework`; API `/api/v1/data-mesh-operating*`; capability `CAP-PLT-MEDIMOP-001`; acronym **MEDIMOP**.
2. Logical BCs inside one SoR: Data Product Operating, Data Governance Operating, Metadata Intelligence, Catalog Experience, Marketplace Operating, Data OS Governance.
3. Federate with P229, P212, P230, P262, Search, Workflow, Policy, Compliance, P228, P214-Z — never replace them; never dual-write `data_mesh_*`; never cross-schema discovery SQL.
4. Inference only via P214-Z; access grants via Identity + Policy + Privacy + Workflow when required; recommendation ≠ access grant; no module-local feature-store SoR.
5. Roadmap: P263 foundation → P263-A…D; unblocks P264.

## Consequences
Positive: governed Data OS experience (portal, marketplace, certification) over canonical mesh.  
Negative: product/contract/lineage truth remains P229-owned — MEDIMOP stores operating state, portal projections and peer refs only.

## Links
Law: `ENTERPRISE_MEOS_DATA_INTELLIGENCE_DATA_MESH_OPERATING_PLATFORM.md` · Prior: ADR 619 · Next: P263-A · Peer: ADR 621 (P264 MEKGSI) · Peer: [ADR 647 / P290 MEDAMIA](647-meos-enterprise-data-architecture-master-data-information-architecture-intelligence-platform.md) (Data Architecture / MDM — never replace Data Mesh runtime) · Canonical: P229 EFDMIFP
