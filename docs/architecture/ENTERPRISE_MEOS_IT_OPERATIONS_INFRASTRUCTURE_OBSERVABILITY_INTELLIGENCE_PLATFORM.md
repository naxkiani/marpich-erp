# MEOS Enterprise IT Operations, Infrastructure & Observability Intelligence Platform (MEITOI)

**Status:** Normative (P286) — series foundation · **Productization & Experience Evolution Phase**  
**SoR:** `technology_operations_operating` · **ADR:** [643](../adr/643-meos-enterprise-it-operations-infrastructure-observability-intelligence-platform.md) · **Capability:** `CAP-PLT-MEITOI-001`  
**Fabric:** `meos_enterprise_it_operations_infrastructure_observability_intelligence_platform_framework` · **Governance Standard:** MEOS 11.0  
> **API:** `/api/v1/technology-operations-operating*` · **Builds on:** P285 MESMIP · P284 MECCPI · P283 MECIAP · P275 MEAIAMP · P270 MEGRSC · P269 MEPCRI · P268 · P267 MEAOSH · P266 MEAAOI · P265 MEDTIP · P264 MEKGSI · P263 MEDIMOP · P262 MEIAOI · P261 MEBRDI · P260 MEWEOP · P258 MESCC · P257 MERAF · P259 MDMAL · **Observability Platform** · **Documents** · Policy · Workflow · Audit · P214-Z · **Next:** P286-A · **Peer series:** [P287 MECPEI](ENTERPRISE_MEOS_CLOUD_PLATFORM_ENGINEERING_INFRASTRUCTURE_AUTOMATION_INTELLIGENCE_PLATFORM.md) (Cloud / Platform Engineering / IaC Automation OS — never replace Technology Operations; P286 observes; P287 provisions/deploys) · [P288 MEDSSAD](ENTERPRISE_MEOS_DEVSECOPS_SECURE_SOFTWARE_SUPPLY_CHAIN_APPLICATION_DELIVERY_INTELLIGENCE_PLATFORM.md) (DevSecOps — never ungated insecure releases) · [P289 MEAAGSI](ENTERPRISE_MEOS_APPLICATION_ARCHITECTURE_API_GOVERNANCE_SOFTWARE_ARCHITECTURE_INTELLIGENCE_PLATFORM.md) (Architecture / API Governance — never ungated architecture mutations) · [P290 MEDAMIA](ENTERPRISE_MEOS_DATA_ARCHITECTURE_MASTER_DATA_INFORMATION_ARCHITECTURE_INTELLIGENCE_PLATFORM.md) (Data / MDM Architecture — never replace P263; never ungated data-model mutations)  
**Hard bindings:** Inference → **P214-Z** · Telemetry foundation → **Observability Platform** (ACL; **never replace Core Observability**; never fork OTel/metrics APIs; never local metrics/alerting stores outside platform) · Service delivery / ITSM → **P285 `service_management_operating`** (ACL; **P286 does not replace P285** — P285 = service delivery; P286 = technology/infra observability ops) · Commercial SLA assurance → **P284** (ACL) · Asset identity/lifecycle → **P275** (ACL) · Cyber/threat signals → **P268** (ACL) · Autonomous remediation → **P267** (ACL; autonomy thresholds) · Agents → **P266** (ACL) · Twin failure/capacity/change scenarios → **P265** (ACL; simulation ≠ production mutation) · Topology KG → **P264** (ACL) · Decisions → **P261** (ACL) · Remediation workflows → **P260 / Workflow** (ACL; never local approval engines) · Experience Technology Operations Command Center → **P258** (ACL) · Runtime → **P257** (ACL) · Module lifecycle → **P259** (ACL) · Analytics → **P262** (ACL) · Privacy/retention → **P269** (ACL) · Ops governance → **P270** (ACL) · Runbook binaries → **Documents** (`document_id` only) · Policy / DoA / Autonomy → **Policy Engine** · Audit → **Audit** · AuthN/AuthZ → **Identity** · Infra connectors → **Integration Platform** · Generic → **Core**.

---

## 1. Header

