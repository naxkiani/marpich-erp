# Enterprise Identity Digital Twin Platform — Architecture Law

**Prompt:** V03-C02-P199-A · Volume 03 · Chapter 02  
**Governance:** Enterprise Architecture Governance 10.0  
**Status:** Canonical — production architecture (not a demo brief)  
**ADR:** [ADR-203](../adr/203-enterprise-identity-digital-twin.md) · [ADR-203a](../adr/203a-digital-twin-type-catalog.md) · Sync [ADR-207](../adr/207-twin-synchronization-engine-event-mesh.md) · Intelligence [ADR-208](../adr/208-twin-ai-intelligence-platform.md) · Ops [ADR-209](../adr/209-twin-platform-engineering-devsecops.md)  
**Owner context:** `backend/contexts/identity_digital_twin/` · schema `identity_twin` · API `/api/v1/identity-twins`  
**Intelligence law:** [ENTERPRISE_TWIN_AI_INTELLIGENCE_PLATFORM.md](ENTERPRISE_TWIN_AI_INTELLIGENCE_PLATFORM.md) (Prompt 199-C)  
**Platform Engineering / DevSecOps:** [ENTERPRISE_TWIN_PLATFORM_ENGINEERING.md](ENTERPRISE_TWIN_PLATFORM_ENGINEERING.md) (Prompt 199-D1)  
**Observability / IR / BCP / DR:** [ENTERPRISE_TWIN_OBSERVABILITY_IR_BCP_DR.md](ENTERPRISE_TWIN_OBSERVABILITY_IR_BCP_DR.md) (Prompt 199-D2.2 · ADR-210)

**Law:** A Digital Twin is an eventually consistent, tenant-isolated **projection**. Source bounded contexts remain authoritative. Twins never replace Core Identity, Authorization, Policy, Consent, Audit, or industry modules. Twin kinds, states, sync rules, and prediction policies are **catalog- and policy-driven** — never hardcoded.

---

## Architecture decision (hard stop)

| Decision | Rationale |
|----------|-----------|
| **One Twin Platform BC** | Separate BCs per industry twin (BankTwin, HospitalTwin, …) would create parallel platforms and cross-domain coupling |
| **Configurable `twin_kind` catalog** | Users, devices, orgs, AI agents, hospitals… are **kinds** in one registry, not separate schemas |
| **Reference-only storage** | Store `subject_ref` / peer IDs + facet JSON; never peer aggregates or cross-schema JOINs |
| **State facets as projections** | Trust, risk, compliance, security, behavior, operational facets are fed by owning platforms via events |
| **Simulation non-mutating** | Predictions/simulations never write authoritative state |
| **AI via AI Platform only** | No embedded LLM clients in the twin context |

---

## SECTION 1 — Business objectives

### 1.1 Business capability map

| Cap ID | Capability | Description |
|--------|------------|-------------|
| CAP-PLT-TWIN-001 | Twin Registry | Register, discover, classify twins by kind |
| CAP-PLT-TWIN-002 | Continuous Synchronization | Event-driven projection sync from source SoR |
| CAP-PLT-TWIN-003 | Twin History & Versioning | Snapshots, versions, time-travel read models |
| CAP-PLT-TWIN-004 | Twin Prediction | Future-state forecasts via AI Platform |
| CAP-PLT-TWIN-005 | Twin Simulation | Non-mutating what-if (access, lifecycle, risk) |
| CAP-PLT-TWIN-006 | Twin Health & Drift | Health scores + divergence from source |
| CAP-PLT-TWIN-007 | Twin Relationship Graph | Typed edges between twins (org→user, device→session) |
| CAP-PLT-TWIN-008 | Twin Governance | Policies, retention, archival, deletion workflow |
| CAP-PLT-TWIN-009 | Twin Security & Trust Facets | Consume Risk / AuthZ / Consent / Compliance signals |
| CAP-PLT-TWIN-010 | Twin Analytics & KPI | Adoption, sync lag, drift rate, prediction accuracy |

### 1.2 Business services

| Service | Consumer | SLA focus |
|---------|----------|-----------|
| Twin Registry API | Modules, Admin UI, AI | Availability |
| Sync Fabric (event ACL) | All source contexts | At-least-once + idempotent |
| Simulation Sandbox | Security, IAM ops, AI | Isolation / no side effects |
| Prediction Facet | Adaptive Auth, Risk, CFO/AI packs | Freshness SLO |
| Drift & Health Monitor | Ops, Security, Compliance | Detection latency |
| Relationship Graph Query | Search, Authorization explain, BI | Tenant isolation |

