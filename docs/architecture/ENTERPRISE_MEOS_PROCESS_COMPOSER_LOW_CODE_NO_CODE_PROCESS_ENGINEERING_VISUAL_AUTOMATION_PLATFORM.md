# MEOS Enterprise Process Composer, Low-Code/No-Code Process Engineering & Visual Automation Platform (MEPCVA)

**Status:** Normative (P301) — series foundation · **Productization & Experience Evolution Phase**  
**SoR:** `process_composer_operating` · **ADR:** [658](../adr/658-meos-enterprise-process-composer-low-code-no-code-process-engineering-visual-automation-platform.md) · **Capability:** `CAP-PLT-MEPCVA-001`  
**Fabric:** `meos_enterprise_process_composer_low_code_no_code_process_engineering_visual_automation_platform_framework` · **Governance Standard:** MEOS 11.0  
> **API:** `/api/v1/process-composer-operating*` · **Builds on:** P300 MEPAMP · P299 MEPICO · P298 MEAPAE · P297 MEAWHC · P270 MEGRSC · P269 MEPCRI · P268 MECZTD · P266 MEAAOI · P265 MEDTIP · P264 MEKGSI · P263 MEDIMOP · P262 MEIAOI · P261 MEBRDI · P260 MEWEOP · P259 MDMAL · P258 MESCC · P257 MERAF · **Plugin Platform** · **Documents** · **Observability** · **Secrets** · **Feature Flags** · Policy · Workflow · Audit · P214-Z · **Next:** P301-A · **Peer series:** [P302 MEPQDV](ENTERPRISE_MEOS_PROCESS_TESTING_SIMULATION_QUALITY_ASSURANCE_DIGITAL_PROCESS_VALIDATION_PLATFORM.md) (Process Quality Engineering OS — never replace Composer; design-time only in P301; no production without Quality Gate)  
**Hard bindings:** Inference → **P214-Z** (ACL; **never module-local LLM**) · Process Marketplace / Packages → **P300** (ACL; asset discovery, package publish; **never replace Marketplace**) · Process Intelligence → **P299** (ACL; prediction/optimization recommendations; never replace) · Agentic Process Automation → **P298** (ACL; consume governed designs; never replace) · Workflow Execution → **P260** (ACL; configure workflow refs only; **never execute**) · Agent Orchestration → **P266** (ACL; configure agent refs only; **never execute**) · Decision Execution → **P261** (ACL; configure decision refs only; **never execute**) · Application Lifecycle → **P259** (ACL; submit release/package for activation; never replace) · Application Runtime → **P257** (ACL; never execute transactions / never modify production state directly) · Digital Twin / Simulation → **P265** (ACL; design-time simulation; **simulation ≠ execute**) · Knowledge Graph → **P264** (ACL; semantic relationships; never become KG engine) · Data Mesh → **P263** (ACL; select Data Products/Contracts only) · Governance → **P270 · Workflow** (ACL; design/release gates; never local approval engines) · Human review → **P297** (ACL) · Application Shell → **P258** (ACL; composer UX entry) · Escalation delivery → **P294 / Notifications** (ACL; never send channels) · Docs → **Documents** (`document_id` only) · Progressive exposure → **Feature Flags** (ACL) · Policy / DoA → **Policy Engine** · Audit → **Audit** · AuthN/AuthZ → **Identity** · Generic → **Core**.

---

## 1. Header

**MARPICH ENTERPRISE PLATFORM (MEOS)** · Master Blueprint · Enterprise Architecture Governance Standard **11.0** · Prompt **P301** · MEOS Enterprise Process Composer, Low-Code/No-Code Process Engineering & Visual Automation Platform (**MEPCVA**).  
**Platform Domain:** MEOS Enterprise Process Composer, Low-Code/No-Code Process Engineering & Visual Automation · **Capability Category:** Visual Process Canvas, Process Modeling, Asset Composition, Natural Language / AI Process Design, Design-Time Validation, Simulation Coordination, Collaboration/Review, Release Preparation, Process Package Generation, Process Engineering Command Center · **Strategic Layer:** MEOS Visual Process Engineering & Low-Code/No-Code Composition Experience.