**MARPICH ENTERPRISE PLATFORM (MEOS)** · Master Blueprint · Enterprise Architecture Governance Standard **11.0** · Prompt **P286** · MEOS Enterprise IT Operations, Infrastructure & Observability Intelligence Platform (**MEITOI**).  
**Platform Domain:** MEOS Enterprise IT Operations, Infrastructure & Observability Intelligence · **Capability Category:** IT Operations Management, Infrastructure/Application/Network/Cloud Operations, Observability, Monitoring, Log/Metrics/Tracing Intelligence, Event Correlation, Infrastructure/Application Health, Service Dependency Intelligence, Incident Prediction, Capacity Optimization, AIOps & Autonomous IT Operations · **Strategic Layer:** MEOS Enterprise Technology Operations & Observability Layer.

## 2. Prompt ID

**P286**

## 3. Mission

Convert infrastructure, applications, network, cloud and runtime into an Operational Intelligence Platform that is observable, analyzable, predictive and — within Governance — autonomously operable.

**Boundary law (hard):**
- **P285** = Service Management / Service Delivery — *manages the service*
- **P286** = Technology Operations / Infrastructure / Application / Network / Cloud Observability — *observes, analyzes and governs the technology/operational infrastructure*
- **Core Observability Platform** remains telemetry foundation — **P286 does not replace it**
- **P286 does not replace P285.**

```
Infrastructure + Applications + Network + Cloud + Runtime + Telemetry + Logs + Metrics + Traces + Events
→ Observability Intelligence → Correlation → Service Health → Incident Prediction → Root Cause
→ Decision → Workflow → Remediation → Verification → Continuous Optimization
```

MEITOI owns **Technology operations operating fabric** (Technology Operations Command Center contracts, infra/app/network/cloud/observability workspace overlays, gated remediation intents); it does **not** replace Service Management, Core Observability, Workflow, Documents or Core — and never executes material production infrastructure mutations outside Policy + Workflow + Delegation-of-Authority (+ human approval when above autonomy threshold) with **Approved Runbook** + **Safe Rollback**.

## 4. Architecture Principles

- Enterprise Architecture Governance Standard **11.0** (binding)
- DDD · CQRS · Event Sourcing · Event-Driven · Hexagonal · Clean · API-First
- Cloud Native · AI Native · Knowledge Graph Native · Digital Twin Native
- Metadata Driven · Configuration Driven · Policy Driven
- Zero Trust · Explainable AI · Responsible AI · Human Governance
- **Privacy By Design** · **Continuous Governance** · Traceability for Infrastructure · Application · Network · Cloud · Telemetry · Dependency · Incident · Remediation
- **Versioned Observability Policies** · **Reproducible Operational Decisions** · **Full Auditability** · **Least Privilege** · **Immutable Operational Evidence**
- Multi-tenant · Fail-closed authorization · Pagination mandatory
- Federate-by-contract only — never peer domain imports / shared tables / local LLM
- **P285 vs P286:** never merge Service Delivery SoR with Technology Operations SoR
- Material production remediation: Policy + Permission + Delegation + Risk Threshold + Approved Runbook + Human Governance (when above autonomy) + Verification + Audit
- **No AI Agent may execute uncontrolled production changes outside Policy + Delegation Authority**
- Twin scenario ≠ production mutation
- Telemetry via Observability Platform; runbooks via Documents (`document_id`)

## 5. Reference Architecture

```
IT Operations Experience (P258 Command Center · Infra · App · Network · Cloud · Observability Explorer · Topology · Incident · Capacity · Change Impact · AI Assistant)
        ↓
┌────────────────────────────────────────────────────────────────────┐
│ Technology Operations Operating Fabric                             │
│ (SoR technology_operations_operating)                              │
│ schema: technology_operations_operating_*                          │
└────────────────────────────────────────────────────────────────────┘
        ↓ ACL              ↓ ACL              ↓ ACL
 Core Observability    P285 Service Mgmt   Workflow / P275 Asset / P268 Cyber
        ↓
 Operations Core overlays · Governance (monitoring · alert · SLO · retention · automation · autonomy)
        ↓
 Foundation: P266 Agents · P264 KG · P265 Twin · P260 Workflow · P261 Decision · P267 Ops
```

| Layer | Role |
|-------|------|
| IT Operations Experience | Command Center · Workspaces · Observability Explorer · AI Assistant |
| Observability Intelligence | Metrics · Logs · Traces · Correlation · Anomaly · Topology · RCA · Capacity · Prediction |
| Operations Core | Infra · Compute · Storage · DB · Network · App · API · Container · K8s · Cloud · Telemetry · Health · Incident · Remediation |
| Governance | Monitoring · Alert · SLO · Retention · Access · Automation · Remediation · Change · Autonomy · Audit |
| Intelligence Foundation | Agents · KG · Twin · Mesh · Decision · Workflow · Service Management · Cyber · Asset · Governance |

