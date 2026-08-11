# MEOS Enterprise Records, Retention, Legal Hold & Information Lifecycle Governance Platform (MERILG)

**Status:** Normative (P309) — series foundation · **Productization & Experience Evolution Phase**  
**SoR:** `records_lifecycle_operating` · **ADR:** [666](../adr/666-meos-enterprise-records-retention-legal-hold-information-lifecycle-governance-platform.md) · **Capability:** `CAP-PLT-MERILG-001`  
**Fabric:** `meos_enterprise_records_retention_legal_hold_information_lifecycle_governance_platform_framework` · **Governance Standard:** MEOS 11.0  
> **API:** `/api/v1/records-lifecycle-operating*` · **Builds on:** P308 MEDCIM · P307 MEKNOL · P306 MEESOP · P305 MEIRRE · P304 MEPOCI · P294 MENCOE · P270 MEGRSC · P266 MEAAOI · P264 MEKGSI · P260 MEWEOP · P257 MERAF · **Documents** (Document Exchange) · Policy · Workflow · Audit · P214-Z · **Next:** P309-A · **Peer series:** [P310 MEIGSI](ENTERPRISE_MEOS_INFORMATION_GOVERNANCE_DATA_CLASSIFICATION_SENSITIVE_INFORMATION_INTELLIGENCE_PLATFORM.md) (delivered) · [P311 DLP / Information Protection](ENTERPRISE_MEOS_DATA_LOSS_PREVENTION_INFORMATION_PROTECTION_ADAPTIVE_DATA_SECURITY_CONTROL_PLATFORM.md) (planned)  
**Hard bindings:** Inference → **P214-Z** (ACL; **never module-local LLM**) · Content/document object → **P308** (ACL; **P308 = CONTENT · P309 = RECORD LIFECYCLE**; never fork Document Intelligence) · Blob/version SoR → **Documents** (ACL; **`document_id` / source content refs only**) · Knowledge → **P307** (ACL; records may be source material; never own Knowledge OS) · Knowledge Graph / Semantic → **P264 · P228** (ACL; publish relationships; never fork graph) · Workflow execution → **P260** (ACL; hold/exception/disposition/custodian workflows; never own) · Agent consumption → **P266** (ACL; authorized records context only; never own Agent Runtime) · Governance / retention / regulatory policy → **P270 · Policy** (ACL; **P309 executes lifecycle under policy; never replace Governance**) · Communications → **P294 / Notifications** (ACL) · Observability → **P304** (ACL) · Incident evidence preservation → **P305** (ACL; P305 remains Incident authority) · Classification specialization → **P310** (delivered) · DLP/protection execution → **P311** (planned) · AuthN/AuthZ → **Identity** · Generic → **Core**.

---

## 1. Header

**MARPICH ENTERPRISE PLATFORM (MEOS)** · Master Blueprint · Enterprise Architecture Governance Standard **11.0** · Prompt **P309** · MEOS Enterprise Records, Retention, Legal Hold & Information Lifecycle Governance Platform (**MERILG**).  
**Platform Domain:** MEOS Enterprise Records, Retention, Legal Hold & Information Lifecycle Governance · **Capability Category:** Record Declaration/Classification, Retention Scheduling & Triggers, Legal/Litigation/Regulatory Hold, Preservation, Chain of Custody, Defensible Disposition, Evidence Packages, Archive Transfer, Retention Risk Intelligence, Records Analytics · **Strategic Layer:** MEOS Information Lifecycle Governance Operating Layer.

## 2. Prompt ID

**P309**

## 3. Mission

Create an Enterprise Information Lifecycle Control Layer that makes every governed record carry:

```
OWNER + CLASSIFICATION + RETENTION RULE + RETENTION TRIGGER
+ LEGAL HOLD STATUS + LIFECYCLE STATUS + AUDIT TRAIL + DISPOSITION STATE
```

**Core information lifecycle:**
```
CONTENT → RECORD DECLARATION → RECORD CLASSIFICATION → RETENTION SCHEDULE
→ RETENTION TRIGGER → ACTIVE RETENTION → LEGAL HOLD CHECK → PRESERVATION
→ REVIEW → DISPOSITION ELIGIBILITY → AUTHORIZATION → DISPOSITION → IMMUTABLE AUDIT
```