## 2. Prompt ID

**P301**

## 3. Mission

Create a Visual Enterprise Process Engineering Environment that unifies:

```
INTENT → DESIGN → COMPOSE → CONFIGURE → VALIDATE → SIMULATE → GOVERN → PACKAGE → ACTIVATE → MONITOR → OPTIMIZE
```

for Business Users, Process Owners, Analysts and Enterprise Architects — enabling design, composition, validation, simulation and deployment preparation of enterprise processes without creating a parallel Runtime or Execution Engine.

**Core principle:**

```
DESIGN ONCE → VALIDATE → SIMULATE → GOVERN → PACKAGE → DEPLOY THROUGH EXISTING MEOS RUNTIME
```

**Boundary law (hard):**
- **P257** = Enterprise Runtime / Application Execution
- **P259** = Application Lifecycle / Activation
- **P260** = Workflow Definition / Execution / State
- **P261** = Business Decision Intelligence / Decision Execution
- **P266** = Agent Registry / Planning / Delegation / Orchestration / Execution
- **P270** = Enterprise Governance / Policy / Risk / Compliance / Approval
- **P298** = Agentic Process Automation / Adaptation
- **P299** = Process Mining / Intelligence / Optimization
- **P300** = Process Asset Marketplace / Reusable Assets / Distribution
- **P301** = Visual Process Engineering / Composition / Design-Time Validation / Release Preparation
- **P302** = Process Testing / QA / Digital Process Validation (delivered)
- **P303** = Process Release / Deployment / Environment Lifecycle (delivered)
- **P304** = Process Observability / Continuous Operational Intelligence (delivered)
- **P305** = Incident Management / Service Reliability / Resilience Engineering (next)
- P301 is **DESIGN-TIME** — may Design · Compose · Configure · Validate · Simulate · Recommend · Package — and must **NOT** Execute Workflow · Execute Agent · Execute Decision · Execute Enterprise Transaction · Modify Production State Directly
- AI-generated processes remain **Draft** until validated and governed; no process enters Production directly from P301

MEPCVA owns **process composer operating fabric** (Canvas / Outline / Validation / Simulation / Governance / Version / Release Command Centers, design/composition overlays, AI design-assist campaigns); it does **not** own workflow/agent/decision/runtime/intelligence/marketplace/governance engines — and never promotes designs to production outside Validate → Simulate → Review → Govern → Package → P259 Lifecycle with **Evidence + Design Score + Version**.

## 4. Architecture Principles

- Enterprise Architecture Governance Standard **11.0** (binding)
- DDD · CQRS · Event Sourcing · Event-Driven · Hexagonal · Clean · API-First · Contract First · Event-First
- Cloud Native · AI Native · Metadata Driven · Configuration Driven · Policy Driven
- Zero Trust · Knowledge Graph Native · Digital Twin Native · Data Mesh Compatible
- Explainable AI · Responsible AI · Human-in-the-Loop · Plugin First · Low-Code/No-Code · Visual Engineering
- Reusable Asset Architecture · Versioned Architecture · Continuous Governance · Auditability
- Multi-tenant · Fail-closed authorization · Pagination mandatory
- Federate-by-contract only — never peer domain imports / shared tables / local LLM
- **P260 vs P266 vs P298 vs P299 vs P300 vs P301 vs P302:** never merge workflow execution, agent orchestration, agentic automation, process intelligence, marketplace, visual composer, and process QA SoRs
- Same process model, multiple abstraction views (Business · Analyst · Technical · Architecture · Runtime)
- Avoid duplication — search P300 / enterprise registry before creating new assets
- **No AI Agent may promote designs to production outside Policy + Governance + P259 Lifecycle + Audit**
- Simulation ≠ execute · Process versions immutable once released

## 5. Reference Architecture

