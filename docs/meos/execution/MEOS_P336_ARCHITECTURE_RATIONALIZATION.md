# MEOS P336 — Enterprise Architecture & Technology Rationalization

**Date:** 2026-08-19T06:15:00Z  
**Decision:** MEOS has an **application registry**, a **monolith FastAPI + Next admin portal**, and **local compose infra**. It does **not** have a production CMDB, ITSM, cloud manager, or second application catalog. `PRODUCTION_ACTIVE` is **false**. **0** ACTIVE applications. Utilization/cost **NOT_MEASURED**. **Not** a new registry, CMDB, ITSM, ERP, inventory, or architecture framework.  
**Maturity:** `INVENTORIED` — **not** RATIONALIZING / HARDENING / MODERNIZING as an operating claim.  
**Machine:** [MEOS_ARCHITECTURE_RATIONALIZATION.v1.yaml](./MEOS_ARCHITECTURE_RATIONALIZATION.v1.yaml)  
**Application SoR:** [MEOS_APPLICATION_REGISTRY.v1.yaml](./MEOS_APPLICATION_REGISTRY.v1.yaml) — **do not fork.**  
**P337:** data overlay **INVENTORIED**. **0** published data products. Lineage **INCOMPLETE**. Quality **NOT_MEASURED**. See [MEOS_P337_DATA_ARCHITECTURE.md](./MEOS_P337_DATA_ARCHITECTURE.md).  
**P338:** decision overlay **FOUNDATION**. **0** executed decisions. See [MEOS_P338_DECISION_INTELLIGENCE.md](./MEOS_P338_DECISION_INTELLIGENCE.md).  
**P339:** execution overlay **INVENTORIED**. **0** authorized actions. See [MEOS_P339_DECISION_EXECUTION.md](./MEOS_P339_DECISION_EXECUTION.md).

## 1. Actual P335 status (precondition)

| Signal | Actual |
|--------|--------|
| P335 | Portfolio **INVENTORIED** · `PF-LAUNCH-GOVERNANCE` ASSESSED · `investment_measured_count: 0` |
| P334 | Change **INVENTORIED** · 0 production changes · ADOPTED = false |
| P333 | Capability **MAPPED** · readiness **NOT_MEASURED** |
| P332 | Knowledge **INVENTORIED** · `validated_count: 0` |
| P331 | Optimization **BLOCKED** |
| P330 | **GATED L0** |
| P329 | Continuity **DOCUMENTED** · RTO/RPO **NOT_VERIFIED** |
| P328 | **RISK_AWARE** · R-01…R-07 |
| P327 | Strategy **NOT_DECLARED** |
| P326 | Value **NOT_REALIZED** |
| `APPLICATION_STATE` | Registry **NOT_READY** · ACTIVE = 0 |
| `SERVICE_STATE` | Local compose + one API process · production **NOT_DEPLOYED** |
| `TECHNOLOGY_STATE` | Inventoried (this overlay) · no vendor CMDB |
| `INTEGRATION_STATE` | P321 **0 ACTIVE** connectors |
| `ARCHITECTURE_STATE` | Docs rich · execution incomplete · drift present |
| `COST_STATE` | **NOT_MEASURED** |
| `RISK_STATE` | Launch register ASSESSED |
| `VALUE_STATE` | Outcomes IDENTIFIED |

Historical 2026-08-12 architecture status (crm/HR as empty scaffolds) is **not** current fact.

## 2. Authoritative application inventory (reconciled)

SoR remains the YAML registry. Reconciled 2026-08-19:

| Source | Count | Notes |
|--------|-------|-------|
| Registry applications | **47** | 0 ACTIVE |
| Status | INTEGRATED 6 · IMPLEMENTED 12 · TESTED 12 · BLUEPRINT 5 · SCAFFOLDED **12** | Legend in registry |
| `backend/contexts/` | **79** | 32 contexts **not** product-app rows (platform/identity/analytics/…) |
| Nav groups | 5 | All item IDs have registry rows (honesty test) |
| `frontend/apps` | **1** (`admin_portal`) | `frontend/modules/` **ABSENT** |
| `EMPTY_INDUSTRY_SCAFFOLD_IDS` | 12 | Matches YAML SCAFFOLDED |
| Missing ROUTER packages | P3 **BASELINED** | Skipped at startup — not live apps |
| Route / menu / folder | exist for many | **≠ ACTIVE** |

Do **not** mark ACTIVE because a route, menu, screen, or folder exists.

## 3–8. Lifecycle, capability, redundancy, utilization, value, cost

See [MEOS_APPLICATION_PORTFOLIO.md](./MEOS_APPLICATION_PORTFOLIO.md).

Lifecycle **recommendations** (not runtime status): RETAIN functional slices · FREEZE empty scaffolds · MONITOR blueprints · CONSOLIDATE legacy TS vs FastAPI · **no RETIRE** of production (none ACTIVE).

Capability mapping: P333 overlay + business capability registry. Coverage **MAPPED** for TESTED Wave 02 processes; production coverage **NOT_MEASURED**.

Redundancy: warehouse vs inventory **PARTIAL_OVERLAP**; university vs school **COMPLEMENTARY**; identity fabric **COMPLEMENTARY**; TS identity-service vs Python identity **FULL_DUPLICATION** of intent (migration path). Do not eliminate on similar names.

Utilization / value / cost: **NOT_MEASURED** (P320/P326/P335). No invented users, transactions, licenses, or infra invoices.

## 9–12. Risk, debt, drift, ownership

Risk: inherit R-01…R-07. No second GRC.