**Boundary law (hard):**
- **P308** = Documents · Content · Document Lifecycle · Document Intelligence
- **P309** = Records · Retention · Legal Hold · Preservation · Disposition · Evidence · Information Lifecycle
- **Documents** = Document Exchange blob / version storage SoR
- **P307** = Knowledge · **P264/P228** = Semantic / Graph · **P266** = Agent Orchestration
- **P270** = Governance / Policy authority · **P260** = Workflow execution
- **P310** = Information Classification / Sensitive Information Intelligence (delivered)
- **P311** = DLP / Information Protection / Adaptive Data Security Control (next)
- P309 may Declare · Classify · Schedule · Hold · Preserve · Review · Dispose · Certify · Package Evidence — and must **NOT** Become Document Management · Content Management · Knowledge Management · Knowledge Graph · Workflow Engine · Governance Policy Engine · Agent Runtime · Legal Case Management System
- Legal Hold overrides ordinary disposition eligibility · Conflict priority: **Legal Hold > Regulatory Preservation > Investigation > Governance Exception > Retention Policy > Ordinary Disposition**
- AI must **never** autonomously Release Holds · Approve Disposition · Override Retention · Delete Records · Bypass Governance · Modify Chain of Custody · Alter Evidence
- Retention calculation must be deterministic and auditable · No irreversible disposal may bypass Policy + Hold check + Human authorization + Audit

MERILG owns **records lifecycle operating fabric** (Records Command / Retention / Legal Hold / Disposition / Risk / Evidence Centers, retention overlays, hold/disposition campaigns); it does **not** own content intelligence (P308), blob SoR (Documents), knowledge publication (P307), graph, agent/workflow/governance engines — and never disposes under active Legal Hold or outside **Policy + Workflow + Audit**.

## 4. Architecture Principles

- Enterprise Architecture Governance Standard **11.0** (binding)
- DDD · CQRS · Event Sourcing · Event-Driven · Hexagonal · Clean · API-First · Contract First · Event-First
- Cloud Native · AI Native · Metadata Driven · Configuration Driven · Policy Driven
- Zero Trust · Privacy By Design · Explainable AI · Human-in-the-Loop · Plugin First
- Multi-Tenant · Immutable Audit · Continuous Governance
- Federate-by-contract only — never peer domain imports / shared tables / local LLM / local policy engine / local workflow
- **P308 vs P309 vs P270 vs P310:** never merge content intelligence, records/ILM, governance policy authority, and sensitive-information classification SoRs
- Tenant isolation default deny cross-tenant · Pagination mandatory · Fail-closed AuthZ

## 5. Reference Architecture

```
                    ENTERPRISE CONTENT (P308) + Documents (document_id)
                                      ↓
┌────────────────────────────────────────────────────────────────────┐
│ Records Lifecycle Operating Fabric (P309)                          │
│ (SoR records_lifecycle_operating)                                  │
│ schema: records_lifecycle_operating_*                              │
│ Declaration · Classification · Retention · Hold · Preservation     │
│ Disposition · Evidence · Analytics                                 │
└────────────────────────────────────────────────────────────────────┘
        ↓ Policy (P270) · Workflow (P260) · Notifications (P294)
        ↓ Graph publish (P264) · Agents (P266) · Telemetry (P304)
                                      ↓
                         IMMUTABLE AUDIT · CERTIFICATES
```

Primary layers: Records Experience · Intelligence · Lifecycle · Retention · Legal Hold · Preservation · Disposition · Evidence & Audit · Policy Integration · Analytics.

## 6. Core Capabilities

| ID | Capability |
|----|------------|
| MERILG-C01 | Record Model · Declaration · Series · Ownership · Custodians |
| MERILG-C02 | Record Classification · Regulatory Categories · Retention Class |
| MERILG-C03 | Retention Schedules · Triggers · Deterministic Calculation · Exceptions |
| MERILG-C04 | Legal Hold · Scope · Custodian Ack · Freeze · Preservation |
| MERILG-C05 | Disposition Eligibility · Review · Approval · Execution · Certificate |
| MERILG-C06 | Chain of Custody · Integrity Hash · Evidence Packages · Controlled Export |
| MERILG-C07 | Archive Transfer · Cold / Regulatory Archive Metadata Continuity |
| MERILG-C08 | Records Discovery · Legal Discovery Support Packages (not case mgmt) |
| MERILG-C09 | Retention Risk · Hold Impact · Conflict Detection · Policy Simulation |
| MERILG-C10 | Retention Forecasting · Lifecycle Analytics · Heatmaps · Dashboards |
| MERILG-C11 | Records Copilot · Classification/Retention/Hold Agents (human-gated) |
| MERILG-C12 | MERILG Governance Kernel |

