# MEOS P337 — Enterprise Data & Information Architecture

**Date:** 2026-08-19T06:45:00Z  
**Decision:** MEOS has **Postgres OLTP** (local `:5433`), **in-memory data-governance catalogs**, and **architecture docs** for mesh/MDM/lineage. It does **not** have a production data mesh runtime, published data products, warehouse, lake, or second catalog. `PRODUCTION_ACTIVE` is **false**. **0** PUBLISHED/ACTIVE data products. Lineage **INCOMPLETE**. Quality **NOT_MEASURED**. **Not** a new database, warehouse, lake, mesh, BI, MDM, catalog, or governance product.  
**Maturity:** `INVENTORIED` — **not** GOVERNED / QUALITY_DRIVEN / VALUE_DRIVEN as an operating claim.  
**Machine:** [MEOS_DATA_ARCHITECTURE.v1.yaml](./MEOS_DATA_ARCHITECTURE.v1.yaml)  
**P338:** feeds decision intelligence — data trust **NOT_MEASURED** for KPIs. See [MEOS_P338_DECISION_INTELLIGENCE.md](./MEOS_P338_DECISION_INTELLIGENCE.md).

## 1. Actual P336 status (precondition)

| Signal | Actual |
|--------|--------|
| P336 | Architecture **INVENTORIED** · registry 47 apps · **0 ACTIVE** |
| P335 | Portfolio **INVENTORIED** · investment **NOT_MEASURED** |
| P334–P326 | Change INVENTORIED · value NOT_REALIZED · strategy NOT_DECLARED |
| `DATA_STATE` | Local PG **present**; default code persistence **memory** |
| `QUALITY_STATE` | Catalog rules in `data_governance` · measured DQ **NOT_MEASURED** |
| `LINEAGE_STATE` | **LINEAGE_INCOMPLETE** |
| `GOVERNANCE_STATE` | P212 APIs CATALOG_ONLY · no `data_governance` PG schema |
| `PRIVACY_STATE` | Wave 04 runbook; **G19 DSAR FAIL** |
| `SECURITY_STATE` | RLS on **93** tables · TRUST_CRITICAL |
| `VALUE_STATE` | P326 IDENTIFIED |
| `LIFECYCLE_STATE` | Migrations **55** · retention **POLICY_GAP** |

`data_mesh` and `data_product_platform` **contexts are ABSENT**. P229/P263/P290 remain **design docs** (ACL). Do not treat them as a live mesh.

## 2. Authoritative data inventory (runtime 2026-08-19)

| Asset | Actual |
|-------|--------|
| Database | `marpich_platform` @ `127.0.0.1:5433` (local, not production) |
| PG schemas | **54** |
| Tables | **223** |
| RLS enabled | **93** |
| `data_governance` schema | **ABSENT** |
| `data_products` table | **ABSENT** |
| SQL migrations | **55** (000–055 applied locally) |
| Event JSON schemas | **47** files |
| Redis / MinIO / Kafka-native | Local compose |
| Default `PERSISTENCE_BACKEND` | **memory** (prod gated to postgres) |

Application → service → DB: one FastAPI process, one database. Not a federated mesh topology.

## 3–8. Domains, products, sources, SoR, duplication, lineage

Domains are **existing PG schemas / bounded contexts**, not new mesh domains. See YAML `domains`.

Data products: **none published**. `/api/v1/data-governance/catalog` returns **in-memory capability catalogs**. Publication requires evidence — none.

Authoritative source **candidates**: local Postgres when `PERSISTENCE_BACKEND=postgres`. Memory store is **not** SoR. Redis = cache. Do not designate SoR merely because a table exists in demo.

Duplication: TS vs Python identity **LIKELY**; money-path schemas **UNKNOWN**; design-docs vs OLTP **CONFIRMED**. **Do not delete.**

Lineage: no field-level production graph. Analytics `GET /analytics/graph/lineage` is a **catalog surface**. State: **LINEAGE_INCOMPLETE**.

