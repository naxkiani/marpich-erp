"""Treasury Workflow Engine."""
from __future__ import annotations

from datetime import UTC, datetime

from contexts.treasury.domain.aggregates.treasury_workflow_engine import (
    ApprovalMode,
    WorkflowStatus,
    WorkflowType,
)

WORKFLOW_CATALOG: dict[str, dict] = {
    WorkflowType.TRANSFER_APPROVAL.value: {"label": "Transfer Approval", "supported": True},
    WorkflowType.PAYMENT_APPROVAL.value: {"label": "Payment Approval", "supported": True},
    WorkflowType.FUND_REQUEST.value: {"label": "Fund Request", "supported": True},
    WorkflowType.CASH_REQUEST.value: {"label": "Cash Request", "supported": True},
    WorkflowType.CASH_TRANSFER.value: {"label": "Cash Transfer", "supported": True},
    WorkflowType.INVESTMENT_APPROVAL.value: {"label": "Investment Approval", "supported": True},
    WorkflowType.BANK_ACCOUNT_APPROVAL.value: {"label": "Bank Account Approval", "supported": True},
    "treasury_limits": {"label": "Treasury Limits", "supported": True},
    "escalation": {"label": "Escalation", "supported": True},
    "delegation": {"label": "Delegation", "supported": True},
    ApprovalMode.PARALLEL.value: {"label": "Parallel Approval", "mode": "parallel"},
    ApprovalMode.SEQUENTIAL.value: {"label": "Sequential Approval", "mode": "sequential"},
    "sla_monitoring": {"label": "SLA Monitoring", "default_sla_hours": 48},
    "audit_trail": {"label": "Audit Trail", "supported": True},
    "digital_signature": {"label": "Digital Signature", "supported": True},
    "workflow_designer": {"label": "Workflow Designer", "supported": True},
}

WORKFLOW_TRANSITIONS: dict[str, list[str]] = {
    WorkflowStatus.DRAFT.value: [WorkflowStatus.SUBMITTED.value, WorkflowStatus.PENDING_APPROVAL.value],
    WorkflowStatus.SUBMITTED.value: [WorkflowStatus.PENDING_APPROVAL.value],
    WorkflowStatus.PENDING_APPROVAL.value: [
        WorkflowStatus.APPROVED.value,
        WorkflowStatus.REJECTED.value,
        WorkflowStatus.ESCALATED.value,
    ],
    WorkflowStatus.ESCALATED.value: [
        WorkflowStatus.APPROVED.value,
        WorkflowStatus.REJECTED.value,
    ],
    WorkflowStatus.APPROVED.value: [WorkflowStatus.EXECUTED.value],
}

APPROVAL_EVENT_MAP: dict[str, str] = {
    WorkflowType.TRANSFER_APPROVAL.value: "treasury.transfer.approval.requested",
    WorkflowType.PAYMENT_APPROVAL.value: "treasury.transaction.approval.requested",
    WorkflowType.CASH_TRANSFER.value: "treasury.transfer.approval.requested",
    WorkflowType.INVESTMENT_APPROVAL.value: "treasury.transaction.approval.requested",
    WorkflowType.BANK_ACCOUNT_APPROVAL.value: "treasury.bank_account.approval.requested",
    WorkflowType.FUND_REQUEST.value: "treasury.transfer.approval.requested",
    WorkflowType.CASH_REQUEST.value: "treasury.transfer.approval.requested",
}


def list_workflow_catalog() -> list[dict]:
    return [{"capability": k, **v} for k, v in WORKFLOW_CATALOG.items()]


def list_workflow_states() -> list[dict]:
    terminal = [WorkflowStatus.REJECTED.value, WorkflowStatus.EXECUTED.value, WorkflowStatus.CANCELLED.value]
    states = [{"status": s, "allowed_transitions": t} for s, t in WORKFLOW_TRANSITIONS.items()]
    states.extend({"status": s, "allowed_transitions": []} for s in terminal)
    return states