### Notes

P308 owns underlying Document/Content; P309 owns Record state.  
Policy definitions originate from / are governed through **P270**.  
Disposition methods: Secure Deletion · Repository Deletion · Cryptographic Erasure · Physical Destruction Reference · Transfer · Archive · Permanent Preservation.  
P309 is **not** a Legal Case Management System — discovery packages only.  
Sensitive data classification specialization owned by **P310** (delivered); DLP execution deepens in **P311**.

## 7. User Experience Architecture

```
Human → Records Command Center → Record Detail · Retention · Legal Hold
→ Disposition · Risk · Evidence Centers · AI Copilot · Command Palette
```

AI answers must include Source · Record · Policy · Evidence · Confidence.  
Actions: Place/Release Hold · Review · Export · Archive · Request Disposition.

## 8. Application Runtime Model

```
Content (P308) → Declare → Classify → Assign Schedule → Trigger → Active Retention
→ Hold? → Preserve → Expiry → Eligibility (no hold/exception/investigation)
→ Review → Policy Check → Human Authorization (P260) → Disposition → Certificate → Audit

Conflict priority:
Legal Hold > Regulatory Preservation > Investigation > Governance Exception
> Retention Policy > Ordinary Disposition
```

States — Record: IDENTIFIED · DECLARED · CLASSIFIED · ACTIVE · ON_HOLD · PRESERVED · RETENTION_COMPLETE · DISPOSITION_REVIEW · DISPOSITION_APPROVED · DISPOSED · ARCHIVED.  
Legal Hold: DRAFT · REQUESTED · APPROVED · ACTIVE · RELEASE_REQUESTED · RELEASED · CLOSED.  
Disposition: NOT_ELIGIBLE · ELIGIBLE · UNDER_REVIEW · APPROVED · SCHEDULED · EXECUTED · CERTIFIED.  
Preservation: NOT_REQUIRED · REQUIRED · PRESERVED · VERIFIED · RELEASED.

**Hard runtime rule:** Content refs via **P308/Documents**; workflows via **P260**; policy via **P270**; graph via **P264**; agents via **P266**; notifications via **P294**; never autonomous high-impact destruction.

## 9. AI Agents

P309 does **not** replace P266. P309 defines Records Intelligence Agents.

| Agent | Role | Gate |
|-------|------|------|
| Retention Intelligence Agent | Schedule · trigger · exception recommendations | Governed authority |
| Hold Discovery Agent | Potential hold scope | Policy-controlled validation |
| Disposition Risk Agent | Hold/regulatory/missing evidence/premature disposition | Block until resolved |
| Records Classification Agent | Record class · series · retention class | Human confirmation |
| Retention Forecast Agent | Disposition volume · archive · storage · hold impact | Explainable |
| Records Copilot | Expiring · holds · why-not-dispose · missing schedules | Source · Policy · Evidence |

**Law:** Agents assist; never release holds / approve disposition / override retention / delete / alter custody or evidence; never module-local LLM; never channel send.

## 10. Domain Driven Design (DDD)

**Core domain:** MEOS Enterprise Records, Retention, Legal Hold & Information Lifecycle Governance (operating)  
**Strategic type:** Supporting Domain (platform / information lifecycle governance)

### Bounded Contexts (logical; single SoR `records_lifecycle_operating`)

| BC | Name | Aggregate root |
|----|------|----------------|
| BC-01 | Records Management Operating | `RecordCampaignAggregate` |
| BC-02 | Retention Management Operating | `RetentionScheduleCampaignAggregate` |
| BC-03 | Legal Hold / Preservation Operating | `LegalHoldCampaignAggregate` |
| BC-04 | Disposition / Archive Operating | `DispositionCampaignAggregate` |
| BC-05 | Evidence / Custody / Integrity Operating | `EvidencePackageCampaignAggregate` |
| BC-06 | Records Intelligence / Analytics Operating | `RecordsIntelligenceCampaignAggregate` |

### Aggregates