```
Business Intent → Process Canvas → Process Model → Asset Discovery (P300) → Visual Composition
        ↓
┌────────────────────────────────────────────────────────────────────┐
│ Process Composer Operating Fabric (P301) — DESIGN-TIME             │
│ (SoR process_composer_operating)                                   │
│ schema: process_composer_operating_*                               │
│ Canvas · Composition · Validation · Simulation Coord · Release Prep│
└────────────────────────────────────────────────────────────────────┘
        ↓
 Validation Engine → Simulation (P265) → Intelligence (P299) → Governance (P270)
        ↓ ACL
 Process Package (P300) → Lifecycle (P259) → Workflow (P260) / Agents (P266) / Agentic (P298) → Runtime (P257)
```

Composition model: Process → Trigger · Activities · Decisions · Workflows · Agents · Policies · Data · Integrations · Exceptions · SLA · KPI · Outcomes.

## 6. Core Capabilities

| ID | Capability |
|----|------------|
| MEPCVA-C01 | Visual Process Canvas · Drag/Drop · Branch/Parallel/Loop/Exception/Subprocess |
| MEPCVA-C02 | Process Design Modes · Modeling · Templates (Blank / P300 / Industry / AI Draft) |
| MEPCVA-C03 | Asset Library · Drag-and-Drop Composition · Component Palette |
| MEPCVA-C04 | AI Process Generation · Natural Language Design · Design Explanation (Draft-only) |
| MEPCVA-C05 | Variables · Data Contract · Decision/Agent/Workflow/Policy Integration (refs only) |
| MEPCVA-C06 | Human-in-the-Loop · SLA · KPI · Exception Design |
| MEPCVA-C07 | Version Control · Visual Diff · Collaboration · Review |
| MEPCVA-C08 | Validation Engine · Design-Time Quality Score |
| MEPCVA-C09 | Simulation / What-If (P265) · Intelligence / Automation Score (P299) |
| MEPCVA-C10 | Process Package Generation · Deployment Readiness · Release Candidates |
| MEPCVA-C11 | Ownership · Documentation Generator · Knowledge Graph enrichment (P264) |
| MEPCVA-C12 | Process Search · Recommendation · Duplication Detection |
| MEPCVA-C13 | Governance Checkpoints · Process Engineering Command Center |
| MEPCVA-C14 | Process Design Agents + MEPCVA Governance Kernel |

### Notes

Component palette: TRIGGER · TASK · HUMAN TASK · AI TASK · AGENT TASK · DECISION · APPROVAL · SUBPROCESS · PARALLEL · CONDITION · WAIT · TIMER · EVENT · EXCEPTION · END.  
Mandatory gates: Design → Validate → Simulate → Review → Govern → Package.  
Desktop-first engineering; mobile focuses on Review · Approval · Monitoring.

## 7. User Experience Architecture

```
Human → Process Design Home → Visual Canvas (Components | Canvas | Properties | AI Copilot)
→ Outline · Validation · Simulation · Governance · Version · Review Mode
```

AI Copilot: Optimize · Explain · Find reusable workflow · Add compliance · Reduce cycle time · Find bottlenecks · Create exception handling.  
Validation panel: Passed · Warning · Error · Governance · AI Recommendation.  
Responsive: Desktop / Tablet / Large screens; mobile = review/approval/monitoring only.

## 8. Application Runtime Model

```
User Intent → P301 Composer → Process Metadata → P300 Asset Discovery → Composition
→ Validation → P265 Simulation → P299 Intelligence → P270 Governance
→ P300 Package → P259 Lifecycle → P260 / P266 / P298 → P257 Runtime
```

ProcessDesignContext: ProcessDesignId · ProcessId · Version · TenantId · Owner · BusinessOwner · TechnicalOwner · Status · Metadata · Model · Dependencies · GovernanceStatus · SimulationStatus · ValidationStatus · TraceId.

