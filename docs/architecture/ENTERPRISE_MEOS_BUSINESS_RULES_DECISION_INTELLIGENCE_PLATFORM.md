# MEOS Enterprise Business Rules & Decision Intelligence Platform (MEBRDI)

**Status:** Normative (P261) — series foundation · **Productization & Experience Evolution Phase**  
**SoR:** `business_decision` · **ADR:** [618](../adr/618-meos-enterprise-business-rules-decision-intelligence-platform.md) · **Capability:** `CAP-PLT-MEBRDI-001`  
**Fabric:** `meos_enterprise_business_rules_decision_intelligence_platform_framework` · **Governance Standard:** MEOS 11.0  
> **API:** `/api/v1/business-decision*` · **Builds on:** P260 MEWEOP · P258 MESCC · P257 MERAF · P259 MDMAL · [Policy Engine](ENTERPRISE_POLICY_ENGINE.md) · [P224 EADIP](ENTERPRISE_AUTONOMOUS_DECISION_INTELLIGENCE_PLATFORM.md) · Workflow Engine · P214-Z · P228 · P227 · P229 · Compliance · Audit · Identity · **Next:** P261-A · **Peer series:** [P262 MEOS Enterprise Intelligence Analytics & Operational Insight](ENTERPRISE_MEOS_INTELLIGENCE_ANALYTICS_OPERATIONAL_INSIGHT_PLATFORM.md)  
**Hard bindings:** Inference → **P214-Z** · Canonical policy evaluate/simulate → **Policy Engine** (`IPolicyEvaluator`, `/api/v1/policies*`) — **never replace / never fork** · Autonomous decision intelligence SoR → **P224 `decision_intelligence`** (ACL; never replace `/api/v1/decision-intelligence*`) · Process/task execution → **Workflow Engine** / **P260** (ACL) · Experience Decision Center → **P258** (ACL) · Runtime → **P257** · Module lifecycle → **P259** · KG reasoning → **P228** · Twin scenario → **P227** · Data products → **P229** · Compliance enforcement signals → **Compliance** (ACL) · AuthN/AuthZ → **Identity** · Audit → **Audit** · Generic → **Core**.

---

## 1. Header

**MARPICH ENTERPRISE PLATFORM (MEOS)** · Master Blueprint · Enterprise Architecture Governance Standard **11.0** · Prompt **P261** · MEOS Enterprise Business Rules & Decision Intelligence Platform (**MEBRDI**).  
**Platform Domain:** MEOS Enterprise Intelligence & Decision Ecosystem · **Capability Category:** Business Rules Management, Policy Execution & Intelligent Decision · **Strategic Layer:** MEOS Cognitive Business Execution Layer.

## 2. Prompt ID

**P261**

## 3. Mission

Deliver the central Decision Intelligence productization layer so Rules, Policies, Business Logic, Decision Models and Enterprise Decisions are managed and executed as Intelligent · Explainable · Policy Driven · AI Assisted · Event Driven · Human Governed.

**Goal:** Transform Static Business Rules into an **Adaptive Enterprise Decision Intelligence Platform**.

```
Business Context → Rule Discovery → Decision Model Evaluation → Policy Validation
→ AI Intelligence Layer → Decision Execution → Event Publication → Learning & Optimization
```

MEBRDI owns **business-rules studio, decision-instance explainability productization and cognitive decision operating fabric**; it does **not** replace Policy Engine, P224 EADIP, Workflow Engine, Compliance or Core — and never hardcodes domain eligibility/limits in modules or issues ungated autonomous decisions without human governance when required.

## 4. Architecture Principles

