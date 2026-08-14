# MEOS Enterprise Human Capital Intelligence & Autonomous Workforce Platform (MEHCAWP)

**Status:** Normative (P274) — series foundation · **Productization & Experience Evolution Phase**  
**SoR:** `human_capital_operating` · **ADR:** [631](../adr/631-meos-enterprise-human-capital-intelligence-autonomous-workforce-platform.md) · **Capability:** `CAP-PLT-MEHCAWP-001`  
**Fabric:** `meos_enterprise_human_capital_intelligence_autonomous_workforce_platform_framework` · **Governance Standard:** MEOS 11.0  
> **API:** `/api/v1/human-capital-operating*` · **Builds on:** P273 MECXARP · P272 MESCIAL · P271 MEFIAF · P270 MEGRSC · P269 MEPCRI · P268 MECZTD · P267 MEAOSH · P266 MEAAOI · P265 MEDTIP · P264 MEKGSI · P263 MEDIMOP · P262 MEIAOI · P261 MEBRDI · P260 MEWEOP · P258 MESCC · P257 MERAF · P259 MDMAL · [P235 EAHRWIP](ENTERPRISE_AUTONOMOUS_HUMAN_RESOURCE_WORKFORCE_INTELLIGENCE_PLATFORM.md) · [P251 EAHCDWIP](ENTERPRISE_AUTONOMOUS_HUMAN_CAPABILITY_DIGITAL_WORKFORCE_INTELLIGENCE_PLATFORM.md) · [P234 EAEHCEP](ENTERPRISE_AUTONOMOUS_EDUCATION_HUMAN_CAPABILITY_EVOLUTION_PLATFORM.md) · HR · Payroll · Identity · Documents · Policy · Workflow · Audit · P214-Z · **Next:** P274-A · **Peer series:** [P275 MEAIAMP](ENTERPRISE_MEOS_ASSET_INTELLIGENCE_AUTONOMOUS_ASSET_MANAGEMENT_PLATFORM.md) (Asset OS productization — never ungated OT actuation; never dual-write asset/stock ledgers) · [P277 MESIARO](ENTERPRISE_MEOS_SALES_INTELLIGENCE_AUTONOMOUS_REVENUE_OPERATIONS_PLATFORM.md) (Sales/RevOps — sales capacity/skills/performance via this Workforce OS; never fork HR/payroll)  
**Hard bindings:** Inference → **P214-Z** · Workforce/HR intelligence SoR → **P235 `workforce_intelligence`** (ACL; never replace `/api/v1/workforce-intelligence*`) · Human capability / skills depth → **P251 `human_capability_intelligence`** (ACL; never replace `/api/v1/human-capability-intelligence*`) · Learning/LMS depth → **P234** (ACL; never become LMS) · Employment truth → **HR / human_resources** (ACL; never dual-write employment ledgers) · Compensation/payroll → **Payroll** (ACL; never dual-write pay ledgers · never ungated pay) · Subject identity → **Identity** (ACL) · Privacy/consent → **P230 / P269** (ACL; Privacy By Design fail-closed) · Employee security/access → **P268** (ACL) · Workforce cost → **P271 / Financial Kernel** (ACL) · Customer-facing workforce impact → **P273** (ACL) · Operational capacity ↔ supply → **P272** (ACL) · Twin workforce simulation → **P227 / P265** (ACL; simulation ≠ hire/terminate/pay) · KG skills graph → **P228 / P264** (ACL) · Decisions → **P261 / P224** (ACL) · HR/recruitment/learning workflows → **P260 / Workflow** (ACL) · Agents → **P266** (ACL) · Experience Workforce Command Center → **P258** (ACL) · ATS/HRIS/LMS vendors → **Integration Platform** · Documents → **Document Exchange** (document_id only) · Policy → **Policy Engine** · Audit → **Audit** · AuthN/AuthZ → **Identity** · Generic → **Core**.

---

## 1. Header