### 1.3 Business goals

1. Every active principal and operational entity has a discoverable twin within **T+5m** of creation events.  
2. Sync p95 lag ≤ **30s** under normal load; alert at **2m**.  
3. Zero twin writes to peer domain schemas.  
4. 100% high-risk decisions (AuthZ obligations, Adaptive Auth, DSAR erase) can query twin facets without peer DB access.  
5. Simulations never mutate SoR; prediction confidence always explainable via AI Platform.

### 1.4 Business processes

```text
Onboard subject → Source SoR create → Event → TwinCreate/Upsert
                                         → Facet sync loop
                                         → Health baseline
Change in SoR → Event → TwinSynchronize → Snapshot → Drift check
What-if        → TwinSimulate (non-mutating) → Audit event
Predict        → AI Platform job → TwinPrediction facet
Compromise     → Risk/Security event → TwinCompromised facet + alert
Offboard       → Lifecycle archive → TwinArchive → Retention → Delete (workflow)
```

### 1.5 Business KPIs & success metrics

| KPI | Target (Y1) |
|-----|-------------|
| Twin coverage (% eligible subjects with active twin) | ≥ 98% |
| Sync lag p95 | ≤ 30s |
| Drift open critical age | ≤ 4h to acknowledge |
| Simulation volume without SoR mutation | 100% |
| False-positive drift rate | ≤ 5% after tuning |
| Twin-powered AuthZ/Adaptive decisions | ≥ 40% of high-risk checks |

### 1.6 Business policies (Policy Engine keys — examples)

| Policy key | Purpose |
|------------|---------|
| `twin.enabled` | Master switch |
| `twin.kinds.{kind}.enabled` | Per-kind activation |
| `twin.sync.max_lag_seconds` | Sync SLO / alerting |
| `twin.simulation.enabled` | Simulation gate |
| `twin.prediction.enabled` | Prediction gate |
| `twin.drift.threshold` | Drift field count / severity |
| `twin.retention.snapshot_days` | History retention |
| `twin.shared_scope.allowed` | Cross-org / partner visibility |
| `twin.deletion.workflow_required` | Governed erase |

### 1.7 Adoption strategy

| Phase | Scope | Outcome |
|-------|-------|---------|
| P0 | Identity / user / session / device twins | IAM operational twin |
| P1 | Org / tenant / role / permission / certificate / API client | Platform graph |
| P2 | AI agent / application / service twins | Zero-trust machine identity |
| P3 | Industry kinds (bank, branch, hospital, university, tax authority) via industry event packs | Vertical coverage |
| P4 | Cross-org / partner / regional / global shared projections | Ecosystem |

### 1.8 ROI model (qualitative → measurable)

| Value lever | Mechanism | Evidence |
|-------------|-----------|----------|
| Faster IAM incident response | Single projection + drift | MTTR ↓ |
| Safer change | Simulation before SoR mutate | Change-fail ↓ |
| Better AuthZ / Adaptive Auth | Trust/risk facets without peer JOINs | False deny/allow ↓ |
| Compliance readiness | Snapshot history + audits | Audit finding ↓ |
| AI readiness | Declared foresight surfaces | Feature cycle time ↓ |

### 1.9 Enterprise value map

```text
Customers (security/compliance) ← Twin Health + Drift + Consent facets
Operators (IAM/SecOps)         ← Registry + Sync + Graph + Simulation
Product modules                 ← Check twin facets via API/events (not peer DB)
Platform Core                   ← Events, Policy, AI, Audit, Search, Workflow
Industry packs                  ← Publish subject events; twin projects kinds
```

---

## SECTION 2 — Digital twin types (catalog-driven)

Kinds are **metadata** (`TwinKindDefinition`), seeded per industry pack / tenant activation — **not** Python enums baked into Core.

### 2.1 Platform kinds

