# ADR 589 — Enterprise Federated Data Mesh & Intelligence Fabric Platform (P229)

## Status
Accepted

## Context
P228 established EKGSIP (knowledge graph & semantic intelligence). P229 opens the Enterprise Federated Data Mesh & Intelligence Fabric Platform (EFDMIFP) for decentralized data ownership, trusted data products, intelligent orchestration, semantic federation and enterprise-scale intelligence delivery. P212 remains enterprise data governance SoR; Analytics/P213 remains BI SoR; domain SoRs remain authoritative for their data — EFDMIFP federates products, contracts, metadata, quality and marketplace.

## Decision
1. SoR `data_mesh`; fabric `meos_enterprise_federated_data_mesh_intelligence_fabric_platform_framework`; API `/api/v1/data-mesh*`; capability `CAP-PLT-EFDMIFP-001`.
2. Ten logical BCs inside one SoR: Data Product Management, Data Governance, Metadata, Quality, Federation, Marketplace, Data Security, Data Analytics hooks, Data Intelligence, Lifecycle.
3. Federate with P212, P213/Analytics, Search, P228, P227, Integration via ACL/events — never replace them.
4. Inference only via P214-Z; exchange via contracts + owner APIs/events; never cross-schema SQL; policy via Policy Engine; audit via Audit; violations via Compliance Platform.
5. Never module-local LLM/search; never dual-write peer tables; never ungoverned sharing; never bypass classification/tenant isolation.
6. Roadmap: P229 foundation → P229-A…D (contracts/metadata → mesh/agents/marketplace → federation/intelligence → civilization-scale gated fabric).

## Consequences
Positive: governed data-product mesh for AI and autonomous platforms.  
Negative: physical datasets remain in owning SoRs — EFDMIFP stores products, contracts, metadata, quality/lineage projections and marketplace listings with peer refs only.

## Links
Law: `ENTERPRISE_FEDERATED_DATA_MESH_INTELLIGENCE_FABRIC_PLATFORM.md` · Prior: ADR 588 · Next: P229-A · Peer: ADR 590 (P230 EPDRTIP)