**MARPICH ENTERPRISE PLATFORM (MEOS)** · Master Blueprint · Enterprise Architecture Governance Standard **11.0** · Prompt **P274** · MEOS Enterprise Human Capital Intelligence & Autonomous Workforce Platform (**MEHCAWP**).  
**Platform Domain:** MEOS Enterprise Human Capital & Workforce Intelligence Ecosystem · **Capability Category:** Employee 360, Talent Intelligence, Workforce Planning, Recruitment Intelligence, Performance Management, Learning & Development, Employee Experience, Skills Intelligence & Autonomous Workforce Operations · **Strategic Layer:** MEOS Human Capital & Workforce Operating Layer.

## 2. Prompt ID

**P274**

## 3. Mission

Deliver the central Human Capital Intelligence productization layer for the full workforce lifecycle — talent, skills, recruitment, performance, learning, employee experience, workforce planning and optimization.

```
Traditional HR Management → Connected Human Capital Intelligence
→ Predictive Workforce Management → Autonomous Workforce Operations
```

**Goal:** Transform Reactive HR Operations into an **AI-Native Human Capital & Workforce Operating System**.

Missions: Employee 360 Intelligence · Workforce Planning · Talent Intelligence · Recruitment Intelligence · Skills Intelligence · Performance Intelligence · Learning & Development · Employee Experience · Workforce Risk Intelligence · Workforce Optimization · Autonomous HR Operations (gated).

```
Workforce Signals → Employee 360 → Skills & Talent Intelligence → Workforce Analysis
→ AI Recommendation → HR Decision → Human Approval → Workflow Execution
→ Outcome Measurement → Continuous Workforce Learning
```

MEHCAWP owns **human capital operating fabric** (Workforce Command Center contracts, Employee 360 / manager / talent / recruitment / learning workspace overlays, skills/talent/attrition campaigns, gated workforce optimization intents); it does **not** replace P235, P251, P234, HR, Payroll, Identity or Core — and never executes hire/terminate/pay/promote/comp-change without owning peer APIs + Policy + Workflow + **Human Governance** (+ explainability + audit).

## 4. Architecture Principles

- Enterprise Architecture Governance Standard **11.0** (binding)
- DDD · CQRS · Event Sourcing · Event-Driven · Hexagonal · Clean · API-First
- Cloud Native · AI Native · Knowledge Graph Native · Digital Twin Native
- Metadata Driven · Configuration Driven · Policy Driven
- Zero Trust · Explainable AI · Responsible AI · Human Governance
- **Privacy By Design** · **Continuous Workforce Governance** · **Human-Centric AI**
- Multi-tenant · Fail-closed authorization · Pagination mandatory
- Federate-by-contract only — never peer domain imports / shared tables / local LLM
- **P235 vs P251 vs MEHCAWP:** P235 = workforce/HR intel SoR; P251 = capability/skills/career depth; MEHCAWP = Human Capital OS productization — never fork either API, never dual-write either catalog
- **HR vs Payroll:** employment vs compensation truth — never dual-write; never merge lifecycles
- High-impact employment decisions (hire, terminate, promote, compensate, evaluate) require Human Governance + Policy + Explainability + Auditability — never opaque auto-decide
- Bias monitoring required on recruitment/talent/performance recommendations
- Twin workforce scenario ≠ production hire/terminate/pay
- ATS/HRIS/LMS only via Integration Platform — never vendor SDKs in domain
- Employee PII fail-closed with Identity + P230/P269

## 5. Reference Architecture

```
Workforce Experience (P258 Command Center · Employee 360 · Manager · Talent · Recruitment · Learning · AI HR Assistant)
        ↓
┌──────────────────────────────────────────────────────────────┐
│ Human Capital Operating Fabric (SoR human_capital_operating) │
│ 360/talent/skills/recruit/perf/learning/risk campaigns       │
│ schema: human_capital_operating_*                            │
└──────────────────────────────────────────────────────────────┘
        ↓ ACL                         ↓ ACL                    ↓ ACL
 P235 Workforce Intel            P251 Capability Intel     HR / Payroll
        ↓
 Human Capital Management Core overlays · Workforce Orchestration (planning · mobility · L&D)
        ↓
 Foundation: P266 Agents · P264 KG · P265 Twin · P263 Mesh · P260 Workflow · P262 Analytics · P269 Privacy · P271 Finance
```