## 6. Core Capabilities

| ID | Capability |
|----|------------|
| MEITOI-C01 | Technology Operations Command Center |
| MEITOI-C02 | Infrastructure Operations |
| MEITOI-C03 | Application Operations |
| MEITOI-C04 | Network Operations |
| MEITOI-C05 | Cloud Operations |
| MEITOI-C06 | Observability Engine (federated) |
| MEITOI-C07 | Metrics Intelligence |
| MEITOI-C08 | Log Intelligence |
| MEITOI-C09 | Distributed Trace Intelligence |
| MEITOI-C10 | Event Correlation |
| MEITOI-C11 | Anomaly Detection |
| MEITOI-C12 | Service Topology Intelligence |
| MEITOI-C13 | Application Performance Intelligence |
| MEITOI-C14 | Infrastructure Health & Capacity Intelligence |
| MEITOI-C15 | Failure Prediction · Root Cause · Alert/SLO Intelligence · Change Impact |
| MEITOI-C16 | AIOps + Autonomous IT Operations (gated) + MEITOI Governance Kernel |

### Notes

Resource lifecycle: Discovered → Registered → Monitored → Healthy → Degraded → Failed → Recovered → Retired.  
Unified model: Metrics + Logs + Traces + Events → Correlation → Operational Context.  
Navigation law: Metric → Trace → Log → Service → Dependency → Incident → Root Cause → Remediation without breaking experience.  
Topology sync: P264 KG + P265 Twin + P285 Service Management.  
Autonomous: Signal → AI Diagnosis → Risk → Policy → Autonomy Threshold → Remediation **OR** Human Approval → Execution → Verification → Audit. Permitted governed actions: restart approved service/container, scale approved resource, clear known failure, failover approved component, execute approved runbook, create/escalate incident, standard operational change.

## 7. User Experience Architecture

```
IT Operator → Technology Operations Command Center → Infra / App / Network / Cloud / Observability / Incidents / Capacity / Changes
→ AI Operations Assistant → Action / Workflow → Verification
```

Workspaces: Infrastructure · Application Operations · Network · Observability Explorer · Incident Operations · Capacity Center · Change Impact Center.  
AI Assistant: *"Why has the payment service slowed down?"* → Service → SLO → App → Traces → Logs → Infra → Dependencies → Recent Changes → Probable Root Cause + Confidence + Evidence → Recommended Action.

## 8. Application Runtime Model

```
Resource Discovery → Registration → Telemetry Activation → Health Monitoring → Event Processing
→ Correlation → Anomaly → Incident → Diagnosis → Decision → Workflow → Remediation → Verification → Knowledge Update
```

OperationsRuntimeInstance: Resource · Application · Service · Network · Cloud · Telemetry · Metrics · Logs · Traces · Events · Dependencies · HealthState · IncidentState · CapacityState · RiskState · ChangeState · AutomationState · RemediationState · AuditHistory.

Activation: Domain Registered → Metadata → Resource Connectors → Telemetry/Monitoring/Alert/SLO Policies → Permissions → Runtime Activated → Command Center → Infra/App/Network/Cloud Monitoring → Observability Explorer → Agents.

## 9. AI Agents

| Agent | Role | Gate |
|-------|------|------|
| IT Operations Intelligence Agent | Health · risk · insights · recommend | Explainability · Audit |
| Observability Agent | Correlate MLT · patterns · context | Observability Platform ACL |
| Infrastructure Agent | Monitor · fail detect/predict · remediate recommend | Autonomy thresholds |
| Application Operations Agent | Health · performance · bottlenecks | Peer ACL |
| Network Intelligence Agent | Connectivity · latency · predict | Peer ACL |
| Cloud Operations Agent | Resource risk · capacity · scaling | Policy · DoA |
| Root Cause Agent | Correlate · dependencies · changes · evidence | Confidence scoring |
| Capacity Agent | Forecast · bottlenecks · scaling | Non-actuating default |
| Incident Intelligence Agent | Detect · classify · mitigate recommend | Workflow |
| Change Impact Agent | Topology · simulate · safe execution | Twin · Policy |
| Remediation Agent | Runbook · policy · execute · verify | Approved runbook · rollback |
| AIOps Orchestrator Agent | Coordinate · conflict resolve · governance routing | No uncontrolled production change |

