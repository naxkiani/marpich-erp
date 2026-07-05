"""Banking Payment Platform engine — catalog, fraud, limits."""
from __future__ import annotations

from datetime import UTC, datetime

from contexts.banking.domain.aggregates.payment_platform_engine import (
    FraudStatus,
    TransferStatus,
    TransferType,
)

PAYMENT_PLATFORM_CATALOG: dict[str, dict] = {
    TransferType.INTERNAL.value: {"label": "Internal Transfer", "supported": True},
    TransferType.INTER_BRANCH.value: {"label": "Inter-Branch Transfer", "supported": True},
    TransferType.BANK_TO_BANK.value: {"label": "Bank-to-Bank Transfer", "supported": True},
    TransferType.BULK.value: {"label": "Bulk Transfer", "supported": True},
    "scheduled_transfer": {"label": "Scheduled Transfer", "supported": True},
    "standing_orders": {"label": "Standing Orders", "supported": True},
    TransferType.BILL_PAYMENT.value: {"label": "Bill Payment", "supported": True},
    TransferType.GOVERNMENT_PAYMENT.value: {"label": "Government Payment", "supported": True},
    TransferType.SALARY_TRANSFER.value: {"label": "Salary Transfer", "supported": True},
    TransferType.MERCHANT_PAYMENT.value: {"label": "Merchant Payment", "supported": True},
    TransferType.QR_PAYMENT.value: {"label": "QR Payment", "supported": True},
    TransferType.REAL_TIME.value: {"label": "Real-Time Payment", "supported": True},
    "transfer_limits": {"label": "Transfer Limits", "policy_key": "payment.transfer.daily_limit"},
    "approval_workflow": {"label": "Approval Workflow", "supported": True},
    "fraud_checks": {"label": "Fraud Checks", "policy_key": "payment.fraud.threshold"},
    "automatic_gl_posting": {"label": "Automatic General Ledger Posting", "supported": True},
    "audit_trail": {"label": "Audit Trail", "supported": True},
}

PAYMENT_POLICY_KEYS: list[dict] = [
    {"key": "payment.transfer.daily_limit", "description": "Per-customer daily transfer limit"},
    {"key": "payment.transfer.single_limit", "description": "Maximum single transfer amount"},
    {"key": "payment.approval.required_level", "description": "Approval levels for transfers"},
    {"key": "payment.fraud.threshold", "description": "Fraud score thresholds and actions"},
    {"key": "payment.fraud.velocity", "description": "Transfer velocity fraud rules"},
    {"key": "payment.scheduled.execution", "description": "Scheduled transfer execution rules"},
    {"key": "payment.standing_order.rules", "description": "Standing order frequency and limits"},
    {"key": "payment.real_time.settlement", "description": "Real-time payment settlement rules"},
    {"key": "payment.government.routing", "description": "Government payment routing codes"},
    {"key": "payment.salary.batch", "description": "Salary transfer batch rules"},
]

REAL_TIME_TYPES = {
    TransferType.REAL_TIME.value,
    TransferType.QR_PAYMENT.value,
    TransferType.MERCHANT_PAYMENT.value,
}


def list_payment_catalog() -> list[dict]:
    return [{"capability": k, **v} for k, v in PAYMENT_PLATFORM_CATALOG.items()]


def list_payment_policy_keys() -> list[dict]:
    return PAYMENT_POLICY_KEYS


def resolve_approval_levels(*, transfer_type: str, amount: float) -> int:
    if transfer_type in {TransferType.GOVERNMENT_PAYMENT.value, TransferType.SALARY_TRANSFER.value}:
        return 2
    if amount >= 100000:
        return 3
    if amount >= 25000:
        return 2
    if transfer_type == TransferType.BULK.value:
        return 2
    return 1


def check_transfer_limits(
    *,
    amount: float,
    daily_total: float,
    daily_limit: float,
    single_limit: float,
    policy_outcome: str | None,
) -> tuple[bool, str | None]:
    if policy_outcome == "deny":
        return False, "banking.errors.transfer_limit_exceeded"
    if single_limit > 0 and amount > single_limit:
        return False, "banking.errors.single_transfer_limit_exceeded"
    if daily_limit > 0 and daily_total + amount > daily_limit:
        return False, "banking.errors.daily_transfer_limit_exceeded"
    return True, None


def run_fraud_check(
    *,
    amount: float,
    transfer_type: str,
    channel: str,
    velocity_count: int,
    policy_thresholds: dict,
) -> dict:
    score = 100.0
    factors: list[dict] = []
    block_threshold = float(policy_thresholds.get("block_score", 30))
    review_threshold = float(policy_thresholds.get("review_score", 60))
    velocity_limit = int(policy_thresholds.get("velocity_limit", 10))

    if amount >= float(policy_thresholds.get("large_amount", 50000)):
        score -= 25
        factors.append({"factor": "large_amount", "value": amount, "impact": -25})

    if transfer_type in REAL_TIME_TYPES:
        score -= 5
        factors.append({"factor": "real_time_channel", "value": transfer_type, "impact": -5})

    if channel in {"qr", "mobile", "atm"}:
        score -= 10
        factors.append({"factor": "high_risk_channel", "value": channel, "impact": -10})

    if velocity_count >= velocity_limit:
        score -= 30
        factors.append({"factor": "velocity", "value": velocity_count, "impact": -30})

    score = max(0, round(score, 2))
    if score < block_threshold:
        status = FraudStatus.BLOCKED.value
    elif score < review_threshold:
        status = FraudStatus.REVIEW.value
    else:
        status = FraudStatus.CLEAR.value

    return {"risk_score": score, "status": status, "factors": factors}


def map_transfer_channel(transfer_type: str) -> str:
    mapping = {
        TransferType.QR_PAYMENT.value: "qr",
        TransferType.MERCHANT_PAYMENT.value: "pos",
        TransferType.REAL_TIME.value: "real_time",
        TransferType.INTER_BRANCH.value: "branch",
        TransferType.BANK_TO_BANK.value: "interbank",
    }
    return mapping.get(transfer_type, "digital")


def build_payment_dashboard(
    *,
    transfers: list[dict],
    batches: list[dict],
    standing_orders: list[dict],
    fraud_checks: list[dict],
) -> dict:
    by_type: dict[str, int] = {}
    by_status: dict[str, int] = {}
    total_volume = 0.0

    for t in transfers:
        by_type[t.get("transfer_type", "unknown")] = by_type.get(t.get("transfer_type", "unknown"), 0) + 1
        by_status[t.get("status", "unknown")] = by_status.get(t.get("status", "unknown"), 0) + 1
        if t.get("status") == TransferStatus.COMPLETED.value:
            total_volume += t.get("amount", 0)

    blocked = sum(1 for f in fraud_checks if f.get("status") == FraudStatus.BLOCKED.value)

    return {
        "as_of": datetime.now(UTC).isoformat(),
        "summary": {
            "transfer_count": len(transfers),
            "completed_transfers": by_status.get(TransferStatus.COMPLETED.value, 0),
            "pending_approval": by_status.get(TransferStatus.PENDING_APPROVAL.value, 0),
            "scheduled_transfers": by_status.get(TransferStatus.SCHEDULED.value, 0),
            "batch_count": len(batches),
            "standing_order_count": len(standing_orders),
            "total_completed_volume": round(total_volume, 2),
            "fraud_blocked_count": blocked,
        },
        "by_transfer_type": by_type,
        "by_status": by_status,
        "policy_keys": list_payment_policy_keys(),
    }