**Record:** Classification · Retention · Holds · Preservation · Ownership · Integrity · Lifecycle  
**RetentionSchedule:** RecordClasses · Trigger · Duration · ReviewRule · DispositionRule · Exceptions  
**LegalHold:** Matter · Scope · Custodians · Records · Preservation · Release  
**Disposition:** Records · Eligibility · Review · Approval · Method · Certificate  
**EvidencePackage:** Records · Metadata · Integrity · ChainOfCustody · ExportManifest

### Value Objects

`RecordOperatingId` · `SourceContentId` · `DocumentIdRef` · `RecordClass` · `RecordSeriesId` · `RetentionScheduleId` · `RetentionTrigger` · `LegalHoldId` · `DispositionId` · `CertificateId` · `IntegrityHash` · `CustodyEventId` · `EvidencePackageId` · `CustodianId` · `TraceId` · `DoAThreshold` · `TenantScope`

### Domain Services

`RecordDeclarationService` · `RecordClassificationService` · `RecordSeriesService` · `RetentionScheduleService` · `RetentionCalculationService` · `RetentionExceptionService` · `LegalHoldService` · `HoldScopeService` · `HoldPreservationService` · `HoldReleaseService` · `CustodianService` · `RecordFreezeService` · `RecordIntegrityService` · `ChainOfCustodyService` · `DispositionEligibilityService` · `DispositionReviewService` · `DispositionApprovalService` · `DispositionExecutionService` · `DispositionCertificateService` · `ArchiveTransferService` · `RecordsDiscoveryService` · `EvidencePackageService` · `RegulatoryRecordsService` · `RecordsRiskService` · `RecordsQualityService` · `RetentionAnalyticsService` · `RetentionForecastService` · `HoldImpactService` · `DispositionConflictService` · `RetentionSimulationService`

**Hard separation:** Content objects in P308; blobs in Documents; policy in P270; workflows in P260; knowledge in P307; graph in P264/P228; agents in P266; sensitive classification specialization in P310; MERILG stores record/retention/hold/disposition/evidence campaigns and `source_content_id` / `document_id` refs only — never dual-write P308/Documents tables as a second SoR.

## 11. Event Architecture

### Domain Events

`RecordDeclared` · `RecordClassified` · `RecordOwnerAssigned` · `RecordCustodianAssigned` · `RetentionScheduleAssigned` · `RetentionStarted` · `RetentionUpdated` · `RetentionExpired` · `RetentionExceptionCreated` · `RetentionExceptionApproved` · `RetentionSuspended` · `RetentionResumed` · `LegalHoldRequested` · `LegalHoldApproved` · `LegalHoldActivated` · `LegalHoldApplied` · `LegalHoldReleased` · `LegalHoldClosed` · `RecordPreservationStarted` · `RecordPreservationCompleted` · `RecordFrozen` · `RecordUnfrozen` · `DispositionEligibilityCalculated` · `DispositionBlocked` · `DispositionReviewStarted` · `DispositionApproved` · `DispositionRejected` · `DispositionScheduled` · `DispositionExecuted` · `DispositionCertified` · `RecordArchived` · `RecordTransferred` · `RecordExported` · `EvidencePackageCreated` · `ChainOfCustodyRecorded` · `RecordIntegrityVerified` · `RecordIntegrityFailureDetected` · `RetentionRiskDetected` · `RetentionConflictDetected` · `DispositionConflictDetected` · `RecordOwnerChanged` · `CustodianChanged` · `RecordsLifecycleGateApplied`

### Event Flow

`Declare → Classify → Schedule → Trigger → Hold?/Preserve → Eligibility → Review → Approve → Dispose/Archive → Certify → Audit`  
Consumers: P257 · P260 · P264 · P266 · P270 · P294 · P304 · P305 · P307 · P308 · P310 · P311 (planned) · Documents · Audit

Envelope + outbox + idempotent ACL consumers mandatory. Hold/disposition/certificate events carry AuthZ + Policy + RecordId + ScheduleId + IntegrityHash + TraceId.

## 12. CQRS

### Commands

