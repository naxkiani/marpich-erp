"""Enterprise Cash Reconciliation Engine."""
from __future__ import annotations

from contexts.treasury.domain.aggregates.cash_reconciliation_engine import (
    CashReconStatus,
    ClosingType,
    VarianceType,
)

CASH_RECONCILIATION_CATALOG: dict[str, dict] = {
    "cash_count": {"label": "Cash Count", "supported": True},
    "cash_difference": {"label": "Cash Difference", "supported": True},
    "cash_over": {"label": "Cash Over", "variance_type": VarianceType.CASH_OVER.value},
    "cash_short": {"label": "Cash Short", "variance_type": VarianceType.CASH_SHORT.value},
    "cash_verification": {"label": "Cash Verification", "supported": True},
    "cash_approval": {"label": "Cash Approval", "manager_required_on_variance": True},
    "cash_closing": {"label": "Cash Closing", "closing_type": ClosingType.CASH_CLOSING.value},
    "shift_closing": {"label": "Shift Closing", "closing_type": ClosingType.SHIFT_CLOSING.value},
    "branch_closing": {"label": "Branch Closing", "closing_type": ClosingType.BRANCH_CLOSING.value},
    "discrepancy_report": {"label": "Discrepancy Report", "supported": True},
    "ai_anomaly_detection": {"label": "AI Anomaly Detection", "autonomous_execution": False},
}

WORKFLOW_TRANSITIONS: dict[str, list[str]] = {
    CashReconStatus.DRAFT.value: [CashReconStatus.COUNTED.value],
    CashReconStatus.COUNTED.value: [CashReconStatus.VERIFIED.value],
    CashReconStatus.VERIFIED.value: [
        CashReconStatus.PENDING_MANAGER_APPROVAL.value,
        CashReconStatus.APPROVED.value,
    ],
    CashReconStatus.PENDING_MANAGER_APPROVAL.value: [
        CashReconStatus.APPROVED.value,
        CashReconStatus.REJECTED.value,
    ],
    CashReconStatus.APPROVED.value: [CashReconStatus.CLOSED.value],
}

VARIANCE_APPROVAL_THRESHOLD = 0.01


def list_cash_reconciliation_catalog() -> list[dict]:
    return [{"capability": k, **v} for k, v in CASH_RECONCILIATION_CATALOG.items()]


def list_workflow_states() -> list[dict]:
    terminal = [CashReconStatus.REJECTED.value, CashReconStatus.CLOSED.value]
    states = [{"status": s, "allowed_transitions": t} for s, t in WORKFLOW_TRANSITIONS.items()]
    states.extend({"status": s, "allowed_transitions": []} for s in terminal)
    return states


def classify_variance(variance: float) -> str:
    if abs(variance) < VARIANCE_APPROVAL_THRESHOLD:
        return VarianceType.BALANCED.value
    return VarianceType.CASH_OVER.value if variance > 0 else VarianceType.CASH_SHORT.value


def requires_manager_approval(variance: float) -> bool:
    return abs(variance) >= VARIANCE_APPROVAL_THRESHOLD


def build_discrepancy_report(
    *,
    location_id: str,
    location_name: str,
    closing_type: str,
    system_balance: float,
    counted_amount: float,
    variance: float,
    variance_type: str,
    currency: str,
    branch_id: str | None = None,
) -> dict:
    return {
        "location_id": location_id,
        "location_name": location_name,
        "branch_id": branch_id,
        "closing_type": closing_type,
        "system_balance": system_balance,
        "counted_amount": counted_amount,
        "variance": variance,
        "variance_type": variance_type,
        "currency": currency,
        "cash_difference": variance,
        "cash_over": variance if variance_type == VarianceType.CASH_OVER.value else 0,
        "cash_short": abs(variance) if variance_type == VarianceType.CASH_SHORT.value else 0,
        "balanced": variance_type == VarianceType.BALANCED.value,
        "requires_manager_approval": requires_manager_approval(variance),
    }


def detect_ai_anomalies(
    *,
    system_balance: float,
    counted_amount: float,
    variance: float,
    historical_variances: list[float],
    closing_type: str,
) -> list[dict]:
    anomalies: list[dict] = []
    pct = abs(variance / system_balance * 100) if system_balance else 0

    if abs(variance) >= VARIANCE_APPROVAL_THRESHOLD:
        anomalies.append(
            {
                "priority": "high",
                "category": "variance",
                "message": f"Cash {classify_variance(variance)} of {abs(variance):.2f} detected.",
                "variance": variance,
                "autonomous_execution": False,
            }
        )

    if pct > 5 and system_balance > 0:
        anomalies.append(
            {
                "priority": "high",
                "category": "high_variance_pct",
                "message": f"Variance exceeds 5% of system balance ({pct:.1f}%).",
                "variance_pct": round(pct, 2),
                "autonomous_execution": False,
            }
        )

    if historical_variances:
        avg = sum(historical_variances) / len(historical_variances)
        if abs(variance) > abs(avg) * 2 and abs(variance) >= VARIANCE_APPROVAL_THRESHOLD:
            anomalies.append(
                {
                    "priority": "medium",
                    "category": "unusual_pattern",
                    "message": f"Variance {variance} is 2x historical average ({avg:.2f}).",
                    "historical_avg": round(avg, 2),
                    "autonomous_execution": False,
                }
            )

    if closing_type == ClosingType.BRANCH_CLOSING.value and abs(variance) >= 100:
        anomalies.append(
            {
                "priority": "medium",
                "category": "branch_closing",
                "message": "Large branch closing variance — review all location counts.",
                "autonomous_execution": False,
            }
        )

    if not anomalies and abs(variance) < VARIANCE_APPROVAL_THRESHOLD:
        anomalies.append(
            {
                "priority": "low",
                "category": "normal",
                "message": "Cash count balanced — no anomalies detected.",
                "autonomous_execution": False,
            }
        )

    return anomalies


def build_cash_reconciliation_dashboard(*, runs: list[dict]) -> dict:
    by_status: dict[str, int] = {}
    by_variance: dict[str, int] = {}
    pending_approval = 0
    total_over = 0.0
    total_short = 0.0

    for run in runs:
        status = run.get("status", "unknown")
        vtype = run.get("variance_type", "balanced")
        by_status[status] = by_status.get(status, 0) + 1
        by_variance[vtype] = by_variance.get(vtype, 0) + 1
        if status == CashReconStatus.PENDING_MANAGER_APPROVAL.value:
            pending_approval += 1
        if vtype == VarianceType.CASH_OVER.value:
            total_over += run.get("variance", 0)
        elif vtype == VarianceType.CASH_SHORT.value:
            total_short += abs(run.get("variance", 0))

    return {
        "summary": {
            "run_count": len(runs),
            "pending_manager_approval": pending_approval,
            "total_cash_over": round(total_over, 2),
            "total_cash_short": round(total_short, 2),
        },
        "by_status": by_status,
        "by_variance_type": by_variance,
        "recent_runs": runs[:10],
        "workflow_states": list_workflow_states(),
    }
