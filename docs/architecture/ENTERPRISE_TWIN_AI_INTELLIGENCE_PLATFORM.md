# Enterprise Twin AI Intelligence Platform — Architecture Law

**Prompt:** V03-C02-P199-C · Volume 03 · Chapter 02  
**Governance:** Enterprise Architecture Governance 10.0  
**Status:** Canonical — production architecture (not a demo brief)  
**ADR:** [ADR-208](../adr/208-twin-ai-intelligence-platform.md)  
**Extends:** [ADR-203](../adr/203-enterprise-identity-digital-twin.md) · [ADR-203a](../adr/203a-digital-twin-type-catalog.md) · [ADR-207](../adr/207-twin-synchronization-engine-event-mesh.md)  
**Companions:** [ENTERPRISE_IDENTITY_DIGITAL_TWIN_PLATFORM.md](ENTERPRISE_IDENTITY_DIGITAL_TWIN_PLATFORM.md) · [ENTERPRISE_TWIN_SYNCHRONIZATION_EVENT_MESH.md](ENTERPRISE_TWIN_SYNCHRONIZATION_EVENT_MESH.md)

**Law:** Every Digital Twin is an intelligent **projection**: it understands current facets, predicts futures via **AI Platform**, reasons over a **projected knowledge graph**, runs **non-mutating simulations**, detects anomalies as **consumer mirrors**, and recommends actions only through **Policy + Workflow**. Twin Intelligence never replaces AI Platform, AI Governance, Directory Graph, Search, Financial Kernel, or industry systems of record.

---

## Hard reuse map (anti-duplication)

| Concern | Owner | Twin Intelligence role |
|---------|-------|------------------------|
| LLM / embeddings / chat / 14 surfaces | AI Platform | ACL only (`application/ai_service.py` → `/api/v1/ai`) |
| Model registry, bias, approval, rollback, inference logs | AI Governance (ADR-172) | Store `model_approval_ref`; never local registry |
| Features, training, drift retraining pipelines | Financial Data Science (ADR-170) | Map twin facets → feature keys; bind `model_ref` |
| NL Q&A / briefing style | Natural Language Analytics (ADR-171) | Copilot patterns; no fork |
| Identity/org/device relationship SoR | Directory Graph (ADR-194) | Hydrate + cache projected edges |
| Semantic / vector retrieval | Search Engine | Index twin docs via events; embeddings via AI |
| KPIs / dashboards | Analytics | Accuracy, drift, latency metrics |
| Alerts | Notification Platform | Template keys only |
| Approvals for autonomous actions | Workflow Engine | Never module-local approval FSM |
| Business rules / thresholds | Policy Engine | All gates configurable |
| Financial predictions / journals | Financial Kernel + owning finance BCs | Twin stores foresight facets only |
| Domain fraud/AML/clinical risk SoR | Owning industry BCs | Twin consumes events → anomaly/risk facets |
| Sync / mesh | ADR-207 | Intelligence **consumes** synchronized facets |

```text
Source facets (sync) ──► Twin projection
        │
        ├──► Feature map ──► FDS Feature Store
        │                         │
        │                         ▼
        │              Approved model (AI Governance)
        │                         │
        │                         ▼
        ├──► AI Platform inference ──► TwinPrediction record + events
        │
        ├──► Projected KG + Directory hydrate ──► Graph Query Engine
        │
        ├──► Simulation Runner (sandbox) ──► TwinSimulation (non-mutating)
        │
        └──► Reasoning / Copilot / Decision ──► Policy + Workflow + Audit
```

### Forbidden (hard stop)

- OpenAI/Anthropic (or any LLM) SDK inside twin domain/application  
- Twin-local model registry, vector DB, data lake, or Neo4j-only SoR without `IGraphStore` port  
- Parallel CRM / Hospital / Bank / University knowledge graph as twin SoR  
- Autonomous journal posts, clinical orders, tax filings, or trust band changes without Workflow + AuthZ  
- Hardcoded thresholds, prediction types, ontology edges, or simulation rules in code

---

## SECTION 1 — AI Prediction Engine

### 1.1 Capability

**Enterprise AI Prediction Platform (Twin profile)** — kind-scoped foresight over twin facets. Catalog: `identity/TWIN_INTELLIGENCE_PREDICTION_CATALOG.yaml`.