| Layer | Role |
|-------|------|
| Workforce Experience | Command Center · Employee 360 · Manager · Talent · Recruitment · Learning · AI Assistant |
| Human Capital Intelligence Engine | Talent · Skills · Analytics · Performance · Forecasting overlays |
| Human Capital Management Core | Employee · Recruit · Onboard · Performance · Learning · Comp · Career (via peers) |
| Workforce Orchestration | Planning · Mobility · Learning · Performance workflows · EX automation (gated) |
| Intelligence Foundation | Agents · KG · Twin · Mesh · Workflow · Decision · Analytics |

## 6. Core Capabilities

| ID | Capability |
|----|------------|
| MEHCAWP-C01 | Employee 360 Intelligence |
| MEHCAWP-C02 | Workforce Planning Intelligence |
| MEHCAWP-C03 | Talent Intelligence Platform |
| MEHCAWP-C04 | Recruitment Intelligence Platform |
| MEHCAWP-C05 | Skills Intelligence Platform (Enterprise Skills Graph overlays) |
| MEHCAWP-C06 | Performance Intelligence Platform |
| MEHCAWP-C07 | Learning & Development Intelligence |
| MEHCAWP-C08 | Employee Experience Intelligence |
| MEHCAWP-C09 | Workforce Risk Intelligence |
| MEHCAWP-C10 | Autonomous Workforce Optimization (gated) + MEHCAWP Governance Kernel |

### Notes

Employee 360 Model: Identity + Role + Skills + Performance + Learning + Experience + Career + Workforce Context → Employee Intelligence Profile.  
Planning: Business Strategy → Demand → Current Workforce → Skills/Capacity Gap → Hiring/Development Plan.  
Talent Score: Skills + Performance + Potential + Experience → Talent Intelligence Score.  
Recruitment: Need → Job Profile → Discovery → Match → Assessment → **Human Decision** → Hiring → Onboarding.  
Skills: Current → Target → Gap → Learning Recommend → Validation (via P234/P251 federation).  
Performance: Strategy → Team Objective → Employee Goal → Signal → AI Analysis → Feedback → Improvement.  
Learning: Skill Gap → Path → Activity → Assessment → Skill Improvement.  
Risk domains: Attrition · Skill Shortage · Capacity · Critical Talent · Continuity · Knowledge Loss.  
Sensitive actions: Human Governance + Policy + Explainability + Auditability.

## 7. User Experience Architecture

```
Employee / Manager / HR → Workforce Command Center → Employee 360
→ Talent / Skills Intelligence → AI Recommendation → Human Decision
→ Workflow Execution → Outcome
```

Command Center: Workforce Health · Headcount · Skills Coverage · Talent Risk · Attrition · Capacity · Open Positions · AI Recommendations.  
Employee 360: Profile · Role · Skills · Goals · Performance · Learning · Career · Feedback · Experience.  
Manager Workspace: Team · Capacity · Skills · Goals · Performance · Risks · Development Plans.  
Talent Workspace: Talent Pool · Succession · Critical Roles · Skills Gap · Internal Mobility · Career Paths.  
AI HR Assistant: *"Which skills will our organization need next year?"* → Strategy → Skills KG → Workforce → Forecast → Gaps → Recommend.

## 8. Application Runtime Model

```
Workforce Signal → Context Enrichment → Analysis → AI Intelligence
→ Decision → Human Approval → Workflow Execution → Outcome → Learning
```

EmployeeWorkforceInstance: EmployeeIdentity · EmploymentState · Role · Skills · Goals · PerformanceState · LearningState · CareerState · ExperienceState · WorkforceRisk · Recommendations · AuditHistory.

