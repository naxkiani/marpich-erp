# MEOS Enterprise Application Architecture, API Governance & Software Architecture Intelligence Platform (MEAAGSI)

**Status:** Normative (P289) — series foundation · **Productization & Experience Evolution Phase**  
**SoR:** `application_architecture_operating` · **ADR:** [646](../adr/646-meos-enterprise-application-architecture-api-governance-software-architecture-intelligence-platform.md) · **Capability:** `CAP-PLT-MEAAGSI-001`  
**Fabric:** `meos_enterprise_application_architecture_api_governance_software_architecture_intelligence_platform_framework` · **Governance Standard:** MEOS 11.0  
> **API:** `/api/v1/application-architecture-operating*` · **Builds on:** P288 MEDSSAD · P287 MECPEI · P286 MEITOI · P270 MEGRSC · P269 MEPCRI · P268 MECZTD · P267 MEAOSH · P266 MEAAOI · P265 MEDTIP · P264 MEKGSI · P263 MEDIMOP · P262 MEIAOI · P261 MEBRDI · P260 MEWEOP · P258 MESCC · P257 MERAF · P259 MDMAL · **Documents** · **Observability** · Policy · Workflow · Audit · P214-Z · **Next:** P289-A · **Peer series:** [P290 MEDAMIA](ENTERPRISE_MEOS_DATA_ARCHITECTURE_MASTER_DATA_INFORMATION_ARCHITECTURE_INTELLIGENCE_PLATFORM.md) (Enterprise Data / MDM / Information Architecture OS — never replace Application Architecture; never ungated data-model mutations; never replace P263 Data Mesh)  
**Hard bindings:** Inference → **P214-Z** · Secure delivery / SBOM / release security → **P288 `devsecops_operating`** (ACL; **P289 does not replace P288**) · Platform provision/deploy/env mapping → **P287** (ACL; never replace) · Runtime architecture signals / drift → **P286 + P257** (ACL) · Architecture KG projection → **P264** (ACL; never replace Knowledge Graph SoR) · Architecture twin / simulation → **P265** (ACL; **simulation ≠ execute**) · Data Mesh products → **P263** (ACL; **P289 ≠ P290**; never replace Data Mesh) · Cyber / trust boundaries → **P268** (ACL) · Privacy data-flow evidence → **P269** (ACL) · Architecture standards / exceptions → **P270** (ACL) · Architecture reviews / ADR approvals → **P260 / Workflow** (ACL; never local approval engines) · Architecture decisions → **P261** (ACL) · Agents → **P266** (ACL) · Autonomous architecture actions → **P267** (ACL; autonomy thresholds) · Experience Architecture Command Center → **P258** (ACL) · Application/API lifecycle → **P259** (ACL) · ADR/docs binaries → **Documents** (`document_id` only) · Policy / DoA / Autonomy / Architecture-as-Code → **Policy Engine** · Audit → **Audit** · AuthN/AuthZ → **Identity** · Generic → **Core**.

---

## 1. Header

**MARPICH ENTERPRISE PLATFORM (MEOS)** · Master Blueprint · Enterprise Architecture Governance Standard **11.0** · Prompt **P289** · MEOS Enterprise Application Architecture, API Governance & Software Architecture Intelligence Platform (**MEAAGSI**).  
**Platform Domain:** MEOS Enterprise Application Architecture, API Governance & Software Architecture Intelligence · **Capability Category:** Application Portfolio Architecture, Software Architecture Governance, API Architecture/Lifecycle/Governance, Microservice/Service Architecture, Application Dependency Mapping, Architecture Decision Records, Architecture Patterns, Technical Debt Intelligence, Architecture Risk, Application Modernization, Legacy Transformation, API Intelligence, Contract Governance, Service Catalog, Architecture Compliance/Fitness/Simulation, AI Architecture Copilot · **Strategic Layer:** MEOS Enterprise Architecture Intelligence Layer.

## 2. Prompt ID

**P289**

## 3. Mission

Create an Architecture Operating Layer that models, analyzes, governs, simulates and continuously optimizes:

```
Business Capability → Application → Service → API → Component → Dependency
→ Infrastructure → Deployment → Runtime
```

MEOS must know: which applications exist and which capabilities they support; services and APIs provided/consumed; dependencies; patterns; legacy footprint; technical debt; architecture risk; duplicate/obsolete APIs; excessive coupling; modernization candidates; ADRs; compliance with enterprise standards; and change impact of component modifications.