ProcessNodeContext: NodeId · NodeType · Name · Configuration · Inputs · Outputs · AssetReference · PolicyReference · DecisionReference · AgentReference · WorkflowReference · DataContractReference.

ProcessReleaseContext: ReleaseId · ProcessId · Version · Validation · Simulation · Governance · Certification · PackageId · ReleaseStatus.

**Hard runtime rule:** P301 never executes peers in-process; `RequestDeploymentCommand` emits governed package/lifecycle intents to **P300 + P259 + P270** only.

## 9. AI Agents

P301 does **not** replace P266. P301 defines Design-Time Process Engineering Agents.

| Agent | Role | Gate |
|-------|------|------|
| Process Design Agent | Intent → process structure | Draft |
| Process Modeling Agent | NL → structured model | Draft |
| Asset Discovery Agent | Search P300 reusable components | — |
| Process Composition Agent | Recommend workflow/agent/decision/policy/connector | Evidence |
| Process Validation Agent | Structural/dependency/data issues | — |
| Process Optimization Agent | Automation/parallelization via P299 | — |
| Simulation Agent | Scenarios / stress / failure / what-if (P265) | Simulation ≠ execute |
| Documentation Agent | Enterprise docs generation | — |
| Governance Assistant | Policies · approvals · risk · compliance | P270 |
| Duplication Detection Agent | Similar processes/assets | Prefer reuse |
| Test Generation Agent | Happy/failure/boundary/exception/security tests | Prep for P302 |
| Explainability Agent | Explain every AI design decision | Safe summaries |

**Law:** Design agents produce Draft designs only; execution via P257/P260/P266/P261; packaging via P300; activation via P259; never module-local LLM; never channel send; simulation ≠ execute.

## 10. Domain Driven Design (DDD)

**Core domain:** MEOS Enterprise Process Composer, Low-Code/No-Code Process Engineering & Visual Automation (operating)  
**Strategic type:** Supporting Domain (platform / visual process engineering experience)

### Bounded Contexts (logical; single SoR `process_composer_operating`)

| BC | Name | Aggregate root |
|----|------|----------------|
| BC-01 | Process Design / Model / Version Operating | `ProcessDesignCampaignAggregate` |
| BC-02 | Composition / Asset Reference Operating | `ProcessCompositionCampaignAggregate` |
| BC-03 | Validation / Design Score Operating | `ProcessValidationCampaignAggregate` |
| BC-04 | Simulation Coordination Operating | `ProcessSimulationCampaignAggregate` |
| BC-05 | Release / Package Prep Operating | `ProcessReleaseCampaignAggregate` |
| BC-06 | Collaboration / Documentation / Governance Operating | `ProcessCollaborationCampaignAggregate` |

### Aggregates

**ProcessDesign:** ProcessModel · Nodes · Connections · Variables · Dependencies · Policies · Version  
**Composition:** Components · AssetReferences · Configurations · Dependencies  
**ValidationRun:** Rules · Issues · Scores · Result  
**ReleaseCandidate:** Version · Validation · Simulation · Governance · Certification · Package

### Value Objects

`ProcessDesignId` · `ProcessModelId` · `ProcessVersionId` · `NodeId` · `NodeType` · `ConnectionId` · `AssetReference` · `CompositionId` · `ValidationRunId` · `DesignScore` · `SimulationRef` · `ReleaseCandidateId` · `PackageIdRef` · `AutomationScore` · `MaturityScore` · `DiffRef` · `DocumentIdRef` · `DoAThreshold` · `ExplainabilityTraceRef` · `TenantScope`

### Domain Services

`ProcessDesignService` · `ProcessModelService` · `ProcessCanvasService` · `ProcessCompositionService` · `AssetDiscoveryService` · `AssetRecommendationService` · `ProcessValidationService` · `ProcessDependencyService` · `ProcessSimulationService` · `ProcessOptimizationService` · `ProcessGovernanceService` · `ProcessReleaseService` · `ProcessVersionService` · `ProcessDiffService` · `ProcessDocumentationService` · `ProcessCollaborationService` · `ProcessTestGenerationService` · `ProcessKnowledgeGraphService` · `ProcessDuplicationService` · `ProcessPackageService` · `ProcessAuditService`