**Law:** Agents recommend; production remediation via Policy + Workflow + Human DoA (or within Autonomy Threshold) + Approved Runbook + Verification + Audit. Never module-local LLM. Simulation ≠ execute. Safe rollback mandatory.

## 10. Domain Driven Design (DDD)

**Core domain:** MEOS Enterprise IT Operations, Infrastructure & Observability Intelligence (operating)  
**Strategic type:** Supporting Domain (platform / technology operations)

### Bounded Contexts (logical; single SoR `technology_operations_operating`)

| BC | Name | Aggregate root |
|----|------|----------------|
| BC-01 | IT Operations Operating | `OperationalResourceCampaignAggregate` |
| BC-02 | Infrastructure / Cloud Operating | `InfrastructureCampaignAggregate` |
| BC-03 | Application / Network Operating | `ApplicationOperationsCampaignAggregate` |
| BC-04 | Observability / Topology Operating | `ObservabilityCampaignAggregate` |
| BC-05 | Incident / RCA / Capacity Operating | `OperationalIncidentCampaignAggregate` |
| BC-06 | Remediation / Governance / Autonomy Operating | `RemediationCampaignAggregate` |

### Aggregates

**OperationalResource:** Identity · Health · Telemetry · Dependencies · Alerts · Incidents · Changes · History  
**Application:** Components · Instances · Dependencies · Performance · SLO · Deployments · History  
**Observation:** Metrics · Logs · Traces · Events · Correlations · History  
**TopologySnapshot:** Nodes · Dependencies · Paths · Services · History  
**OperationalIncident:** Alerts · Signals · Impact · Diagnosis · Remediation · Verification · History  
**CapacityPlan:** Measurements · Forecasts · Risks · Recommendations · History  
**RemediationAction:** Runbook · Policy · Approval · Execution · Verification · Audit

### Value Objects

`ObservabilityPolicyVersionId` · `SLOVersionId` · `TelemetrySourceRef` · `TopologySnapshotId` · `BreachProbability` · `AutonomyThreshold` · `DoAThreshold` · `ApprovedRunbookRef` · `ExplainabilityTraceRef` · `PeerServiceRef` · `PeerAssetRef` · `DocumentIdRef` · `TenantScope`

### Domain Services

`ResourceDiscoveryService` · `InfrastructureMonitoringService` · `ApplicationMonitoringService` · `NetworkMonitoringService` · `CloudOperationsService` · `TelemetryIngestionService` · `MetricsIntelligenceService` · `LogIntelligenceService` · `TraceIntelligenceService` · `EventCorrelationService` · `TopologyService` · `AnomalyDetectionService` · `IncidentIntelligenceService` · `RootCauseAnalysisService` · `CapacityIntelligenceService` · `FailurePredictionService` · `ChangeImpactService` · `RemediationService` · `RunbookService` · `OperationsGovernanceService` · `AutonomousOperationsService` · `OperationsExplainabilityService`

**Hard separation:** Service catalog/ITSM in P285; Core Observability owns telemetry plumbing; asset identity in P275; MEITOI stores ops campaigns, correlation/RCA/remediation overlays and peer refs only.

## 11. Event Architecture

### Domain Events

`ResourceDiscovered` · `ResourceRegistered` · `ResourceHealthChanged` · `ApplicationDiscovered` · `ApplicationHealthChanged` · `ApplicationPerformanceDegraded` · `NetworkDeviceDiscovered` · `NetworkHealthChanged` · `CloudResourceDiscovered` · `TelemetrySourceRegistered` · `MetricRecorded` · `MetricAnomalyDetected` · `LogReceived` · `LogPatternDetected` · `TraceRecorded` · `TraceAnomalyDetected` · `OperationalEventReceived` · `EventsCorrelated` · `TopologyChanged` · `DependencyFailureDetected` · `ServiceHealthDegraded` · `AlertCreated` · `AlertCorrelated` · `IncidentPredicted` · `OperationalIncidentCreated` · `OperationalIncidentEscalated` · `RootCauseCandidateIdentified` · `RootCauseConfirmed` · `CapacityRiskDetected` · `FailurePredicted` · `ChangeImpactDetected` · `RemediationRequested` · `RemediationApproved` · `RemediationExecuted` · `RemediationVerified` · `OperationalIncidentResolved` · `SLOBreached` · `ErrorBudgetConsumed` · `OperationsOutcomeRecorded` · `OperationsGateApplied`

