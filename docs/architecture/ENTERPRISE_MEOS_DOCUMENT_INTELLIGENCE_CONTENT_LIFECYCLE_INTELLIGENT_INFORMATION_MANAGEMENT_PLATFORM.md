# MEOS Enterprise Document Intelligence, Content Lifecycle & Intelligent Information Management Platform (MEDCIM)

**Status:** Normative (P308) — series foundation · **Productization & Experience Evolution Phase**  
**SoR:** `document_intelligence_operating` · **ADR:** [665](../adr/665-meos-enterprise-document-intelligence-content-lifecycle-intelligent-information-management-platform.md) · **Capability:** `CAP-PLT-MEDCIM-001`  
**Fabric:** `meos_enterprise_document_intelligence_content_lifecycle_intelligent_information_management_platform_framework` · **Governance Standard:** MEOS 11.0  
> **API:** `/api/v1/document-intelligence-operating*` · **Builds on:** P307 MEKNOL · P306 MEESOP · P305 MEIRRE · P304 MEPOCI · P303 MEPRED · P301 MEPCVA · P299 MEPICO · P294 MENCOE · P270 MEGRSC · P266 MEAAOI · P264 MEKGSI · P260 MEWEOP · P257 MERAF · **Documents** (Document Exchange) · **Enterprise Search** · **Secrets** · Policy · Workflow · Audit · P214-Z · **Next:** P308-A · **Peer series:** [P309 MERILG](ENTERPRISE_MEOS_RECORDS_RETENTION_LEGAL_HOLD_INFORMATION_LIFECYCLE_GOVERNANCE_PLATFORM.md) (delivered) · [P310 MEIGSI](ENTERPRISE_MEOS_INFORMATION_GOVERNANCE_DATA_CLASSIFICATION_SENSITIVE_INFORMATION_INTELLIGENCE_PLATFORM.md) (delivered) · [P311 DLP / Information Protection](ENTERPRISE_MEOS_DATA_LOSS_PREVENTION_INFORMATION_PROTECTION_ADAPTIVE_DATA_SECURITY_CONTROL_PLATFORM.md) (planned)  
**Hard bindings:** Inference → **P214-Z** (ACL; **never module-local LLM**) · Document Exchange blob/version SoR → **Documents** (ACL; **`document_id` / storage abstraction; never fork blob store / hard-code storage vendor as architectural authority**) · Knowledge lifecycle / publication → **P307** (ACL; **P308 = CONTENT · P307 = KNOWLEDGE**; never publish authoritative knowledge without P307 governance) · Knowledge Graph / Semantic → **P264 · P228** (ACL; publish relationships; never fork graph) · Search execution → **Enterprise Search** (ACL; never module-local search) · Workflow execution → **P260** (ACL; approval/review/disposition workflows; never own) · Agent consumption → **P266** (ACL; authorized document context only; never own Agent Runtime) · Governance / classification / retention policy → **P270 · Policy** (ACL; never replace Governance) · Communications → **P294 / Notifications** (ACL; never send channels) · Observability → **P304** (ACL) · Service/Incident attachments → **P306 · P305** (ACL) · Records specialization → **P309** (delivered) · Classification specialization → **P310** (delivered) · DLP/protection → **P311** (planned) · AuthN/AuthZ → **Identity** · Generic → **Core**.

---

## 1. Header

**MARPICH ENTERPRISE PLATFORM (MEOS)** · Master Blueprint · Enterprise Architecture Governance Standard **11.0** · Prompt **P308** · MEOS Enterprise Document Intelligence, Content Lifecycle & Intelligent Information Management Platform (**MEDCIM**).  
**Platform Domain:** MEOS Enterprise Document Intelligence, Content Lifecycle & Intelligent Information Management · **Capability Category:** Document/Content Lifecycle, Intelligent Document Processing, Classification, OCR (pluggable), Metadata Extraction, Versioning, Collaboration, Discovery, Content Governance Coordination, Records/Retention/Legal Hold foundation (deepened by P309), Document Intelligence Copilot, Document-to-Knowledge Candidates · **Strategic Layer:** MEOS Enterprise Content Intelligence Operating Layer.