**Boundary law (hard):**
- **P287** = Cloud / Platform Engineering / Infrastructure Automation
- **P288** = DevSecOps / Secure Software Delivery
- **P289** = Application / Software Architecture / API Governance
- **P290** = Enterprise Data & Information Architecture (next; distinct from P263 Data Mesh)
- **P268 / P270 / P286 / P264 / P265** = Cyber · Governance · Ops · KG · Twin — federate, never replace

```
Business Capability → Application Portfolio → Application Architecture → Service Architecture
→ API Architecture → Dependency Graph → Architecture Assessment → Risk / Debt
→ Modernization → Governance → Continuous Architecture Intelligence
```

MEAAGSI owns **Application architecture operating fabric** (Architecture Command Center contracts, portfolio/API/dependency/debt/modernization/fitness workspace overlays, gated ADR/compliance/modernization intents); it does **not** replace DevSecOps, Platform Engineering, Data Mesh, Knowledge Graph, Governance or Core — and never converts architecture recommendations into autonomous production mutations outside Policy + Workflow + Delegation-of-Authority (+ human approval when above autonomy threshold) with **Evidence + Explainability + Verification + Audit**.

## 4. Architecture Principles

- Enterprise Architecture Governance Standard **11.0** (binding)
- DDD · CQRS · Event Sourcing · Event-Driven · Hexagonal · Clean · API-First
- Cloud Native · AI Native · Knowledge Graph Native · Digital Twin Native
- Metadata Driven · Configuration Driven · Policy Driven
- Zero Trust · Explainable AI · Responsible AI · Human Governance · Privacy By Design · Continuous Governance
- **Architecture as Code** · **Policy as Code** · **Contract First** · **Schema First**
- Versioned · Reproducible · Traceable Architecture Decisions
- Interoperability · Backward Compatibility · Loose Coupling · High Cohesion · Domain Boundary Enforcement
- Full Architecture Auditability
- Multi-tenant · Fail-closed authorization · Pagination mandatory
- Federate-by-contract only — never peer domain imports / shared tables / local LLM
- **P287 vs P288 vs P289 vs P263/P290:** never merge Platform Engineering, DevSecOps, Application Architecture, or Data Architecture SoRs
- Architecture Drift: Designed State vs Actual Runtime State must be detectable
- **No AI Agent may execute uncontrolled architecture mutations outside Policy + Delegation Authority**
- Twin simulation ≠ execute migration/decommission
- Architecture Recommendation → Autonomous Action only with Evidence + Policy + Risk + Explainability

## 5. Reference Architecture

```
Enterprise Architecture Experience (P258 Command Center · Portfolio · Application/API Workspaces · Dependency · ADR · Debt · Modernization · Fitness · Simulation · AI Copilot)
        ↓
┌────────────────────────────────────────────────────────────────────┐
│ Application Architecture Operating Fabric                          │
│ (SoR application_architecture_operating)                           │
│ schema: application_architecture_operating_*                       │
└────────────────────────────────────────────────────────────────────┘
        ↓ ACL              ↓ ACL              ↓ ACL
 P288 Secure Delivery  P287 Deploy/Env     P264 KG · P265 Twin · P286 Runtime · P270 Governance
        ↓
 Architecture Core overlays · Governance & Control (API · service · pattern · deprecation · exception)
        ↓
 Foundation: P266 Agents · P261 Decision · P260 Workflow · P259 Lifecycle · P257 Runtime
```

| Layer | Role |
|-------|------|
| Enterprise Architecture Experience | Command Center · Portfolio · Workspaces · Debt/Modernization/Fitness/Simulation · AI Copilot |
| Architecture Intelligence | Application · Service · API · Dependency · Risk · Debt · Modernization · Compliance · Fitness · Change Impact · Simulation |
| Architecture Core | Application · Capability · Service · Component · API · Contract · Event · DataFlow · Dependency · Pattern · Decision · Rule · Version · Debt · Risk · ModernizationPlan · Assessment |
| Governance & Control | Architecture/API/Service/Security/Data policies · Technology/Pattern standards · Version/Deprecation/Exception policies |
| MEOS Foundation | P257–P270 · P286–P288 |

## 6. Core Capabilities

