# MEOS Knowledge Governance

**Date:** 2026-08-18T14:05:00Z  
**Architecture (not runtime):** P307 MEKNOL / `knowledge_operating` — **not** in `contexts/registry.py`. **Do not implement it here.**  
**Reuse:** Documents (`documents`) · Search (`search`) · Analytics graph ACL · Policy · Audit · Workflow · AI assist stub.

P332 does **not** create a wiki, LMS, second graph, second search, or document platform.

## Inventory (authoritative program sources)

| Type | Where | Production tenant KB |
|------|-------|----------------------|
| POLICY | Policy Engine + architecture policy docs | Evaluate API exists; prod **NOT_AVAILABLE** |
| PROCEDURE / RUNBOOK | `docs/meos/execution/*RUNBOOK*`, IR, DR, rollback | **DOCUMENTED** |
| DECISION | [MEOS_DECISION_REGISTRY.v1.yaml](./MEOS_DECISION_REGISTRY.v1.yaml) | DECIDE-only; outcomes **NOT_MEASURED** |
| LESSON | [MEOS_LESSONS_LEARNED.v1.yaml](./MEOS_LESSONS_LEARNED.v1.yaml) | **DRAFT** · `validated_count: 0` |
| INCIDENT | [MEOS_INCIDENT_RESPONSE.md](./MEOS_INCIDENT_RESPONSE.md) | Log empty |
| RISK / CONTROL | Launch register + control matrix | ASSESSED; not MONITORED |
| ARCHITECTURE | `docs/architecture/` | Canonical law |
| BUSINESS_PROCESS | P326 outcome registry | IDENTIFIED |
| TRAINING / FAQ / EXPERTISE | — | **NOT_IMPLEMENTED** as MEOS LMS |
| AI_CONTEXT | Copilot → `/ai/assist` | Stub (G18) |

University module is an **education vertical**, not an operator LMS.

## Authority classes

`AUTHORITATIVE` · `VALIDATED` · `USER_GENERATED` · `AI_GENERATED` · `UNVERIFIED` · `PROGRAM_DOCUMENT`

AI-generated must **never** silently become AUTHORITATIVE. Stub output is **UNVERIFIED** / not FACT.

Documents in `docs/meos/execution` are **PROGRAM_DOCUMENT** (launch SoR), not tenant-published knowledge objects with owners.

## Lifecycle

```
CAPTURE → REVIEW → VALIDATE → PUBLISH → USE → REASSESS → UPDATE → DEPRECATE
```

No runtime knowledge aggregate this phase. Freshness: P313 p95 marked **STALE_FOR_P331**. Review intervals / expiry: **NOT_SET**. Owners: **NOT_AVAILABLE**.

## Gaps / conflicts (evidence, not a scanner)

| Gap / conflict | Evidence |
|----------------|----------|
| MISSING tenant KB | `knowledge_operating` not in registry |
| UNOWNED | All P327–P331 owners **NOT_AVAILABLE** |
| OUTDATED | Local p95 **STALE_FOR_P331** |
| UNVERIFIED | AI stub; graph/search production **NOT_AVAILABLE** |
| CONFLICT | Privacy pack “ACTIVATED” vs G19 DSAR **FAIL** |
| CONFLICT | Analytics `maximize_profit` examples vs not tenant OKRs |
| CONFLICT | P316 quality CRITICAL vs P329 declared crisis **NONE** |
| CONFLICT | Local `RTO_MS=22762` vs production RTO **NOT_VERIFIED** |

Do not auto-resolve. Governance required.

## Search / graph

Search: Wave 03 event index; production **NOT_AVAILABLE**. Authority facet on hits: **NOT_IMPLEMENTED**.  
Graph: P213-L ACL / BI graph docs; live GOAL→LESSON graph **NOT_AVAILABLE**. **No second graph.**

## Security / privacy

Knowledge retrieval must use JWT + permissions + tenant_id. Copilot must not dump other-tenant docs. Do not ingest PII into a generalized store — none created this phase.

## Quality / analytics

No arbitrary quality score. MOST_USED / STALE / CONFLICTED metrics: **NOT_MEASURED** (no production usage telemetry).