## 2. Prompt ID

**P308**

## 3. Mission

Create an Enterprise Content Intelligence Platform that makes content:

```
Captured → Classified → Understood → Governed → Discoverable → Secure
→ Traceable → Retainable → Reusable → Transformable into Knowledge
```

**Core content flow:**
```
DOCUMENT / CONTENT → INGESTION → CLASSIFICATION → DOCUMENT UNDERSTANDING
→ METADATA EXTRACTION → VALIDATION → GOVERNANCE → VERSIONING → STORAGE REFERENCE
→ DISCOVERY → COLLABORATION → RETENTION → KNOWLEDGE EXTRACTION
→ P307 KNOWLEDGE → P264 SEMANTIC INTELLIGENCE → P266 AI CONSUMPTION
```

**Boundary law (hard):**
- **P308** = Documents · Content · Document Lifecycle · Document Intelligence · Content Discovery · Collaboration · Document-to-Knowledge Extraction (candidates)
- **Documents** = Document Exchange blob / version storage SoR
- **P307** = Knowledge Lifecycle / Publication · **P264/P228** = Semantic / Graph · **P266** = Agent Orchestration
- **P270** = Governance / Policy authority · **P260** = Workflow execution
- **P309** = Records / Retention / Legal Hold / Information Lifecycle Governance (delivered)
- **P310** = Information Classification / Sensitive Information Intelligence (delivered)
- **P311** = DLP / Information Protection / Adaptive Data Security Control (next)
- P308 may Ingest · Understand · Classify · Version · Coordinate governance states · Discover · Collaborate · Extract knowledge candidates — and must **NOT** Become Knowledge Management · Knowledge Graph · Semantic Engine · Agent Runtime · Workflow Engine · Governance Engine · Process Intelligence · Incident · Service Management · Observability Platform
- Storage provider must remain replaceable (abstraction) · Published versions immutable · AI output clearly identified · AI retrieval must re-evaluate AuthZ + classification + purpose before content enters AI context
- **P308 MUST NOT directly publish authoritative knowledge into P307** without defined governance workflow

MEDCIM owns **document intelligence operating fabric** (Content Center / Author / Governance / Discovery / Records foundation / AI Document Command Centers, content overlays, AI document-assist campaigns); it does **not** own blob storage SoR, knowledge publication, graph, search indices, or agent/workflow engines — and never disposes content under legal hold or outside **Policy + Audit**.

## 4. Architecture Principles

- Enterprise Architecture Governance Standard **11.0** (binding)
- DDD · CQRS · Event Sourcing · Event-Driven · Hexagonal · Clean · API-First · Contract First · Event-First
- Cloud Native · AI Native · Metadata Driven · Configuration Driven · Policy Driven
- Knowledge Graph Compatible · Digital Twin Compatible · Data Mesh Compatible
- Zero Trust · Privacy By Design · Responsible AI · Explainable AI · Human-in-the-Loop · Plugin First
- Multi-Tenant · Immutable Audit · Continuous Governance
- Federate-by-contract only — never peer domain imports / shared tables / local LLM / local search / local graph / vendor-locked storage in domain
- **P308 vs Documents vs P307 vs P264 vs P309:** never merge content intelligence, blob SoR, knowledge OS, semantic graph, and specialized records/ILM SoRs
- Metadata evolves independently from binary content · Encryption at rest/in transit · Tenant isolation default deny cross-tenant
- Pagination mandatory · Fail-closed AuthZ

## 5. Reference Architecture

```
 Content Sources: Applications · Users · External Approved · Workflow Attachments
                                ↓
                         CONTENT INGESTION (security validation)
                                ↓
┌────────────────────────────────────────────────────────────────────┐
│ Document Intelligence Operating Fabric (P308)                      │
│ (SoR document_intelligence_operating)                              │
│ schema: document_intelligence_operating_*                          │
│ Understanding · Classification · Metadata · Lifecycle · Discovery  │
│ Collaboration · Intelligence · Knowledge Candidates                │
└────────────────────────────────────────────────────────────────────┘
        ↓ Storage Abstraction → Documents Exchange (document_id)
        ↓ Search ACL · Collaboration · Records foundation (→ P309)
                                ↓
                 P307 KNOWLEDGE ← candidates · P264 SEMANTICS · P266 AGENTS
```