## 9–13. Quality, incidents, contracts, evolution, MDM

Quality dimensions completeness/accuracy/… : **NOT_MEASURED**. Quality APIs are required-flag catalogs (P212). Incidents: **0** evidenced (no production DQ pipeline).

Contracts: OpenAPI + event JSON exist; **data-product contracts unpublished**. Breaking-change governance = P334 (no APPROVED changes).

Schema evolution: SQL migrations **IMPLEMENTED**. Consumer impact **NOT_MEASURED**.

Master/reference data: P290 MEDAMIA is **normative docs**. No MDM merge engine. **Do not build one.**

## 14–20. Security, privacy, isolation, lifecycle, retention, archive, recovery

Security: JWT + tenant header + RLS (93). Classification catalogs in `data_security`. Unauthorized path hunt in production: **NOT_MEASURED**.

Privacy: Wave 04 pack **documented**. G19 **FAIL** (DSAR/erasure not runtime-certified). Retention periods **not invented** → **POLICY_GAP**. Minimization: documents store `document_id` (law).

Tenant isolation: `set_config('app.tenant_id')` + RLS. Production cross-tenant **NOT_MEASURED** as a continuous control (workstation tests exist elsewhere). Search/export isolation: **IMPLEMENTED_UNVERIFIED**.

Lifecycle CREATE/USE/… : OLTP in use locally; archive/delete legal path **BLOCKED** (G19).

Recovery: P313 **G07 PASS** (MinIO listing, local). Production multi-region RTO/RPO **NOT_VERIFIED**. Registry flag `p313_offsite_backup: blocked` **conflicts** with G07 PASS — documentation drift, not a new restore claim.

## 21–33. Value, cost, debt, semantics, KG, analytics, AI, twin, events, APIs, health

Value/cost: **NOT_MEASURED** (P326/P335).

Data debt: missing `data_governance` PG schema vs context.yaml; unpublished products; `TD-EVENT-PAYLOAD-SCHEMA`; default memory vs postgres; lineage incomplete.

Semantics/KG: P228/P264 **docs**; live enterprise KG **NOT_AVAILABLE** (P326). Conflicting definitions **NOT_MEASURED**.

Analytics: home pulse `CATALOG_COUNT` — unknown-source business KPI. GraphQL **NOT_AVAILABLE**.

AI: G18 stub. Provenance **NOT_AVAILABLE**. Must not silently consume unauthorized data.

Twin: `identity_twin` schema present; ops/value twin **NOT_AVAILABLE**. Stale twin **N/A**.

Events: 47 schemas; bus often **direct**; orphan/failed consumers **NOT_MEASURED** in prod.

API overexposure: **NOT_MEASURED**. P336: REST only.

Data product health: **NOT_MEASURED** (none published).

## 34–42. Rationalization, migration, governance, observability, AI, UX, audit, security

See [MEOS_DATA_RATIONALIZATION_RUNBOOK.md](./MEOS_DATA_RATIONALIZATION_RUNBOOK.md).

RETAIN OLTP in use · RETAIN_AS_DESIGNED governance catalogs · FREEZE empty apps · **DO_NOT_PUBLISH** fake products · `retirement_candidates: []`.

AI may infer lineage **INFERRED_UNVERIFIED**. Must not delete data, change retention/access, declare SoR, or approve migration.

UX: existing AppShell. No fake lineage or HEALTHY tiles.

Audit: git of this overlay. No fake DATA_PRODUCT_PUBLISHED events.

## Required final report (mandate §45)

Live snapshot 2026-08-19T06:45:00Z against `marpich_platform` @ `:5433` plus repository evidence. Missing evidence → `NOT_MEASURED` / `BLOCKED` / `IMPLEMENTED_UNVERIFIED` / `INFERRED_UNVERIFIED`.

