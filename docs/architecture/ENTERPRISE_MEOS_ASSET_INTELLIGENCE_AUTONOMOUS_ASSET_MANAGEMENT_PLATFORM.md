# MEOS Enterprise Asset Intelligence & Autonomous Asset Management Platform (MEAIAMP)

**Status:** Normative (P275) — series foundation · **Productization & Experience Evolution Phase**  
**SoR:** `enterprise_asset_operating` · **ADR:** [632](../adr/632-meos-enterprise-asset-intelligence-autonomous-asset-management-platform.md) · **Capability:** `CAP-PLT-MEAIAMP-001`  
**Fabric:** `meos_enterprise_asset_intelligence_autonomous_asset_management_platform_framework` · **Governance Standard:** MEOS 11.0  
> **API:** `/api/v1/enterprise-asset-operating*` · **Builds on:** P274 MEHCAWP · P273 MECXARP · P272 MESCIAL · P271 MEFIAF · P270 MEGRSC · P269 MEPCRI · P268 MECZTD · P267 MEAOSH · P266 MEAAOI · P265 MEDTIP · P264 MEKGSI · P263 MEDIMOP · P262 MEIAOI · P261 MEBRDI · P260 MEWEOP · P258 MESCC · P257 MERAF · P259 MDMAL · [P236 EAMII](ENTERPRISE_AUTONOMOUS_MANUFACTURING_INDUSTRIAL_INTELLIGENCE_PLATFORM.md) · [P227 EDTISP](ENTERPRISE_DIGITAL_TWIN_INTELLIGENCE_SIMULATION_PLATFORM.md) · Inventory · Warehouse · Facility peers · P216 Robotics · Integration · Policy · Workflow · Audit · P214-Z · **Next:** P275-A · **Peer series:** [P276 MEPIASP](ENTERPRISE_MEOS_PROCUREMENT_INTELLIGENCE_AUTONOMOUS_SOURCING_PLATFORM.md) (Source-to-Pay OS — never fork supply-network or dual-write PO ledgers) · [P277 MESIARO](ENTERPRISE_MEOS_SALES_INTELLIGENCE_AUTONOMOUS_REVENUE_OPERATIONS_PLATFORM.md) (Sales/RevOps — installed-base / upgrade / replacement opportunity signals)  
**Hard bindings:** Inference → **P214-Z** · Manufacturing/industrial intel (incl. PdM depth) → **P236 `manufacturing_intelligence`** (ACL; never replace `/api/v1/manufacturing-intelligence*`) · Twin fabric → **P227 / P265** (ACL; never replace `/api/v1/digital-twin*` or `/api/v1/twin-intelligence*`; simulation ≠ actuate) · Stock/spare parts truth → **inventory / warehouse** (ACL; never dual-write stock) · Facility/building peers → facility SoRs when present (ACL) · Physical/OT actuation → **Manufacturing / Robotics (P216) / owning OT SoRs** via Workflow — **never ungated** · Technician matching → **P274** (ACL) · Parts demand → **P272 / procurement** (ACL) · CAPEX/OPEX/TCO → **P271 / Financial Kernel** (ACL) · Cyber-physical security → **P268** (ACL) · Ops healing handoff → **P267 / P225** (ACL) · IoT/telemetry vendors → **Integration Platform** (never vendor SDKs in domain) · Decisions → **P261 / P224** (ACL) · Maintenance workflows → **P260 / Workflow** (ACL) · Agents → **P266** (ACL) · Experience Asset Command Center → **P258** (ACL) · Policy → **Policy Engine** · Audit → **Audit** · AuthN/AuthZ → **Identity** · Generic → **Core**.

---

## 1. Header

