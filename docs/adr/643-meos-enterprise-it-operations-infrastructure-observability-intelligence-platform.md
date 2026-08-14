# ADR 643 — MEOS Enterprise IT Operations, Infrastructure & Observability Intelligence Platform (MEITOI)

- **Status:** Accepted
- **Date:** 2026-08-11
- **Deciders:** Chief Enterprise Architect · MEOS Architecture Board
- **Tags:** meos · p286 · meitoi · it-operations · observability · aiops · infrastructure · capacity · productization
- **Related:** [ADR 642](642-meos-enterprise-service-management-sla-operations-intelligent-service-delivery-platform.md) · [ADR 641](641-meos-enterprise-commercial-compliance-obligation-contract-performance-intelligence-platform.md) · [ADR 632](632-meos-enterprise-asset-intelligence-autonomous-asset-management-platform.md) · [ADR 644](644-meos-enterprise-cloud-platform-engineering-infrastructure-automation-intelligence-platform.md) · [Law P286](../architecture/ENTERPRISE_MEOS_IT_OPERATIONS_INFRASTRUCTURE_OBSERVABILITY_INTELLIGENCE_PLATFORM.md) · Governance Standard 11.0

## Context

MEOS needs a specialized **IT Operations / Infrastructure / Observability Intelligence / AIOps** productization layer — without replacing Service Management (P285), Core Observability Platform, Workflow, or Asset Intelligence (P275), and without ungated production infrastructure mutations.

## Decision

1. Establish SoR **`technology_operations_operating`** as MEITOI fabric under API **`/api/v1/technology-operations-operating*`**, schema **`technology_operations_operating_*`**.
2. Capability **`CAP-PLT-MEITOI-001`**; fabric id **`meos_enterprise_it_operations_infrastructure_observability_intelligence_platform_framework`**.
3. **Boundary law (hard):**
   - **P285** = Service Management / Service Delivery (*manages the service*)
   - **P286** = Technology Operations / Infra / App / Network / Cloud Observability (*observes and operates technology*)
   - **Core Observability Platform** = telemetry foundation (**authoritative for collection plumbing**)
   - **P286 does not replace P285 or Core Observability**
4. Federate-by-contract: Observability Platform, P285, P275, P268, P260, P265, P264 — never fork Observability APIs; never local metrics/alerting stores; never local approval engines; runbooks via `document_id` only.
5. Observability/SLO/automation policies are **versioned, explainable, reproducible, auditable**. Material remediations require **Policy + Permission + Delegation + Risk Threshold + Approved Runbook + Verification + Audit** (or published Autonomy Threshold) with **safe rollback**.
6. **No AI Agent may execute uncontrolled production changes outside Policy + Delegation Authority.**
7. Inference → **P214-Z** only; no module-local LLM.
8. Twin failure/capacity/change scenarios via P265 are non-actuating unless Policy + Workflow + DoA (or autonomy threshold) approve.

## Consequences

- Unlocks Phase 1–4 MEITOI roadmap (P286-A…D) and **P287** Cloud / Platform Engineering / Infrastructure Automation series (delivered as normative law + ADR 644).
- P285 remains service delivery SoR; Core Observability remains telemetry SoR; MEITOI owns ops intelligence, correlation, AIOps and gated remediation overlays.
- Ungated infrastructure mutation or merging P285+P286 or forking Core Observability is an architecture failure.

## Alternatives considered

| Alternative | Rejected because |
|-------------|------------------|
| Embed AIOps inside P285 Service Management | Violates service delivery vs technology ops split |
| Replace Core Observability with module-local stack | Violates Observability Platform law |
| Local metrics/alerting stores | Violates platform observability charter |
| Ungated agent production remediation | Violates human ops governance |
| Local approval engines for remediation | Violates Workflow Engine law |

## Compliance checklist

- [x] DDD · CQRS · events · hexagonal boundaries documented
- [x] Peer federation matrix (Observability · P285 · P275 · P268 · Workflow · Policy · Audit)
- [x] Versioned observability/SLO policies · approved runbook + rollback law
- [x] P285 and Core Observability boundaries preserved explicitly
- [x] No ungated production mutations
- [x] P287 delivered — [ADR 644 / MECPEI](644-meos-enterprise-cloud-platform-engineering-infrastructure-automation-intelligence-platform.md)
- [x] P288 delivered — [ADR 645 / MEDSSAD](645-meos-enterprise-devsecops-secure-software-supply-chain-application-delivery-intelligence-platform.md)
- [x] P289 delivered — [ADR 646 / MEAAGSI](646-meos-enterprise-application-architecture-api-governance-software-architecture-intelligence-platform.md)