| Kind | Subject SoR | Primary facets |
|------|-------------|----------------|
| `identity.user` | identity | attributes, roles, lifecycle, trust, risk |
| `identity.employee` | hr / identity | employment, org unit refs |
| `identity.student` | university / school | enrollment refs |
| `identity.customer` | crm | segment, consent prefs |
| `identity.patient` | hospital / clinic | care relationship refs (no PHI blob) |
| `identity.citizen` | government | citizen case refs |
| `organization` | organization | units, status |
| `department` | organization | parent org |
| `branch` | banking / retail | branch ops status |
| `tenant` | core_platform | pack activation, region |
| `device` | mfa / devices | trust, posture |
| `browser` | session / device | fingerprint refs |
| `session` | identity / auth | absolute expiry ref only |
| `application` | apps / OAuth clients | client_id refs |
| `service` | platform services | service account refs |
| `api_client` | OAuth / API keys | scopes metadata (no secrets) |
| `certificate` | PKI / federation | cert fingerprint refs |
| `role` | permission_registry | permission set hashes |
| `permission` | permission_registry | code, risk tier |
| `ai_agent` | ai / ai_governance | model approval refs |
| `iot_device` | integrations | device registry refs |

### 2.2 Industry kinds (event packs)

| Kind | Owning industry context | Notes |
|------|-------------------------|-------|
| `bank` | banking | Institution projection |
| `currency_exchange` | currency_exchange | Exchange entity |
| `university` | university | Institution |
| `hospital` | hospital | Facility |
| `government_agency` | government | Agency |
| `tax_authority` | tax | Authority node |

### 2.3 Lifecycle (every kind)

`discovered|created → registered → active → synchronized ↔ predicted/simulated → suspended|compromised → archived → recovered|deleted`

State transitions are **policy-validated** and emit integration events. Physical/logical deletion requires Workflow when `twin.deletion.workflow_required`.

---

## SECTION 3 — Twin lifecycle capabilities

| Stage | Mechanism |
|-------|-----------|
| Creation | Command `CreateTwin` or ACL on SoR create event |
| Registration | Kind validation against catalog; subject uniqueness `(tenant, kind, subject_ref)` |
| Discovery | Query registry by kind/facet/tags; Search platform index |
| Synchronization | `SynchronizeTwin` from event projection; idempotent by `(tenant, event_id, consumer)` |
| Versioning | Immutable `TwinVersion` + `TwinSnapshot` on significant sync |
| State changes | Facet merges; never delete history mid-retention |
| Prediction | AI Platform job → `TwinPrediction` record |
| Simulation | Deterministic engine; outcome only; `mutation_applied=false` |
| Health monitoring | Lag, completeness, drift severity → `TwinHealth` |
| Archiving | Soft archive + cold snapshot policy |
| Recovery | Rehydrate from snapshots + event replay |
| Deletion | Workflow + purge job; publish `identity_twin.deleted` |

---

## SECTION 4 — Domain model

### 4.1 Bounded contexts (modular monolith modules within platform BC — logical packs)

| Logical pack | Responsibility | Implementation note |
|--------------|----------------|---------------------|
| Twin Registry | Kind catalog, twin roots | Same BC, `domain/` |
| Twin Synchronization | ACL + sync engine | `application` + ACL handlers |
| Twin Analytics | Dashboard KPIs | Queries + Analytics events |
| Twin Prediction | Prediction records | Orchestrates AI Platform |
| Twin Governance | Retention, archive, delete | Policy + Workflow |
| Twin Security | Compromised/trust facets | Consumes Risk/AuthZ/Consent |
| Twin Simulation | Sandbox | Non-mutating domain service |

**Forbidden:** cross-import of `contexts.hospital.domain`, etc.

### 4.2 Aggregates

| Aggregate | Root ID | Invariants |
|-----------|---------|------------|
| `DigitalTwin` | `twin_ref` | Unique `(tenant, kind, subject_ref)`; no secrets |
| `TwinKindDefinition` | `kind` | Versioned catalog entry |
| `TwinSnapshot` | `snapshot_ref` | Immutable |
| `TwinVersion` | `(twin_ref, version)` | Monotonic |
| `TwinRelationship` | `edge_ref` | Typed, directional, tenant-scoped |
| `TwinHealth` | `twin_ref` | Derived score |
| `TwinRiskFacet` / `TwinTrustFacet` | `twin_ref` | From Risk/Trust events only |
| `TwinPrediction` | `prediction_ref` | Explanation refs mandatory |
| `TwinSimulation` | `simulation_ref` | Non-mutating |
| `TwinDriftAlert` | `alert_ref` | Evidence only |
| `TwinPolicyBinding` | binding id | Points to Policy Engine keys |
| `TwinAuditPointer` | n/a | Prefer Audit platform; local append-only only if outbox lag buffer |

### 4.3 Entities / value objects