**Hard separation:** Marketplace in P300; intelligence in P299; adaptation in P298; workflow/agent/decision/runtime in P260/P266/P261/P257; lifecycle in P259; governance in P270; MEPCVA stores design-time campaigns, canvas overlays, validation/release assessments and peer refs only — never dual-write execution tables.

## 11. Event Architecture

### Domain Events

`ProcessDesignCreated` · `ProcessDesignUpdated` · `ProcessNodeAdded` · `ProcessNodeRemoved` · `ProcessNodeConfigured` · `ProcessConnectionCreated` · `ProcessConnectionRemoved` · `ProcessAssetSelected` · `ProcessAssetConfigured` · `ProcessCompositionCreated` · `ProcessCompositionValidated` · `ProcessDependencyDetected` · `ProcessDependencyResolved` · `ProcessValidationStarted` · `ProcessValidationCompleted` · `ProcessValidationFailed` · `ProcessSimulationRequested` · `ProcessSimulationStarted` · `ProcessSimulationCompleted` · `ProcessOptimizationRequested` · `ProcessOptimizationSuggested` · `ProcessPolicyAttached` · `ProcessSLAConfigured` · `ProcessKPIConfigured` · `ProcessExceptionConfigured` · `ProcessReviewRequested` · `ProcessReviewCompleted` · `ProcessChangeRequested` · `ProcessChangeApproved` · `ProcessChangeRejected` · `ProcessDocumentationGenerated` · `ProcessTestGenerated` · `ProcessDuplicationDetected` · `ProcessReleaseCandidateCreated` · `ProcessReleaseValidated` · `ProcessReleaseApproved` · `ProcessReleaseRejected` · `ProcessPackageGenerated` · `ProcessPackagePublished` · `ProcessDeploymentRequested` · `ProcessComposerGateApplied`

### Event Flow

`Intent → Design → Compose → Validate → Simulate → Optimize → Review → Govern → Package → Publish → Deploy`  
Consumers: P257 · P259 · P260 · P261 · P263 · P264 · P265 · P266 · P270 · P297 · P298 · P299 · P300 · Observability · Audit · Feature Flags

Envelope + outbox + idempotent ACL consumers mandatory. Release/package events carry AuthZ + Policy + Validation + Simulation + Approval + Version refs.

## 12. CQRS

### Commands

`CreateProcessDesignCommand` · `UpdateProcessDesignCommand` · `AddProcessNodeCommand` · `RemoveProcessNodeCommand` · `ConnectProcessNodesCommand` · `DisconnectProcessNodesCommand` · `ConfigureProcessNodeCommand` · `SelectProcessAssetCommand` · `ConfigureProcessAssetCommand` · `CreateCompositionCommand` · `ValidateCompositionCommand` · `ResolveDependencyCommand` · `ValidateProcessCommand` · `RunSimulationCommand` · `RequestOptimizationCommand` · `AttachPolicyCommand` · `ConfigureSLACommand` · `ConfigureKPICommand` · `ConfigureExceptionCommand` · `RequestReviewCommand` · `ApproveChangeCommand` · `RejectChangeCommand` · `GenerateDocumentationCommand` · `GenerateTestsCommand` · `CreateReleaseCandidateCommand` · `ValidateReleaseCommand` · `ApproveReleaseCommand` · `RejectReleaseCommand` · `GenerateProcessPackageCommand` · `PublishProcessPackageCommand` · `RequestDeploymentCommand` · `ApplyProcessComposerGateCommand`

(AI generation creates Draft only; deployment via P300/P259/P270; never direct production mutation.)

### Queries