### Event Flow

`Telemetry → Metrics/Logs/Traces/Events → Normalization → Correlation → Topology → Anomaly → Incident/Risk → Root Cause → Decision → Workflow → Remediation → Verification → Outcome`  
Subscribers: P257 · P258 · P259 · P260 · P261 · P262 · P263 · P264 · P265 · P266 · P267 · P268 · P269 · P270 · P275 · P285 · P284 · Audit · Observability Platform

Envelope + outbox + idempotent ACL consumers mandatory. Remediation events carry authorization + runbook + verification + audit refs.

## 12. CQRS

### Commands

`DiscoverResourceCommand` · `RegisterResourceCommand` · `ActivateMonitoringCommand` · `RecordMetricCommand` · `IngestLogCommand` · `RecordTraceCommand` · `PublishOperationalEventCommand` · `CorrelateSignalsCommand` · `CreateAlertCommand` · `ClassifyAnomalyCommand` · `CreateOperationalIncidentCommand` · `EscalateOperationalIncidentCommand` · `AnalyzeRootCauseCommand` · `CreateCapacityPlanCommand` · `RecordCapacityMeasurementCommand` · `PredictFailureCommand` · `AssessChangeImpactCommand` · `CreateRemediationCommand` · `ApproveRemediationCommand` · `ExecuteRemediationCommand` · `VerifyRemediationCommand` · `UpdateTopologyCommand` · `RecordSLOMeasurementCommand` · `EvaluateErrorBudgetCommand` · `ApplyOperationsGateCommand`

(Authoritative infra mutations only via Integration/approved runbook adapters under Policy + Workflow — never uncontrolled agent mutations.)

### Queries

`GetTechnologyHealthQuery` · `GetInfrastructureHealthQuery` · `GetApplicationHealthQuery` · `GetNetworkHealthQuery` · `GetCloudHealthQuery` · `GetMetricQuery` · `GetLogQuery` · `GetTraceQuery` · `GetEventQuery` · `GetTopologyQuery` · `GetDependencyQuery` · `GetIncidentQuery` · `GetAlertQuery` · `GetAnomalyQuery` · `GetRootCauseQuery` · `GetCapacityQuery` · `GetFailurePredictionQuery` · `GetChangeImpactQuery` · `GetRemediationQuery` · `GetSLOStatusQuery` · `GetServiceDependencyHealthQuery`

Read models under `technology_operations_operating_*` only; pagination mandatory; live telemetry via Observability Platform.

## 13. MEOS Integration

| Peer | Mode |
|------|------|
| **Observability Platform** | Telemetry foundation — **never replace** |
| **P285 MESMIP** | Service → app/infra dependency → incident handoff — **never replace** |
| **P284 MECCPI** | Availability/SLA signals → commercial performance |
| **P275** | Asset identity · health · lifecycle · cost context |
| **P268** | Secure ops · threat enrichment |
| **P267 · P266 · P265 · P264** | Autonomous ops · agents · twin · KG topology |
| **P260 · P261 · P257–P259** | Remediation workflow · decisions · runtime · shell · lifecycle |
| **P269 · P270** | Privacy/retention · ops governance |
| Policy · Audit · Identity · Integration | DoA · evidence · authority · connectors |
| **P287 MECPEI** | Cloud / Platform Engineering / IaC Automation OS — **never replace Technology Operations; P286 observes; P287 provisions/deploys** |
| Core | Generic platform services |

Permissions: `technology_operations_operating.infra.*` · `technology_operations_operating.app.*` · `technology_operations_operating.network.*` · `technology_operations_operating.cloud.*` · `technology_operations_operating.observability.*` · `technology_operations_operating.incident.*` · `technology_operations_operating.capacity.*` · `technology_operations_operating.remediation.*` · `technology_operations_operating.governance.*` · `technology_operations_operating.ai.read` · `technology_operations_operating.ai.infer`.

## 14. Implementation Roadmap