**MARPICH ENTERPRISE PLATFORM (MEOS)** · Master Blueprint · Enterprise Architecture Governance Standard **11.0** · Prompt **P275** · MEOS Enterprise Asset Intelligence & Autonomous Asset Management Platform (**MEAIAMP**).  
**Platform Domain:** MEOS Enterprise Asset Intelligence & Asset Operations Ecosystem · **Capability Category:** Asset 360, Asset Registry, Asset Lifecycle Management, Predictive Maintenance, IoT Intelligence, Digital Asset Twin, Field Service, Asset Risk Intelligence & Autonomous Asset Operations · **Strategic Layer:** MEOS Enterprise Asset & Physical Operations Layer.

## 2. Prompt ID

**P275**

## 3. Mission

Deliver the central Asset Intelligence productization layer for the full lifecycle of physical, digital and operational enterprise assets — from register and deploy through monitor, maintain, repair, optimize, transfer and retire.

```
Traditional Asset Management → Connected Asset Intelligence
→ Predictive Asset Operations → Autonomous Asset Management
```

**Goal:** Transform Reactive Asset Maintenance into an **AI-Native Autonomous Asset Operating System**.

Missions: Enterprise Asset 360 · Asset Registry Intelligence · Asset Lifecycle Management · Asset Performance Management · Predictive Maintenance · Condition Monitoring · IoT Asset Intelligence · Field Service Intelligence · Asset Cost Intelligence · Asset Risk Intelligence · Digital Asset Twin · Autonomous Asset Operations (gated).

```
Asset Signals → Asset 360 → Condition Intelligence → Predictive Analytics
→ Risk Assessment → Maintenance Decision → Workflow Execution
→ Asset Optimization → Continuous Learning
```

MEAIAMP owns **enterprise asset operating fabric** (Asset Command Center contracts, Asset 360 / maintenance / field-service workspace overlays, health/PdM/risk/TCO campaigns, gated work-order and optimization intents); it does **not** replace P236, P227/P265, inventory, manufacturing/OT SoRs or Core — and never actuates physical equipment, isolates devices, or mutates stock/asset ledgers without owning peer APIs + Policy + Workflow (+ human authority for critical/safety classes).

## 4. Architecture Principles

- Enterprise Architecture Governance Standard **11.0** (binding)
- DDD · CQRS · Event Sourcing · Event-Driven · Hexagonal · Clean · API-First
- Cloud Native · AI Native · Knowledge Graph Native · Digital Twin Native · **IoT Native**
- Metadata Driven · Configuration Driven · Policy Driven
- Zero Trust · Explainable AI · Responsible AI · Human Governance
- **Privacy By Design** · **Predictive Operations** · **Continuous Asset Governance**
- Multi-tenant · Fail-closed authorization · Pagination mandatory
- Federate-by-contract only — never peer domain imports / shared tables / local LLM
- **P236 vs MEAIAMP:** P236 = manufacturing/industrial intel SoR; MEAIAMP = Enterprise Asset OS productization across asset classes — never fork `/api/v1/manufacturing-intelligence*`
- **P265/P227:** twin simulation only; never treat twin as production actuate
- Critical autonomous actions: Policy + Risk Threshold + Human Governance + Auditability
- IoT/edge/OT vendors only via Integration Platform — never vendor SDKs in domain
- Cyber-physical: device identity, secure telemetry, threat monitoring via P268
- No silent block/isolate/actuate without audit trail

## 5. Reference Architecture

```
Asset Experience (P258 Command Center · Asset 360 · Maintenance · Field Service · Performance · AI Assistant)
        ↓
┌──────────────────────────────────────────────────────────────┐
│ Enterprise Asset Operating Fabric (SoR enterprise_asset_operating)│
│ Registry/lifecycle/health/PdM/field/risk/TCO campaigns       │
│ schema: enterprise_asset_operating_*                         │
└──────────────────────────────────────────────────────────────┘
        ↓ ACL                         ↓ ACL                    ↓ ACL
 P236 Manufacturing Intel        P227/P265 Twin            inventory / OT peers
        ↓
 Connected Asset Layer (IoT via Integration) · Digital Asset Twin overlays
        ↓
 Foundation: P266 Agents · P264 KG · P263 Mesh · P260 Workflow · P267 Ops · P274 Workforce · P272 Supply · P271 Finance · P268 Cyber
```