| Prediction class | Examples (catalog keys) | Owning feature/signal upstream |
|------------------|-------------------------|--------------------------------|
| Behavior | `behavior.trajectory`, session patterns | Identity / Adaptive Auth |
| Risk | `risk.score.horizon`, composite band | Identity Risk / AuthZ |
| Fraud | `fraud.probability` | Banking / FX / AML events |
| Compliance | `compliance.violation.likelihood` | Compliance Platform |
| Cash flow / Revenue | `finance.cashflow`, `finance.revenue` | Finance BC + Financial Kernel signals |
| Identity trust | `identity.trust.forecast` | Trust facet + risk |
| User growth | `growth.users` | Analytics projections |
| Resource / capacity | `ops.resource.consumption` | Observability + scheduler |
| Operational health | `ops.health.forecast` | Twin health + sync lag |
| Failure / performance | `ops.failure`, `ops.latency` | Observability |
| Security threat | `security.threat.probability` | AI Security / Risk |
| Churn / attrition / dropout / patient risk / tax risk | Industry keys | Owning BC events only |

### 1.2 Pipelines (production)

| Pipeline | Location | Notes |
|----------|----------|-------|
| Feature engineering | FDS + twin feature mapper | Tenant-scoped keys; PII/PHI minimization |
| Training | FDS / governed MLOps | Triggered by drift policy — not twin cron inventing models |
| Offline / batch prediction | AI jobs + Scheduler | Cursor-paginated twin batches (max 100 per page) |
| Online / real-time | AI inference + twin write path | Timeout + circuit breaker; fail closed on gate deny |
| Online learning | FDS policy | Twin records feedback events only |
| Model registry / versioning / rollback | AI Governance | Twin binds approved `model_version` |
| Explainability | AI + Governance explain APIs | Every prediction stores `explanation_ref` |

### 1.3 Twin aggregates / records

| Aggregate | Responsibility |
|-----------|----------------|
| `TwinPrediction` | Outcome: horizon, scores, confidence, `model_approval_ref`, `feature_snapshot_ref`, `explanation_ref` |
| Prediction request command | Validates Policy `twin.prediction.enabled` + AuthZ `twin.ai.infer` + consent facet gates |

### 1.4 Events

- Publish: `identity_twin.predicted`  
- Consume (optional): `ai.prediction.completed` → map to twin prediction if correlation matches

---

## SECTION 2 — Knowledge Graph

### 2.1 Role

**Enterprise Knowledge Graph (Twin profile)** = projected **ontology + edges** for twin neighborhood intelligence — not a global enterprise SoR graph.

| Layer | Store | Authority |
|-------|-------|-----------|
| Ontology / vocabulary | Catalog YAML + Policy | Twin intelligence pack |
| Twin projected edges | `identity_twin` schema (`TwinRelationship`) | Projection from sync events |
| Identity/org/device truth | Directory Graph API | ADR-194 |
| Industry entities | Peer BC + `subject_ref` | Peer SoR |

### 2.2 Node kinds (catalog-driven)

Users · Organizations · Departments · Branches · Devices · Applications · Sessions · Banks · Accounts · Transactions · Invoices · Payments · Employees · Students · Patients · Courses · Hospitals · Currencies · Tax Records · Assets · Contracts · AI Agents  

Each maps to `twin_kind` (ADR-203a) or **external subject ref** — never duplicated rows of peer aggregates.

### 2.3 Relationship types (catalog-driven)

`OWNS` · `WORKS_FOR` · `STUDIES_AT` · `BELONGS_TO` · `CONNECTED_TO` · `AUTHORIZES` · `APPROVES` · `CREATED` · `UPDATED` · `SIGNED` · `MANAGES` · `TRANSFERRED` · `USES` · `VISITED` · `TRUSTS` · `DEPENDS_ON` · `RELATED_TO`

Normalized in ontology as uppercase codes; binders map source events → edge upserts.

### 2.4 Graph lifecycle

```text
Source event → ACL mapper → Upsert/Delete edge (idempotent by edge_ref)
           → identity_twin.relationship.changed
           → Search/Analytics optional consumers
Retention → Policy twin.graph.retention → soft-delete → Workflow hard-delete
```

Reasoning/inference over graph: **hybrid** — rule packs (Policy) + AI jobs; results cached as twin insight facets, not new truth tables.

Catalog: `identity/TWIN_KNOWLEDGE_GRAPH_ONTOLOGY.yaml`.

---

## SECTION 3 — Graph Query Engine

### 3.1 Ports (hexagonal)