`GetProcessDesignQuery` · `GetProcessModelQuery` · `GetProcessVersionQuery` · `GetProcessNodesQuery` · `GetProcessConnectionsQuery` · `GetProcessAssetsQuery` · `GetProcessDependenciesQuery` · `GetValidationResultQuery` · `GetSimulationResultQuery` · `GetOptimizationSuggestionsQuery` · `GetPolicyRequirementsQuery` · `GetProcessKPIQuery` · `GetProcessSLAQuery` · `GetProcessExceptionsQuery` · `GetProcessReviewsQuery` · `GetProcessChangeHistoryQuery` · `GetProcessDiffQuery` · `GetReleaseCandidateQuery` · `GetReleaseStatusQuery` · `GetProcessDocumentationQuery` · `GetGeneratedTestsQuery` · `GetProcessPackageQuery` · `GetDeploymentReadinessQuery`

Read models under `process_composer_operating_*` only; pagination mandatory.

## 13. MEOS Integration

| Peer | Mode |
|------|------|
| **P300** | Asset discovery · package publish — **never replace Marketplace** |
| **P299** | Performance/cost/risk/optimization predictions |
| **P298** | Consumes governed designs for adaptation |
| **P265 · P264 · P263** | Simulation · semantic graph · data contracts |
| **P260 · P266 · P261 · P257** | Configure refs only — peers execute |
| **P259 · P270** | Lifecycle activation · governance gates |
| **P297 · P258** | Human review · shell entry |
| **P294 / Notifications** | Review/release alerts — never send |
| **P302** | Process Testing / QA (delivered; distinct) |
| **P303** | Process Release / Deployment (delivered; distinct) |
| **P304** | Process Observability (delivered; distinct) |
| **P305** | Incident / Reliability (planned) |
| Observability · Documents · Feature Flags · Audit · Identity | MLT · document_id · progressive exposure · evidence · AuthZ |
| Core | Generic platform services |

Permissions: `process_composer_operating.design.*` · `process_composer_operating.canvas.*` · `process_composer_operating.composition.*` · `process_composer_operating.validation.*` · `process_composer_operating.simulation.*` · `process_composer_operating.release.*` · `process_composer_operating.collaboration.*` · `process_composer_operating.documentation.*` · `process_composer_operating.governance.*` · `process_composer_operating.ai.read` · `process_composer_operating.ai.infer`.

## 14. Implementation Roadmap

| Phase | Focus | Window | Deliverables |
|-------|-------|--------|--------------|
| **P301** | Foundation | — | ADR · capability · fabric · DDD/CQRS · API skeleton · dual tests |
| **Phase 1 / P301-A** | Process Canvas Foundation | 3–6 mo | Canvas · nodes · connections · zoom/pan · grouping · properties |
| **Phase 2 / P301-B** | Process Modeling | 6–12 mo | Events · tasks · decisions · human/agent tasks · exceptions · subprocess |
| **Phase 3 / P301-C** | Asset Composition | 9–15 mo | P300 integration · search · selection · config · dependency resolution |
| **Phase 4 / P301-D** | AI Process Engineering | 12–18 mo | NL design · AI generation · suggestions · explanation · duplication detection |
| **Phase 5 / P301-E** | Validation | 15–24 mo | Structural · contract · security · policy · dependency validation |
| **Phase 6 / P301-F** | Simulation | 18–30 mo | P265 · scenario · what-if · stress · failure testing |
| **Phase 7 / P301-G** | Intelligence | 24–36 mo | P299 · optimization · cost · SLA · risk · automation score |
| **Phase 8 / P301-H** | Governed Release | 30–42 mo | Review · approval · version · RC · certification · package |
| **Phase 9 / P301-I** | Enterprise Process Engineering | 36–48 mo | Multi-team collaboration · standards · reuse · industry templates · library |

Catalogs (planned): `docs/architecture/process_composer_operating/MEPCVA_*_{CAPABILITIES,DDD_CQRS,SECURITY,VALIDATION,ARCHITECTURE}.v1.yaml`

## 15. Quality Gates

