# ADR 663 — MEOS Enterprise IT Service Management, Service Catalog, Request Fulfillment & Enterprise Service Operations Platform (MEESOP)

- **Status:** Accepted
- **Date:** 2026-08-11
- **Deciders:** Chief Enterprise Architect · MEOS Architecture Board
- **Tags:** meos · p306 · meesop · itsm · service-catalog · request-fulfillment · service-desk · service-operations · productization
- **Related:** [ADR 662](662-meos-enterprise-incident-management-service-reliability-resilience-engineering-platform.md) · [ADR 661](661-meos-enterprise-process-observability-monitoring-sla-slo-continuous-operational-intelligence-platform.md) · [ADR 642](642-meos-enterprise-service-management-sla-operations-intelligent-service-delivery-platform.md) · [Law P306](../architecture/ENTERPRISE_MEOS_IT_SERVICE_MANAGEMENT_SERVICE_CATALOG_REQUEST_FULFILLMENT_ENTERPRISE_SERVICE_OPERATIONS_PLATFORM.md) · Governance Standard 11.0

## Context

MEOS needs a specialized **ITSM / Service Catalog / Request Fulfillment / Enterprise Service Operations** productization layer — without replacing Service Management peer (**P285 MESMIP**), Incident/Reliability (**P305**), Observability (**P304**), Workflow (**P260**), Autonomous Remediation (**P267**), Change/Release (**P303**), Governance (**P270**), Notifications (**P294**), Process Composer (**P301**), or Knowledge Graph (**P264**) — while converting MEOS capabilities into requestable, fulfillable enterprise services.

## Decision

1. Establish SoR **`service_operations_operating`** as MEESOP fabric under API **`/api/v1/service-operations-operating*`**, schema **`service_operations_operating_*`**.
2. Capability **`CAP-PLT-MEESOP-001`**; fabric id **`meos_enterprise_it_service_management_service_catalog_request_fulfillment_enterprise_service_operations_platform_framework`**.
3. **Boundary law (hard):**
   - **P304** = OBSERVE · **P305** = RESPOND TO INCIDENTS · **P306** = OPERATE & FULFILL SERVICES
   - **P267** = REMEDIATE · **P303** = CHANGE & DEPLOY · **P270** = GOVERN
   - **P285** = Service Management peer — federate; never merge SoRs
   - ITSM Service Catalog ≠ P305 Reliability Service Catalog
   - **P306** = Catalog · Requests · Cases · Desk · Fulfillment Coordination · Self-Service · Experience · Analytics
   - **P307** = Enterprise Knowledge / Organizational Learning (delivered)
   - **P308** = Document Intelligence / Content Lifecycle (delivered)
   - **P309** = Records / Retention / Legal Hold / ILM (delivered)
   - **P310** = Information Classification / Sensitive Information Intelligence (delivered)
   - **P311** = DLP / Information Protection / Adaptive Data Security Control (next)
4. Federate-by-contract: P285, P305, P304, P260, P267, P303, P257, P270–P281, P294, P299–P302, P214-Z, Policy, Workflow — never dual-write execution tables; never embed local LLM; never local metrics/approval engines.
5. Services, requests, cases and knowledge articles are **tenant-scoped, explainable, auditable** with TraceId and immutable evidence.
6. P306 may Discover · Request · Route · Coordinate Approval/Fulfillment · Validate · Analyze — and must **NOT** Own incident management · Own observability · Own workflow/runtime/remediation/release execution · Bypass policy.
7. Fulfillment executes only via **P260 / P267 / P303 / human / approved external adapters**.
8. Communications via **P294** only; AI must not bypass approval policy.
9. Inference → **P214-Z** only; no module-local LLM.
10. Knowledge lifecycle deepens in **P307**; P264 remains Knowledge Graph / semantic intelligence authority.

## Consequences

- Unlocks Phase 1–11 MEESOP roadmap (P306-A…K); **P307** MEKNOL delivered; **P308** Document Intelligence series unblocked.
- P285 remains federated peer; P305 remains incident authority; P304 remains observe; MEESOP owns service request fulfillment and enterprise service experience.
- Merging P285/P305/P306 SoRs or creating parallel workflow/incident/observability engines is an architecture failure.

## Alternatives considered

| Alternative | Rejected because |
|-------------|------------------|
| Merge into P285 MESMIP only | Productization series needs distinct Service Operations experience SoR; federation preserves both |
| Embed request fulfillment inside P305 | Violates incident/reliability vs service operations split |
| Own workflow/remediation/change execution | Violates P260/P267/P303 ownership |
| Parallel incident management in P306 | Violates P305 Incident authority |
| Local notification / metrics stores | Violates P294 / Observability Platform laws |

## Compliance checklist

- [x] DDD · CQRS · events · hexagonal boundaries documented
- [x] Peer federation matrix (P285 · P305 · P304 · P260 · P267 · P303 · P270 · P294 · Workflow · Policy · Audit)
- [x] Coordinate fulfillment only · no local LLM · no channel send
- [x] P285 · P305 · P304 · execution peer boundaries preserved explicitly
- [x] Critical services Owner/SLA · requests lifecycle · approvals audited · TraceId on fulfillment
- [x] P307 MEKNOL · P308 MEDCIM · P309 MERILG · P310 MEIGSI delivered · P311 stub announced