| ID | Capability |
|----|------------|
| MEAAGSI-C01 | Architecture Command Center |
| MEAAGSI-C02 | Application Portfolio Architecture · Capability Mapping |
| MEAAGSI-C03 | Application Architecture Modeling · Software Architecture Governance |
| MEAAGSI-C04 | Architecture Pattern Registry |
| MEAAGSI-C05 | API Architecture · Lifecycle · Governance · Contract Governance |
| MEAAGSI-C06 | Microservice / Service Architecture Governance |
| MEAAGSI-C07 | Application Dependency Mapping · Architecture Knowledge Graph (P264) |
| MEAAGSI-C08 | Architecture Decision Records |
| MEAAGSI-C09 | Technical Debt Intelligence · Architecture Risk Intelligence |
| MEAAGSI-C10 | Architecture Fitness · Architecture Compliance |
| MEAAGSI-C11 | Change Impact Intelligence |
| MEAAGSI-C12 | Application Modernization · Legacy Transformation |
| MEAAGSI-C13 | Architecture Simulation (P265) |
| MEAAGSI-C14 | AI Architecture Copilot + MEAAGSI Governance Kernel |

### Notes

Application lifecycle: Proposed → Designed → Approved → Developed → Production → Modernization → Retirement.  
API lifecycle: Design → Review → Approve → Develop → Test → Secure → Publish → Consume → Monitor → Version → Deprecate → Retire.  
Compliance results: COMPLIANT · NON_COMPLIANT · WARNING · EXCEPTION_REQUIRED.  
Modernization strategies: Rehost · Replatform · Refactor · Rearchitect · Replace · Retire · Strangler.  
Debt model: Debt + Impact + Interest + Risk + Remediation Cost → Priority.  
Fitness dimensions: Modularity · Scalability · Security · Reliability · Maintainability · Performance · Interoperability · Observability · Testability · Deployability.

## 7. User Experience Architecture

```
Architect / API Owner / Platform Lead → Architecture Command Center → Portfolio / Application / API
→ Dependency Explorer → ADR / Debt / Modernization / Fitness / Simulation → AI Copilot
```

Workspaces: Application Portfolio · Application Architecture · API Catalog/Workspace · Dependency Explorer · Architecture Decision Center · Technical Debt · Modernization · Fitness · Simulation.  
AI Copilot: *"Should I convert this Application to Microservices or Modular Monolith?"* → Domain · Team · Complexity · Scaling · Cost · Coupling · Risk → Compare Options → Recommendation → Evidence → ADR Proposal.

## 8. Application Runtime Model

```
Architecture Definition → Validation → Registration → Governance → Runtime Mapping
→ Observation → Assessment → Optimization
```

ArchitectureRuntimeInstance: Application · ArchitectureVersion · Services · APIs · Components · Dependencies · DataFlows · Events · Policies · Risks · TechnicalDebt · FitnessScore · ComplianceState · Decisions · ModernizationState · AuditHistory.

Activation: Domain Registered → Portfolio Loaded → Metadata → API/Service Registry → KG → Policy → Risk → Twin → Analytics → AI Agents.

## 9. AI Agents

| Agent | Role | Gate |
|-------|------|------|
| Application Architecture Agent | Analyze apps · risks · improvements | Explainability · Audit |
| API Architecture Agent | Contracts · improvements | Policy |
| Dependency Intelligence Agent | Coupling · circular deps | Evidence |
| Architecture Governance Agent | Standards · violations · exceptions | Workflow · P270 |
| Technical Debt Agent | Detect · impact · prioritize | Non-actuating default |
| Modernization Agent | Legacy · target · migration strategy | DoA for execution |
| Change Impact Agent | Impact radius · critical consumers | Evidence |
| API Lifecycle Agent | Usage · obsolete · deprecation recommend | Policy |
| Architecture Fitness Agent | Fitness · degradation · corrective recommend | Audit |
| Architecture Simulation Agent | Simulate changes · compare options | P265 · simulation ≠ execute |
| Architecture Copilot Agent | Explain · propose · generate ADR | Human governance |
| Architecture Orchestrator Agent | Coordinate · evidence · policy · explainability | No uncontrolled mutation |

**Law:** Agents recommend; material architecture mutations/migrations via Policy + Workflow + Human DoA (or Autonomy Threshold) + Verification + Audit. Never module-local LLM. Simulation ≠ execute.

## 10. Domain Driven Design (DDD)

**Core domain:** MEOS Enterprise Application Architecture, API Governance & Software Architecture Intelligence (operating)  
**Strategic type:** Supporting Domain (platform / architecture intelligence)

### Bounded Contexts (logical; single SoR `application_architecture_operating`)

