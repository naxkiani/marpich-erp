# MEOS Enterprise Information Governance, Data Classification & Sensitive Information Intelligence Platform (MEIGSI)

**Status:** Normative (P310) — series foundation · **Information Intelligence & Classification Governance Phase**  
**SoR:** `information_classification_operating` · **ADR:** [667](../adr/667-meos-enterprise-information-governance-data-classification-sensitive-information-intelligence-platform.md) · **Capability:** `CAP-PLT-MEIGSI-001`  
**Fabric:** `meos_enterprise_information_governance_data_classification_sensitive_information_intelligence_platform_framework` · **Governance Standard:** MEOS 11.0  
> **API:** `/api/v1/information-classification-operating*` · **Builds on:** P309 MERILG · P308 MEDCIM · P307 MEKNOL · P270 MEGRSC · P269 Privacy · P268 Cybersecurity · P266 MEAAOI · P264 MEKGSI · P263 Data Mesh · P260 MEWEOP · P257 MERAF · **Documents** · Policy · Workflow · Audit · P214-Z · **Next:** P310-A · **Peer series:** [P311 MEOS Enterprise Data Loss Prevention, Information Protection & Adaptive Data Security Control Platform](ENTERPRISE_MEOS_DATA_LOSS_PREVENTION_INFORMATION_PROTECTION_ADAPTIVE_DATA_SECURITY_CONTROL_PLATFORM.md) (planned)  
**Hard bindings:** Inference → **P214-Z** (ACL; **never module-local LLM**) · Content → **P308** (ACL; never fork Content OS) · Records/ILM → **P309** (ACL; never own retention/hold/disposition) · Data Mesh / Data Products → **P263** (ACL; never replace Data Mesh) · Knowledge Graph → **P264 · P228** (ACL; publish semantic metadata; never fork graph) · Privacy/compliance policy → **P269** (ACL; **P310 detects; P269 governs privacy**) · Cybersecurity / Zero Trust defense → **P268** (ACL; **P310 = information intelligence; P268 = security control/defense**) · Governance / enterprise policy → **P270 · Policy** (ACL; never replace Governance) · Workflow → **P260** (ACL; review/exception/conflict workflows; never own) · Agents → **P266** (ACL; authorized context only; never own Agent Runtime) · DLP / protection execution → **P311** (planned) · Communications → **P294** · Observability → **P304** · AuthN/AuthZ → **Identity** · Generic → **Core**.

---

## 1. Header

**MARPICH ENTERPRISE PLATFORM (MEOS)** · Master Blueprint · Enterprise Architecture Governance Standard **11.0** · Prompt **P310** · MEOS Enterprise Information Governance, Data Classification & Sensitive Information Intelligence Platform (**MEIGSI**).  
**Platform Domain:** Enterprise Information Governance · Data Classification · Sensitive Information Intelligence · **Capability Category:** Information Discovery/Profiling, Data/Content Classification, Sensitivity Labeling, PII/PHI/Secret/Financial/IP Detection, Information Risk & Exposure Intelligence, Taxonomy, Classification Drift, Handling Requirements Intelligence, Governance Score · **Strategic Layer:** MEOS Information Intelligence Control Plane.

## 2. Prompt ID

**P310**

## 3. Mission

Create an Information Intelligence Control Layer that ensures every governed information object carries:

```
OWNER + CLASSIFICATION + SENSITIVITY + POLICY + RISK
+ HANDLING REQUIREMENT + PROVENANCE + AUDITABILITY
```

**Core flow:**
```
DATA / CONTENT → DISCOVERY → DETECTION → CLASSIFICATION → SENSITIVITY
→ INFORMATION RISK → POLICY EVALUATION → HANDLING CONTROL
→ MONITORING → GOVERNANCE
```