1. **P336 status:** Architecture overlay **INVENTORIED**. Registry **47** apps, **0 ACTIVE**. No CMDB/ITSM. Utilization/cost **NOT_MEASURED**.
2. **Authoritative data inventory:** Local PG **54** schemas, **223** tables, **93** RLS tables (`pg_tables.rowsecurity`), **57** RLS policies. **55** SQL migrations. **47** event JSON files. One FastAPI process → one database. Default persistence **memory**. Production data plane **NOT_DEPLOYED**.
3. **Data domains:** Groupings of **existing** PG schemas / contexts (identity, tenant, commercial, workforce, healthcare, platform). `data_governance` is **CONTEXT_WITHOUT_PG_SCHEMA**. Not a second mesh domain catalog. Owners **NOT_AVAILABLE**.
4. **Data products:** `published_data_product_count: 0` · `active_data_product_count: 0`. `/api/v1/data-governance/catalog` is **CATALOG_ONLY** (in-memory capability flags). `data_products` table **ABSENT**.
5. **Authoritative sources:** Local Postgres is an **AUTHORITATIVE_CANDIDATE** when `PERSISTENCE_BACKEND=postgres`, **not** production SoR. Redis = **CACHE**. Memory store is **not** SoR. No table is SoR merely because it exists.
6. **Data duplication:** DUP-IDENTITY-TS-PY **LIKELY**; DUP-MONEY-SURFACES **UNKNOWN**; DUP-GOVERNANCE-DOCS-VS-OLTP **CONFIRMED**. Action: **DO_NOT_DELETE** / **DO_NOT_CONSOLIDATE**.
7. **Lineage completeness:** **LINEAGE_INCOMPLETE**. Analytics `GET /analytics/graph/lineage` returns static `DECISION_LINEAGE` catalog dict, not field-level runtime graph.
8. **Data quality:** **NOT_MEASURED** on completeness/accuracy/consistency/timeliness/uniqueness/validity. Quality incidents **0** evidenced.
9. **Data contracts:** OpenAPI + 47 event JSON files exist. Data-product contracts **unpublished**. Breaking-change gate = P334 (**0** APPROVED production changes).
10. **Schema evolution:** SQL migrations **IMPLEMENTED** (55 files). Consumer impact **NOT_MEASURED**.
11. **Master/reference data:** P290 MEDAMIA **design docs**. MDM merge engine **NOT_IMPLEMENTED**. Do not build another MDM.
12. **Security state:** JWT + tenant header + RLS **93**. Classification catalogs in `data_security`. Production unauthorized-path hunt **NOT_MEASURED**.
13. **Privacy state:** Wave 04 pack documented. G19 DSAR/erasure **FAIL**. Legal basis / purpose inventory **NOT_MEASURED**. Retention periods **not invented**.
14. **Tenant isolation:** RLS + `app.tenant_id`. Search/export/cache/event isolation **IMPLEMENTED_UNVERIFIED** as a continuous production control.
15. **Data lifecycle:** Local OLTP CREATE/USE present. SHARE/TRANSFORM pipelines **NOT_MEASURED**. Legal DELETE **BLOCKED** (G19).
16. **Retention state:** **POLICY_GAP**. No invented periods.
17. **Archive/recovery:** Local P313 **G07 PASS** (MinIO listing). Production RTO/RPO **NOT_VERIFIED**. Registry `p313_offsite_backup: blocked` vs G07 PASS is **documentation drift**, not a restore claim.
18. **Data value:** **NOT_MEASURED** (P326 IDENTIFIED / P335 investment **NOT_MEASURED**). Expected vs realized **not separable**.
19. **Data cost:** **NOT_MEASURED** (storage/compute/transfer/pipeline/backup/license).
20. **Data technical debt:** `data_governance` PG schema missing vs `context.yaml`; unpublished products; `TD-EVENT-PAYLOAD-SCHEMA`; default memory vs postgres; lineage incomplete; TS vs Python identity overlap.
21. **Semantic consistency:** Live enterprise KG **NOT_AVAILABLE**. Conflicting definitions **NOT_MEASURED**.
22. **Knowledge graph integration:** Analytics/P228/P264 **catalog/docs**. Runtime DATA→ENTITY→DECISION graph **NOT_AVAILABLE**.
23. **Analytics data readiness:** Home pulse uses catalog counts. Business KPI source **UNKNOWN_SOURCE**. GraphQL **NOT_AVAILABLE**. Quality **NOT_MEASURED**. Lineage **BROKEN** (incomplete).
24. **AI data readiness:** G18 stub. Availability/authorization/quality/traceability for AI inputs **NOT_MEASURED**. Provenance **NOT_AVAILABLE**.
25. **Digital twin data:** `identity_twin` schema **present**. Ops/value twins **NOT_AVAILABLE**. Stale/incomplete twin **N/A** (not an ops twin claim).
26. **Event data:** **47** JSON schemas. Bus often `EVENT_BUS_MODE=direct`. Orphan/duplicate/schema-drift in production **NOT_MEASURED**. `TD-EVENT-PAYLOAD-SCHEMA` open.
27. **API data exposure:** REST only (P336). Overexposure / duplicate endpoint / missing version **NOT_MEASURED**. GraphQL **NOT_AVAILABLE**.
28. **Data product health:** **NOT_MEASURED**. None published — never HEALTHY/DEGRADED without evidence.
29. **Rationalization candidates:** RETAIN OLTP in use; RETAIN_AS_DESIGNED P212 catalogs; FREEZE empty apps; DO_NOT_PUBLISH products; later CONSOLIDATE TS/Python identity (P336). `retirement_candidates: []`. No destructive migration authorized.
30. **Unresolved blockers:** BLK-G26 (no production data plane); G19 DSAR FAIL; lineage incomplete; 0 published products; `data_governance` schema absent; default memory persistence; G23 alerting; P336 **0 ACTIVE** apps. Next action remains production cluster → then measure quality/lineage on real traffic.

