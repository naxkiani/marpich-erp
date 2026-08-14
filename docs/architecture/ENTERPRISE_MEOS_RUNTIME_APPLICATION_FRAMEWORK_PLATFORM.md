# MEOS Enterprise Runtime & Application Framework Platform (MERAF)

**Status:** Normative (P257) — series foundation · **Productization & Experience Evolution Phase**  
**SoR:** `enterprise_runtime` · **ADR:** [614](../adr/614-meos-enterprise-runtime-application-framework-platform.md) · **Capability:** `CAP-PLT-MERAF-001`  
**Fabric:** `meos_enterprise_runtime_application_framework_platform_framework` · **Governance Standard:** MEOS 11.0  
> **API:** `/api/v1/enterprise-runtime*` · **Builds on:** P254 EAEISPP · P001–P256 capability blueprints · Module Registry · Plugin Platform · Feature Flags · Workflow · API Gateway · Identity · UI Page Standard / AppShell · P214-Z · Policy · Audit · Observability · **Next:** P257-A · **Peer series:** [P258 MESCC](ENTERPRISE_MEOS_APPLICATION_SHELL_COMMAND_CENTER_PLATFORM.md) · [P259 MDMAL](ENTERPRISE_MEOS_DYNAMIC_MODULE_ACTIVATION_LIFECYCLE_PLATFORM.md) (lifecycle depth — never fork this API)  
**Hard bindings:** Inference → **P214-Z** · First-party module catalog/activation → **Module Registry** (ACL; never replace) · Third-party signed extensions → **Plugin Platform** (ACL; never replace `/api/v1/plugins*`) · Feature gates → **Feature Flag System** · Approvals/runtime workflow instances → **Workflow Engine** · AuthN/AuthZ → **Identity + Authorization** · Shell widgets (command palette, search, notifications) → **AppShell / UI_PAGE_STANDARD** (deepened by **P258**) · Event bus → **Enterprise Event Fabric** · Gateway → **API Gateway** · Policy → **Policy Engine** · Audit → **Audit** · Observability → **Observability Platform** · Generic → **Core**.

---

## 1. Header

**MARPICH ENTERPRISE PLATFORM (MEOS)** · Master Blueprint · Enterprise Architecture Governance Standard **11.0** · Prompt **P257** · MEOS Enterprise Runtime & Application Framework Platform (**MERAF**).  
**Platform Domain:** MEOS Enterprise Runtime Ecosystem · **Capability Category:** Enterprise Application Execution Infrastructure · **Strategic Layer:** MEOS Operating System Runtime Layer.

## 2. Prompt ID

**P257**

## 3. Mission

Convert MEOS from a vast Enterprise Blueprint corpus into a real **Enterprise Operating Product** that activates defined domains, modules and capabilities as an executable Application Runtime.

Runtime core responsibilities:

- Dynamic module activation
- Application lifecycle management
- Enterprise Application Shell composition contracts (execution side)
- Navigation framework metadata (execution side; UX depth → P258)
- Metadata-driven application execution
- UI Layer ↔ Domain Runtime binding
- Module discovery orchestration
- Permission-aware execution
- Next-generation ERP experience enablement

Final progression:

```
MEOS Capability Blueprint
        ↓
MEOS Runtime Ecosystem (P257)
        ↓
Enterprise Operating System Experience (P258+)
```

MERAF owns **runtime orchestration and application framework** fabric; it does **not** replace Module Registry, Plugin Platform, AppShell, Feature Flags, Workflow, Core Identity/AuthZ or AI — and never loads unsigned third-party code or bypasses Zero Trust / Policy gates.

## 4. Architecture Principles

- Enterprise Architecture Governance Standard **11.0** (binding)
- DDD · CQRS · Event Sourcing · Event-Driven · Hexagonal · Clean · API-First
- Cloud Native · AI Native · Knowledge Graph Native · Digital Twin Native
- Metadata Driven · Configuration Driven · Policy Driven
- Zero Trust · Explainable AI · Responsible AI · Human Governance
- Enterprise Capability Mapping · Multi-tenant · Fail-closed authorization
- Federate-by-contract only — never peer domain imports / shared tables / local LLM
- **Module Registry vs MERAF:** Registry remains first-party module SoR; MERAF orchestrates runtime activation sessions and composition intents via ACL
- **Plugin Platform vs MERAF:** Plugins remain signed/sandboxed SoR; MERAF invokes via `IPluginRuntime` — never direct plugin imports
- **AppShell / P258 vs MERAF:** Shell UX SoR deepens in P258; MERAF publishes workspace/runtime composition contracts consumed by the shell
- **Feature Flags:** every capability gate evaluates Feature Flag System — no local flag stores
- Activation ≠ bypass security — Identity + AuthZ + Policy + Audit on every runtime action