| Layer | Role |
|-------|------|
| Asset Experience | Command Center · 360 · Maintenance · Field Service · Performance · AI Assistant |
| Asset Intelligence Engine | Health · PdM · Condition · Risk · Performance optimization overlays |
| Asset Management Core | Registry · Lifecycle · Maintenance · Work Orders · Field · Cost (via peers) |
| Connected Asset | IoT · Telemetry · Edge · Industrial systems (Integration) |
| Digital Asset Twin | State · Behavior · Simulation · Scenarios (P265/P227) |
| Intelligence Foundation | Agents · KG · Mesh · Workflow · Decision · Autonomy |

## 6. Core Capabilities

| ID | Capability |
|----|------------|
| MEAIAMP-C01 | Enterprise Asset 360 |
| MEAIAMP-C02 | Enterprise Asset Registry |
| MEAIAMP-C03 | Asset Lifecycle Management |
| MEAIAMP-C04 | Asset Performance Management |
| MEAIAMP-C05 | Predictive Maintenance Intelligence |
| MEAIAMP-C06 | Condition Monitoring Intelligence |
| MEAIAMP-C07 | IoT Asset Intelligence (Integration-gated) |
| MEAIAMP-C08 | Field Service Intelligence |
| MEAIAMP-C09 | Asset Cost / TCO Intelligence |
| MEAIAMP-C10 | Asset Risk Intelligence |
| MEAIAMP-C11 | Digital Asset Twin federation |
| MEAIAMP-C12 | Autonomous Asset Operations (gated) + MEAIAMP Governance Kernel |

### Notes

Asset 360 Model: Identity + Location + Ownership + Financial + Operational + Condition + Maintenance + Risk → Asset Intelligence Profile.  
Registry categories: Physical · Infrastructure · Industrial · IT · Digital · Vehicles · Equipment · Facilities · Energy · Strategic.  
Lifecycle: Register → Classify → Assign → Activate → Operate → Maintain → Optimize → Retire.  
PdM: Telemetry → Condition → Failure Prediction → RUL → Recommendation → Work Order (gated).  
Field service: Issue → Diagnosis → Technician Match (P274) → Parts (P272) → Dispatch → Repair → Verification → Closure.  
TCO: Acquisition + Operation + Maintenance + Downtime + Disposal.  
Critical actions: Policy + Risk Threshold + Human Governance + Auditability.

## 7. User Experience Architecture

```
Asset Manager / Engineer / Operator → Asset Command Center → Asset 360
→ Asset Health → AI Insight → Decision → Work Order / Action (gated) → Outcome
```

Command Center: Asset Health · Critical Assets · Availability · Maintenance Due · Failure Predictions · Risk · Utilization · Cost · AI Recommendations.  
Asset 360: Identity · Location · Ownership · Status · Financial Value · Condition · Maintenance History · Dependencies · Risk · Digital Twin.  
Maintenance Workspace: Queue · Predictive Alerts · Work Orders · Technician Assignment · Parts · SLA · History.  
Field Service Workspace: Technician Map · Work Orders · Asset Context · Route · Skills · Parts · Mobile Execution.  
AI Assistant: *"Which critical assets are most likely to fail in the next 30 days?"* → Telemetry → History → KG → Prediction → Risk → Explain → Recommend plan.

## 8. Application Runtime Model

```
Asset Event → Telemetry / Op Signal → Context Enrichment → AI Analysis
→ Condition Assessment → Risk Prediction → Maintenance Decision → Workflow
→ Execution → Verification → Learning
```

AssetIntelligenceInstance: AssetIdentity · AssetType · Location · Ownership · OperationalState · ConditionState · PerformanceState · MaintenanceState · RiskState · FinancialState · DigitalTwinReference · RecommendedActions · AuditHistory.

Activation: Domain Registered → Metadata → Policy → Permissions → Runtime Activated → Command Center → IoT/Event Streams → Twin → Agents.

## 9. AI Agents