Content layers: Experience · Discovery · Document Intelligence · Governance · Lifecycle · Records · Repository Abstraction · Integration · Ingestion.

## 6. Core Capabilities

| ID | Capability |
|----|------------|
| MEDCIM-C01 | Document/Content Model · Types · Packages · Workspaces · Relationships |
| MEDCIM-C02 | Ingestion · Storage Abstraction · Integrity Hash · Malware/Security Validation |
| MEDCIM-C03 | Document Understanding · Pluggable OCR · Structure/Entity/Metadata Extraction |
| MEDCIM-C04 | Classification · Versioning · Lifecycle · Review/Approval State Coordination |
| MEDCIM-C05 | Collaboration · Comparison · Discovery · Search (via Enterprise Search + P264) |
| MEDCIM-C06 | Content Quality · Duplicate/Contradiction/Stale Detection · Gap Analysis |
| MEDCIM-C07 | Records/Retention/Legal Hold foundation (execution deepens in **P309**) |
| MEDCIM-C08 | Document Intelligence · Contract/Policy Document Intelligence (doc-only) |
| MEDCIM-C09 | Document-to-Knowledge Candidates → P307 · Impact Analysis · Analytics |
| MEDCIM-C10 | AI Document Copilot · Authorized Retrieval · Source Attribution |
| MEDCIM-C11 | Content Center UX · Governance / Records / AI Workspaces |
| MEDCIM-C12 | MEDCIM Governance Kernel |

### Notes

Contract/Policy document intelligence extracts facts only — contract lifecycle / policy authority remain owning domains / P270.  
OCR engines replaceable via adapters.  
Disposition irreversible only under Policy + Legal Hold check + Audit.  
Specialized defensible disposition / ILM analytics owned by **P309** (delivered).

## 7. User Experience Architecture

```
Human → Enterprise Content Center → Document Experience · Author Workspace
→ Governance · Discovery · Records foundation · AI Document Workspace · Command Palette
```

AI answers must include Source · Document · Version · Location · Confidence.  
Commands: Upload · Create · Search · Compare · Related · Review · Approve · Expiring · Legal Hold · Ask AI · Knowledge Candidate.

## 8. Application Runtime Model

```
Source → Ingest → Security Validation → Type Detection → Extract → Classify
→ Governance Validation → Lifecycle → Index (Search) → Discover/Collaborate
→ Knowledge Candidate → P307

AI: AuthZ → Classification → Purpose → Policy → Context → Response + Attribution
```

States: DRAFT · IN_PROCESSING · PROCESSING_FAILED · IN_REVIEW · PENDING_APPROVAL · PUBLISHED · ACTIVE · SUPERSEDED · DEPRECATED · ON_HOLD · ARCHIVED · DISPOSED.

**Hard runtime rule:** Binary content via **Documents** storage abstraction; workflows via **P260**; policy via **P270**; knowledge publication via **P307**; graph via **P264**; agents via **P266**; notifications via **P294**.

## 9. AI Agents

P308 does **not** replace P266. P308 defines Document Intelligence Agents.

| Agent | Role | Gate |
|-------|------|------|
| Document Classification Agent | Type · category · retention class · security | Governed authority |
| Document Extraction Agent | Metadata · entities · dates · sections · tables | — |
| Document Quality Agent | Completeness · freshness · metadata · consistency | Explainable |
| Document Review Agent | Approve / reject / update / reclassify / escalate | Human authoritative |
| Document Search Agent | Semantic/contextual retrieval | Search + AuthZ |
| Document Synthesis Agent | Multi-doc summary | Source attribution |
| Document Comparison Agent | Version/related diffs | — |
| Content Gap Agent | Missing · zero-result · evidence gaps | — |
| Document Impact Agent | Affected processes/services/policies/knowledge | — |
| Retention Agent | Review / retain / archive / dispose recommendations | Cannot bypass Legal Hold/Policy |
| Knowledge Extraction Agent | FAQ/procedure/lesson candidates | P307 publishes |
| Document Copilot | Q&A · summarize · extract · classify · recommend | Attribution · AuthZ |

