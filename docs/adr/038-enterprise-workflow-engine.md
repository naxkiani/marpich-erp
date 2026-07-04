# ADR-038: Enterprise Workflow Engine — Visual Designer + Runtime

## Status

Accepted

## Context

Marpich requires enterprise BPM for approvals across procurement, HR, finance, and industry modules. The existing `workflow` context implements sequential steps, tasks, delegation, and definition versioning — but lacks a canonical design for visual drag-and-drop builder, parallel/conditional flows, SLA, signatures, AI decisions, rollback, and full history.

Product leadership mandated: **Workflow Builder must be visual** with comprehensive enterprise capabilities; modules must not duplicate approval engines.

## Decision

Adopt **`docs/architecture/ENTERPRISE_WORKFLOW_ENGINE.md`** as canonical workflow law.

### Visual Workflow Designer

- Drag-and-drop canvas (React Flow target)
- Node palette: approvals, gateways, timers, SLA, notifications, signature, AI decision, rollback
- Validates against `docs/architecture/workflow/DEFINITION_SCHEMA.v1.yaml`
- Draft → publish creates immutable `ProcessDefinition` version

### Runtime engine

- Graph interpreter with token/state management
- Integrates Notification, Documents, AI, Scheduling, Event Bus, Audit, Identity
- Append-only `WorkflowHistory`
- Compensation/rollback subgraphs

### Module integration

- Start via REST or integration event trigger
- Outcomes via `workflow.process.completed` / `rejected` / `rolled_back`
- No module-local approval state machines

### Existing code

Current step-list engine remains valid for simple flows; graph interpreter is incremental migration path.

## Consequences

- Designer frontend is new work (`apps/web/workflow-designer/`)
- Extended REST API for draft/publish/history/rollback
- New integration events: `workflow.sla.breached`, `workflow.process.rolled_back`, etc.
- Modules refactor local approvals to workflow triggers over time

## Alternatives considered

- Embed Camunda/Temporal fully — rejected for tenant multi-model control and platform integration consistency
- JSON-only workflow editing — rejected; visual builder is mandatory
- Per-module approval tables — rejected; violates Platform Charter