| Agent | Role | Gate |
|-------|------|------|
| Asset Intelligence Agent | Signals · health · operational changes | Explainability · Audit |
| Predictive Maintenance Agent | Failures · RUL · maintenance recommend | Workflow · human for critical |
| Condition Monitoring Agent | Telemetry · anomalies · alert correlation | Non-actuating default |
| Field Service Agent | Technician match · dispatch · work orders | P274 ACL · Workflow |
| Asset Optimization Agent | Utilization · downtime · performance | Gated execute |
| Asset Lifecycle Agent | Lifecycle · replacement · upgrade/retire recommend | Human for material CAPEX |
| Asset Risk Agent | Risk · impact · mitigation | P270 ACL · Policy |

**Law:** Agents recommend; actuate/dispatch/isolate via owning OT/peer SoRs + Workflow + Policy. Never module-local LLM. Never ungated physical actuation. Twin sim ≠ execute.

## 10. Domain Driven Design (DDD)

**Core domain:** MEOS Enterprise Asset Intelligence & Autonomous Asset Management (operating)  
**Strategic type:** Supporting Domain (platform / physical operations operating layer)

### Bounded Contexts (logical; single SoR `enterprise_asset_operating`)

| BC | Name | Aggregate root |
|----|------|----------------|
| BC-01 | Asset Registry Operating | `AssetRegistryCampaignAggregate` |
| BC-02 | Asset Lifecycle Operating | `AssetLifecycleCampaignAggregate` |
| BC-03 | Maintenance Operating | `MaintenanceCampaignAggregate` |
| BC-04 | Asset Condition Operating | `ConditionMonitoringCampaignAggregate` |
| BC-05 | Field Service Operating | `FieldServiceCampaignAggregate` |
| BC-06 | Performance / Risk / Twin Operating | `AssetIntelligenceCampaignAggregate` |

### Aggregates

**Asset (operating projection):** Identity · Type · Location · Ownership · OperationalState · Condition · Maintenance · History  
**MaintenancePlan (operating):** Asset · Schedule · WorkOrders · Resources · Parts · History  
**WorkOrder (operating):** Asset · Issue · Priority · Technician · Parts · Actions · Verification · Closure  
**AssetTwin (operating ref):** State · Behavior · Dependencies · Telemetry · Simulation · History (truth in P227/P265)

### Value Objects

`AssetHealthScore` · `AssetPerformanceScore` · `RemainingUsefulLife` · `AssetRiskScore` · `TCOSnapshot` · `ExplainabilityTraceRef` · `PeerAssetId` · `PeerWorkOrderId` · `PeerTwinId` · `TenantScope`

### Domain Services

`AssetRegistryService` · `AssetLifecycleService` · `AssetHealthService` · `PredictiveMaintenanceService` · `ConditionMonitoringService` · `FieldServiceOptimizationService` (ACL) · `AssetPerformanceService` · `AssetCostService` (ACL) · `AssetRiskService` · `DigitalTwinService` (ACL) · `EnterpriseAssetGovernanceEngine` · `AssetExplainabilityService`

**Hard separation:** Manufacturing PdM catalog in P236; twin models in P227/P265; stock/parts in inventory; OT actuation in manufacturing/robotics. MEAIAMP stores operating campaigns, registry overlays and peer refs only.

## 11. Event Architecture

### Domain Events

`AssetRegistered` · `AssetClassified` · `AssetCommissioned` · `AssetActivated` · `AssetStateChanged` · `TelemetryReceived` · `ConditionChanged` · `AnomalyDetected` · `AssetHealthDegraded` · `FailurePredicted` · `MaintenanceDue` · `MaintenanceTriggered` · `WorkOrderCreated` · `TechnicianAssigned` · `ServiceStarted` · `ServiceCompleted` · `AssetRecovered` · `AssetPerformanceChanged` · `AssetRiskDetected` · `AssetReplacementRecommended` · `AssetRetired` · `AssetGateApplied`

### Event Flow