**Law:** Agents assist; high-impact disposition/hold requires governance; never module-local LLM; never channel send; never put unauthorized content into AI context.

## 10. Domain Driven Design (DDD)

**Core domain:** MEOS Enterprise Document Intelligence, Content Lifecycle & Intelligent Information Management (operating)  
**Strategic type:** Supporting Domain (platform / content intelligence)

### Bounded Contexts (logical; single SoR `document_intelligence_operating`)

| BC | Name | Aggregate root |
|----|------|----------------|
| BC-01 | Document Repository / Lifecycle Operating | `DocumentCampaignAggregate` |
| BC-02 | Document Intelligence / Processing Operating | `DocumentIntelligenceCampaignAggregate` |
| BC-03 | Content Governance / Review Operating | `ContentGovernanceCampaignAggregate` |
| BC-04 | Content Discovery / Collaboration Operating | `ContentDiscoveryCampaignAggregate` |
| BC-05 | Records / Hold / Disposition Foundation Operating | `RecordsFoundationCampaignAggregate` |
| BC-06 | Content Quality / Intelligence / Knowledge Candidate Operating | `ContentIntelligenceCampaignAggregate` |

### Aggregates

**Document:** Versions · Metadata · Classification · Lifecycle · References · Security · Retention  
**DocumentReview:** Reviewers · Findings · Comments · Decision  
**ContentPackage:** Documents · Metadata · Relationships · Lifecycle  
**LegalHold:** Scope · Documents · Custodians · Status · Audit  
**Disposition:** EligibleContent · Policy · Approval · Execution

### Value Objects

`DocumentOperatingId` · `DocumentIdRef` · `VersionId` · `ContentHash` · `MimeType` · `Classification` · `Sensitivity` · `RetentionClass` · `LegalHoldId` · `DispositionId` · `QualityScore` · `ExtractionResult` · `KnowledgeCandidateId` · `TraceId` · `StorageAdapterRef` · `DoAThreshold` · `TenantScope`

### Domain Services

`DocumentRepositoryService` · `ContentIngestionService` · `DocumentProcessingService` · `OCRAdapterService` · `DocumentUnderstandingService` · `DocumentClassificationService` · `MetadataExtractionService` · `DocumentVersionService` · `DocumentLifecycleService` · `DocumentReviewService` · `DocumentApprovalService` · `ContentGovernanceService` · `ContentSecurityService` · `ContentSearchService` · `SemanticContentService` · `ContentRelationshipService` · `ContentQualityService` · `ContentDuplicateService` · `ContentContradictionService` · `ContentFreshnessService` · `RecordsManagementService` · `RetentionService` · `LegalHoldService` · `DispositionService` · `ContentCollaborationService` · `ContentPackageService` · `DocumentIntelligenceService` · `DocumentComparisonService` · `ContentImpactService` · `ContentAnalyticsService` · `KnowledgeExtractionService` · `DocumentCopilotService`

**Hard separation:** Blobs/versions in Documents Exchange; knowledge publication in P307; graph in P264/P228; search in Enterprise Search; workflow in P260; agents in P266; policy in P270; specialized ILM in P309; MEDCIM stores intelligence/lifecycle campaigns, metadata overlays, candidate extractions and `document_id` refs only — never dual-write Documents blob tables as a second SoR.

## 11. Event Architecture

### Domain Events

