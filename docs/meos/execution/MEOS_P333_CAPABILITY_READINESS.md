# MEOS P333 — Enterprise Capability & Organizational Readiness

**Date:** 2026-08-18T17:00:00Z  
**Decision:** MEOS has a **capability catalog** and **people systems** (identity, organization, HR employment, payroll). It does **not** have an evidence-backed organizational readiness or workforce-intelligence product. No production cluster. No skill inventory. No validated lessons to convert into capability. **Not** a new HRM, HCM, LMS, recruitment, payroll, talent, or organizational-graph platform.  
**Maturity:** `MAPPED` — **not** READY / SKILLED / CAPABLE as an operating claim.  
**Machine:** [MEOS_CAPABILITY_READINESS.v1.yaml](./MEOS_CAPABILITY_READINESS.v1.yaml)  
**P334:** change/adoption overlay **INVENTORIED**; readiness still **NOT_MEASURED**. See [MEOS_P334_CHANGE_INTELLIGENCE.md](./MEOS_P334_CHANGE_INTELLIGENCE.md).  
**P335:** capability gate on portfolio items remains **BLOCKED**. See [MEOS_P335_PORTFOLIO_INTELLIGENCE.md](./MEOS_P335_PORTFOLIO_INTELLIGENCE.md).

## 1. Actual P332 status (precondition)

| Signal | Actual |
|--------|--------|
| P332 | Knowledge **INVENTORIED** · lessons **DRAFT** · `validated_count: 0` |
| P331 | Optimization **BLOCKED** · `implemented_this_phase: 0` |
| P330 | **GATED L0** · `observe_operational: false` |
| P329 | Continuity **DOCUMENTED** · IR not active · command **unstaffed** |
| P328 | **RISK_AWARE** · production DR **NOT_VERIFIED** |
| P327 | Strategy **NOT_DECLARED** · 0 ACTIVE OKRs · PLATFORM_GATE **DRAFT** |
| P326 | Value **NOT_REALIZED** · outcomes IDENTIFIED · `measured_count: 0` |
| P325 | Evolution **BLOCKED** |
| `PEOPLE_STATE` | Identity users + HR Employee hire/terminate **TESTED** (workstation) |
| `ROLE_STATE` | Identity Role/Permission (authorization). Not a job-architecture SoR |
| `SKILL_STATE` | **NOT_IMPLEMENTED** |
| `KNOWLEDGE_STATE` | Program docs; no tenant KB; expertise **NOT_IMPLEMENTED** |
| `TRAINING_STATE` | University = student lifecycle. Operator LMS **NOT_IMPLEMENTED** |
| `CAPABILITY_STATE` | Catalog EXISTS; production OPERATIONAL/MATURE **0** |
| `PERFORMANCE_STATE` | CAP-ENT-014 catalog only. Employee performance **NOT_IMPLEMENTED** |
| `STRATEGY_STATE` | PLATFORM_GATE DRAFT only |
| `WORKFORCE_STATE` | Employment records possible; capacity **NOT_MEASURED** |

Users and roles existing ≠ organizational capability to execute strategy.

## 2–9. People systems, capability model, strategy map, roles, skills

See [MEOS_CAPABILITY_MODEL.md](./MEOS_CAPABILITY_MODEL.md) and [MEOS_WORKFORCE_INTELLIGENCE.md](./MEOS_WORKFORCE_INTELLIGENCE.md).

Taxonomy SoR remains [BUSINESS_CAPABILITIES_REGISTRY.md](../architecture/BUSINESS_CAPABILITIES_REGISTRY.md). P333 does **not** fork IDs.

## 10–16. Maturity, gaps, capacity, workload, risk, knowledge, continuity

See YAML + [MEOS_ORGANIZATIONAL_READINESS.md](./MEOS_ORGANIZATIONAL_READINESS.md).

| Claim | Actual |
|-------|--------|
| Capability MATURE / OPERATIONAL | **`operational_count: 0`** · **`mature_count: 0`** |
| CMMI MEASURED / OPTIMIZED | **NOT_MEASURED** |
| Workforce capacity / utilization | **NOT_MEASURED** (do not infer from demo employees) |
| Workload (P330/P331) | Task volume / duration / wait / rework **NOT_MEASURED** |
| Named-person SPOF / skill concentration | **NOT_MEASURED** — do not invent PII risk |
| Crisis command backup | **CRITICAL_ROLE_GAP** (roles `NOT_AVAILABLE`, not named people) |
| Knowledge → skill | P332 `validated_count: 0` → **BLOCKED** |

## 17–24. Training, validation, performance, value, strategic/org/change readiness

Training requirement from gaps is **IDENTIFIED** as documentation (production ops, DSAR, alerting). **No** LMS assignment. Training completion ≠ capability.

Capability validation evidence (assessment, certification, work result, business outcome): **none** in production. TESTED demo loops remain **IMPLEMENTED_UNVERIFIED**.

Performance integration: reuse HR/payroll as employment/pay SoR only. **Do not** create a review engine.

Business value: P326 IDENTIFIED; capability → outcome **NOT_MEASURED**.

Strategic readiness for OBJ-GATE-P314/P317/P326: **BLOCKED**. Organizational / change readiness: **NOT_MEASURED** (P324 not a release candidate).

## 25–28. AI, safety, privacy, tenant isolation

AI may **assist** with gap summaries citing YAML/docs. Must expose evidence and uncertainty. Stub (G18) must not invent skills or experts.

**AI must not** independently decide employment, termination, compensation, promotion, or discipline.