Activation: Domain Registered → Metadata → Policy → Permissions → Runtime Activated → Workspaces → Events → Agents.

## 9. AI Agents

| Agent | Role | Gate |
|-------|------|------|
| Workforce Intelligence Agent | Signals · health · gaps | Explainability · Audit |
| Talent Intelligence Agent | Talent · potential · succession · talent risk | Bias monitoring · human for critical |
| Recruitment Intelligence Agent | Match · skill fit · workflow support | Human hiring decision mandatory |
| Skills Intelligence Agent | Skills graph · gaps · forecast · development | P251/P234 ACL |
| Performance Intelligence Agent | Goals · signals · development recommend | Human review for high-impact evaluations |
| Learning Agent | Paths · content · skill improvement | P234 ACL · non-actuating default |
| Employee Experience Agent | EX signals · risks · improvements | Consent/privacy · non-actuating default |

**Law:** Agents recommend; hire/terminate/pay/promote/comp via HR/Payroll + Workflow + Policy + Human Governance. Never module-local LLM. Never opaque employment auto-decide. Simulation ≠ execute. Bias monitoring required.

## 10. Domain Driven Design (DDD)

**Core domain:** MEOS Enterprise Human Capital Intelligence & Autonomous Workforce (operating)  
**Strategic type:** Supporting Domain (platform / human capital operating layer) — Generic HR/Payroll remain peer-owned

### Bounded Contexts (logical; single SoR `human_capital_operating`)

| BC | Name | Aggregate root |
|----|------|----------------|
| BC-01 | Employee Management Operating | `Employee360OperatingAggregate` |
| BC-02 | Recruitment Operating | `RecruitmentCampaignAggregate` |
| BC-03 | Talent Operating | `TalentIntelligenceCampaignAggregate` |
| BC-04 | Skills Operating | `SkillsIntelligenceCampaignAggregate` |
| BC-05 | Performance Operating | `PerformanceIntelligenceCampaignAggregate` |
| BC-06 | Learning / Experience / Risk Operating | `WorkforceDevelopmentCampaignAggregate` |

### Aggregates

**Employee (operating projection):** Identity · Employment · Role · Skills · Goals · Learning · History (HR truth)  
**Candidate (operating):** Profile · Skills · Applications · Assessments · Interviews · HiringDecision  
**TalentProfile (operating):** Skills · Performance · Potential · Career · Succession · Risk  
**LearningPlan (operating):** Objectives · Activities · Assessments · Certifications · Outcomes

### Value Objects

`WorkforceHealthScore` · `TalentIntelligenceScore` · `SkillGapScore` · `AttritionRiskScore` · `ExplainabilityTraceRef` · `BiasMonitorRef` · `PeerEmployeeId` · `PeerPayrollId` · `ConsentRef` · `TenantScope`

### Domain Services

`WorkforcePlanningService` · `TalentIntelligenceService` · `RecruitmentIntelligenceService` (ACL) · `SkillsIntelligenceService` (ACL) · `PerformanceIntelligenceService` · `LearningOptimizationService` (ACL) · `EmployeeExperienceService` · `WorkforceRiskService` · `HumanCapitalGovernanceEngine` · `WorkforceExplainabilityService`

**Hard separation:** Employment in HR; pay in Payroll; workforce intel catalog in P235; capability/skills depth in P251; learning journey in P234. MEHCAWP stores operating campaigns, 360 projections and peer refs only.

## 11. Event Architecture

### Domain Events

`EmployeeCreated` · `EmployeeRoleChanged` · `EmployeeSkillUpdated` · `EmployeeGoalCreated` · `PerformanceSignalRecorded` · `PerformanceReviewCompleted` · `LearningPlanCreated` · `SkillGapDetected` · `CertificationCompleted` · `JobRequisitionCreated` · `CandidateMatched` · `InterviewCompleted` · `HiringDecisionCreated` · `EmployeeOnboarded` · `TalentRiskDetected` · `AttritionRiskDetected` · `WorkforceCapacityChanged` · `WorkforcePlanUpdated` · `EmployeeExperienceSignalDetected` · `CareerPathUpdated` · `WorkforceGateApplied`

