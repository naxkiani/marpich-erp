# MEOS Process Orchestration

**Date:** 2026-08-18T06:40:00Z  
**SoR:** Workflow Engine + Event Fabric + domain ACLs. No second orchestrator.

## Intended path

```
APPLICATION → EVENT → RULE/POLICY → TASK → APPROVAL → ACTION → AUDIT
```

## Actual Q2C chain (coded, not production-active)

```
CRM opportunity won
  → sales ACL drafts quotation
  → order placed
  → inventory reserves SKU
  → accounting AR invoice / payment received
  → procurement restock (when reorder)
  → notifications (finance.payment.received subscription)
  → audit via integration events
```

Evidence: Wave 02 script + P313 G10/G13 **PASS** on workstation Postgres.  
Traceability: event envelope `tenant_id`, `correlation_id`, `event_id`.  
Compensation if a mid-chain step fails: **NOT_IMPLEMENTED** as a generic saga (do not pretend distributed transactions exist).

## Actual care chain (coded, not production-active)

```
hospital/clinic encounter
  → laboratory / pharmacy ACL projections
```

Clinical decisions must remain HITL. P319 does **not** add autonomous diagnosis or prescribe.

## Workflow orchestration

`ProcessDefinition` → `ProcessInstance` → `Task` (Task Center).  
Human work from automation **must** use this inbox — no parallel task product.

## Cross-application observability

Discoverability via existing Search (event index) and Audit desks **when** those services have data. Production search of workflow executions: **NOT_AVAILABLE**.