`Asset Signal → Event Processing → Context → Condition Intelligence → AI Analysis → Risk/Prediction → Decision → Maintenance Workflow → Field Execution → Verification → Asset State Update`  
Subscribers: Workflow · Decision · AI Agents · Analytics · KG · Twin · Autonomous Ops · Finance · Supply · Governance · Audit

Envelope + outbox + idempotent ACL consumers mandatory.

## 12. CQRS

### Commands

`RegisterAssetCommand` · `ClassifyAssetCommand` · `ActivateAssetCommand` · `UpdateAssetStateCommand` · `RecordTelemetryCommand` · `CreateMaintenancePlanCommand` · `CreateWorkOrderCommand` · `AssignTechnicianCommand` · `ScheduleMaintenanceCommand` · `TriggerPredictiveMaintenanceCommand` · `OptimizeAssetCommand` · `RecommendReplacementCommand` · `RetireAssetCommand` · `ApplyAssetGateCommand`

(Canonical stock/OT/twin mutations via peer SoR ACL.)

### Queries

`GetAsset360Query` · `GetAssetHealthQuery` · `GetAssetPerformanceQuery` · `GetAssetConditionQuery` · `GetMaintenanceStatusQuery` · `GetFailurePredictionQuery` · `GetRemainingUsefulLifeQuery` · `GetAssetRiskQuery` · `GetFieldServiceStatusQuery` · `GetAssetCostQuery` · `GetAssetTwinQuery`

Read models under `enterprise_asset_operating_*` only; pagination mandatory; live twin/stock/OT truth via peers.

## 13. MEOS Integration

| Peer | Mode |
|------|------|
| P236 EAMII | Manufacturing/industrial intel / PdM depth — **never replace** |
| P227 · **P265** | Digital twin — simulation ≠ actuate |
| inventory · warehouse | Spare parts / stock — **never dual-write** |
| Manufacturing · Robotics (P216) | OT / physical actuation — **gated** |
| P274 | Technician skills / field workforce |
| P272 · procurement | Parts demand · maintenance supply |
| P271 · Financial Kernel | CAPEX · OPEX · TCO |
| P273 | Asset availability → customer experience |
| P268 | Cyber-physical security · device identity |
| P267 · P225 | Failure → self-healing handoff |
| P270 · P269 | Lifecycle governance · compliance |
| P261 · P260 · P262 | Decision · workflows · analytics |
| P263 · P264 · P266 | Mesh · KG · agents |
| P257 · P258 · P259 | Runtime · Command Center · lifecycle |
| Integration · Policy · Audit | IoT vendors · gates · evidence |
| **P276 MEPIASP** | Source-to-Pay OS — **never fork supply-network or dual-write PO ledgers** |
| **P277 MESIARO** | Sales / RevOps OS — **installed-base / upgrade / replacement opportunity signals** |
| Core | Generic platform services |

Permissions: `enterprise_asset_operating.registry.*` · `enterprise_asset_operating.lifecycle.*` · `enterprise_asset_operating.maintenance.*` · `enterprise_asset_operating.condition.*` · `enterprise_asset_operating.field.*` · `enterprise_asset_operating.performance.*` · `enterprise_asset_operating.risk.*` · `enterprise_asset_operating.twin.*` · `enterprise_asset_operating.cost.*` · `enterprise_asset_operating.governance.*` · `enterprise_asset_operating.ai.read` · `enterprise_asset_operating.ai.infer`.

## 14. Implementation Roadmap

| Phase | Focus | Window | Deliverables |
|-------|-------|--------|--------------|
| **P275** | Foundation | — | ADR · capability · fabric · DDD/CQRS · API skeleton · dual tests |
| **Phase 1 / P275-A** | Asset Management Foundation | 3–6 mo | Enterprise Asset Registry · Asset 360 · lifecycle · maintenance · work orders · dashboard |
| **Phase 2 / P275-B** | Connected Asset Intelligence | 6–12 mo | IoT integration · condition monitoring · performance analytics · predictive maintenance · asset risk |
| **Phase 3 / P275-C** | Autonomous Asset Operations | 12–18 mo | Automated maintenance triggers (gated) · predictive work orders · intelligent dispatch · asset optimization · automated failure response (gated) |
| **Phase 4 / P275-D** | Autonomous Asset Operating System | 18–36 mo | Self-optimizing asset assists · twin-driven ops · autonomous maintenance assists · predictive lifecycle · continuous performance optimization (gated) |