## 5. Reference Architecture

```
MEOS Enterprise Experience Layer (AppShell · P258 Command Center)
        ↓ contracts
┌──────────────────────────────────────────────────────────────┐
│ MEOS Application Runtime Layer (SoR enterprise_runtime)      │
│ Module Runtime Engine · Application Lifecycle Manager        │
│ Plugin Runtime ACL · Workflow Runtime ACL · UI Component RT  │
│ Metadata Execution Engine                                    │
│ schema: enterprise_runtime_*                                 │
└──────────────────────────────────────────────────────────────┘
        ↓                    ↓                      ↓
 Domain Runtime        Integration Layer         Data Fabric
 (BC services)         Gateway · Event Bus       P229 · P228 · P227
                       Identity · Connectors      Event Store
```

| Layer | Role |
|-------|------|
| Experience | Enterprise Shell · Launcher · Workspace · Navigation · AI Copilot (P258 depth) |
| Application Runtime | MERAF — module/app lifecycle, metadata execution, permission-aware load |
| Domain Runtime | Existing bounded contexts — aggregates, policy, rules (unchanged ownership) |
| Integration | API Gateway · Event Fabric · Service Mesh · Identity Federation · Connectors |
| Data Fabric | Data Mesh · KG · Twin · Event Store · Lake (peer SoRs) |

## 6. Core Capabilities

| ID | Capability |
|----|------------|
| MERAF-C01 | Enterprise Application Shell composition contracts |
| MERAF-C02 | Unified workspace / multi-application session orchestration |
| MERAF-C03 | Context switching & permission-aware execution |
| MERAF-C04 | Dynamic Module Runtime Engine (discover · activate · execute · govern) |
| MERAF-C05 | Application Lifecycle Management (register→retire) |
| MERAF-C06 | Metadata Execution Engine (UI schema · API contract · events) |
| MERAF-C07 | Enterprise Module Marketplace orchestration (first-party catalog + Plugin Platform listings ACL) |
| MERAF-C08 | Dependency & version validation gates |
| MERAF-C09 | Runtime observability & fault isolation |
| MERAF-C10 | AI Copilot runtime guidance (via P214-Z) |
| MERAF-C11 | MERAF Governance Kernel (kill-switch, signed-load only, transparency) |

### 6.1 Enterprise Application Shell (runtime side)

Capabilities (contracts for Experience Layer): Unified Workspace · Multi Application Window · Context Switching · Enterprise Search handoff · Command Palette handoff · Notification Center handoff · User Workspace Personalization.

Flow: `User Login → MEOS Command Center → Enterprise Applications → Runtime Activation`

### 6.2 Dynamic Module Runtime Engine

Every MEOS module must be Discoverable · Activatable · Executable · Governable.

Module metadata (normative shape — stored as composition document, not peer domain):

```yaml
module:
  id: string
  name: string
  domain: string
  version: string
  permissions: string[]
  workflows: string[]
  ui_schema: ref
  api_contract: ref
  events: string[]
```

First-party truth remains Module Registry; third-party truth remains Plugin Platform. MERAF stores activation sessions + composition snapshots + peer refs.

### 6.3 Application Lifecycle Management

`Register → Validate → Deploy → Activate → Monitor → Upgrade → Retire`

### 6.4 Enterprise Module Marketplace (orchestration)

Internal Enterprise App Store **orchestration** only: discovery · version · install intent · configuration · dependency · security validation — installs of third-party packages via Plugin Platform; first-party activation via Module Registry. Never a parallel unsigned marketplace.

## 7. User Experience Architecture

MEOS Experience Model:

```
User → MEOS Command Center → Application Experience Layer
    → Domain Application Workspace → Intelligent Business Actions
```

**Principle:** Traditional ERP menu becomes AI-powered workspace. Navigation intent: *"What do you want to accomplish?"* — not only Menu → Submenu → Module.

AI Assistant actions (examples): Create Purchase Order · Analyze Supply Risk · Approve Employee Request — always Policy + Workflow + owning domain SoR; never MERAF-owned business aggregates.

Universal Command Center capabilities: Global Search · AI Actions · Quick Commands · Recent Activities · Business Alerts · Workflow Tasks — **UX implementation depth → P258**; MERAF supplies runtime status, module catalog projections and activation APIs.

## 8. Application Runtime Model

Activation flow:

```
User Request → Identity Validation → Policy Evaluation → Module Discovery
→ Runtime Loading → UI Composition → Domain Service Execution
→ Event Publication → Analytics Update
```

Dynamic Application Composition includes: UI Metadata · Domain Capability ref · Workflow Definition ref · Security Policy · AI Agent surface · Data Contract — executed under tenant scope with fail-closed AuthZ.

## 9. AI Agents