**Boundary law (hard):**
- **P308** = Documents · Content · **P309** = Records · Retention · Legal Hold · Disposition
- **P310** = Information Classification · Sensitive Detection · Sensitivity · Taxonomy · Risk/Exposure Intelligence · Handling Requirements Intelligence
- **P263** = Data Mesh / Data Products · **P264/P228** = Semantic / Graph
- **P268** = Cybersecurity / Zero Trust Defense · **P269** = Privacy / Compliance policy
- **P270** = Governance / Policy authority · **P260** = Workflow · **P266** = Agents
- **P311** = DLP / Information Protection execution (next)
- P310 may Discover · Profile · Detect · Classify · Label · Score Risk · Emit Handling Requirements · Detect Drift/Exposure — and must **NOT** Become Data Governance Platform · Data Mesh · DLP Engine · Document/Records Management · Privacy Compliance Platform · Cybersecurity Platform · Knowledge Graph · Agent Runtime · Workflow Engine
- Propagation must **never blindly lower** classification · Low-confidence classifications enter Human Review · AI must never auto-downgrade sensitivity, remove controls, or expose sensitive data via AI responses
- Cross-tenant discovery / AI cross-tenant learning: **DENY BY DEFAULT**

MEIGSI owns **information classification operating fabric** (Information Governance Command / Classification / Sensitive Inventory / Risk Centers, taxonomy, detection/classification campaigns); it does **not** own content/records repositories, data mesh products, DLP enforcement, privacy/security policy engines — and never executes prevent/block/quarantine (that is **P311** / **P268**).

## 4. Architecture Principles

- Enterprise Architecture Governance Standard **11.0** (binding)
- DDD · CQRS · Event Sourcing (where applicable) · Event-Driven · Hexagonal · Clean · API-First · Contract First · Event-First
- Cloud Native · AI Native · Metadata Driven · Configuration Driven · Policy Driven
- Zero Trust · Privacy By Design · Security By Design · Explainable AI · Human-in-the-Loop · Plugin First
- Multi-Tenant · Immutable Audit · Continuous Governance
- Federate-by-contract only — never peer domain imports / shared tables / local LLM / local DLP / local privacy/security engines
- **P308 vs P309 vs P310 vs P311 vs P263/P268/P269/P270:** never merge content, records, classification intelligence, DLP execution, data mesh, security defense, privacy, and governance SoRs
- Tenant isolation · Pagination mandatory · Fail-closed AuthZ · Sensitive search results policy-filtered

## 5. Reference Architecture

```
         P263 DATA MESH · P308 CONTENT · P309 RECORDS · Apps / Storage / SaaS
                                    ↓
┌────────────────────────────────────────────────────────────────────┐
│ Information Classification Operating Fabric (P310)                 │
│ (SoR information_classification_operating)                         │
│ schema: information_classification_operating_*                     │
│ Discovery · Profiling · Detection · Classification · Sensitivity   │
│ Risk · Exposure · Taxonomy · Drift · Handling Requirements         │
└────────────────────────────────────────────────────────────────────┘
        ↓ Policy (P270) · Privacy (P269) · Security (P268) · Workflow (P260)
        ↓ Graph publish (P264) · Agents (P266) · DLP execution (P311 planned)
                                    ↓
                         MONITORING / AUDIT / INTELLIGENCE
```

Layers: Discovery · Profiling · Detection · Classification · Sensitivity · Risk · Policy Integration · Handling Control · Human Review · Analytics · AI · Audit & Observability.

## 6. Core Capabilities

| ID | Capability |
|----|------------|
| MEIGSI-C01 | Information Discovery · Profiling · Ownership · Metadata (no repository ownership) |
| MEIGSI-C02 | Data & Content Classification · Taxonomy · Labels · Confidence |
| MEIGSI-C03 | Sensitivity Hierarchy (PUBLIC→…→HIGHLY_RESTRICTED; tenant-configurable) |
| MEIGSI-C04 | Sensitive Detection — PII/PHI · Financial · Secrets · IP · Regulatory · Credentials |
| MEIGSI-C05 | Human Review · Override · Exceptions (audited) |
| MEIGSI-C06 | Information Risk · Exposure Intelligence · Governance Score |
| MEIGSI-C07 | Handling Requirements Intelligence (encrypt/mask/restrict/export controls — execute elsewhere) |
| MEIGSI-C08 | Classification Propagation · Lineage (P263 authority for data mesh lineage) |
| MEIGSI-C09 | Classification Drift · Policy Drift Detection |
| MEIGSI-C10 | Classification Analytics · Sensitive Inventory · Command Centers |
| MEIGSI-C11 | AI Classification/Risk/Drift Agents · Governance Copilot (human-gated) |
| MEIGSI-C12 | MEIGSI Governance Kernel |