| Port | Dialects / capability |
|------|------------------------|
| `ITwinGraphQuery` | Path, neighborhood, relationship discovery, impact, root-cause assist |
| `IGraphDialectAdapter` | Cypher · Gremlin · GraphQL schema views (gateway) |
| `IDirectoryGraphClient` | Hydration when twin projection cold/incomplete |

### 3.2 Query capabilities

| Capability | Notes |
|------------|-------|
| Path analysis / shortest path | Tenant + permission filtered |
| Relationship discovery | Typed edge filters from ontology |
| Dependency mapping | `DEPENDS_ON` / `CONNECTED_TO` traversals |
| Knowledge / similarity search | Twin graph + Search semantic for text |
| Community detection / centrality | Batch analytics job — results to Analytics KPIs |
| Impact / root-cause assist | Graph + reasoning plan; not automatic remediations |

### 3.3 Security

Fail closed: omit unauthorized nodes (AuthZ + consent). No cross-tenant traversal without policy grant. Cypher/Gremlin never expose raw SQL to peer schemas.

---

## SECTION 4 — Simulation Engine

### 4.1 Law

**All simulations are sandboxed and non-mutating.** SoR and twin authoritative facets change only via source events / governed commands — never simulation side effects.

### 4.2 Scenario domains (catalog)

Business · Identity · Financial · Risk · Fraud · Attack · Policy · Capacity · Growth · Banking · Treasury · Tax · Healthcare · University · ERP  

Catalog: `identity/TWIN_SIMULATION_SCENARIO_CATALOG.yaml`.

### 4.3 Components

| Component | Responsibility |
|-----------|----------------|
| Scenario Builder | Load catalog + Policy parameters; validate inputs |
| Simulation Runner | Deterministic engine (+ optional AI-assisted scenario synthesis via AI Platform) |
| Monte Carlo profile | Configurable trials / seeds; aggregates distributions into simulation result |
| Scenario Comparison | Diff metrics across `simulation_ref`s |
| Digital Sandbox | Isolated run context; no outbox to industry write topics |

Existing engine: `twin_simulation_engine.py` (access / lifecycle / federation) — **extend via catalog**, do not fork.

Events: `identity_twin.simulation.completed` with `mutation_applied: false`.

---

## SECTION 5 — AI Reasoning Engine

### 5.1 Modes (configuration-driven)

| Mode | Mechanism |
|------|-----------|
| Rule-based | Policy Engine evaluate + twin facet predicates |
| Knowledge-based | Ontology constraints + catalog facts |
| Graph reasoning | Traversals + edge constraints |
| LLM reasoning | AI Platform job (prompt versions governed) |
| Hybrid | Ordered plan steps with confidence fusion |
| Decision trees / Bayesian / probabilistic | Model packs in FDS + AI; twin stores scores |

Every reasoning result: `confidence`, `evidence[]`, `explanation_ref`, `policy_decision_ref`.

### 5.2 Recommendation vs decision

Recommendations are advisory. **Decisions** that change trust, risk thresholds, or invoke remediations require Autonomous Decision Engine (Section 7) + Workflow when risk ≥ policy threshold.

---

## SECTION 6 — Anomaly Detection

### 6.1 Classes (projection keys)

Identity · Behavior · Financial · Banking · Treasury · Tax · Healthcare · University · Device · Network · API · Session  

### 6.2 Pipeline

```text
Owning detector / AI Security / Financial Anomaly
        → integration / domain event
        → Twin ACL → anomaly facet + identity_twin.anomaly.detected
        → Alert Engine (Notification templates)
        → Response Workflow (catalog workflow_id)
```

Twin does **not** re-implement AML, PHI anomaly, or banking fraud models.

---

## SECTION 7 — Autonomous Decision Engine

### 7.1 Capability set

AI recommendations · risk mitigation suggestions · automatic policy **suggestions** · adaptive threshold **proposals** · automatic trust **updates** (only if Policy allows + Workflow) · automatic risk scoring (via Risk platform APIs) · self-healing recommendations · optimization suggestions  

### 7.2 Approval workflow (mandatory for high impact)

| Impact band | Path |
|-------------|------|
| `advisory` | Persist recommendation; notify |
| `guarded` | Workflow approval task |
| `critical` | Dual control + Compliance/Audit listeners |

**Never** auto-post to Financial Kernel, mutate clinical SoR, or override AuthZ PDP.

Events (additive): `identity_twin.recommendation.created`, `identity_twin.decision.requested`, `identity_twin.decision.applied` (after Workflow completion).