`DeclareRecordCommand` · `ClassifyRecordCommand` · `AssignRetentionScheduleCommand` · `StartRetentionCommand` · `CreateRetentionExceptionCommand` · `ApproveRetentionExceptionCommand` · `CreateLegalHoldCommand` · `ApproveLegalHoldCommand` · `ApplyLegalHoldCommand` · `ReleaseLegalHoldCommand` · `AssignCustodianCommand` · `FreezeRecordCommand` · `PreserveRecordCommand` · `VerifyRecordIntegrityCommand` · `EvaluateDispositionCommand` · `RequestDispositionCommand` · `ApproveDispositionCommand` · `RejectDispositionCommand` · `ScheduleDispositionCommand` · `ExecuteDispositionCommand` · `CertifyDispositionCommand` · `ArchiveRecordCommand` · `TransferRecordCommand` · `CreateEvidencePackageCommand` · `ExportEvidencePackageCommand` · `ApplyRecordsLifecycleGateCommand`

(Workflows via P260; policy via P270; content refs via P308/Documents.)

### Queries

`GetRecordQuery` · `SearchRecordsQuery` · `GetRecordLifecycleQuery` · `GetRetentionScheduleQuery` · `GetRetentionStatusQuery` · `GetExpiringRecordsQuery` · `GetLegalHoldQuery` · `GetActiveLegalHoldsQuery` · `GetAffectedRecordsQuery` · `GetCustodianQuery` · `GetPreservationStatusQuery` · `GetDispositionEligibilityQuery` · `GetDispositionQueueQuery` · `GetDispositionCertificateQuery` · `GetArchiveStatusQuery` · `GetChainOfCustodyQuery` · `GetEvidencePackageQuery` · `GetRecordIntegrityQuery` · `GetRetentionRiskQuery` · `GetRetentionForecastQuery` · `GetHoldImpactQuery` · `GetDispositionConflictQuery` · `SimulateRetentionPolicyQuery`

Read models under `records_lifecycle_operating_*` only; pagination mandatory; fail-closed AuthZ.

## 13. MEOS Integration

| Peer | Mode |
|------|------|
| **P308** | Content/document source — Record state owned here; never fork content intelligence |
| **Documents** | Blob/version refs (`document_id`) — never fork blob store |
| **P270 · Policy** | Retention/hold/disposition/regulatory policy authority |
| **P260 · P266 · P294** | Workflow · authorized agent context · notifications |
| **P264 · P228** | Record/custodian/regulatory relationship publish |
| **P304 · P305 · P307** | Telemetry · incident evidence preservation · knowledge source material |
| **P310** | Information Classification / Sensitive Intelligence (delivered; distinct) |
| **P311** | DLP / Information Protection / Adaptive Data Security (planned) |
| Audit · Identity · Secrets · Core | Evidence · AuthZ · secret refs · generic |

Permissions: `records_lifecycle_operating.record.*` · `records_lifecycle_operating.retention.*` · `records_lifecycle_operating.hold.*` · `records_lifecycle_operating.disposition.*` · `records_lifecycle_operating.evidence.*` · `records_lifecycle_operating.analytics.*` · `records_lifecycle_operating.ai.read` · `records_lifecycle_operating.ai.infer`.

## 14. Record Discovery & Evidence

Discovery: Identity → Authorization → Purpose → Scope → Search → Hold Validation → Policy Validation → Evidence Retrieval → Result (source-traceable).  
Evidence Package: Records · Original References · Metadata · Hashes · Custody Events · Hold/Retention Info · Export Manifest — authorized, audited, integrity-verified.

## 15. Security Architecture

Zero Trust record access: Identity → Tenant → Role → Attribute → Record Classification → Legal/Governance Policy → Purpose → Access Decision → Audit.  
Controls: Encryption at rest/in transit · RBAC/ABAC · Tenant isolation · Immutable audit · Privacy · No implicit trust · Cross-tenant DENY BY DEFAULT.

## 16. Implementation Roadmap