### Notes

P310 identifies; **P269** owns privacy policy; **P268** owns security response; **P270** owns enterprise policy; **P309** owns retention/hold/disposition; **P311** executes DLP/protection controls.  
Detection configurable by jurisdiction and tenant policy.  
Classification may influence P309 recommendations but never owns records lifecycle.

## 7. User Experience Architecture

```
Human → Information Governance Command Center → Classification Center
→ Sensitive Inventory · Risk Center · Review Queue · AI Copilot
```

AI answers must include Source · Evidence · Classification · Policy · Confidence · Risk.  
Actions: Classify · Review · Override · Exception · Reclassify.

## 8. Application Runtime Model

```
Source → Discover → Profile → Detect Sensitive Signals → Classify (+ Confidence)
→ Sensitivity → Risk → Policy Evaluate → Handling Requirements
→ Review if low confidence / high impact → Governed
→ Monitor Drift / Exposure → Reclassify when required

Propagation: Source Classification → Transform → Derived → Policy Reassess
(never blindly lower)
```

States — InformationObject: DISCOVERED · PROFILED · CLASSIFIED · SENSITIVITY_ASSIGNED · RISK_EVALUATED · POLICY_EVALUATED · GOVERNED · REVIEW_REQUIRED · HUMAN_REVIEWED.  
Classification: UNCLASSIFIED · DETECTED · RECOMMENDED · REVIEW_REQUIRED · APPROVED · APPLIED.  
Review: PENDING · ASSIGNED · IN_REVIEW · APPROVED · REJECTED · RECLASSIFICATION_REQUIRED.

**Hard runtime rule:** Policy via **P270**; privacy via **P269**; security response via **P268**; workflows via **P260**; data mesh via **P263**; graph via **P264**; agents via **P266**; DLP execution via **P311**; never module-local LLM.

## 9. AI Agents

P310 does **not** replace P266. P310 defines Information Intelligence Agents.

| Agent | Role | Gate |
|-------|------|------|
| Information Classification Agent | Class · sensitivity · regulatory · handling | Evidence · Confidence · Policy |
| Sensitive Information Discovery Agent | PII · financial · secrets · IP · confidential | Continuous · jurisdiction-aware |
| Classification Drift Agent | Reclassification triggers | Explainable |
| Information Risk Agent | Exposure · impact · regulatory risk | Explainable |
| Policy Conflict Agent | Classification vs governance/security/privacy/retention | Escalate via P260 |
| Information Governance Copilot | Inventory · why-classified · exposure · gaps | Source · Evidence · Policy · Confidence · Risk |

**Law:** AI must **never** change classification without authorization · lower sensitivity automatically · remove security/privacy controls · bypass governance · expose sensitive information in AI responses · export protected information.

## 10. Domain Driven Design (DDD)

**Core domain:** MEOS Enterprise Information Governance, Data Classification & Sensitive Information Intelligence (operating)  
**Strategic type:** Supporting Domain (platform / information intelligence)

### Bounded Contexts (logical; single SoR `information_classification_operating`)

| BC | Name | Aggregate root |
|----|------|----------------|
| BC-01 | Information Discovery / Profiling Operating | `InformationDiscoveryCampaignAggregate` |
| BC-02 | Classification / Taxonomy Operating | `ClassificationCampaignAggregate` |
| BC-03 | Sensitivity / Detection Operating | `SensitivityProfileCampaignAggregate` |
| BC-04 | Information Risk / Exposure Operating | `InformationRiskCampaignAggregate` |
| BC-05 | Review / Exception Operating | `ReviewCaseCampaignAggregate` |
| BC-06 | Lineage / Drift / Analytics Operating | `InformationIntelligenceCampaignAggregate` |

