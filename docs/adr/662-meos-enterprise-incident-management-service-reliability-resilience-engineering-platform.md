# ADR 662 — MEOS Enterprise Incident Management, Service Reliability & Resilience Engineering Platform (MEIRRE)

- **Status:** Accepted
- **Date:** 2026-08-11
- **Deciders:** Chief Enterprise Architect · MEOS Architecture Board
- **Tags:** meos · p305 · meirre · incident · reliability · resilience · on-call · sre · problem-management · productization
- **Related:** [ADR 661](661-meos-enterprise-process-observability-monitoring-sla-slo-continuous-operational-intelligence-platform.md) · [ADR 660](660-meos-enterprise-process-release-deployment-environment-lifecycle-management-platform.md) · [Law P305](../architecture/ENTERPRISE_MEOS_INCIDENT_MANAGEMENT_SERVICE_RELIABILITY_RESILIENCE_ENGINEERING_PLATFORM.md) · Governance Standard 11.0

## Context

MEOS needs a specialized **Incident Management, Service Reliability & Resilience Engineering** productization layer — without replacing Process Observability (P304), Autonomous Remediation (P267), Release/Deployment (P303), Observability Platform (MLT), Runtime/Workflow/Agent execution (P257/P260/P266), Governance (P270), Process Intelligence (P299), or ITSM/Service Management (P285/P306) — while converting operational signals into coordinated reliability response.

## Decision

1. Establish SoR **`incident_reliability_operating`** as MEIRRE fabric under API **`/api/v1/incident-reliability-operating*`**, schema **`incident_reliability_operating_*`**.
2. Capability **`CAP-PLT-MEIRRE-001`**; fabric id **`meos_enterprise_incident_management_service_reliability_resilience_engineering_platform_framework`**.
3. **Boundary law (hard):**
   - **P304** = OBSERVE · **P305** = RESPOND · **P267** = REMEDIATE · **P304** = VALIDATE
   - **P303** = Release / Deployment · **P270** = Final Governance
   - **P257 / P260 / P266** = Execution authorities
   - Reliability Service Catalog (ownership/SLO/runbook) ≠ ITSM Service Catalog (**P306** / **P285**)
   - **P305** = Incident · Major Incident · Command · On-Call · Escalation · Reliability · Problem · Runbooks · Resilience · DR · PIR
   - **P306** = ITSM / Service Operations / Request Fulfillment (delivered)
   - **P307** = Enterprise Knowledge / Organizational Learning (delivered)
   - **P308** = Document Intelligence / Content Lifecycle (delivered)
   - **P309** = Records / Retention / Legal Hold / ILM (delivered)
   - **P310** = Information Classification / Sensitive Information Intelligence (delivered)
   - **P311** = DLP / Information Protection / Adaptive Data Security Control (next)
4. Federate-by-contract: P304, P267, P303, P257–P270, P285, P294, P298–P302, P214-Z, Policy, Workflow — never dual-write execution tables; never embed local LLM; never local metrics/approval engines.
5. Incidents, runbooks, problems and reviews are **tenant-scoped, explainable, auditable** with TraceId / CorrelationId and immutable evidence.
6. P305 may Command · Coordinate · Recommend · Score · Assess — and must **NOT** Own observability · Own remediation execution · Own runtime/workflow/agent · Replace release/governance/ITSM.
7. High-risk actions and external communications require Policy + Human Approval; chaos experiments authorized/isolated/reversible/auditable.
8. Blameless post-incident reviews; critical services require Owner · Runbook · SLO.
9. Inference → **P214-Z** only; no module-local LLM.
10. Communications via **P294 / Notifications** only — never channel send from MEIRRE.

## Consequences

- Unlocks Phase 1–11 MEIRRE roadmap (P305-A…K); **P306** MEESOP delivered; **P307** Knowledge / Organizational Learning series unblocked.
- P304 remains observe/validate; P267 remains remediate; P303 remains release; MEIRRE owns reliability response coordination.
- Merging P304/P305/P267/P306 SoRs or creating parallel execution/observability engines is an architecture failure.

## Alternatives considered

| Alternative | Rejected because |
|-------------|------------------|
| Embed incident command inside P304 | Violates observe vs respond split |
| Own autonomous remediation | Violates P267 ownership |
| Merge with P285/P306 ITSM catalog | Violates reliability catalog vs request-fulfillment split |
| Own runtime/workflow/agent execution | Violates P257/P260/P266 boundaries |
| AI autonomous high-risk prod changes | Violates Human-in-the-Loop / Policy |

## Compliance checklist

- [x] DDD · CQRS · events · hexagonal boundaries documented
- [x] Peer federation matrix (P304 · P267 · P303 · P257 · P260 · P266 · P270 · P285 · P306 · Workflow · Policy · Audit)
- [x] Respond/coordinate only · remediation via P267 · no local LLM
- [x] P304 · P267 · P303 · execution peer boundaries preserved explicitly
- [x] Critical incidents audited · Commander for majors · Owner/Runbook/SLO for critical services
- [x] P306 MEESOP · P307 MEKNOL · P308 MEDCIM · P309 MERILG · P310 MEIGSI delivered · P311 stub announced