def resolve_required_levels(amount: float, limits: list[dict], workflow_type: str) -> int:
    applicable = [
        lim for lim in limits
        if lim.get("workflow_type") == workflow_type and lim.get("is_active", True)
    ]
    if not applicable:
        if amount <= 1000:
            return 0
        if amount <= 10000:
            return 1
        if amount <= 50000:
            return 2
        return 3

    for lim in sorted(applicable, key=lambda x: x["max_amount"]):
        if amount <= lim["max_amount"]:
            return lim.get("approval_levels", 1)
    return applicable[-1].get("approval_levels", 3)


def build_workflow_steps(
    *,
    approval_mode: str,
    required_levels: int,
    step_roles: list[str] | None = None,
) -> list[dict]:
    roles = step_roles or [f"approver_level_{i + 1}" for i in range(max(required_levels, 1))]
    steps = []
    for i, role in enumerate(roles[: max(required_levels, 1)]):
        steps.append(
            {
                "step_id": f"step-{i + 1}",
                "level": i + 1,
                "role": role,
                "order": i + 1 if approval_mode == ApprovalMode.SEQUENTIAL.value else 0,
            }
        )
    return steps


def build_workflow_designer_view(*, definitions: list[dict]) -> dict:
    by_type: dict[str, list[dict]] = {}
    for d in definitions:
        wt = d.get("workflow_type", "unknown")
        by_type.setdefault(wt, []).append(d)

    return {
        "definition_count": len(definitions),
        "by_workflow_type": by_type,
        "approval_modes": [ApprovalMode.SEQUENTIAL.value, ApprovalMode.PARALLEL.value],
        "workflow_types": [wt.value for wt in WorkflowType],
        "definitions": definitions,
    }


def build_workflow_dashboard(
    *,
    requests: list[dict],
    definitions: list[dict],
    limits: list[dict],
) -> dict:
    by_status: dict[str, int] = {}
    by_type: dict[str, int] = {}
    sla_breached = 0
    pending = 0
    escalated = 0

    for req in requests:
        status = req.get("status", "unknown")
        wtype = req.get("workflow_type", "unknown")
        by_status[status] = by_status.get(status, 0) + 1
        by_type[wtype] = by_type.get(wtype, 0) + 1
        if req.get("sla_breached"):
            sla_breached += 1
        if status == WorkflowStatus.PENDING_APPROVAL.value:
            pending += 1
        if status == WorkflowStatus.ESCALATED.value:
            escalated += 1

    return {
        "as_of": datetime.now(UTC).isoformat(),
        "summary": {
            "total_requests": len(requests),
            "pending_approval": pending,
            "escalated": escalated,
            "sla_breached": sla_breached,
            "active_definitions": len([d for d in definitions if d.get("is_active")]),
            "active_limits": len([l for l in limits if l.get("is_active")]),
        },
        "by_status": by_status,
        "by_workflow_type": by_type,
        "recent_requests": requests[:10],
        "workflow_states": list_workflow_states(),
    }


def monitor_sla(*, requests: list[dict]) -> dict:
    breached = [r for r in requests if r.get("sla_breached")]
    pending = [
        r for r in requests
        if r.get("status") in {WorkflowStatus.PENDING_APPROVAL.value, WorkflowStatus.ESCALATED.value}
    ]
    return {
        "monitored_at": datetime.now(UTC).isoformat(),
        "pending_count": len(pending),
        "sla_breached_count": len(breached),
        "breached_requests": breached,
        "pending_requests": pending[:20],
    }


def generate_digital_signature_hash(*, request_id: str, step_id: str, approver_id: str) -> str:
    import hashlib

    payload = f"{request_id}:{step_id}:{approver_id}:{datetime.now(UTC).isoformat()}"
    return hashlib.sha256(payload.encode()).hexdigest()[:32]