Catalogs (planned): `docs/architecture/enterprise_asset_operating/MEAIAMP_*_{CAPABILITIES,DDD_CQRS,SECURITY,VALIDATION,ARCHITECTURE}.v1.yaml`

## 15. Quality Gates

- Never MEOS Enterprise Asset Intelligence & Autonomous Asset Management Platform is missing
- Never Registry / 360 / Lifecycle / PdM / Condition / Field / TCO / Risk / Twin capabilities are missing
- Never MEAIAMP Event Architecture / CQRS Model is missing
- Never MEOS MEAIAMP Integration Map is missing
- Never Sibling Enterprise Asset Operating BC (second deployable)
- Never Replace P236 · P227 · P265 · inventory · Manufacturing/OT · Core · AI
- Never Dual-Write Stock/Asset Ledgers · Never Fork `/api/v1/manufacturing-intelligence*` or twin APIs
- Never Ungated Physical/OT Actuation · Never Opaque Critical Maintenance Auto-Execute
- Never Module-Local LLM · Never Vendor IoT SDK in Domain · Never Treat Twin Simulation as Actuate
- Zero Trust Connected Assets · Device Identity · Secure Telemetry · Threat Monitoring · Isolation Controls (via P268)

Validate: asset domain architecture · DDD · CQRS · events · identity/registry integrity · telemetry integrity · lifecycle traceability · health monitoring · PdM · work-order traceability · field visibility · explainable predictions · RUL monitoring · false +/- monitoring · human approval for critical maintenance · responsible autonomy · command center · workspaces · twin visualization · AI assistant.

## 16. Definition of Done

- [ ] ADR **632** accepted; capability `CAP-PLT-MEAIAMP-001` registered
- [ ] Law + YAML catalogs under `docs/architecture/enterprise_asset_operating/`
- [ ] Context `backend/contexts/enterprise_asset_operating/` scaffolded
- [ ] Fabric wired + ACL to P236, P265, inventory, Workflow, Integration
- [ ] Outbox events + ACL stubs (P236 · P265 · inventory · P274 · P272 · Workflow · P266 · P214-Z · Audit)
- [ ] Dual tests green; scorecard **ENTERPRISE_GRADE**
- [ ] OpenAPI `/api/v1/enterprise-asset-operating*`
- [ ] Telemetry → predict → gated work-order path demonstrated
- [ ] **P275-A** unlocked · **P276** procurement intelligence series unblocked

**MEAIAMP is complete when:** MEOS has an Enterprise Asset Intelligence OS fabric over P236/peers; registry and Asset 360 operate; lifecycle, performance, condition, IoT, PdM, field service, TCO and risk intelligence assist under gates; Digital Asset Twin integrates with P265; agents participate; events join the Event Mesh; technician matching with P274 and parts with P272; financial with P271; cyber-physical with P268; critical autonomous actions remain Policy- and Human-Governance-gated; MEOS progresses toward Autonomous Asset Operations under human/OT authority — Governance Standard **11.0**.

**Principle:** MEAIAMP productizes autonomous asset intelligence; it never replaces P236/twins/inventory/OT SoRs, and never actuates physical assets without Policy + Workflow + Audit accountability.

---

**NEXT EXECUTION:** **P276** — MEOS Enterprise Procurement Intelligence & Autonomous Sourcing Platform — Strategic Sourcing, Supplier Discovery, Spend Intelligence, Contract Intelligence, Purchase Optimization, Supplier Risk, Procurement Analytics and Autonomous Procurement Operations (federate P272 / procurement; never fork `/api/v1/supply-network-operating*` or dual-write PO ledgers; keep P271 for financial spend).