| Phase | Focus | Window | Deliverables |
|-------|-------|--------|--------------|
| **P309** | Foundation | — | ADR · capability · fabric · DDD/CQRS · API skeleton · dual tests |
| **Phase 1 / P309-A** | Record Foundation | 3–6 mo | Record model · classification · ownership · series · lifecycle |
| **Phase 2 / P309-B** | Retention | 6–12 mo | Schedules · triggers · calculation · exceptions · expiration |
| **Phase 3 / P309-C** | Legal Hold | 9–15 mo | Hold · scope · custodians · preservation · release |
| **Phase 4 / P309-D** | Disposition | 12–18 mo | Eligibility · review · approval · execution · certificate |
| **Phase 5 / P309-E** | Evidence | 15–24 mo | Custody · integrity · packages · controlled export |
| **Phase 6 / P309-F** | Archive | 18–30 mo | Transfer · archive metadata · integrity verification |
| **Phase 7 / P309-G** | Intelligence | 24–36 mo | Risk · hold impact · conflict · forecast · simulation |
| **Phase 8 / P309-H** | AI | 30–42 mo | Copilot · classification/retention/hold/disposition agents |
| **Phase 9 / P309-I** | Autonomous Governance Assistance | 36–48 mo | Continuous risk/gap detection (no autonomous destruction) |

Catalogs (planned): `docs/architecture/records_lifecycle_operating/MERILG_*_{CAPABILITIES,DDD_CQRS,SECURITY,VALIDATION,ARCHITECTURE}.v1.yaml`

## 17. Quality Gates

- Never Record Declaration / Retention / Legal Hold / Disposition / Evidence capabilities are missing
- Never Sibling Records Lifecycle Operating BC (second deployable)
- Never Replace **P308** · **Documents** · **P307** · **P264/P228** · **P266** · **P260** · **P270** · **P310** · Workflow · Core · AI
- Never Dual-write P308/Documents tables as second SoR · Never Local policy/workflow/LLM engines
- Never Become Document/Content/Knowledge/Graph/Agent/Workflow/Governance/Legal Case Management Engine
- Never Autonomous hold release / disposition / retention override / custody or evidence mutation
- Never Dispose while Legal Hold / unresolved conflict · Deterministic retention · Defensible certificates · Tenant isolation · Immutable audit

Validate: Records/ILM OS · DDD · CQRS · events · P308/P270/P260 boundaries · portals · AI copilot (human-gated).

## 18. Definition of Done

- [ ] ADR **666** accepted; capability `CAP-PLT-MERILG-001` registered
- [ ] Law + YAML catalogs under `docs/architecture/records_lifecycle_operating/`
- [ ] Context `backend/contexts/records_lifecycle_operating/` scaffolded
- [ ] Fabric wired + ACL to P308, Documents, P270, P260, P266, P294, P304, P305, P307, Policy
- [ ] Outbox events + ACL stubs (P308 · P270 · P260 · P294 · P214-Z · Audit)
- [ ] Dual tests green; scorecard **ENTERPRISE_GRADE**
- [ ] OpenAPI `/api/v1/records-lifecycle-operating*`
- [ ] Gated declare→retain→hold→dispose→certify path demonstrated (no parallel record/governance/workflow engines)
- [ ] **P309-A** unlocked · **P310** MEIGSI delivered · **P311** DLP / Information Protection / Adaptive Data Security Control series unblocked

**MERILG is complete when:** MEOS has an Enterprise Information Lifecycle Governance Operating Layer; record declaration, retention, legal hold, preservation, defensible disposition and evidence packages operate under gates; P308 remains content authority; P270 remains policy authority; P260 remains workflow; events join the Event Mesh — Governance Standard **11.0**.

**Architectural boundary guarantee:** MERILG must not re-own P308 Content, Documents blob SoR, P307 Knowledge, P264 Graph, P266 Agents, P260 Workflow, P270 Governance, or P310 sensitive classification as a merge. MERILG owns Enterprise Records, Retention, Legal Hold, Preservation, Custodians, Disposition, Evidence and Information Lifecycle only.

**Principle:** MERILG productizes records and information lifecycle governance; it never replaces P308/P270/Documents, never dual-writes peer content/blob tables, never embeds local LLMs, and never disposes or releases holds without Policy + Workflow + Audit accountability.

---

**NEXT EXECUTION:** **P311** — MEOS Enterprise Data Loss Prevention, Information Protection & Adaptive Data Security Control Platform — convert P310 Classification/Sensitivity into operational Data Protection and DLP controls (Prevent / Allow / Block / Quarantine / Redact) under Policy + Context + Risk (federate P310, P268, P269, P270, P260; never fork Classification Intelligence or Cybersecurity; never create parallel mesh/content/records/workflow/agent engines).

> **P309 delivered:** this law · [ADR 666](../adr/666-meos-enterprise-records-retention-legal-hold-information-lifecycle-governance-platform.md)