### Aggregates

**InformationObject:** Source · Owner · Classification · Sensitivity · Risk · Policy · Lineage · Labels  
**Classification:** Class · Confidence · Evidence · Method · Reviewer · Version  
**Taxonomy:** Domain · Category · Class · Type · Labels · Version  
**SensitivityProfile:** Level · Signals · Rules · Risk · HandlingRequirements  
**ClassificationPolicy:** Scope · Rules · Priority · Jurisdiction · Exceptions · Version  
**InformationRisk:** Sensitivity · Exposure · Access · Threat · RegulatoryImpact · Score  
**ReviewCase:** InformationObject · Classification · Reviewer · Decision · Reason · Audit

### Value Objects

`InformationObjectId` · `SourceRef` · `DocumentIdRef` · `RecordIdRef` · `DataProductIdRef` · `ClassificationLabel` · `SensitivityLevel` · `ConfidenceScore` · `DetectionEvidence` · `RiskLevel` · `HandlingRequirement` · `TaxonomyVersion` · `ExceptionId` · `TraceId` · `JurisdictionCode` · `DoAThreshold` · `TenantScope`

### Domain Services

`InformationDiscoveryService` · `InformationProfilingService` · `DataClassificationService` · `ContentClassificationService` · `SensitiveInformationDetectionService` · `PIIDetectionService` · `SecretDetectionService` · `FinancialInformationDetectionService` · `IPDetectionService` · `ClassificationService` · `SensitivityService` · `TaxonomyService` · `ClassificationConfidenceService` · `ClassificationReviewService` · `ClassificationExceptionService` · `InformationRiskService` · `ExposureAnalysisService` · `HandlingPolicyService` · `ClassificationPropagationService` · `InformationLineageService` · `ClassificationDriftService` · `PolicyDriftService` · `GovernanceScoreService` · `InformationIntelligenceService`

**Hard separation:** Content in P308; records in P309; data products in P263; privacy in P269; security defense in P268; policy in P270; DLP execution in P311; MEIGSI stores classification/sensitivity/risk/taxonomy campaigns and peer IDs only — never dual-write peer repository tables as a second SoR.

## 11. Event Architecture

### Domain Events

`InformationDiscovered` · `InformationProfiled` · `SensitiveInformationDetected` · `PIIDetected` · `SecretDetected` · `FinancialInformationDetected` · `InformationClassified` · `ClassificationRecommended` · `ClassificationApproved` · `ClassificationRejected` · `ClassificationOverridden` · `SensitivityAssigned` · `SensitivityChanged` · `InformationRiskCalculated` · `InformationRiskChanged` · `InformationPolicyMatched` · `InformationPolicyConflictDetected` · `HandlingRequirementCreated` · `ClassificationExceptionCreated` · `ClassificationExceptionApproved` · `ClassificationReviewRequested` · `ClassificationReviewCompleted` · `InformationExposureDetected` · `InformationExposureResolved` · `ClassificationDriftDetected` · `PolicyDriftDetected` · `InformationLineageCreated` · `ClassificationPropagated` · `InformationGovernanceScoreCalculated` · `InformationClassificationGateApplied`

### Event Flow

`Discover → Profile → Detect → Classify → Sensitivity → Risk → Policy → Handling Req → Review? → Govern → Drift/Exposure Monitor`  
Consumers: P263 · P264 · P268 · P269 · P270 · P260 · P266 · P294 · P304 · P307 · P308 · P309 · P311 (planned) · Audit

Envelope + outbox + idempotent ACL consumers mandatory. Classification/detection events carry AuthZ + Policy + Confidence + Evidence + TraceId — never raw secrets in event payloads.

## 12. CQRS

### Commands