| Agent | Role | Gate |
|-------|------|------|
| MEOS Runtime Assistant Agent | Module discovery · error analysis · user guidance · runtime optimization | Explainability + Audit · P214-Z |
| Application Builder Agent | Requirement → domain map → UI/workflow generation → gated deploy | Workflow + Policy · human authority |
| Experience Optimization Agent | Behavior · navigation · performance · productivity insights | Non-actuating default · personalization via preferences |

**Law:** Agents recommend and compose; activation/deploy/retire via Workflow + Policy + Module Registry / Plugin Platform. Never module-local LLM. Never treat generated UI as production without Validate + Deploy gates.

## 10. Domain Driven Design (DDD)

**Core domain:** MEOS Enterprise Runtime & Application Framework  
**Strategic type:** Supporting Domain (platform / OS runtime)  
**Supporting:** Runtime management · Application experience contracts · Module governance orchestration

### Bounded Contexts (logical; single SoR `enterprise_runtime`)

| BC | Name | Aggregate root |
|----|------|----------------|
| BC-01 | Runtime Management | `RuntimeInstanceAggregate` |
| BC-02 | Application Experience | `WorkspaceAggregate` |
| BC-03 | Module Governance | `ModulePolicyAggregate` / composition |
| BC-04 | Application Catalog | `ApplicationAggregate` |
| BC-05 | Deployment | `DeploymentAggregate` |
| BC-06 | Runtime Governance | `RuntimeGovernancePolicyAggregate` |

### Aggregates / Entities

`RuntimeInstance` · `Application` · `ModuleComposition` · `PluginRef` · `Deployment` · `Configuration` · `Workspace` · `DashboardRef` · `NavigationTree` · `UIComponentRef` · `UserPreference` · `CapabilityRef` · `ModulePolicy` · `VersionPin` · `DependencyGraph`

### Application Aggregate (composition)

```
Application
 ├── ModuleComposition (peer module_id / plugin_id)
 ├── UI Definition ref
 ├── Workflow ref
 ├── Security Policy
 └── Integration Contract
```

### Value Objects

`ModuleMetadata` · `RuntimeStatus` · `ActivationToken` · `VersionConstraint` · `PermissionSet` · `UiSchemaRef` · `ApiContractRef` · `ExperienceProfile` · `FaultIsolationBoundary` · `TenantScope`

### Domain Services

`ModuleActivationService` · `ApplicationCompositionService` · `RuntimeDeploymentService` · `ExperiencePersonalizationService` · `RuntimeGovernanceEngine` · `RuntimeExplainabilityService`

**Hard separation:** Business aggregates remain in owning contexts (finance, hospital, …). MERAF never imports peer domain packages or owns GL/patient/order tables.

## 11. Event Architecture

### Domain Events

`ModuleRegistered` · `ModuleActivated` · `ApplicationStarted` · `WorkflowExecuted` · `RuntimeConfigurationChanged` · `UserExperienceOptimized` · `RuntimeFaultIsolated` · `GovernanceGateApplied`

### Event Flow

`Runtime Action → Command → Domain Processing → Event → Event Bus → Subscribers (Analytics / AI / Security / Audit)`

Envelope + outbox + idempotent ACL consumers mandatory. Infrastructure transport via Enterprise Event Fabric (Kafka/Pulsar adapters) — never module-local brokers.

## 12. CQRS

### Commands

`RegisterModuleCommand` · `ActivateApplicationCommand` · `DeployRuntimeCommand` · `ConfigureWorkspaceCommand` · `UpgradeApplicationCommand` · `RetireApplicationCommand` · `ApplyRuntimeGovernanceGateCommand`

### Queries

`GetAvailableModulesQuery` · `GetApplicationWorkspaceQuery` · `GetRuntimeStatusQuery` · `GetUserExperienceProfileQuery` · `GetDeploymentHistoryQuery` · `GetExecutiveRuntimeDashboardQuery`

Read models under `enterprise_runtime_*` only; pagination mandatory; live module truth via Module Registry / Plugin Platform ACL — never duplicate peer catalogs as mutable SoR copies.

## 13. MEOS Integration

| Peer | Mode |
|------|------|
| P001–P256 domains | Capability blueprints → activatable via registry + runtime |
| Module Registry | First-party module SoR — **never replace** |
| Plugin Platform | Third-party signed plugins — **never replace** |
| Feature Flag System | Capability gates — **never local flags** |
| Workflow Engine | Runtime workflow instances / approvals |
| Identity · Authorization · Federation | Zero Trust execution |
| API Gateway | Single entry · rate limit · tenant |
| AppShell / UI_PAGE_STANDARD · **P258** | Experience shell / Command Center |
| P214-Z · P224 · P228 · P229 · P227 | AI · decisions · KG · mesh · twin |
| Policy · Audit · Observability · Notifications · Search | Gates · evidence · alerts · discovery |
| Core | Generic enterprise services |