`DocumentCreated` · `DocumentIngested` · `DocumentProcessingStarted` · `DocumentProcessingCompleted` · `DocumentProcessingFailed` · `DocumentClassified` · `DocumentMetadataExtracted` · `DocumentValidated` · `DocumentSubmittedForReview` · `DocumentReviewStarted` · `DocumentApproved` · `DocumentRejected` · `DocumentPublished` · `DocumentVersionCreated` · `DocumentSuperseded` · `DocumentDeprecated` · `DocumentArchived` · `DocumentMarkedForRetention` · `DocumentRetentionUpdated` · `LegalHoldCreated` · `LegalHoldApplied` · `LegalHoldReleased` · `DispositionRequested` · `DispositionApproved` · `DocumentDisposed` · `DocumentOwnerChanged` · `DocumentClassificationChanged` · `DocumentAccessed` · `DocumentShared` · `DocumentDownloaded` · `DocumentCommentAdded` · `DocumentAnnotationAdded` · `DocumentDuplicateDetected` · `DocumentContradictionDetected` · `DocumentMarkedStale` · `DocumentImpactDetected` · `ContentGapDetected` · `KnowledgeCandidateCreatedFromDocument` · `DocumentInsightGenerated` · `DocumentRiskDetected` · `DocumentObligationDetected` · `DocumentSearchPerformed` · `DocumentSearchFailed` · `DocumentCompared` · `DocumentRelationshipCreated` · `DocumentIntelligenceGateApplied`

### Event Flow

`Ingest → Process → Classify → Validate → Review/Approve → Publish → Index → Discover → Knowledge Candidate → P307`  
Consumers: P257 · P260 · P264 · P266 · P270 · P294 · P299 · P301 · P303 · P304 · P305 · P306 · P307 · P309 · P310 · P311 (planned) · Documents · Search · Audit

Envelope + outbox + idempotent ACL consumers mandatory. Publish/dispose/hold events carry AuthZ + Policy + DocumentId + Version + Hash + TraceId.

## 12. CQRS

### Commands

`CreateDocumentCommand` · `UploadDocumentCommand` · `IngestDocumentCommand` · `ProcessDocumentCommand` · `ClassifyDocumentCommand` · `ExtractMetadataCommand` · `ValidateDocumentCommand` · `CreateDocumentVersionCommand` · `SubmitDocumentReviewCommand` · `ApproveDocumentCommand` · `RejectDocumentCommand` · `PublishDocumentCommand` · `SupersedeDocumentCommand` · `DeprecateDocumentCommand` · `ArchiveDocumentCommand` · `CreateLegalHoldCommand` · `ApplyLegalHoldCommand` · `ReleaseLegalHoldCommand` · `CreateRetentionPolicyCommand` · `MarkForDispositionCommand` · `ApproveDispositionCommand` · `DisposeDocumentCommand` · `CreateCommentCommand` · `CreateAnnotationCommand` · `ShareDocumentCommand` · `CreateContentPackageCommand` · `CreateKnowledgeCandidateCommand` · `CreateDocumentImpactAnalysisCommand` · `ReportDocumentIssueCommand` · `ApplyDocumentIntelligenceGateCommand`

(Binary persist via Documents adapters; workflows via P260; authoritative knowledge via P307.)

### Queries

`GetDocumentQuery` · `GetDocumentVersionQuery` · `SearchDocumentsQuery` · `SemanticDocumentSearchQuery` · `GetDocumentMetadataQuery` · `GetDocumentClassificationQuery` · `GetDocumentLifecycleQuery` · `GetDocumentReviewQuery` · `GetDocumentApprovalQuery` · `GetDocumentRelationsQuery` · `GetRelatedDocumentsQuery` · `GetDocumentHistoryQuery` · `GetDocumentQualityQuery` · `GetDocumentTrustQuery` · `GetDocumentUsageQuery` · `GetRetentionStatusQuery` · `GetLegalHoldQuery` · `GetDispositionQuery` · `GetContentGapQuery` · `GetDocumentInsightsQuery` · `GetDocumentObligationsQuery` · `GetDocumentRisksQuery` · `GetDocumentKnowledgeCandidatesQuery` · `GetDocumentImpactQuery` · `GetContentAnalyticsQuery`