- VO: `TwinKind`, `SubjectRef`, `FacetMap`, `SourceVersionMap`, `HealthScore`, `DriftField`, `GraphEdgeType`, `PredictionHorizon`
- Entity: `TwinFacetState` (current facet blob with schema version)

### 4.4 Ports / repositories

`IDigitalTwinRepository`, `ITwinKindRepository`, `ITwinSnapshotRepository`, `ITwinVersionRepository`, `ITwinRelationshipRepository`, `ITwinHealthRepository`, `ITwinPredictionRepository`, `ITwinSimulationRepository`, `ITwinDriftAlertRepository`

### 4.5 Commands / queries

**Commands:** `CreateTwin`, `RegisterKind`, `SynchronizeTwin`, `RecordFacet`, `RunSimulation`, `RequestPrediction`, `ArchiveTwin`, `RecoverTwin`, `DeleteTwin`, `UpsertRelationship`, `RaiseCompromise`  
**Queries:** `GetTwin`, `ListTwinsByKind`, `GetDashboard`, `GetHistory`, `GetGraphNeighborhood`, `GetHealth`, `GetPrediction`, `ExplainDrift`

### 4.6 Domain / integration events

See Section 6. Domain events stay inside the BC; integration events cross the fabric.

---

## SECTION 5 — Database design (PostgreSQL)

Schema: `identity_twin` only. All tables: `tenant_id` NOT NULL + RLS.

### 5.1 Tables (canonical)

| Table | Purpose |
|-------|---------|
| `twin_kinds` | Catalog of kinds + JSON schema versions |
| `digital_twins` | Twin roots (`kind`, `subject_ref`, lifecycle) |
| `twin_states` | Current facet map (JSONB) |
| `twin_snapshots` | Point-in-time projections |
| `twin_versions` | Monotonic version metadata |
| `twin_events` | Local outbox / replay cursor (production uses platform outbox) |
| `twin_relationships` | Graph edges |
| `twin_metadata` | Tags, labels, classification |
| `twin_health` | Health scores / lag |
| `twin_risk` | Risk facet projection |
| `twin_trust` | Trust facet projection |
| `twin_predictions` | Prediction outcomes |
| `twin_policies` | Cached policy binding snapshots (evaluate via Policy Engine) |
| `twin_audits` | Optional hot buffer — durable audit remains Audit Platform |
| `twin_simulations` | Simulation outcomes |
| `twin_drift_alerts` | Open/closed drift |

### 5.2 Indexes (mandatory patterns)

- `(tenant_id, twin_ref)` unique  
- `(tenant_id, kind, subject_ref)` unique  
- `(tenant_id, kind, updated_at DESC)`  
- `(tenant_id, twin_ref, captured_at DESC)` on snapshots (partition candidate)  
- GIN on facet JSONB paths used in filters  

### 5.3 Partitioning

- `twin_snapshots`, `twin_predictions`, `twin_events` → RANGE by `captured_at` / month  
- High-volume tenants: hash sub-partition by `tenant_id` when > threshold (ops policy)

### 5.4 Encryption / RLS

- TLS in transit; AES-256 at rest (platform storage)  
- No raw secrets/tokens/PHI in JSONB (refs only)  
- RLS: `tenant_id = current_setting('app.tenant_id')`  
- Column encryption optional for sensitive attribute bags via Data Protection

### 5.5 Migrations

Baseline: `029_enterprise_identity_digital_twin.sql`  
Expansion: `031_enterprise_identity_digital_twin_p199a.sql` (kinds, facets, graph, health, risk, trust, predictions, policies)

---

## SECTION 6 — Event model

### 6.1 Integration events (publish)

| Event | When |
|-------|------|
| `identity_twin.created` | Twin root created |
| `identity_twin.updated` | Facet/state update |
| `identity_twin.deleted` | Governed deletion |
| `identity_twin.synchronized` | Sync from source event |
| `identity_twin.predicted` | Prediction recorded |
| `identity_twin.compromised` | Security/risk compromise facet |
| `identity_twin.recovered` | Recovery from archive/compromise |
| `identity_twin.archived` | Soft archive |
| `identity_twin.activated` | Return to active |
| `identity_twin.suspended` | Suspended |
| `identity_twin.simulation.completed` | Simulation done |
| `identity_twin.drift.detected` | Drift open |

Envelope: standard Event Fabric fields (`tenant_id`, `correlation_id`, `event_id`, …).

### 6.2 Consumes (ACL)