Technical debt SoR: [MEOS_TECHNICAL_DEBT_REGISTRY.md](./MEOS_TECHNICAL_DEBT_REGISTRY.md). P0 G26/G25/G27. Additional architecture debt: missing routers (BASELINED), default memory persistence, event payload schema, FE modules absent. Classification stays on the debt registry — this overlay does **not** invent CRITICAL scores for unnamed components.

Drift: [MEOS_ARCHITECTURE_DRIFT_REPORT.md](./MEOS_ARCHITECTURE_DRIFT_REPORT.md).

Owners: **NOT_AVAILABLE** (same as P333–P335). Production-critical components **do not exist** in production; ownership-ambiguous **workstation** code is documented, not staffed.

## 13–16. Service, API, event, data

| Portfolio | Actual |
|-----------|--------|
| Services | FastAPI `:8000`, Next `:3001`, Postgres `:5433`, Redis `:6379`, MinIO `:9000`, Kafka-native `:9092` (local). Legacy TS `services/*` **MIGRATION_PATH**. Production k8s **not** the local runtime. |
| API | REST `/api/v1/*`. GraphQL runtime **NOT_AVAILABLE**. Duplicate/unused APIs **NOT_MEASURED**. No second gateway. |
| Events | Outbox + schemas exist; `EVENT_BUS_MODE=direct` locally; `TD-EVENT-PAYLOAD-SCHEMA` open. Orphan/failed consumers **NOT_MEASURED** in production (no prod). |
| Data | `marpich_platform` Postgres; default code path **memory**. Data Mesh docs exist; live mesh **NOT_AVAILABLE**. Duplicate data **NOT_MEASURED**. |

## 17–24. Technology, dependencies, SPOF, resilience, security, privacy, observability, performance

See [MEOS_TECHNOLOGY_PORTFOLIO.md](./MEOS_TECHNOLOGY_PORTFOLIO.md).

SPOF (local / intended prod gap): single API process, single admin portal, single DB, no region. P329: failover/RTO/RPO **NOT_VERIFIED**. Local restore drill ≠ production resilience.

Security/privacy: P317 TRUST_CRITICAL; G18 stub AI; G19 DSAR incomplete. No invented residual scores.

Observability: `/health` `/ready` `/live` exist; production alerting **FAIL** (G23). Tracing in prod **NOT_AVAILABLE**.

Performance: P331 **BLOCKED**. Local p95 **STALE_FOR_P331**.

## 25–30. Lifecycle, target, modernization, consolidation, decommission

[MEOS_MODERNIZATION_RUNBOOK.md](./MEOS_MODERNIZATION_RUNBOOK.md).

Target: **preserve** DDD, CQRS, hexagonal, modular monolith→optional extract, events, API-first, plugin-first, metadata, zero-trust, AI-native, data mesh, graph, twin. **No reset.** Transition: honest catalog + production cluster (G26) + postgres in prod + consumers, **not** a microservice rewrite (Wave 01 law still holds).

P335 feed: architecture needs attach to **existing** INIT-G26 / INIT-G23 / TD-EVENT-PAYLOAD-SCHEMA. **No new initiative rows.**

Retirement candidates: **[]**. Consolidation candidate: legacy TS vs FastAPI (after usage evidence). Decommission from static inventory: **FORBIDDEN**.

## 31–36. AI, autonomy, UX, audit

AI may cite this overlay. **Must not** delete apps, retire services, migrate DBs, or change security boundaries.

Autonomy L0: inventory refresh / doc sync / health check only in future. Destructive changes: human approval.

Executive view: existing AppShell. Do not show fake ACTIVE, cost, or usage %.

Audit: git history of this overlay. No fake RETIREMENT_APPROVAL events.

## Unresolved blockers

BLK-G26 (no production topology), BLK-G23 (alerting), default memory vs prod postgres, missing router baseline, FE modules absent, owners NOT_AVAILABLE, cost/usage **NOT_MEASURED**. Next operational action remains G26 → G25 → G27 → P314 APPROVED.

## Architecture validation scorecard

| Dimension | Score | Pass? |
|-----------|-------|-------|
| Architecture | 4 | Overlay on registry/startup/debt |
| DDD | 4 | No second catalog; no context merge by name |
| Security | 4 | AI cannot mutate architecture |
| Scalability | 3 | YAML overlay |
| Performance | 3 | No extra warehouse |
| Testing | 4 | Rationalization honesty |
| AI Integration | 3 | Cite-or-refuse |
| Documentation | 4 | Stale status corrected; SoR not forked |
| Accessibility | 3 | Existing shell |
| Localization | 3 | Docs English |
| Observability | 3 | G23 open |
| Workflow | 4 | No ITSM product |
| Audit | 4 | No fake retire events |
| Policy Compliance | 4 | Evidence-only lifecycle |
| Plugin Compatibility | 4 | Unchanged |

**Verdict:** ENTERPRISE_GRADE as **honest inventory**. Architecture rationalization **not** operational.

## Reuse analysis

Reused application registry, startup honesty sets, P3 router baseline, debt registry, P335 portfolio, compose/runtime, AppShell.  
Rejected: new CMDB/ITSM/registry/cloud manager; inventing ACTIVE, usage, cost, retirement.

## Architectural decisions

- **Decision:** Registry YAML remains application SoR; P336 adds lifecycle classes only. **Rejected:** a parallel application database.
- **Decision:** 32 extra contexts are not auto-promoted to applications. **Rejected:** inventing 32 product apps to close the count gap.
- **Decision:** FREEZE scaffolds; do not RETIRE them as production. **Rejected:** decommission-from-folder.
- **Long-horizon:** After GO_LIVE, bind usage/cost from existing observability + finance adapters — still one registry.