Read models under `document_intelligence_operating_*` only; pagination mandatory; fail-closed AuthZ.

## 13. MEOS Integration

| Peer | Mode |
|------|------|
| **Documents** | Blob/version SoR · storage adapters — never fork |
| **P307** | Knowledge candidates only — never auto-publish knowledge |
| **P264 · P228** | Entity/relationship publish · semantic resolution |
| **Enterprise Search** | Index/query execution |
| **P260 · P266 · P270 · P294** | Workflow · agent context · policy · notifications |
| **P305 · P306** | Incident/service evidence attachments |
| **P299 · P301 · P303 · P304** | Process docs · composition refs · change impact · telemetry |
| **P309** | Records / Retention / Legal Hold / ILM (delivered; distinct) |
| **P310** | Information Classification / Sensitive Intelligence (delivered; distinct) |
| **P311** | DLP / Information Protection / Adaptive Data Security (planned) |
| Audit · Identity · Secrets · Core | Evidence · AuthZ · secret refs · generic |

Permissions: `document_intelligence_operating.content.*` · `document_intelligence_operating.lifecycle.*` · `document_intelligence_operating.intelligence.*` · `document_intelligence_operating.governance.*` · `document_intelligence_operating.discovery.*` · `document_intelligence_operating.records.*` · `document_intelligence_operating.knowledge_candidate.*` · `document_intelligence_operating.ai.read` · `document_intelligence_operating.ai.infer`.

## 14. Storage Architecture

P308 MUST implement a **Storage Abstraction Layer**. Domain never depends on a specific storage vendor. Adapters may target Object / File / Enterprise Content Repository / Cloud / On-Prem storage via Documents Exchange.

Content storage model: Metadata + Content Reference (`document_id`) + Integrity Hash + Version Reference + Security Classification + Retention Metadata — metadata and binary evolve independently.

## 15. Security Architecture

Zero Trust content access: Identity → Tenant → Authorization → Classification → Context Policy → Purpose → Access Decision → Audit.  
AI retrieval must evaluate User Identity + Tenant + Document Authorization + Classification + Purpose + Policy before content enters AI context.  
Controls: Encryption at rest/in transit · RBAC/ABAC · Tenant isolation · Watermarking · Download/share controls · Immutable audit · Privacy.

## 16. Implementation Roadmap

| Phase | Focus | Window | Deliverables |
|-------|-------|--------|--------------|
| **P308** | Foundation | — | ADR · capability · fabric · DDD/CQRS · API skeleton · dual tests |
| **Phase 1 / P308-A** | Content Foundation | 3–6 mo | Document model · metadata · repository abstraction · versioning · lifecycle · ownership |
| **Phase 2 / P308-B** | Document Ingestion | 6–12 mo | Upload · API · email · scanner · storage adapters |
| **Phase 3 / P308-C** | Document Intelligence | 9–15 mo | OCR adapter · text/structure · classification · metadata extraction |
| **Phase 4 / P308-D** | Content Governance | 12–18 mo | Classification · retention foundation · legal hold foundation · approval · audit |
| **Phase 5 / P308-E** | Document Experience | 15–24 mo | Viewer · authoring · collaboration · comparison · workspaces |
| **Phase 6 / P308-F** | Content Discovery | 18–30 mo | Search · faceted · semantic · similar · related |
| **Phase 7 / P308-G** | Records Foundation | 24–36 mo | Records · retention · disposition · legal hold · archive (→ P309 specialize) |
| **Phase 8 / P308-H** | Advanced Intelligence | 30–42 mo | Entity · obligation · risk · contradiction · duplicate |
| **Phase 9 / P308-I** | P307 Knowledge Integration | 36–48 mo | Candidate pipeline · attribution · knowledge impact |
| **Phase 10 / P308-J** | P264 Semantic Integration | 42–54 mo | Entity linking · content graph refs · concept discovery |
| **Phase 11 / P308-K** | P266 AI Integration | 48–60 mo | Copilot · Q&A · summarization · grounding · attribution |
| **Phase 12 / P308-L** | Autonomous Content Intelligence | 54–66 mo | Stale/duplicate/gap/retention candidates (human-gated high-impact) |