- Enterprise Architecture Governance Standard **11.0** (binding)
- DDD · CQRS · Event Sourcing · Event-Driven · Hexagonal · Clean · API-First
- Cloud Native · AI Native · Knowledge Graph Native · Digital Twin Native
- Metadata Driven · Configuration Driven · Policy Driven
- Zero Trust · Explainable AI · Responsible AI · Human Governance
- Multi-tenant · Fail-closed authorization
- Federate-by-contract only — never peer domain imports / shared tables / local LLM
- **Policy Engine vs MEBRDI:** Policy Engine remains SoR for versioned policies, evaluate/simulate APIs; MEBRDI owns decision studios, rule authoring productization overlays, decision instances with explanation packs and optimization campaigns — ACL, never dual-write policy catalogs as mutable copy-of-truth
- **P224 vs MEBRDI:** EADIP remains autonomous decision-intelligence SoR; MEBRDI is productization/cognitive execution fabric for rules+decisions across MEOS — never fork `/api/v1/decision-intelligence*`
- **Modules:** no hardcoded business rules — always Policy Engine (+ MEBRDI overlays when applicable)
- Decision recommendation ≠ execute — Workflow / owning SoR for mutations; human approval for critical decisions
- Simulation (tables/trees/twin) ≠ production enforce

## 5. Reference Architecture

```
Decision Experience (P258 Decision Center · Studio · Explanation · Policy Console · Analytics)
        ↓
┌──────────────────────────────────────────────────────────────┐
│ Business Decision Engine (SoR business_decision)             │
│ Rule studio overlays · Decision instances · Explanation packs│
│ Recommendation campaigns · schema: business_decision_*       │
└──────────────────────────────────────────────────────────────┘
        ↓ ACL                         ↓ ACL
 Policy Engine (evaluate/simulate)   P224 Decision Intelligence
        ↓
 Knowledge Intelligence (P228 Ontology/Context) · AI (P214-Z)
        ↓
 Domain Execution (Workflow · P260 · Domain Services · Events)
```

| Layer | Role |
|-------|------|
| Decision Experience | Dashboard · Studio · Explanation Center · Policy Console |
| Business Decision Engine | MEBRDI — rules/decision productization fabric |
| Knowledge Intelligence | P228 KG · context · semantic reasoning ACL |
| AI Decision Intelligence | P214-Z · ML/prediction via platform — never local LLM |
| Domain Execution | Workflow / domains enforce outcomes |

## 6. Core Capabilities

| ID | Capability |
|----|------------|
| MEBRDI-C01 | Enterprise Business Rules Engine (definition · version · execute · test · govern · monitor) |
| MEBRDI-C02 | Decision Model Management (tables · trees · graphs · AI models · scenario simulation) |
| MEBRDI-C03 | Policy Execution Engine federation (security · compliance · financial · HR · operational) |
| MEBRDI-C04 | Intelligent Decision Engine (rules + AI + KG + context) |
| MEBRDI-C05 | Decision Explanation Platform |
| MEBRDI-C06 | Risk evaluation & compliance enforcement signals |
| MEBRDI-C07 | Continuous decision optimization |
| MEBRDI-C08 | Conflict detection across rule sets |
| MEBRDI-C09 | MEBRDI Governance Kernel (human gates, kill-switch, transparency) |

### 6.1 Enterprise Business Rules Engine

Model: `Business Context → Rule Condition → Decision Logic → Action → Event`  
Example: Purchase Request IF Amount > Approval Limit THEN Require Executive Approval — limit values from Policy Engine, not hardcoded.

### 6.2 Decision Model Management

Lifecycle: `Create → Validate → Test → Deploy → Execute → Optimize`  
Models stored as MEBRDI documents with peer policy/decision refs; production evaluate still Policy Engine / P224 as applicable.

### 6.3 Policy Execution Engine (federation)

Categories: Security · Compliance · Financial · HR · Operational.  
Flow: `Request → Policy Evaluation (Policy Engine) → Decision → Enforcement (Workflow/owning SoR)`.

### 6.4 Intelligent Decision Engine

`Data → Context Understanding → Reasoning → Recommendation → Human Approval → Execution`

### 6.5 Decision Explanation Platform

Why · Rule Trace · AI Reasoning · Data Evidence · Confidence Score — mandatory for AI-assisted outcomes.

## 7. User Experience Architecture

```
User → Decision Center (P258) → Business Context → AI Assisted Decision → Action
```

Decision Center: Pending · Recommended Actions · Risk Alerts · Policy Violations · History.  
Executive Decision Dashboard: Strategic · Risks · Forecasts · Recommendations · Scenarios.  
Explainability View: Decision → Rules Applied → AI Factors → Evidence → Outcome.

## 8. Application Runtime Model

```
Business Event → Context Collection → Rule Evaluation → AI Analysis → Decision Generation
→ Policy Validation → Execution (gated) → Event Publication
```

