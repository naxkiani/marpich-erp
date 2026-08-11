# ADR 642 — MEOS Enterprise Service Management, SLA Operations & Intelligent Service Delivery Platform (MESMIP)

- **Status:** Accepted
- **Date:** 2026-08-11
- **Deciders:** Chief Enterprise Architect · MEOS Architecture Board
- **Tags:** meos · p285 · mesmip · service-management · itsm · sla · incident · problem · change · catalog · productization
- **Related:** [ADR 641](641-meos-enterprise-commercial-compliance-obligation-contract-performance-intelligence-platform.md) · [ADR 640](640-meos-enterprise-contract-intelligence-commercial-agreement-autonomous-contract-platform.md) · [ADR 630](630-meos-enterprise-customer-experience-crm-intelligence-autonomous-relationship-platform.md) · [ADR 628](628-meos-enterprise-financial-intelligence-autonomous-finance-platform.md) · [ADR 643](643-meos-enterprise-it-operations-infrastructure-observability-intelligence-platform.md) · [Law P285](../architecture/ENTERPRISE_MEOS_SERVICE_MANAGEMENT_SLA_OPERATIONS_INTELLIGENT_SERVICE_DELIVERY_PLATFORM.md) · Governance Standard 11.0

## Context

MEOS needs a specialized **Service Management / Service Delivery / SLA Operations** productization layer — without replacing Contract Lifecycle (P283), Commercial Performance Assurance (P284), Workflow, Observability, or Document Exchange, and without ungated production remediation.

## Decision

1. Establish SoR **`service_management_operating`** as MESMIP fabric under API **`/api/v1/service-management-operating*`**, schema **`service_management_operating_*`**.
2. Capability **`CAP-PLT-MESMIP-001`**; fabric id **`meos_enterprise_service_management_sla_operations_intelligent_service_delivery_platform_framework`**.
3. **Boundary law (hard):**
   - **P283** = Contract definition (*what contract exists*)
   - **P284** = Commercial obligation/performance assurance (*whether commitment is met*)
   - **P285** = Service definition, request, delivery, support, monitoring, improvement
   - **P285 does not replace P283 or P284**
4. Federate-by-contract: P283, P284, P260, P257–P259, P273, P275, Documents, Observability — never fork peer APIs; never local approval engines or local metrics stores; knowledge binaries via `document_id` only.
5. Service definitions, SLA policies and service policies are **versioned, explainable, reproducible, auditable**. Material production-impacting remediation/changes require **Policy + DoA + Human Governance + Audit** (or published Autonomy Threshold) with **safe rollback**.
6. **No AI Agent may create binding service commitments or uncontrolled production changes outside Policy + Delegation Authority.**
7. Inference → **P214-Z** only; no module-local LLM.
8. Twin service scenarios via P265 are non-actuating unless Policy + Workflow + DoA (or autonomy threshold) approve.

## Consequences

- Unlocks Phase 1–4 MESMIP roadmap (P285-A…D) and **P286** IT Operations / Infrastructure / Observability Intelligence series (delivered as normative law + ADR 643).
- P283 remains contract SoR; P284 remains commercial assurance SoR; MESMIP owns service catalog/delivery/operations overlays.
- Ungated production change or merging P283/P284/P285 SoRs is an architecture failure.

## Alternatives considered

| Alternative | Rejected because |
|-------------|------------------|
| Embed ITSM inside P284 commercial performance | Violates commercial assurance vs service delivery split |
| Embed inside P283 contracts | Violates contract definition vs service operations |
| Local metrics/alerting store in service module | Violates Observability Platform law |
| Local approval state machines | Violates Workflow Engine law |
| Ungated agent production remediation | Violates human service governance |

## Compliance checklist

- [x] DDD · CQRS · events · hexagonal boundaries documented
- [x] Peer federation matrix (P283 · P284 · Workflow · Observability · Documents · Policy · Audit)
- [x] Versioned services/SLA policies · document_id knowledge refs
- [x] P283/P284 boundaries preserved explicitly
- [x] No ungated production changes · autonomy + safe rollback
- [x] P286 delivered — [ADR 643 / MEITOI](643-meos-enterprise-it-operations-infrastructure-observability-intelligence-platform.md)
- [x] P287 delivered — [ADR 644 / MECPEI](644-meos-enterprise-cloud-platform-engineering-infrastructure-automation-intelligence-platform.md)
- [x] P288 delivered — [ADR 645 / MEDSSAD](645-meos-enterprise-devsecops-secure-software-supply-chain-application-delivery-intelligence-platform.md)
- [x] P289 delivered — [ADR 646 / MEAAGSI](646-meos-enterprise-application-architecture-api-governance-software-architecture-intelligence-platform.md)