Privacy: data minimization. Do not aggregate employee PII for this overlay. Command-center workforce health remains **NOT_AVAILABLE**. Tenant isolation unchanged (`tenant_id` on HR/identity/org). No cross-tenant workforce export created.

## 29–38. Graph, search, expertise, collective, bottlenecks, automation, risk/continuity/opt/learning

Reuse Knowledge Graph ACL catalogs — **do not** create an org/expertise graph. Live graph **NOT_AVAILABLE**.

Search: conceptual extension (capability/role/skill) **not implemented**. Expertise discovery remains **NOT_IMPLEMENTED** (P332). Distinguish VERIFIED/INFERRED/SELF_DECLARED: **N/A** (no results).

Collective capability at org/tenant: catalog **MAPPED**; scored capability **NOT_MEASURED**. Focus remains organizational, not individual scoring.

Bottlenecks / automation opportunities: P331 candidates IDENTIFIED at platform (outbox, G23); **not** workforce utilization claims. `BLOCK_AUTOMATION` held. Do not automate people decisions.

Risk: GAP-PROD-CLUSTER → R-01; GAP-OBSERVE → R-03; GAP-PRIVACY-DSAR → R-05. No new RISK_IDs.

Continuity: GAP-CRISIS-ROLES → P329 unstaffed command. Backup capability **NOT_VERIFIED**.

Optimization: P331 **BLOCKED**. Do not optimize utilization without outcomes.

Learning: DRAFT lessons must **not** auto-update capability requirements.

## 39–42. Executive view, UX, audit, observability

Extend existing home / AppShell only. Display authorized **gate** language: DRAFT objectives, capability gaps as BLOCKED/NOT_MEASURED. **No** fake skill heatmaps, readiness scores, or named experts.

Audit: overlay is documentation. Do not emit fake `CAPABILITY_VALIDATED` / `SKILL_VALIDATED` / `TRAINING_ASSIGNED`. Future mutations on real capability objects must go through Audit Platform events.

Observability: no new capability-sync pipeline. Mapping is git-versioned YAML.

## 43–44. Documents and integration

| Doc | Role |
|-----|------|
| This file | P333 decision |
| [MEOS_CAPABILITY_MODEL.md](./MEOS_CAPABILITY_MODEL.md) | Overlay on capability registry |
| [MEOS_WORKFORCE_INTELLIGENCE.md](./MEOS_WORKFORCE_INTELLIGENCE.md) | People/skill/capacity honesty |
| [MEOS_ORGANIZATIONAL_READINESS.md](./MEOS_ORGANIZATIONAL_READINESS.md) | Strategy/change/continuity readiness |

Loop TARGET: STRATEGY → CAPABILITY → PEOPLE → KNOWLEDGE → EXECUTION → OUTCOME → LEARNING → CAPABILITY_IMPROVEMENT  
**Actual:** DRAFT strategy → catalog capabilities → employment SoR → DRAFT lessons → no production execution → IDENTIFIED outcomes → unvalidated lessons. Loop **BLOCKED**.

## 45. Unresolved capability gaps

See YAML `gaps:` (8). Material: production cluster (P0), observe/alerting (P0), DSAR (P0), unstaffed continuity roles (P1), outcome measurement (P1), skill/knowledge/capacity **NOT_IMPLEMENTED** / **NOT_MEASURED**.

**Do not** implement a talent platform, LMS, or second capability taxonomy this phase.

## Architecture validation scorecard

| Dimension | Score | Pass? |
|-----------|-------|-------|
| Architecture | 4 | Overlay on registry/identity/HR; no new HRM |
| DDD | 4 | No parallel skill/capability bounded context |
| Security | 4 | No PII aggregation; AI not employment-deciding |
| Scalability | 3 | YAML/docs only |
| Performance | 3 | No extra people-analytics store |
| Testing | 4 | Readiness honesty contract |
| AI Integration | 3 | Stub; cite-or-refuse; HITL for people decisions |
| Documentation | 4 | Taxonomy not forked |
| Accessibility | 3 | Existing shell |
| Localization | 3 | Docs English |
| Observability | 3 | No fake capability-sync metrics |
| Workflow | 3 | Training/tasks not assigned |
| Audit | 4 | No fake VALIDATED events |
| Policy Compliance | 4 | Evidence-only statuses |
| Plugin Compatibility | 4 | Unchanged |

**Verdict:** ENTERPRISE_GRADE as **honest mapping**. Organizational readiness **NOT_MEASURED**. Capability **not** production-OPERATIONAL.

## Reuse analysis

Reused: `BUSINESS_CAPABILITIES_REGISTRY` + JSON catalog, application registry, identity RBAC, `organization`, `human_resources` CAP-ENT-010, `payroll` CAP-ENT-015, Search/Workflow/AI/Audit/Policy, P326–P332 overlays, risk register R-01…R-07, crisis roles, AppShell.  
Rejected: new HRM/HCM/LMS/talent/org-graph; inventing skills, experts, capacity, MATURE, readiness scores; using `university` as operator training; implementing MEKNOL.

## Architectural decisions

- **Decision:** Capability IDs stay in the architecture registry; P333 is status/gap overlay only. **Rejected:** `MEOS_CAPABILITY_TAXONOMY` fork.
- **Decision:** Identity Role ≠ job capability model. **Rejected:** second authorization model.
- **Decision:** Unstaffed P329 command roles are an organizational CRITICAL_ROLE_GAP without naming people. **Rejected:** inventing succession candidates.
- **Long-horizon:** After production + privacy path, skill/evidence objects belong in HR or a dedicated supporting context with events — never by scraping identity users into an expertise index.
