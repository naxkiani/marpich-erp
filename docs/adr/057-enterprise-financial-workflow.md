# ADR-057: Enterprise Financial Workflow

## Status

Accepted

## Context

Financial Kernel (ADR-049) catalog defines a Financial Workflow engine delegating to the Workflow Engine, but lacks implementation for financial-specific approval types. Modules need unified workflows for approval, payment, purchase, expense, transfer, budget, invoice, payroll, tax, and treasury — each with SLA, escalation, AI recommendation, audit, history, and digital signature.

## Decision

Adopt **`docs/architecture/ENTERPRISE_FINANCIAL_WORKFLOW.md`** as canonical financial workflow law within `financial_kernel` context.

Financial Workflow Engine:
- `FinancialWorkflow` aggregate with 10 workflow types
- SLA tracking with configurable hours and breach detection
- Manual and automatic escalation on SLA breach
- AI recommendation stub (risk-scored approve/review/escalate)
- Immutable audit history on every action
- Digital signature after approval
- API prefix: `/api/v1/financial-kernel/workflows/*`

Integration events: `workflow.started`, `workflow.approved`, `workflow.rejected`, `workflow.escalated`, `workflow.signed`

Delegates complex multi-step BPM to Enterprise Workflow Engine (`contexts/workflow/`).

## Consequences

- All modules start financial approvals via kernel API
- Idempotent workflow start via `idempotency_key`
- SLA auto-escalation endpoint for scheduling integration
- Generic Workflow Engine remains for non-financial and complex flows

## Alternatives considered

- Workflow types in each module — rejected (ADR-049 single kernel)
- Workflow Engine only — rejected (financial SLA defaults and AI risk belong in kernel)