| BC | Name | Aggregate root |
|----|------|----------------|
| BC-01 | Application Portfolio Operating | `ApplicationCampaignAggregate` |
| BC-02 | Software / Service Architecture Operating | `ArchitectureCampaignAggregate` |
| BC-03 | API Governance Operating | `APICampaignAggregate` |
| BC-04 | Dependency / Impact Operating | `DependencyGraphCampaignAggregate` |
| BC-05 | Decision / Debt / Risk / Fitness Operating | `ArchitectureDecisionCampaignAggregate` |
| BC-06 | Modernization / Simulation / Compliance Operating | `ModernizationCampaignAggregate` |

### Aggregates

**Application:** BusinessCapabilities · Architecture · Services · APIs · Components · Dependencies · Risks · TechnicalDebt · Lifecycle  
**Architecture:** Components · Services · APIs · Events · DataFlows · Patterns · Policies · Version  
**API:** Endpoints · Contracts · Schemas · Versions · Consumers · Policies · Lifecycle  
**DependencyGraph:** Nodes · Relationships · CriticalPaths · Risks · ImpactModels  
**ArchitectureDecision:** Context · Options · Evaluation · Decision · Consequences · Approval · Review  
**TechnicalDebt:** Category · Impact · Interest · Risk · Remediation · History  
**ModernizationPlan:** SourceApplication · TargetArchitecture · MigrationStrategy · MigrationSteps · Risks · Dependencies · Progress

### Value Objects

`ArchitectureVersionId` · `APIContractVersionId` · `PatternId` · `FitnessScore` · `DebtInterest` · `ImpactRadius` · `ComplianceVerdict` · `AutonomyThreshold` · `DoAThreshold` · `ExplainabilityTraceRef` · `DocumentIdRef` · `PeerAssetRef` · `TenantScope`

### Domain Services

`ApplicationArchitectureService` · `ApplicationPortfolioService` · `SoftwareArchitectureService` · `ArchitectureGovernanceService` · `ServiceArchitectureService` · `APIGovernanceService` · `APILifecycleService` · `APIContractService` · `DependencyMappingService` · `DependencyImpactService` · `ArchitectureDecisionService` · `TechnicalDebtService` · `ArchitectureRiskService` · `ArchitectureFitnessService` · `ModernizationService` · `LegacyTransformationService` · `ArchitectureSimulationService` · `ArchitectureComplianceService` · `ArchitectureIntelligenceService` · `ArchitectureExplainabilityService`

**Hard separation:** Secure delivery in P288; deploy/env in P287; data products/mesh in P263; data architecture OS in P290 (planned); MEAAGSI stores architecture campaigns, API/contract overlays, debt/modernization plans and peer refs only.

## 11. Event Architecture

### Domain Events

`ApplicationRegistered` · `ApplicationArchitectureCreated` · `ApplicationArchitectureUpdated` · `ArchitectureVersionCreated` · `ArchitecturePatternApplied` · `ArchitecturePatternViolationDetected` · `ArchitecturePolicyViolationDetected` · `ServiceRegistered` · `ServiceBoundaryDefined` · `ServiceDependencyCreated` · `ServiceDependencyChanged` · `CircularDependencyDetected` · `APICreated` · `APIUpdated` · `APIVersionCreated` · `APIContractCreated` · `APIContractChanged` · `APIBreakingChangeDetected` · `APIConsumerRegistered` · `APIDeprecated` · `APIRetired` · `ArchitectureDecisionCreated` · `ArchitectureDecisionApproved` · `ArchitectureDecisionSuperseded` · `TechnicalDebtDetected` · `TechnicalDebtReassessed` · `TechnicalDebtPrioritized` · `ModernizationCandidateIdentified` · `ModernizationPlanCreated` · `MigrationStarted` · `MigrationCompleted` · `ArchitectureRiskDetected` · `ArchitectureRiskChanged` · `ArchitectureFitnessAssessed` · `ArchitectureFitnessDegraded` · `ArchitectureCompliancePassed` · `ArchitectureComplianceFailed` · `ArchitectureSimulationStarted` · `ArchitectureSimulationCompleted` · `ChangeImpactCalculated` · `ArchitectureRecommendationGenerated` · `ArchitectureDriftDetected` · `ArchitectureGateApplied`

### Event Flow