Catalogs (planned): `docs/architecture/document_intelligence_operating/MEDCIM_*_{CAPABILITIES,DDD_CQRS,SECURITY,VALIDATION,ARCHITECTURE}.v1.yaml`

## 17. Quality Gates

- Never Document Model / Lifecycle / Intelligence / Discovery / Governance capabilities are missing
- Never Sibling Document Intelligence Operating BC (second deployable)
- Never Replace **Documents** · **P307** · **P264/P228** · **Search** · **P266** · **P260** · **P270** · **P309** · Workflow · Core · AI
- Never Dual-write Documents blob tables as second SoR · Never Vendor-lock storage in domain · Never Local search/graph/LLM
- Never Become Knowledge / Graph / Agent / Workflow / Governance / Incident / Service Ops / Observability Engine
- Never Auto-publish authoritative knowledge · Never Dispose under Legal Hold · Never AI retrieval without AuthZ+classification+purpose
- Published versions immutable · TraceId on processing · Tenant isolation · Immutable audit

Validate: Document intelligence OS · DDD · CQRS · events · Documents/P307/P264/P260 boundaries · portals · AI copilot.

## 18. Definition of Done

- [ ] ADR **665** accepted; capability `CAP-PLT-MEDCIM-001` registered
- [ ] Law + YAML catalogs under `docs/architecture/document_intelligence_operating/`
- [ ] Context `backend/contexts/document_intelligence_operating/` scaffolded
- [ ] Fabric wired + ACL to Documents, P307, P264, Search, P260, P266, P270, P294, Policy
- [ ] Outbox events + ACL stubs (Documents · P307 · P264 · P260 · P294 · P270 · P214-Z · Audit)
- [ ] Dual tests green; scorecard **ENTERPRISE_GRADE**
- [ ] OpenAPI `/api/v1/document-intelligence-operating*`
- [ ] Gated ingest→understand→govern→discover→knowledge-candidate path demonstrated (no parallel blob/knowledge/graph engines)
- [ ] **P308-A** unlocked · **P309** MERILG · **P310** MEIGSI delivered · **P311** DLP / Information Protection / Adaptive Data Security Control series unblocked

**MEDCIM is complete when:** MEOS has an Enterprise Content Intelligence Operating Layer; ingestion, understanding, lifecycle, discovery, collaboration, intelligence and knowledge-candidate pipelines operate under gates; Documents remains blob SoR; P307 remains knowledge publication; P264 remains semantic/graph; storage providers remain replaceable; events join the Event Mesh — Governance Standard **11.0**.

**Architectural boundary guarantee:** MEDCIM must not re-own Documents blob SoR, P307 Knowledge, P264 Graph, P266 Agents, P260 Workflow, P270 Governance, P305/P306, or P309 specialized ILM as a merge. MEDCIM owns Enterprise Documents/Content Intelligence, Document Lifecycle, Discovery, Collaboration, Records foundation, Retention/Legal Hold foundation execution coordination and Document-to-Knowledge Extraction only.

**Principle:** MEDCIM productizes document intelligence and content lifecycle; it never replaces Documents/P307/P264, never dual-writes peer blob/knowledge/graph tables, never embeds local LLMs, and never disposes or AI-grounds content without Policy + AuthZ + Audit accountability.

---

**NEXT EXECUTION:** **P311** — MEOS Enterprise Data Loss Prevention, Information Protection & Adaptive Data Security Control Platform — convert P310 Classification/Sensitivity into operational Data Protection and DLP controls (Prevent / Allow / Block / Quarantine / Redact) under Policy + Context + Risk (federate P310, P268, P269, P270, P260; never fork Classification Intelligence or Cybersecurity; never create parallel mesh/content/records/workflow/agent engines).

> **P308 delivered:** this law · [ADR 665](../adr/665-meos-enterprise-document-intelligence-content-lifecycle-intelligent-information-management-platform.md)
