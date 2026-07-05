"""Deposit Management engine."""
from __future__ import annotations

from datetime import UTC, datetime, timedelta

from contexts.banking.domain.aggregates.deposit_management_engine import (
    DepositStatus,
    DepositType,
    TransactionType,
)

DEPOSIT_MANAGEMENT_CATALOG: dict[str, dict] = {
    DepositType.SAVINGS.value: {"label": "Savings Deposits", "supported": True},
    DepositType.CURRENT.value: {"label": "Current Deposits", "supported": True},
    DepositType.TERM.value: {"label": "Term Deposits", "supported": True},
    DepositType.RECURRING.value: {"label": "Recurring Deposits", "supported": True},
    "profit_distribution_rules": {"label": "Profit Distribution Rules", "supported": True},
    "interest_calculation": {"label": "Interest Calculation", "supported": True},
    "interest_accrual": {"label": "Interest Accrual", "supported": True},
    "maturity": {"label": "Maturity", "supported": True},
    "renewal": {"label": "Renewal", "supported": True},
    "early_withdrawal_rules": {"label": "Early Withdrawal Rules", "policy_key": "deposit.early_withdrawal.penalty"},
    "deposit_certificates": {"label": "Deposit Certificates", "supported": True},
    "deposit_statements": {"label": "Deposit Statements", "supported": True},
    "automatic_gl_posting": {"label": "Automatic General Ledger Posting", "supported": True},
    "approval_workflow": {"label": "Approval Workflow", "supported": True},
    "audit_trail": {"label": "Audit Trail", "supported": True},
}

DEPOSIT_POLICY_KEYS: list[dict] = [
    {"key": "deposit.interest.rate", "description": "Interest rate by deposit type"},
    {"key": "deposit.early_withdrawal.penalty", "description": "Early withdrawal penalty rules"},
    {"key": "deposit.term.maturity_notice", "description": "Maturity notice period in days"},
    {"key": "deposit.recurring.schedule", "description": "Recurring deposit schedule rules"},
    {"key": "deposit.profit.distribution", "description": "Profit sharing distribution rules"},
    {"key": "deposit.approval.required_level", "description": "Approval levels for deposit transactions"},
]


def list_deposit_catalog() -> list[dict]:
    return [{"capability": k, **v} for k, v in DEPOSIT_MANAGEMENT_CATALOG.items()]


def list_deposit_policy_keys() -> list[dict]:
    return DEPOSIT_POLICY_KEYS


def calculate_daily_interest(*, principal: float, rate_annual: float, days: int = 1) -> float:
    if principal <= 0 or rate_annual <= 0 or days <= 0:
        return 0.0
    return round(principal * (rate_annual / 100) * (days / 365), 2)


def calculate_early_withdrawal_penalty(
    *, amount: float, penalty_pct: float, policy_outcome: str | None
) -> float:
    if policy_outcome == "waive_penalty":
        return 0.0
    if penalty_pct <= 0:
        return 0.0
    return round(amount * (penalty_pct / 100), 2)


def resolve_approval_levels(*, transaction_type: str, amount: float) -> int:
    if transaction_type == TransactionType.WITHDRAWAL.value and amount >= 10000:
        return 2
    if transaction_type == TransactionType.MATURITY_PAYOUT.value:
        return 1
    if amount >= 50000:
        return 2
    return 1


def build_deposit_dashboard(
    *,
    deposits: list[dict],
    transactions: list[dict],
    accruals: list[dict],
    certificates: list[dict],
) -> dict:
    by_type: dict[str, int] = {}
    by_status: dict[str, int] = {}
    total_principal = 0.0
    total_accrued = 0.0
    pending_txns = 0

    for d in deposits:
        by_type[d.get("deposit_type", "unknown")] = by_type.get(d.get("deposit_type", "unknown"), 0) + 1
        by_status[d.get("status", "unknown")] = by_status.get(d.get("status", "unknown"), 0) + 1
        if d.get("status") == DepositStatus.ACTIVE.value:
            total_principal += d.get("principal", 0)
            total_accrued += d.get("accrued_interest", 0)

    for t in transactions:
        if t.get("status") == "pending":
            pending_txns += 1

    matured = by_status.get(DepositStatus.MATURED.value, 0)

    return {
        "as_of": datetime.now(UTC).isoformat(),
        "summary": {
            "deposit_count": len(deposits),
            "active_deposits": by_status.get(DepositStatus.ACTIVE.value, 0),
            "matured_deposits": matured,
            "total_principal": round(total_principal, 2),
            "total_accrued_interest": round(total_accrued, 2),
            "pending_transactions": pending_txns,
            "accrual_count": len(accruals),
            "certificate_count": len(certificates),
        },
        "by_deposit_type": by_type,
        "by_status": by_status,
        "policy_keys": list_deposit_policy_keys(),
    }


def build_statement_lines(
    *,
    transactions: list[dict],
    period_start: datetime,
    period_end: datetime,
) -> tuple[list[dict], float, float, float]:
    lines: list[dict] = []
    credits = 0.0
    debits = 0.0
    interest = 0.0

    for txn in transactions:
        posted = txn.get("posted_at") or txn.get("created_at")
        if not posted:
            continue
        ts = datetime.fromisoformat(posted.replace("Z", "+00:00"))
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=UTC)
        if not (period_start <= ts <= period_end):
            continue
        if txn.get("status") != "posted":
            continue

        ttype = txn.get("transaction_type", "")
        amount = txn.get("net_amount") or txn.get("amount", 0)
        if ttype in {TransactionType.DEPOSIT.value, TransactionType.INTEREST_CREDIT.value, TransactionType.PROFIT_DISTRIBUTION.value}:
            credits += amount
            if ttype == TransactionType.INTEREST_CREDIT.value:
                interest += amount
        else:
            debits += amount

        lines.append(
            {
                "date": ts.isoformat(),
                "type": ttype,
                "reference": txn.get("transaction_ref"),
                "amount": amount,
                "status": txn.get("status"),
            }
        )

    return lines, round(credits, 2), round(debits, 2), round(interest, 2)