`identity.*`, `federation.*`, `lifecycle.*`, `identity_risk.*`, `authorization.*` (facet only), `consent.*` / `privacy.*`, `organization.*`, industry packs (`banking.*`, `hospital.*`, …) — **payload ACL only**.

### 6.3 Kafka topics (enterprise profile)

| Topic | Event family |
|-------|--------------|
| `marpich.twin.lifecycle.v1` | created/updated/deleted/archived/activated/suspended/recovered |
| `marpich.twin.sync.v1` | synchronized |
| `marpich.twin.intelligence.v1` | predicted, simulation.completed, drift.detected |
| `marpich.twin.security.v1` | compromised |

Contracts: `docs/architecture/identity/DIGITAL_TWIN_EVENT_CONTRACTS.v1.yaml`

---

## SECTION 7 — Multi-tenancy scopes

| Scope | Meaning | Control |
|-------|---------|---------|
| Tenant isolation (default) | Twin visible only in owning tenant | RLS + API |
| Shared twins | Read-only projection shared to linked tenants | Policy `twin.shared_scope.allowed` + explicit grants |
| Cross-organization | Org A twin edges readable by Org B under grant | Org graph + AuthZ |
| Partner twins | External partner subject refs | Partner federation + Consent |
| Regional twins | Region-tagged twins for residency | Metadata + region policy |
| Global twins | Platform-level kinds (careful) | Super-tenant / control plane only; rare |

**Never** loosen RLS in application code for convenience.

---

## SECTION 8 — Architecture principles (checklist)

| Principle | Enforcement |
|-----------|-------------|
| DDD | One BC; aggregates; no peer domain imports |
| CQRS | Commands mutate projections; queries separate dashboards |
| Hexagonal | Ports in domain; adapters in infrastructure |
| Event-driven | Sync only via events + ACL |
| Cloud native | Stateless API, Postgres, Redis cache optional, Kafka topics |
| API first | OpenAPI under `/api/v1/identity-twins` |
| Plugin first | Twin kind plugins / industry packs via Plugin + catalog |
| Metadata-driven | Kind schemas in `twin_kinds` |
| Configuration-driven | Settings for lag, retention |
| Policy-driven | All gates via Policy Engine |
| AI native | 14 AI surfaces declared; AI Service only |
| Zero Trust | AuthN+AuthZ on every route; no secret in twin |
| Digital Twin native | Every eligible subject eventual twin |

### Never hardcode

Twin types · twin policies · twin states · twin rules · synchronization mapping → **catalog + Policy + versioned ACL mappers**.

---

## Implementation status vs P199-A / P199-B

| Area | Status |
|------|--------|
| Identity twin core (create/sync/simulate/drift) | ✅ Implemented |
| Kind catalog + multi-subject kinds | 📋 Architecture (ADR-203a) — incremental delivery |
| Full facet tables (risk/trust/health/predictions/graph) | 📋 Schema in migration `031` |
| Industry kind packs | 📋 Event pack design |
| Kafka topic bindings | 📋 Contracts published; fabric wiring phased |
| Twin Synchronization Engine (coordinator/workers/conflict/delta) | 📋 Architecture (ADR-207 / P199-B) |
| Event Mesh profile (Fabric + Bus + Orchestration) | 📋 Architecture (ADR-207) — reuse, not new bus |
| Sync lifecycle + conflict events | 📋 Contracts in `DIGITAL_TWIN_EVENT_CONTRACTS.v1.yaml` |
| OpenAPI 3.1 + RFC 9457 | 📋 `TWIN_API.openapi.v1.yaml` |

Legend: ✅ shipped · 📋 designed for production delivery · ⚠️ partial

---

## Related

- [ADR-203](../adr/203-enterprise-identity-digital-twin.md)  
- [ADR-203a](../adr/203a-digital-twin-type-catalog.md)  
- [ADR-207](../adr/207-twin-synchronization-engine-event-mesh.md)  
- [ENTERPRISE_TWIN_SYNCHRONIZATION_EVENT_MESH.md](ENTERPRISE_TWIN_SYNCHRONIZATION_EVENT_MESH.md)  
- Catalog: `docs/architecture/identity/DIGITAL_TWIN_KIND_CATALOG.yaml`  
- Events: `docs/architecture/identity/DIGITAL_TWIN_EVENT_CONTRACTS.v1.yaml`  
- Sync policies: `docs/architecture/identity/TWIN_SYNC_POLICY_CATALOG.yaml`  
- API: `docs/architecture/identity/TWIN_API.openapi.v1.yaml`