`Business Capability → Application → Architecture → Service → API → Dependency → Assessment → Risk/Debt → Decision → Modernization → Runtime`  
Subscribers: P257 · P258 · P259 · P260 · P261 · P262 · P263 · P264 · P265 · P266 · P267 · P268 · P269 · P270 · P286 · P287 · P288 · Audit · Observability

Envelope + outbox + idempotent ACL consumers mandatory. Decision/migration events carry policy + risk + approval + evidence refs.

## 12. CQRS

### Commands

`RegisterApplicationCommand` · `CreateArchitectureCommand` · `UpdateArchitectureCommand` · `CreateArchitectureVersionCommand` · `ApplyArchitecturePatternCommand` · `RegisterServiceCommand` · `DefineServiceBoundaryCommand` · `RegisterAPICommand` · `CreateAPIContractCommand` · `CreateAPIVersionCommand` · `DeprecateAPICommand` · `RetireAPICommand` · `RegisterDependencyCommand` · `AnalyzeDependencyCommand` · `CreateArchitectureDecisionCommand` · `ApproveArchitectureDecisionCommand` · `RecordTechnicalDebtCommand` · `PrioritizeTechnicalDebtCommand` · `CreateRemediationPlanCommand` · `CreateModernizationCandidateCommand` · `CreateModernizationPlanCommand` · `ExecuteMigrationStepCommand` · `AssessArchitectureRiskCommand` · `AssessArchitectureFitnessCommand` · `EvaluateArchitectureComplianceCommand` · `RunArchitectureSimulationCommand` · `CalculateChangeImpactCommand` · `GenerateArchitectureRecommendationCommand` · `ApplyArchitectureGateCommand`

(Authoritative migrations/decommissions via Workflow + peer deploy/security ACLs — never uncontrolled agent mutations.)

### Queries

`GetApplicationQuery` · `GetApplicationPortfolioQuery` · `GetApplicationArchitectureQuery` · `GetArchitectureVersionQuery` · `GetServiceQuery` · `GetServiceDependenciesQuery` · `GetAPIQuery` · `GetAPIContractQuery` · `GetAPIConsumersQuery` · `GetAPIVersionsQuery` · `GetDependencyGraphQuery` · `GetImpactAnalysisQuery` · `GetArchitectureDecisionQuery` · `GetTechnicalDebtQuery` · `GetTechnicalDebtByApplicationQuery` · `GetModernizationCandidateQuery` · `GetModernizationPlanQuery` · `GetArchitectureRiskQuery` · `GetArchitectureFitnessQuery` · `GetArchitectureComplianceQuery` · `GetArchitecturePatternQuery` · `GetArchitectureSimulationQuery` · `GetArchitectureRecommendationQuery`

Read models under `application_architecture_operating_*` only; pagination mandatory.

## 13. MEOS Integration

| Peer | Mode |
|------|------|
| **P288 MEDSSAD** | Secure delivery info · release/artifact security context — **never replace** |
| **P287 MECPEI** | Deployment · environment · infrastructure mapping |
| **P286 MEITOI** | Runtime telemetry → architecture reality / drift |
| **P264 · P265** | Architecture KG · twin simulation |
| **P263** | Architecture data products — **never replace Data Mesh; P290 owns data architecture OS** |
| **P268 · P269 · P270** | Trust boundaries · privacy data flows · architecture standards/exceptions |
| **P259 · P260 · P261 · P257–P258** | Lifecycle · review workflow · decisions · runtime · command center |
| **P266 · P267** | Agents · gated autonomous architecture actions |
| Policy · Audit · Identity · Documents | Architecture-as-Code · evidence · authority · ADR docs |
| **P290 MEDAMIA** | Enterprise Data / MDM / Information Architecture OS — **never replace Application Architecture; never replace P263; never ungated data-model mutations** |
| Core | Generic platform services |

Permissions: `application_architecture_operating.portfolio.*` · `application_architecture_operating.architecture.*` · `application_architecture_operating.api.*` · `application_architecture_operating.dependency.*` · `application_architecture_operating.decision.*` · `application_architecture_operating.debt.*` · `application_architecture_operating.modernization.*` · `application_architecture_operating.governance.*` · `application_architecture_operating.ai.read` · `application_architecture_operating.ai.infer`.

## 14. Implementation Roadmap