| Phase | Focus | Window | Deliverables |
|-------|-------|--------|--------------|
| **P286** | Foundation | — | ADR · capability · fabric · DDD/CQRS · API skeleton · dual tests |
| **Phase 1 / P286-A** | Operations Foundation | 3–6 mo | Discovery · infra/app/network/cloud monitoring · basic metrics/logs · command center |
| **Phase 2 / P286-B** | Observability Intelligence | 6–12 mo | Unified MLT · correlation · topology · dependencies · anomaly · SLO |
| **Phase 3 / P286-C** | AIOps Intelligence | 12–18 mo | Incident/failure prediction · RCA · capacity forecast · change impact · AI assistant · intelligent alerting |
| **Phase 4 / P286-D** | Autonomous IT Ops | 18–36 mo | Autonomous triage · governed auto-remediation · predictive prevention · continuous learning · self-healing (gated) |

Catalogs (planned): `docs/architecture/technology_operations_operating/MEITOI_*_{CAPABILITIES,DDD_CQRS,SECURITY,VALIDATION,ARCHITECTURE}.v1.yaml`

## 15. Quality Gates

- Never MEOS Enterprise IT Operations Platform is missing
- Never Infra/App/Network/Cloud Ops · Observability · Topology · RCA · Capacity · AIOps capabilities are missing
- Never Versioned Observability/SLO Policies missing
- Never Sibling Technology Operations Operating BC (second deployable)
- Never Replace **P285** · **Core Observability** · Workflow · Documents · Core · AI
- Never Fork Observability APIs · Never Local metrics/alerting stores · Never Local approval engines
- Never Ungated Production Mutations · Never Bypass Ops Policy · Never Module-Local LLM
- Never Treat Twin Scenario as Production Mutation
- Unified MLT correlation · Metric→Trace→Log→Service→Incident→RCA→Remediation navigation
- Explainable diagnosis · Confidence scoring · Evidence · Human governance · Autonomy thresholds · Safe rollback · Action auditability

Validate: ops architecture · DDD · CQRS · events · P285/Observability boundaries · workspaces · AI assistant.

## 16. Definition of Done

- [ ] ADR **643** accepted; capability `CAP-PLT-MEITOI-001` registered
- [ ] Law + YAML catalogs under `docs/architecture/technology_operations_operating/`
- [ ] Context `backend/contexts/technology_operations_operating/` scaffolded
- [ ] Fabric wired + ACL to Observability Platform, P285, P275, P268, Workflow, Policy
- [ ] Outbox events + ACL stubs (Observability · P285 · P275 · Workflow · P266 · P214-Z · Audit)
- [ ] Dual tests green; scorecard **ENTERPRISE_GRADE**
- [ ] OpenAPI `/api/v1/technology-operations-operating*`
- [ ] Versioned observability policy + reproducible gated remediation path demonstrated
- [ ] **P286-A** unlocked · **P287** cloud/platform engineering series delivered (ADR 644) · **P288** DevSecOps series delivered (ADR 645) · **P289** Architecture series delivered (ADR 646) · **P290** Data Architecture series delivered (ADR 647)

**MEITOI is complete when:** MEOS has an Enterprise IT Operations OS fabric over Core Observability; infra/app/network/cloud ops, unified observability intelligence, topology, AIOps and gated autonomous remediation operate under gates; agents participate within autonomy thresholds with approved runbooks and safe rollback; events join the Event Mesh; KG/twin support topology; P285 and Core Observability boundaries preserved; material production actions remain under Policy and Human Governance; no agent executes uncontrolled production changes; MEOS progresses toward Continuous Technology Operations Intelligence and Governed Self-Healing with the end-to-end discovery→telemetry→correlation→remediation→learning chain executable — Governance Standard **11.0**.

**Principle:** MEITOI productizes technology operations and observability intelligence; it never replaces P285 or Core Observability, never embeds local metrics/approval engines, and never executes material production remediation without Policy + Delegation + Approved Runbook + Workflow + Verification + Audit accountability.

---

**NEXT EXECUTION:** **P311** — MEOS Enterprise Data Loss Prevention, Information Protection & Adaptive Data Security Control Platform — convert P310 Classification/Sensitivity into operational Data Protection and DLP controls (Prevent / Allow / Block / Quarantine / Redact) under Policy + Context + Risk (federate P310, P268, P269, P270, P260; never fork Classification Intelligence or Cybersecurity; never create parallel mesh/content/records/workflow/agent engines).

> **P291 delivered:** [MEIEII law](ENTERPRISE_MEOS_INTEGRATION_ARCHITECTURE_EVENT_MESH_INTEROPERABILITY_INTELLIGENCE_PLATFORM.md) · [ADR 648](../adr/648-meos-enterprise-integration-architecture-event-mesh-interoperability-intelligence-platform.md)