DecisionRuntime / DecisionInstance: Context · Rules Applied · AI Model ref · Result · Confidence · Explanation · Audit Trail ref.

## 9. AI Agents

| Agent | Role | Gate |
|-------|------|------|
| Decision Intelligence Agent | Recommendation · pattern · risk · optimization | P214-Z · Explainability · Audit |
| Rule Generation Agent | Requirement → draft rules · suggest policies · conflict detect | Human validate · Policy publish gates |
| Decision Optimization Agent | Historical analysis · accuracy · risk · outcomes | Non-actuating default |
| Explainable AI Agent | Explanation · evidence · human governance support | Mandatory on AI decisions |

**Law:** Agents recommend and explain; enforce via Policy Engine + Workflow + owning SoR. Never module-local LLM. Never opaque decisions. Never treat generated rules as production without Validate + Deploy + approval.

## 10. Domain Driven Design (DDD)

**Core domain:** MEOS Enterprise Business Rules & Decision Intelligence  
**Strategic type:** Supporting Domain (platform / cognitive business execution)

### Bounded Contexts (logical; single SoR `business_decision`)

| BC | Name | Aggregate root |
|----|------|----------------|
| BC-01 | Business Rules | `RuleSetAggregate` |
| BC-02 | Decision Management | `DecisionInstanceAggregate` |
| BC-03 | Policy Governance (overlay) | `PolicyBindingAggregate` |
| BC-04 | Explanation | `DecisionExplanationAggregate` |
| BC-05 | Optimization | `DecisionOptimizationCampaignAggregate` |
| BC-06 | Decision Governance | `DecisionGovernancePolicyAggregate` |

### Aggregates

**Rule:** Conditions · Actions · Version · PolicyRef · Status  
**Decision:** Context · Model · Evidence · Result · Explanation  
Also: `RuleSet` · `DecisionModel` · `Recommendation` · `ComplianceRequirementRef` · `EnforcementActionRef`

### Value Objects

`RuleCondition` · `DecisionOutcome` · `ConfidenceScore` · `ExplanationTrace` · `EvidenceRef` · `PeerPolicyId` · `PeerDecisionIntelId` · `TenantScope`

### Domain Services

`RuleExecutionService` · `DecisionEvaluationService` · `PolicyEnforcementService` (ACL) · `DecisionExplanationService` · `OptimizationService` · `DecisionGovernanceEngine` · `DecisionExplainabilityService`

**Hard separation:** Policy catalogs/evaluate remain Policy Engine; autonomous decision intel remains P224; compliance ledgers remain Compliance. MEBRDI stores rule/decision productization state, explanation packs, optimization campaigns and peer refs only.

## 11. Event Architecture

### Domain Events

`RuleCreated` · `RuleUpdated` · `RuleActivated` · `DecisionRequested` · `DecisionGenerated` · `DecisionApproved` · `DecisionRejected` · `PolicyViolationDetected` · `RecommendationGenerated` · `DecisionOptimized` · `GovernanceGateApplied`

### Event Flow

`Business Event → Decision Command → Decision Engine → Event → MEOS Event Mesh → Workflow / AI / Analytics / Audit / Digital Twin`

Envelope + outbox + idempotent ACL consumers mandatory.

## 12. CQRS

### Commands

`CreateRuleCommand` · `UpdateRuleCommand` · `EvaluateDecisionCommand` · `ApproveDecisionCommand` · `RejectDecisionCommand` · `DeployPolicyCommand` (maps to Policy Engine ACL) · `ApplyDecisionGovernanceGateCommand`

### Queries

`GetRulesQuery` · `GetDecisionModelQuery` · `GetDecisionHistoryQuery` · `GetPolicyStatusQuery` · `GetDecisionExplanationQuery` · `GetDecisionAnalyticsQuery`

Read models under `business_decision_*` only; pagination mandatory; live policy evaluate via Policy Engine; decision-intel via P224 — never mutable dual SoR catalogs.

## 13. MEOS Integration