---

## SECTION 8 — AI Copilot

Enterprise AI Copilot (**Twin surface**) — capabilities via AI Platform assistant + twin ACL tools:

| Surface | Purpose |
|---------|---------|
| Natural language query | Twin + graph + Search tools |
| Business / architecture / policy / risk / fraud / prediction explain | Governed prompts + evidence packs |
| Graph exploration | Calls Graph Query Engine |
| Simulation assistant | Scenario builder UX |
| Executive briefing / operational summary | NL Analytics patterns |
| Developer / administrator assistant | Docs + runbooks retrieval via Search |

Permissions: `twin.ai.read` / `twin.ai.infer`. Prompt injection defenses via AI Platform prompt security — twin never embeds raw user text into system prompts without sanitization port.

---

## SECTION 9 — Model Governance

| Concern | Owner |
|---------|-------|
| Registry, version control, documentation | AI Governance + FDS |
| Approval workflow | AI Governance (+ Workflow when dual-control) |
| Bias / drift detection | AI Governance + FDS drift jobs |
| Retraining policies | Policy keys `twin.model.retrain.*` → FDS |
| Rollback | Governance rollback → twin binds previous `model_approval_ref` |
| Audit trail / compliance reports | Audit + Governance exports |

Twin stores **refs only**. Local `MODEL_REGISTRY` dicts are forbidden.

---

## SECTION 10 — Data Platform

| Capability | Platform owner | Twin use |
|------------|----------------|----------|
| Feature Store | FDS (ADR-170) | Feature map from facets/snapshots |
| Vector DB / embeddings | AI → Search `embedding_ref` | Semantic twin search |
| Knowledge Base | Documents / Search | Copilot RAG |
| Data Lake / Warehouse | Platform data plane | Batch features offline |
| Streaming / batch | Event Mesh (207) + Scheduler | Online vs batch prediction |
| Data lineage / catalog | Platform metadata | Prediction feature lineage refs |
| Master data | MDM / owning BCs | Subject refs only |

---

## SECTION 11 — Observability

### 11.1 Metrics (OTel → Prometheus → Grafana)

| Metric | Type |
|--------|------|
| `twin_prediction_requests_total{kind,status}` | counter |
| `twin_prediction_accuracy{kind,model}` | gauge (from feedback jobs) |
| `twin_model_health{model}` | gauge |
| `twin_graph_nodes`, `twin_graph_edges` | gauge |
| `twin_inference_latency_ms` | histogram |
| `twin_simulation_runs_total{scenario}` | counter |
| `twin_simulation_duration_ms` | histogram |
| `twin_recommendation_total{impact}` | counter |
| `twin_drift_open`, `twin_anomaly_open` | gauge |

Dashboards: Grafana Twin Intelligence · Elastic logs · OTel traces (Predict → AI → Governance → Twin persist).  
Elastic Stack: structured prediction/simulation audit fields.

---

## SECTION 12 — API Platform

### 12.1 Primary REST (OpenAPI 3.1)

Base: `/api/v1/identity-twins`  
Intelligence contract: `identity/TWIN_INTELLIGENCE_API.openapi.v1.yaml`

| Method | Path | Permission |
|--------|------|------------|
| POST | `/{twin_ref}/predict` | `twin.ai.infer` |
| POST | `/{twin_ref}/simulate` | `twin.write` or `twin.simulate` |
| POST | `/{twin_ref}/reason` | `twin.ai.infer` |
| POST | `/{twin_ref}/recommend` | `twin.ai.infer` |
| GET | `/graph` · `/graph/search` · `/graph/path` · `/graph/entity` · `/graph/relationship` | `twin.read` |
| GET | `/models` (proxy refs to governance) | `twin.ai.read` |
| GET | `/predictions` · `/{twin_ref}/predictions` | `twin.read` |

Gateway aliases (optional rewrite): `POST /api/v1/twin-intelligence/prediction` → predict; same for simulation/reasoning/recommendation — **one implementation**.

### 12.2 GraphQL / gRPC / AsyncAPI

Generated per ADR-198 from OpenAPI + event YAML. AsyncAPI topic `marpich.twin.intelligence.v1`.

---

## SECTION 13 — Security