| Phase | Focus | Window | Deliverables |
|-------|-------|--------|--------------|
| **P289** | Foundation | — | ADR · capability · fabric · DDD/CQRS · API skeleton · dual tests |
| **Phase 1 / P289-A** | Application Architecture Foundation | 3–6 mo | Portfolio · capability mapping · registries · dependency mapping · policies |
| **Phase 2 / P289-B** | API & Service Governance | 6–12 mo | API catalog · lifecycle · contracts · schema · versioning · consumer/provider · microservice governance |
| **Phase 3 / P289-C** | Architecture Intelligence | 12–18 mo | Debt · risk · fitness · change impact · compliance · KG · AI Copilot |
| **Phase 4 / P289-D** | Modernization & Simulation | 18–36 mo | Legacy assessment · modernization · migration planning · twin simulation · gated autonomous recommendations |

Catalogs (planned): `docs/architecture/application_architecture_operating/MEAAGSI_*_{CAPABILITIES,DDD_CQRS,SECURITY,VALIDATION,ARCHITECTURE}.v1.yaml`

## 15. Quality Gates

- Never Enterprise Application Portfolio / API Catalog / ADR / Debt / Fitness capabilities are missing
- Never Versioned Architecture Models missing
- Never Sibling Application Architecture Operating BC (second deployable)
- Never Replace **P288** · **P287** · **P286** · **P264** · **P263** · **P270** · Workflow · Core · AI
- Never Fork DevSecOps / Platform Engineering / Cyber / Data Mesh APIs
- Never Local approval engines · Never Ungated Architecture Mutations · Never Bypass Architecture Policy
- Never Module-Local LLM · Never Treat Twin Scenario as Executed Migration
- Breaking API changes detectable · Architecture violations detectable · Designed vs Runtime drift detectable
- Recommendation → Autonomous Action only with Evidence + Policy + Risk + Explainability
- Explainable · Evidence-based · Confidence · Human governance · Decision traceability

Validate: architecture OS · DDD · CQRS · events · P287/P288/P263 boundaries · workspaces · AI copilot.

## 16. Definition of Done

- [ ] ADR **646** accepted; capability `CAP-PLT-MEAAGSI-001` registered
- [ ] Law + YAML catalogs under `docs/architecture/application_architecture_operating/`
- [ ] Context `backend/contexts/application_architecture_operating/` scaffolded
- [ ] Fabric wired + ACL to P288, P287, P286, P264, P265, P270, Workflow, Policy
- [ ] Outbox events + ACL stubs (P288 · P287 · P286 · P264 · P265 · P270 · Workflow · P266 · P214-Z · Audit)
- [ ] Dual tests green; scorecard **ENTERPRISE_GRADE**
- [ ] OpenAPI `/api/v1/application-architecture-operating*`
- [ ] Versioned architecture + gated ADR/compliance path demonstrated
- [ ] **P289-A** unlocked · **P290** Data Architecture / MDM / Information Architecture series delivered (ADR 647)

**MEAAGSI is complete when:** MEOS has an Enterprise Architecture Intelligence OS fabric; portfolio, capability mapping, API lifecycle/contracts, dependency graph, ADRs, debt, risk, fitness, compliance, change impact, modernization and simulation operate under gates; every Application connects Capability→Domain→Service→API→Component→Data→Infrastructure→Deployment→Runtime; every API has Owner+Contract+Version+Consumers+Security+Lifecycle+Risk; designed vs runtime drift is detectable; agents participate within autonomy thresholds; P287/P288/P263 boundaries preserved; no architecture recommendation becomes autonomous action without Evidence+Policy+Risk+Explainability; events join the Event Mesh — Governance Standard **11.0**.

**Principle:** MEAAGSI productizes application/software architecture and API governance intelligence; it never replaces P288, P287, P263 or P270, never embeds local approval engines, and never executes material architecture mutations without Policy + Delegation + Workflow + Verification + Audit accountability.

---

**NEXT EXECUTION:** **P311** — MEOS Enterprise Data Loss Prevention, Information Protection & Adaptive Data Security Control Platform — convert P310 Classification/Sensitivity into operational Data Protection and DLP controls (Prevent / Allow / Block / Quarantine / Redact) under Policy + Context + Risk (federate P310, P268, P269, P270, P260; never fork Classification Intelligence or Cybersecurity; never create parallel mesh/content/records/workflow/agent engines).

> **P291 delivered:** [MEIEII law](ENTERPRISE_MEOS_INTEGRATION_ARCHITECTURE_EVENT_MESH_INTEROPERABILITY_INTELLIGENCE_PLATFORM.md) · [ADR 648](../adr/648-meos-enterprise-integration-architecture-event-mesh-interoperability-intelligence-platform.md)