| Peer | Mode |
|------|------|
| Policy Engine | Canonical policy SoR — **never replace** |
| P224 EADIP | Decision intelligence SoR — **never replace** |
| Workflow Engine · P260 MEWEOP | Decision → process trigger |
| P257 · P258 · P259 | Runtime · Decision Center UX · module lifecycle |
| P214-Z · P228 · P227 · P229 | Inference · KG · twin · mesh |
| Compliance · Audit · Identity | Enforcement signals · evidence · Zero Trust |
| Core | Generic platform services |

Permissions: `business_decision.rules.*` · `business_decision.models.*` · `business_decision.evaluate.*` · `business_decision.explain.*` · `business_decision.governance.*` · `business_decision.ai.read` · `business_decision.ai.infer`.

## 14. Implementation Roadmap

| Phase | Focus | Window | Deliverables |
|-------|-------|--------|--------------|
| **P261** | Foundation | — | ADR · capability · fabric · DDD/CQRS · API skeleton · dual tests |
| **Phase 1 / P261-A** | Business Rules Foundation | 3–6 mo | Rule repository overlays · lifecycle · basic decision execution ACL |
| **Phase 2 / P261-B** | Decision Intelligence Platform | 6–12 mo | Decision models · Policy Engine ACL · dashboard · explainability |
| **Phase 3 / P261-C** | AI Decision Automation | 12–18 mo | AI decision agents · predictive decisions · autonomous recommendations (gated) |
| **Phase 4 / P261-D** | Autonomous Enterprise Decision System | 18–36 mo | Self-optimizing decisions · continuous learning · autonomous governance (gated) |

Catalogs (planned): `docs/architecture/business_decision/MEBRDI_*_{CAPABILITIES,DDD_CQRS,SECURITY,VALIDATION,ARCHITECTURE}.v1.yaml`

## 15. Quality Gates

- Never MEOS Enterprise Business Rules & Decision Intelligence Platform is missing
- Never Rules / Decision Models / Explanation / Policy Federation capabilities are missing
- Never MEBRDI Event Architecture / CQRS Model is missing
- Never MEOS MEBRDI Integration Map is missing
- Never Sibling Business Decision BC (second deployable)
- Never Replace Policy Engine · P224 · Workflow · Compliance · Core · AI
- Never Dual-Write Policy catalogs · Never Fork `/api/v1/policies*` or `/api/v1/decision-intelligence*`
- Never Hardcoded Business Rules in Modules · Never Local Policy Tables
- Never Module-Local LLM · Never Opaque Unexplainable Decisions
- Never Treat Recommendation/Simulation as Enforce · Never Ungated Autonomous Decisions for critical classes

Validate: domain isolation · DDD · event-driven · CQRS · explainability · AI validation · human oversight · confidence · policy enforcement · audit · Zero Trust · rule accuracy · process integration.

## 16. Definition of Done

- [ ] ADR **618** accepted; capability `CAP-PLT-MEBRDI-001` registered
- [ ] Law + YAML catalogs under `docs/architecture/business_decision/`
- [ ] Context `backend/contexts/business_decision/` scaffolded
- [ ] Fabric wired + ACL to Policy Engine and P224
- [ ] Outbox events + ACL stubs (Policy · P224 · Workflow/P260 · P258 · P214-Z · Audit)
- [ ] Dual tests green; scorecard **ENTERPRISE_GRADE**
- [ ] OpenAPI `/api/v1/business-decision*`
- [ ] Explainable decision path + Workflow consumption demonstrated
- [ ] **P261-A** unlocked · **P262** analytics insight series unblocked

**MEBRDI is complete when:** MEOS has an Enterprise Decision Intelligence productization fabric; business rules are managed dynamically under governance; policy execution federates Policy Engine; AI-assisted decisions operate with explanation; workflows consume decision outcomes; event-driven decision architecture and CQRS models run; MEOS supports Intelligent Enterprise Decision Making — under Governance Standard **11.0**.

**Principle:** MEBRDI productizes adaptive rules and explainable decisions; it never replaces Policy Engine or P224, and never enforces critical decisions without Identity + Policy + Audit (+ human authority when required).

---

**NEXT EXECUTION:** **P262** — MEOS Enterprise Intelligence Analytics & Operational Insight Platform — central Analytics Intelligence for Insight, Prediction, KPI, Monitoring and Enterprise Intelligence.
