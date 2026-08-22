# MEOS Workforce Intelligence

**Date:** 2026-08-18T17:00:00Z  
**Decision:** Workforce intelligence is **not implemented** as a product. Authoritative people data stays in existing systems. P333 maps those systems honestly and **does not** invent skills, experts, capacity, or performance.  
**Companion:** [MEOS_P333_CAPABILITY_READINESS.md](./MEOS_P333_CAPABILITY_READINESS.md)

## Authoritative people systems (reuse)

| System | Context | What it actually holds | P333 use |
|--------|---------|------------------------|----------|
| Users / sessions / MFA | `identity` | Authentication subjects | Identity SoR |
| Roles / permissions | `identity` + `authorization` | RBAC/ABAC **authorization** | Access control — **not** job architecture |
| Organizations / units / membership | `organization` | Hierarchy + membership | Org structure — **not** expertise graph |
| Employee | `human_resources` | Hire, job_title string, department string, terminate | Employment SoR (CAP-ENT-010) |
| Payroll | `payroll` | Pay lifecycle TESTED | Pay SoR — not performance |
| University | `university` | Student lifecycle | **Not** operator LMS |

`human_resources` `context.yaml` lists JobOpening, Candidate, LeaveRequest, Department; **domain aggregates on disk:** `Employee` only. Treat extra names as **DEFINED**, not OPERATIONAL.

Civilization / space / quantum “skill” catalogs are **blueprint** strings — **not** MEOS skill records.

## Role model

```
IDENTITY ROLE (permission grant)
  ≠ JOB ROLE (responsibility, authority, capabilities, skills)
```

P333 represents authorization roles as they exist. Responsibility/authority/capability/skill/process maps for jobs are **NOT_IMPLEMENTED**. Do **not** create a second identity or authorization model.

Crisis **command** roles (P329) are process roles, all `NOT_AVAILABLE` — organizational gap, not a named-person directory.

## Skill model

| Field | Actual |
|-------|--------|
| SKILL / DOMAIN / LEVEL | **NOT_IMPLEMENTED** · `skill_record_count: 0` |
| EVIDENCE / VALIDATION / EXPIRATION | **N/A** |
| Levels AWARENESS…EXPERT | Vocabulary reserved; **no rows** |

Unsupported skill claims are forbidden. Self-declared expertise is **not** collected.

## Knowledge → skill → role → capability

P332 knowledge is **INVENTORIED**; lessons **DRAFT**. Link to skill/capability: **BLOCKED**. Validated enterprise knowledge does **not** yet support capability development.

## Workforce capacity

AVAILABLE / REQUIRED / UTILIZATION / BOTTLENECK / OVERLOAD / UNDERUTILIZATION: **NOT_MEASURED**.

Do **not** infer capacity from:

- Count of identity users
- Demo HR employees
- Local P313 p95 (STALE_FOR_P331)
- Home pulse open-task **catalog count**

## Workload intelligence (P330/P331)

TASK_VOLUME, WORK_DURATION, WAIT_TIME, REWORK, ESCALATION, MANUAL vs AUTOMATABLE: **NOT_MEASURED** in production. Workflow Task Center exists as code; production loop **NOT_AVAILABLE**. `BLOCK_AUTOMATION` remains.

## Workforce risk (P328) — evidence only

| Type | Actual |
|------|--------|
| SINGLE_POINT_OF_FAILURE (named person) | **NOT_MEASURED** — do not invent |
| CRITICAL_ROLE_GAP | **Yes** — P329 command roles unstaffed (`NOT_AVAILABLE`) |
| SKILL_CONCENTRATION | **NOT_MEASURED** (no skill records) |
| CAPACITY_RISK | **NOT_MEASURED** |
| KNOWLEDGE_LOSS_RISK | **NOT_MEASURED** (no expertise index) |

Do not expose employee PII in this overlay. Knowledge concentration (team/role/person): **NOT_MEASURED**.

## Succession / continuity

CRITICAL_ROLE + BACKUP_CAPABILITY: only the **unstaffed command roster** is evidenced. No HR succession platform. Do **not** build one.

## Training needs / learning path

```
CAPABILITY_GAP → SKILL_GAP → KNOWLEDGE_GAP → TRAINING_REQUIREMENT
```

Documented needs (not assigned enrollments): production operations (G26), alerting (G23), DSAR (G19).  
University ≠ LMS. Completion of training (none assigned) does **not** prove capability. `training_assigned_count: 0`.

## Performance integration

CAP-ENT-014 is **DEFINED** only. Connect ROLE → WORK → OUTCOME using existing workflow/P326 when production exists. **Do not** create another performance-management engine.

## Expertise discovery

TOPIC → SKILL → AUTHORIZED_EXPERT: **NOT_IMPLEMENTED**. No VERIFIED / INFERRED / SELF_DECLARED results to distinguish. Search must not return invented experts. Graph: reuse ACL catalogs; do not add an org graph.

## Collective capability

Analyze at organization/tenant as **catalog mapping** only. Individual scoring **not performed**. `civilization` talent_intelligence is **not** evidence.

## Privacy / AI safety

Purpose: organizational readiness for **platform gates**, not employee ranking.  
AI must not independently make employment, termination, compensation, promotion, or disciplinary decisions.

## Forbidden

- New HRM / HCM / LMS / recruitment / talent / payroll / org-graph product
- Invented skills, experts, utilization %, or performance ratings
- Aggregating HR PII into a “workforce heatmap” on the executive home
