# ADR 647 — MEOS Enterprise Data Architecture, Master Data & Information Architecture Intelligence Platform (MEDAMIA)

- **Status:** Accepted
- **Date:** 2026-08-11
- **Deciders:** Chief Enterprise Architect · MEOS Architecture Board
- **Tags:** meos · p290 · medamia · data-architecture · mdm · golden-record · data-contracts · lineage · productization
- **Related:** [ADR 646](646-meos-enterprise-application-architecture-api-governance-software-architecture-intelligence-platform.md) · [ADR 620](620-meos-enterprise-data-intelligence-data-mesh-operating-platform.md) · [ADR 645](645-meos-enterprise-devsecops-secure-software-supply-chain-application-delivery-intelligence-platform.md) · [ADR 648](648-meos-enterprise-integration-architecture-event-mesh-interoperability-intelligence-platform.md) · [Law P290](../architecture/ENTERPRISE_MEOS_DATA_ARCHITECTURE_MASTER_DATA_INFORMATION_ARCHITECTURE_INTELLIGENCE_PLATFORM.md) · Governance Standard 11.0

## Context

MEOS needs a specialized **Enterprise Data Architecture / Master Data / Information Architecture Intelligence** productization layer — without replacing Data Mesh runtime (P263), Knowledge Graph (P264), Application Architecture (P289), Privacy (P269), or Governance (P270), and without ungated data-model mutations or dual-writing mesh product tables.

## Decision

1. Establish SoR **`data_architecture_operating`** as MEDAMIA fabric under API **`/api/v1/data-architecture-operating*`**, schema **`data_architecture_operating_*`**.
2. Capability **`CAP-PLT-MEDAMIA-001`**; fabric id **`meos_enterprise_data_architecture_master_data_information_architecture_intelligence_platform_framework`**.
3. **Boundary law (hard):**
   - **P263** = Data Mesh / Data Operating Platform (*product runtime & federated execution*)
   - **P290** = Enterprise Data & Information Architecture (*domains, MDM, contracts, lineage design, quality architecture*)
   - **P290 does not replace P263**
   - Never replace P264 · P289 · P268 · P269 · P270
4. Federate-by-contract: P263, P264, P289, P288, P287, P286, P268, P269, P270, Workflow, Policy — never fork Data Mesh APIs; never dual-write `data_mesh_operating_*` product tables; never local approval engines.
5. Data models, contracts, golden records and assessments are **versioned, explainable, reproducible, auditable**. Material merges, schema publishes, migrations and disposals require **Policy + Risk + Approval + Verification + Audit** (or published Autonomy Threshold).
6. Autonomous Data Action only with **Evidence + Policy + Authorization + Audit**.
7. **No AI Agent may execute uncontrolled data mutations outside Policy + Delegation Authority.** Simulation ≠ execute.
8. Inference → **P214-Z** only; no module-local LLM.
9. Designed vs Actual data architecture drift must be detectable via P286/P257/P263 ACL.

## Consequences

- Unlocks Phase 1–4 MEDAMIA roadmap (P290-A…D) and **P291** Integration / Event Mesh / Interoperability series (delivered as normative law + ADR 648).
- P263 remains data product runtime SoR; MEDAMIA owns data architecture, MDM and gated migration/modernization overlays.
- Ungated data-model mutation or merging P263+P290 SoRs is an architecture failure.

## Alternatives considered

| Alternative | Rejected because |
|-------------|------------------|
| Embed MDM inside P263 Data Mesh | Violates mesh runtime vs data architecture split |
| Embed data architecture inside P289 App Architecture | Violates application vs data architecture split |
| Dual-write data products into mesh tables | Violates service boundary / schema isolation |
| Local approval for golden-record merge | Violates Workflow Engine law |
| Treat twin simulation as executed migration | Violates simulation ≠ execute law |

## Compliance checklist

- [x] DDD · CQRS · events · hexagonal boundaries documented
- [x] Peer federation matrix (P263 · P264 · P289 · P268 · P269 · P270 · Workflow · Policy · Audit)
- [x] Versioned models/contracts · MDM/golden-record law · drift law
- [x] P263 boundary preserved explicitly
- [x] No ungated data-model mutations · no dual-write mesh tables
- [x] P291 delivered — [ADR 648 / MEIEII](648-meos-enterprise-integration-architecture-event-mesh-interoperability-intelligence-platform.md)
