# ADR 646 — MEOS Enterprise Application Architecture, API Governance & Software Architecture Intelligence Platform (MEAAGSI)

- **Status:** Accepted
- **Date:** 2026-08-11
- **Deciders:** Chief Enterprise Architect · MEOS Architecture Board
- **Tags:** meos · p289 · meaagsi · application-architecture · api-governance · technical-debt · modernization · productization
- **Related:** [ADR 645](645-meos-enterprise-devsecops-secure-software-supply-chain-application-delivery-intelligence-platform.md) · [ADR 644](644-meos-enterprise-cloud-platform-engineering-infrastructure-automation-intelligence-platform.md) · [ADR 643](643-meos-enterprise-it-operations-infrastructure-observability-intelligence-platform.md) · [ADR 647](647-meos-enterprise-data-architecture-master-data-information-architecture-intelligence-platform.md) · [Law P289](../architecture/ENTERPRISE_MEOS_APPLICATION_ARCHITECTURE_API_GOVERNANCE_SOFTWARE_ARCHITECTURE_INTELLIGENCE_PLATFORM.md) · Governance Standard 11.0

## Context

MEOS needs a specialized **Application Architecture / API Governance / Software Architecture Intelligence** productization layer — without replacing DevSecOps (P288), Platform Engineering (P287), Data Mesh (P263), Knowledge Graph (P264), or Enterprise Governance (P270), and without ungated architecture mutations or treating twin simulations as executed migrations.

## Decision

1. Establish SoR **`application_architecture_operating`** as MEAAGSI fabric under API **`/api/v1/application-architecture-operating*`**, schema **`application_architecture_operating_*`**.
2. Capability **`CAP-PLT-MEAAGSI-001`**; fabric id **`meos_enterprise_application_architecture_api_governance_software_architecture_intelligence_platform_framework`**.
3. **Boundary law (hard):**
   - **P287** = Cloud / Platform Engineering
   - **P288** = DevSecOps / Secure Software Delivery
   - **P289** = Application / Software Architecture / API Governance
   - **P290** = Enterprise Data & Information Architecture (next; distinct from P263 Data Mesh)
   - Never replace P263 · P264 · P268 · P270 · P286
4. Federate-by-contract: P288, P287, P286, P264, P265, P263, P270, Workflow, Policy — never fork peer APIs; never local approval engines.
5. Architecture models, API contracts, ADRs and assessments are **versioned, explainable, reproducible, auditable**. Material migrations/deprecations/decommissions require **Policy + Risk + Approval + Impact Analysis + Verification + Audit** (or published Autonomy Threshold).
6. Architecture Recommendation → Autonomous Action only with **Evidence + Policy + Risk + Explainability**.
7. **No AI Agent may execute uncontrolled architecture mutations outside Policy + Delegation Authority.** Simulation ≠ execute.
8. Inference → **P214-Z** only; no module-local LLM.
9. Designed State vs Actual Runtime State drift must be detectable via P286/P257 ACL.

## Consequences

- Unlocks Phase 1–4 MEAAGSI roadmap (P289-A…D) and **P290** Data Architecture / MDM / Information Architecture series (delivered as normative law + ADR 647).
- P288 remains secure delivery SoR; P287 remains platform/deploy SoR; MEAAGSI owns architecture portfolio, API governance and gated modernization overlays.
- Ungated architecture mutation or merging P287+P288+P289+P263 SoRs is an architecture failure.

## Alternatives considered

| Alternative | Rejected because |
|-------------|------------------|
| Embed API governance inside P288 DevSecOps | Violates secure delivery vs architecture governance split |
| Embed portfolio architecture inside P270 GRC | Violates enterprise risk vs application architecture split |
| Replace P263 Data Mesh with architecture OS | Violates data product mesh vs application architecture split |
| Local approval for ADR/modernization | Violates Workflow Engine law |
| Treat twin simulation as executed migration | Violates simulation ≠ execute law |

## Compliance checklist

- [x] DDD · CQRS · events · hexagonal boundaries documented
- [x] Peer federation matrix (P288 · P287 · P286 · P264 · P265 · P270 · Workflow · Policy · Audit)
- [x] Versioned architecture/API contracts · ADR law · drift law
- [x] P287 · P288 · P263 boundaries preserved explicitly
- [x] No ungated architecture mutations · no local approval engines
- [x] P290 delivered — [ADR 647 / MEDAMIA](647-meos-enterprise-data-architecture-master-data-information-architecture-intelligence-platform.md)