### Event Flow

`Workforce Signal → Event Processing → Context → AI Intelligence → Decision → Human Governance → Workflow → Outcome`  
Subscribers: Workflow · Decision · AI Agents · Analytics · KG · Twin · Governance · Finance · Learning peers · Audit

Envelope + outbox + idempotent ACL consumers mandatory.

## 12. CQRS

### Commands

`CreateEmployeeCommand` · `UpdateEmployeeProfileCommand` · `AssignRoleCommand` · `UpdateSkillProfileCommand` · `CreateGoalCommand` · `RecordPerformanceSignalCommand` · `CreateLearningPlanCommand` · `CreateJobRequisitionCommand` · `MatchCandidateCommand` · `AdvanceRecruitmentCommand` · `ApproveHiringDecisionCommand` · `CreateSuccessionPlanCommand` · `ExecuteTalentActionCommand` · `ApplyWorkforceGateCommand`

(Canonical employment/payroll mutations via HR/Payroll ACL.)

### Queries

`GetEmployee360Query` · `GetWorkforceHealthQuery` · `GetSkillGapQuery` · `GetTalentRiskQuery` · `GetCandidateMatchQuery` · `GetPerformanceInsightQuery` · `GetLearningProgressQuery` · `GetEmployeeExperienceQuery` · `GetAttritionRiskQuery` · `GetWorkforceForecastQuery`

Read models under `human_capital_operating_*` only; pagination mandatory; live employment/pay truth via HR/Payroll.

## 13. MEOS Integration

| Peer | Mode |
|------|------|
| P235 EAHRWIP | Workforce/HR intelligence SoR — **never replace** |
| P251 EAHCDWIP | Capability/skills depth — **never replace** |
| P234 EAEHCEP | Learning/capability journey — **never become LMS** |
| HR · Payroll | Employment / compensation truth — **never dual-write · never ungated pay** |
| Identity · P230 · **P269** | Subject · privacy · consent — **fail-closed** |
| P268 | Employee identity trust / access |
| P271 · Financial Kernel | Workforce cost · compensation impact |
| P273 | Customer-facing workforce / service performance |
| P272 | Operational workforce capacity ↔ supply |
| P270 | Workforce strategy ↔ enterprise governance |
| P261 · P260 · P262 | Decision · workflows · people analytics |
| P263 · P264 · P265 · P266 · P267 | Mesh · KG · twin · agents · ops |
| P257 · P258 · P259 | Runtime · Command Center · lifecycle |
| Documents · Integration · Policy · Audit | Blobs · ATS/HRIS · gates · evidence |
| **P275 MEAIAMP** | Asset OS — **never ungated OT actuation; never dual-write asset/stock ledgers** |
| **P277 MESIARO** | Sales / RevOps OS — **sales capacity/skills/performance via Workforce OS ACL** |
| Core | Generic platform services |

Permissions: `human_capital_operating.employee360.*` · `human_capital_operating.planning.*` · `human_capital_operating.talent.*` · `human_capital_operating.recruitment.*` · `human_capital_operating.skills.*` · `human_capital_operating.performance.*` · `human_capital_operating.learning.*` · `human_capital_operating.experience.*` · `human_capital_operating.risk.*` · `human_capital_operating.governance.*` · `human_capital_operating.ai.read` · `human_capital_operating.ai.infer`.

## 14. Implementation Roadmap

| Phase | Focus | Window | Deliverables |
|-------|-------|--------|--------------|
| **P274** | Foundation | — | ADR · capability · fabric · DDD/CQRS · API skeleton · dual tests |
| **Phase 1 / P274-A** | Human Capital Foundation | 3–6 mo | Employee management overlays · Employee 360 · recruitment · performance · learning · workforce dashboard |
| **Phase 2 / P274-B** | Workforce Intelligence Platform | 6–12 mo | Skills intelligence · talent intelligence · workforce forecasting · attrition · EX analytics |
| **Phase 3 / P274-C** | Autonomous Workforce Operations | 12–18 mo | AI recruitment assistance · workforce optimization (gated) · talent mobility · personalized learning · automated planning assists |
| **Phase 4 / P274-D** | Autonomous Human Capital OS | 18–36 mo | Predictive workforce management · self-optimizing capacity assists · autonomous skill development assists · continuous talent optimization · workforce twin ops (gated) |