| Control | Implementation |
|---------|----------------|
| Zero Trust AI | AuthN + AuthZ on every infer; tenant from JWT |
| Model security | Only approved `model_approval_ref` |
| Data encryption | TLS + at-rest platform encryption; minimize PHI/PII in features |
| Inference authorization | `twin.ai.infer` + Policy + consent checks |
| Prompt security | AI Platform sanitization / injection defenses |
| Knowledge / vector / graph protection | Tenant RLS + AuthZ per hit |
| Isolation | Partition keys; no shared mutable caches across tenants |

---

## SECTION 14 — Multi-tenancy

| Mode | Policy gate |
|------|-------------|
| Tenant AI models | `twin.model.scope=tenant` |
| Shared / regional / global models | Governance scopes + tenant opt-in |
| Federated learning | Explicit `twin.federated_learning.enabled` + consent + legal hold |
| Cross-tenant analytics | Aggregates only via Analytics privacy profiles — never raw peer graph export |
| Policy / knowledge isolation | Default deny cross-tenant edges |

---

## SECTION 15 — Architecture principles checklist

DDD · CQRS · Hexagonal · Event-driven · Cloud native · API first · Plugin first · Metadata-driven · Configuration-driven · Policy-driven · AI native · Digital Twin native · Knowledge Graph native · Zero Trust  

**Never hardcode:** AI models · thresholds · policies · rules · predictions · knowledge relations · simulation rules · inference logic.

---

## Schema / infrastructure (production design)

| Artifact | Notes |
|----------|-------|
| Tables | `twin_predictions`, `twin_simulations`, `twin_relationships`, `twin_recommendations`, `twin_reasoning_runs` (tenant_id indexed) |
| Migration | Extend `031_…` / next twin migration — no peer schemas |
| Graph port | `IGraphStore` adapter (e.g. PostgreSQL recursive + optional Neo4j adapter behind port) |
| SDK | `packages/` client: predict/simulate/graph query against OpenAPI |
| Tests | Unit (engines), contract (events/OpenAPI), integration (AI ACL mock), performance (p95 inference path) |
| Deployment | Feature flags `twin.intelligence.*`; canary models via Governance |
| Runbooks | Prediction outage · drift storm · graph rebuild · simulation backlog · governance rollback |

---

## Delivery roadmap (architecture → production)

| Phase | Deliverable |
|-------|-------------|
| **C0** | Prediction command path + `identity_twin.predicted` + Policy gates + AI ACL |
| **C1** | Graph neighborhood API + ontology catalog bindings + relationship events |
| **C2** | Simulation catalog expansion + Monte Carlo profile + comparison API |
| **C3** | Reasoning + recommendation aggregates + Workflow approval path |
| **C4** | Anomaly ACL consumers + alert templates + response workflows |
| **C5** | Copilot tool surface + Search retrieval + NL briefing templates |
| **C6** | Observability dashboards + federation learning policy (opt-in) + SDK |

---

## Testing strategy

| Layer | Focus |
|-------|-------|
| Unit | Feature map, ontology bind, simulation purity (`mutation_applied=false`), confidence fusion |
| Contract | Event schemas, OpenAPI, Policy key presence |
| Integration | Twin → AI mock; Twin → Directory hydrate; Workflow decision apply |
| Security | Cross-tenant graph deny; unapproved model reject; consent-gated facets |
| Performance | Batch predict pagination; graph hop limits; p95 inference SLA |
| Chaos | AI timeout → fail closed; Governance deny → no twin write |

---

## Administrator / Developer guides (outline)

**Admin:** enable flags, bind models in Governance, set Policy thresholds, review drift dashboards, approve autonomous decisions, run graph rebuild jobs.  

**Developer:** call twin OpenAPI; never import `contexts.ai` domain; register new prediction keys in catalog + Policy; publish source events for graph edges; write ACL mappers only.

---

## Related

- [AI_PLATFORM_STANDARD.md](AI_PLATFORM_STANDARD.md)  
- [ENTERPRISE_SEARCH_ENGINE.md](ENTERPRISE_SEARCH_ENGINE.md)  
- [ENTERPRISE_OBSERVABILITY_PLATFORM.md](ENTERPRISE_OBSERVABILITY_PLATFORM.md)  
- ADR-170 · ADR-171 · ADR-172 · ADR-194 · ADR-198 · ADR-203 · ADR-203a · ADR-207 · ADR-208 · [ADR-209 Platform Engineering](../adr/209-twin-platform-engineering-devsecops.md) · [ENTERPRISE_TWIN_PLATFORM_ENGINEERING.md](ENTERPRISE_TWIN_PLATFORM_ENGINEERING.md)