Permissions (activation): `enterprise_runtime.modules.*` · `enterprise_runtime.applications.*` · `enterprise_runtime.workspace.*` · `enterprise_runtime.deploy.*` · `enterprise_runtime.governance.*` · `enterprise_runtime.ai.read` · `enterprise_runtime.ai.infer`.

## 14. Implementation Roadmap

| Phase | Focus | Window | Deliverables |
|-------|-------|--------|--------------|
| **P257** | Foundation | — | ADR · capability · fabric · DDD/CQRS catalogs · API skeleton · dual tests |
| **Phase 1 / P257-A** | Runtime Foundation | 3–6 mo | Enterprise Shell contracts · Module Registry ACL · Runtime API · Application Loader |
| **Phase 2 / P257-B** (+ **P258**) | Experience Platform | 6–12 mo | Command Center · Dynamic Navigation · Workspace Engine · Dashboard Framework |
| **Phase 3 / P257-C** | AI Native Runtime | 12–18 mo | AI Application Builder · Autonomous Configuration · Intelligent Optimization |
| **Phase 4 / P257-D** | Enterprise OS | 18–36 mo | Dynamic Enterprise Applications · Autonomous Runtime Governance · Self-Optimizing ERP Ecosystem |

Catalogs (planned): `docs/architecture/enterprise_runtime/MERAF_*_{CAPABILITIES,DDD_CQRS,SECURITY,VALIDATION,ARCHITECTURE}.v1.yaml`

## 15. Quality Gates

- Never MEOS Enterprise Runtime & Application Framework Platform is missing
- Never Dynamic Module Runtime / Lifecycle / Metadata Execution is missing
- Never MERAF Event Architecture / CQRS Model is missing
- Never MEOS MERAF Integration Map is missing
- Never Sibling Enterprise Runtime BC (second deployable)
- Never Replace Module Registry · Plugin Platform · Feature Flags · Workflow · AppShell · Identity · Core · AI · Policy · Audit
- Never Dual-Write Module Registry or Plugin catalogs as mutable SoR
- Never Fork `/api/v1/plugins*` · Never Unsigned Third-Party Load
- Never Local Feature Flag Store · Never Module-Local LLM
- Never Bypass Zero Trust / Policy / Audit on activation
- Never Business Logic / Peer Aggregates inside `enterprise_runtime`
- Never Treat Generated App as Production without Validate + Deploy + Workflow

Validate: DDD · domain isolation · event-driven execution · API-first · Zero Trust · policy · federation · auditability · modern ERP UX contracts · AI-assisted navigation contracts · dynamic loading · version management · fault isolation · observability.

Gates: P257 · Module Registry · Plugin Platform · Feature Flags · Workflow · Identity · P214-Z · Core platforms · P258 (experience).

## 16. Definition of Done

- [ ] ADR **614** accepted; capability `CAP-PLT-MERAF-001` registered
- [ ] Law + YAML catalogs under `docs/architecture/enterprise_runtime/`
- [ ] Context `backend/contexts/enterprise_runtime/` scaffolded (MODULE_ARCHITECTURE)
- [ ] Fabric wired: service · router · container · `context.yaml` (AI 14 surfaces)
- [ ] Outbox events + ACL stubs (Module Registry · Plugin Platform · Feature Flags · Workflow · Identity · AppShell/P258 · P214-Z · Audit)
- [ ] Dual tests green; architecture scorecard **ENTERPRISE_GRADE**
- [ ] Permissions + OpenAPI `/api/v1/enterprise-runtime*`
- [ ] Dependency graph clean; no plugin/registry dual-write; no unsigned load
- [ ] Blueprint → Runtime Activation path demonstrated for at least one first-party module
- [ ] Series entry **P257-A** unlocked · **P258** experience series unblocked

**MERAF is complete when:** MEOS has an Enterprise Runtime Core; P001–P256 modules can be activated under governance; ERP experience can evolve from menu-based to intelligent workspace (with P258); dynamic application loading works; AI Copilot guides users via P214-Z; UI Layer binds to Domain Runtime by contract; event architecture and CQRS runtime model operate; MEOS progresses from Blueprint to Operating Product — under Governance Standard **11.0**.

**Principle:** MERAF productizes MEOS as an executable runtime under MEOS; it never replaces Module Registry, Plugin Platform or AppShell, and never activates modules without Identity + Policy + Audit accountability.

---

**NEXT EXECUTION:** **P258** — MEOS Enterprise Application Shell & Command Center Platform — full user experience, central dashboard, Workspace Engine and Enterprise Command Center as the human interaction heart of MEOS.