Catalogs (planned): `docs/architecture/human_capital_operating/MEHCAWP_*_{CAPABILITIES,DDD_CQRS,SECURITY,VALIDATION,ARCHITECTURE}.v1.yaml`

## 15. Quality Gates

- Never MEOS Enterprise Human Capital Intelligence & Autonomous Workforce Platform is missing
- Never Employee 360 / Planning / Talent / Recruitment / Skills / Performance / L&D / EX / Risk capabilities are missing
- Never MEHCAWP Event Architecture / CQRS Model is missing
- Never MEOS MEHCAWP Integration Map is missing
- Never Sibling Human Capital Operating BC (second deployable)
- Never Replace P235 · P251 · P234 · HR · Payroll · Core · AI
- Never Dual-Write Employment/Payroll Ledgers · Never Fork `/api/v1/workforce-intelligence*` or `/api/v1/human-capability-intelligence*`
- Never Ungated Hire/Terminate/Pay/Promote/Comp · Never Opaque High-Impact Employment Decisions
- Never Module-Local LLM · Never Vendor ATS/HRIS SDK in Domain · Never Treat Twin Simulation as Execute
- Bias Monitoring · Human Override · Appeal/Review Workflow · Complete Audit Trail

Validate: human capital architecture · DDD · CQRS · events · Employee 360 accuracy · identity resolution · skills consistency · command center · workspaces · AI assistant · explainable recommendations · bias monitoring · human approval · responsible AI · Zero Trust · Privacy By Design · sensitive HR data protection · no unreviewed high-impact employment decisions.

## 16. Definition of Done

- [ ] ADR **631** accepted; capability `CAP-PLT-MEHCAWP-001` registered
- [ ] Law + YAML catalogs under `docs/architecture/human_capital_operating/`
- [ ] Context `backend/contexts/human_capital_operating/` scaffolded
- [ ] Fabric wired + ACL to P235, P251, HR, Payroll, Identity, P269
- [ ] Outbox events + ACL stubs (P235 · P251 · HR · Payroll · Workflow · P266 · P214-Z · Audit)
- [ ] Dual tests green; scorecard **ENTERPRISE_GRADE**
- [ ] OpenAPI `/api/v1/human-capital-operating*`
- [ ] Signal → 360 → recommend → human-gated HR/Payroll path demonstrated
- [ ] **P274-A** unlocked · **P275** asset intelligence series unblocked

**MEHCAWP is complete when:** MEOS has a Human Capital Intelligence OS fabric over P235/HR peers; Employee 360, planning, talent, recruitment, skills graph, performance, L&D, EX and workforce risk intelligence operate under gates; agents participate; events join the Event Mesh; KG/twin support skills/workforce reasoning; privacy/security/finance/customer peers integrate; high-impact HR decisions remain under Human Governance + Policy; MEOS progresses toward Autonomous Workforce Optimization under human authority — Governance Standard **11.0**.

**Principle:** MEHCAWP productizes autonomous human-capital intelligence; it never replaces P235/HR/Payroll, and never hires, terminates, or pays without Human Governance + Policy + Workflow + Audit accountability.

---

**NEXT EXECUTION:** **P275** — MEOS Enterprise Asset Intelligence & Autonomous Asset Management Platform — Asset 360, Enterprise Asset Registry, Lifecycle Management, Predictive Maintenance, IoT Intelligence, Digital Asset Twin, Field Service, Asset Risk and Autonomous Asset Operations (federate asset/maintenance peers; never dual-write asset ledgers; never ungated physical actuation).