- Never Visual Canvas / Modeling / Composition / Validation / Release Prep capabilities are missing
- Never Sibling Process Composer Operating BC (second deployable)
- Never Replace **P300** · **P299** · **P298** · **P260** · **P266** · **P261** · **P257** · **P259** · **P270** · Workflow · Core · AI
- Never Dual-write workflow/agent/decision/runtime tables · Never Local metrics/approval engines
- Never Become Workflow / Agent / Decision / Runtime / Governance / Intelligence / Marketplace / Transaction Engine
- Never Promote AI Draft Directly to Production · Never Bypass Governance Gate · Never Modify Production State Directly
- Never Module-Local LLM · Never Channel Delivery · Never Treat Simulation as Live Execution
- Versions immutable when released · Release candidates traceable · AI suggestions explainable · Designs audited
- Simulation ≠ execute · Prefer reuse via P300 · Human-in-the-Loop for sensitive nodes

Validate: Process composer OS · DDD · CQRS · events · P300/P260/P266/P259/P270 boundaries · portals · AI copilot.

## 16. Definition of Done

- [ ] ADR **658** accepted; capability `CAP-PLT-MEPCVA-001` registered
- [ ] Law + YAML catalogs under `docs/architecture/process_composer_operating/`
- [ ] Context `backend/contexts/process_composer_operating/` scaffolded
- [ ] Fabric wired + ACL to P300, P299, P265, P270, P259, P260, P266, Policy
- [ ] Outbox events + ACL stubs (P300 · P259 · P270 · P294 · P297 · P214-Z · Audit)
- [ ] Dual tests green; scorecard **ENTERPRISE_GRADE**
- [ ] OpenAPI `/api/v1/process-composer-operating*`
- [ ] Gated design→validate→simulate→govern→package path demonstrated (no direct production)
- [ ] **P301-A** unlocked · **P302** MEPQDV · **P303** MEPRED · **P304** MEPOCI · **P305** MEIRRE · **P306** MEESOP · **P307** MEKNOL · **P308** MEDCIM · **P309** MERILG · **P310** MEIGSI delivered · **P311** DLP / Information Protection / Adaptive Data Security Control series unblocked

**MEPCVA is complete when:** MEOS has a Visual Process Engineering / Low-Code Composition OS fabric; canvas, modeling, composition, AI draft design, validation, simulation coordination, collaboration and release preparation operate under gates; P300 remains marketplace; P260/P266/P261/P257 remain execution; P259 remains lifecycle; P270 remains governance; no process enters Production directly from P301; AI drafts remain Draft until governed; events join the Event Mesh — Governance Standard **11.0**.

**Architectural boundary guarantee:** MEPCVA must not re-own P257 Runtime, P259 Lifecycle, P260 Workflow, P261 Decision Execution, P266 Agent Orchestration, P270 Governance, P298 Adaptation, P299 Intelligence, P300 Marketplace. MEPCVA owns Visual Process Engineering, Process Composition, Low-Code/No-Code Design, Process Configuration, Design-Time Validation, Design-Time Simulation Coordination, Process Release Preparation, Process Package Generation and Process Engineering Experience only.

**Principle:** MEPCVA productizes design-time visual process engineering; it never replaces P300/P260/P266/P259/P270, never dual-writes peer execution tables, never embeds local LLMs, and never deploys processes without Validate → Simulate → Review → Govern → Package → P259 Lifecycle + Audit accountability.

---

**NEXT EXECUTION:** **P311** — MEOS Enterprise Data Loss Prevention, Information Protection & Adaptive Data Security Control Platform — convert P310 Classification/Sensitivity into operational Data Protection and DLP controls (Prevent / Allow / Block / Quarantine / Redact) under Policy + Context + Risk (federate P310, P268, P269, P270, P260; never fork Classification Intelligence or Cybersecurity; never create parallel mesh/content/records/workflow/agent engines).

> **P301 delivered:** this law · [ADR 658](../adr/658-meos-enterprise-process-composer-low-code-no-code-process-engineering-visual-automation-platform.md)