`DiscoverInformationCommand` · `ProfileInformationCommand` · `ClassifyInformationCommand` · `AssignSensitivityCommand` · `EvaluateInformationRiskCommand` · `ApplyInformationPolicyCommand` · `CreateClassificationReviewCommand` · `ApproveClassificationCommand` · `RejectClassificationCommand` · `OverrideClassificationCommand` · `CreateClassificationExceptionCommand` · `ApproveClassificationExceptionCommand` · `PropagateClassificationCommand` · `ReclassifyInformationCommand` · `ResolveExposureCommand` · `RecalculateGovernanceScoreCommand` · `ApplyInformationClassificationGateCommand`

(Workflows via P260; policy via P270; privacy via P269; security response via P268; DLP via P311.)

### Queries

`GetInformationObjectQuery` · `SearchInformationQuery` · `GetClassificationQuery` · `GetSensitivityQuery` · `GetRiskQuery` · `GetHandlingRequirementsQuery` · `GetClassificationPolicyQuery` · `GetReviewQueueQuery` · `GetClassificationExceptionsQuery` · `GetInformationExposureQuery` · `GetInformationLineageQuery` · `GetClassificationDriftQuery` · `GetPolicyDriftQuery` · `GetGovernanceScoreQuery` · `GetSensitiveInformationInventoryQuery`

Read models under `information_classification_operating_*` only; pagination mandatory; fail-closed AuthZ; sensitive results masked/filtered by policy.

## 13. MEOS Integration

| Peer | Mode |
|------|------|
| **P263** | Data Mesh / Data Products — classify; never own mesh |
| **P308 · P309** | Content/Records — classify/sensitize; never own content/ILM |
| **P268 · P269 · P270** | Security response · Privacy policy · Enterprise policy |
| **P260 · P266 · P294** | Workflow · agent context · notifications |
| **P264 · P228** | Semantic metadata publish |
| **P304 · P307** | Telemetry · knowledge source classification signals |
| **P311** | DLP / protection execution (planned) |
| Audit · Identity · Secrets · Core | Evidence · AuthZ · secret refs · generic |

Permissions: `information_classification_operating.discovery.*` · `information_classification_operating.classification.*` · `information_classification_operating.sensitivity.*` · `information_classification_operating.risk.*` · `information_classification_operating.review.*` · `information_classification_operating.analytics.*` · `information_classification_operating.ai.read` · `information_classification_operating.ai.infer`.

## 14. Privacy, Security & Data Mesh

- **Privacy:** P310 detects PII/sensitive attributes; **P269** governs privacy/compliance.
- **Cybersecurity:** P310 detects secrets/exposure; **P268** executes security controls.
- **Data Mesh:** P263 owns data products; P310 adds classification/sensitivity/risk/handling intelligence.
- **Records:** P309 owns retention/hold; P310 may recommend classification/sensitivity only.
- **Zero Trust access:** Identity → Tenant → Role → Attribute → Classification → Sensitivity → Purpose → Policy → Decision → Audit · DEFAULT DENY.

## 15. Security Architecture

Encryption at rest/in transit · Tenant isolation · RBAC/ABAC · Purpose-based access · Immutable audit · Secret protection · Sensitive result masking · AI output filtering · Data minimization · Least privilege · No secrets in events/logs · Sensitive information never revealed merely because an AI agent has technical access.

## 16. Implementation Roadmap

| Phase | Focus | Window | Deliverables |
|-------|-------|--------|--------------|
| **P310** | Foundation | — | ADR · capability · fabric · DDD/CQRS · API skeleton · dual tests |
| **Phase 1 / P310-A** | Information Foundation | 3–6 mo | Object · discovery · profiling · ownership · metadata |
| **Phase 2 / P310-B** | Classification | 6–12 mo | Taxonomy · engine · sensitivity · labels · confidence |
| **Phase 3 / P310-C** | Sensitive Information | 9–15 mo | PII · financial · secrets · IP · regulatory detection |
| **Phase 4 / P310-D** | Governance | 12–18 mo | Policy integration · handling reqs · exceptions · human review |
| **Phase 5 / P310-E** | Risk | 15–24 mo | Risk · exposure · classification/policy drift |
| **Phase 6 / P310-F** | Lineage | 18–30 mo | Lineage · propagation · derived information |
| **Phase 7 / P310-G** | Intelligence | 24–36 mo | Governance score · analytics · forecasting |
| **Phase 8 / P310-H** | AI | 30–42 mo | Agents · governance copilot (human-gated) |
| **Phase 9 / P310-I** | Continuous Information Governance | 36–48 mo | Continuous discover/classify/drift/exposure loop |