## Unresolved blockers

BLK-G26 (no production data plane), G19 DSAR, lineage incomplete, no published products, `data_governance` schema absent, default memory, G23 alerting, P336 0 ACTIVE apps. Next action remains production cluster → then measure quality/lineage on real traffic.

## Architecture validation scorecard

| Dimension | Score | Pass? |
|-----------|-------|-------|
| Architecture | 4 | Overlay on PG + P212 catalogs; no warehouse |
| DDD | 4 | Did not add `data_mesh` / MDM context |
| Security | 4 | AI cannot mutate data/SoR |
| Scalability | 3 | YAML overlay |
| Performance | 3 | No extra OLAP |
| Testing | 4 | Data-architecture honesty |
| AI Integration | 3 | Stub; inferred≠validated |
| Documentation | 4 | SoRs pointed, not forked |
| Accessibility | 3 | Existing shell |
| Localization | 3 | Docs English |
| Observability | 3 | No DQ pipeline / G23 |
| Workflow | 4 | Erasure workflow not certified (honest FAIL) |
| Audit | 4 | No fake publish events |
| Policy Compliance | 4 | POLICY_GAP not invented periods |
| Plugin Compatibility | 4 | Unchanged |

**Verdict:** ENTERPRISE_GRADE as **honest inventory**. Information architecture **not** operational.

## Reuse analysis

Reused Postgres, migrations, RLS, `data_governance`/`data_security`/`data_isolation` APIs, event JSON, P212/P229/P263/P290 as **design**, P313 backup evidence, P336/P335.  
Rejected: new warehouse/lake/mesh/catalog/MDM; publishing catalog flags as ACTIVE products.

## Architectural decisions

- **Decision:** Runtime inventory = PG schemas/tables; P212 catalog ≠ published data product. **Rejected:** dual-write a `data_products` table this phase.
- **Decision:** Mesh/MDM docs stay design SoRs via ACL. **Rejected:** creating `data_mesh` context to “complete” P229.
- **Long-horizon:** After GO_LIVE, bind products/contracts to existing `/api/v1/data-governance*` and P229 paths — still one mesh, one catalog.