Catalogs (planned): `docs/architecture/information_classification_operating/MEIGSI_*_{CAPABILITIES,DDD_CQRS,SECURITY,VALIDATION,ARCHITECTURE}.v1.yaml`

## 17. Quality Gates

- Never Discovery / Classification / Sensitivity / Detection / Risk / Review capabilities are missing
- Never Sibling Information Classification Operating BC (second deployable)
- Never Replace **P263** · **P308** · **P309** · **P268** · **P269** · **P270** · **P264** · **P266** · **P260** · **P311** · Workflow · Core · AI
- Never Dual-write peer repository tables · Never Local DLP/privacy/security/policy/workflow/LLM engines
- Never Become Data Governance / Mesh / DLP / Content / Records / Privacy / Cyber / Graph / Agent / Workflow Engine
- Never Auto-downgrade sensitivity · Never Expose secrets via AI · Never Blind classification lowering on aggregation
- Tenant isolation · Immutable audit · Confidence + Evidence on automated classifications

Validate: Information intelligence OS · DDD · CQRS · events · P308/P309/P263/P268/P269/P270 boundaries · portals · AI copilot.

## 18. Definition of Done

- [ ] ADR **667** accepted; capability `CAP-PLT-MEIGSI-001` registered
- [ ] Law + YAML catalogs under `docs/architecture/information_classification_operating/`
- [ ] Context `backend/contexts/information_classification_operating/` scaffolded
- [ ] Fabric wired + ACL to P263, P308, P309, P268, P269, P270, P260, P266, P294, Policy
- [ ] Outbox events + ACL stubs (P268 · P269 · P270 · P260 · P294 · P214-Z · Audit)
- [ ] Dual tests green; scorecard **ENTERPRISE_GRADE**
- [ ] OpenAPI `/api/v1/information-classification-operating*`
- [ ] Gated discover→detect→classify→risk→handling-req path demonstrated (no parallel DLP/governance/mesh engines)
- [ ] **P310-A** unlocked · **P311** DLP / Information Protection / Adaptive Data Security Control series unblocked

**MEIGSI is complete when:** MEOS has an Information Intelligence Control Plane; discovery, classification, sensitivity, risk, exposure and handling-requirement intelligence operate under gates; P263 remains Data Mesh; P308/P309 remain content/records; P268/P269/P270 remain security/privacy/governance; DLP execution remains **P311**; events join the Event Mesh — Governance Standard **11.0**.

**Architectural boundary guarantee:** MEIGSI must not re-own P263 Mesh, P308 Content, P309 Records, P268 Security, P269 Privacy, P270 Governance, P264 Graph, P266 Agents, P260 Workflow, or P311 DLP as a merge. MEIGSI owns Information Classification, Sensitive Detection, Sensitivity, Taxonomy, Risk/Exposure Intelligence, Drift and Handling Requirements Intelligence only.

**Principle:** MEIGSI productizes information classification and sensitive intelligence; it never replaces mesh/content/records/privacy/security/governance, never dual-writes peer tables, never embeds local LLMs, and never auto-downgrades or AI-exposes sensitive information without Policy + AuthZ + Audit accountability.

---

**NEXT EXECUTION:** **P311** — MEOS Enterprise Data Loss Prevention, Information Protection & Adaptive Data Security Control Platform — convert P310 Classification/Sensitivity into operational Data Protection and DLP controls (Prevent / Allow / Block / Quarantine / Redact) under Policy + Context + Risk (federate P310, P268, P269, P270, P260; never fork Classification Intelligence or Cybersecurity; never create parallel mesh/content/records/workflow/agent engines).

> **P310 delivered:** this law · [ADR 667](../adr/667-meos-enterprise-information-governance-data-classification-sensitive-information-intelligence-platform.md)
