"""Enterprise Cash Management engine."""
from __future__ import annotations

from contexts.treasury.domain.aggregates.cash_management import CashLocationType, CashTransactionType

CASH_MANAGEMENT_CATALOG: dict[str, dict] = {
    "cash_registers": {"label": "Cash Registers", "location_type": CashLocationType.CASH_REGISTER.value},
    "petty_cash": {"label": "Petty Cash", "location_type": CashLocationType.PETTY_CASH.value},
    "main_cash_office": {"label": "Main Cash Office", "location_type": CashLocationType.MAIN_CASH_OFFICE.value},
    "vault": {"label": "Vault", "location_type": CashLocationType.VAULT.value},
    "safe": {"label": "Safe", "location_type": CashLocationType.SAFE.value},
    "branch_cash": {"label": "Branch Cash", "location_type": CashLocationType.BRANCH_CASH.value},
    "department_cash": {"label": "Department Cash", "location_type": CashLocationType.DEPARTMENT_CASH.value},
    "cash_transfer": {"label": "Cash Transfer", "transaction_type": CashTransactionType.TRANSFER.value},
    "cash_deposit": {"label": "Cash Deposit", "transaction_type": CashTransactionType.DEPOSIT.value},
    "cash_withdrawal": {"label": "Cash Withdrawal", "transaction_type": CashTransactionType.WITHDRAWAL.value},
    "cash_receipt": {"label": "Cash Receipt", "transaction_type": CashTransactionType.RECEIPT.value},
    "cash_payment": {"label": "Cash Payment", "transaction_type": CashTransactionType.PAYMENT.value},
    "cash_adjustment": {"label": "Cash Adjustment", "transaction_type": CashTransactionType.ADJUSTMENT.value},
    "cash_counting": {"label": "Cash Counting", "supported": True},
    "cash_verification": {"label": "Cash Verification", "supported": True},
    "cash_closing": {"label": "Cash Closing", "supported": True},
    "cash_reconciliation": {"label": "Cash Reconciliation", "supported": True},
    "cash_forecast": {"label": "Cash Forecast", "supported": True},
    "enterprise_cash_dashboard": {"label": "Enterprise Cash Dashboard", "supported": True},
}


def list_cash_management_catalog() -> list[dict]:
    return [{"capability": k, **v} for k, v in CASH_MANAGEMENT_CATALOG.items()]


def assert_location_type(location_type: str) -> None:
    if location_type not in {t.value for t in CashLocationType}:
        raise ValueError("invalid_cash_location_type")


def assert_transaction_type(transaction_type: str) -> None:
    if transaction_type not in {t.value for t in CashTransactionType}:
        raise ValueError("invalid_cash_transaction_type")


def build_cash_dashboard(
    *,
    locations: list[dict],
    transactions: list[dict],
    counts: list[dict],
    closings: list[dict],
    reconciliations: list[dict],
    forecasts: list[dict],
) -> dict:
    active = [l for l in locations if l.get("status") == "active"]
    total_balance = round(sum(l.get("balance", 0) for l in active), 2)
    by_type: dict[str, float] = {}
    by_branch: dict[str, float] = {}
    for loc in active:
        lt = loc.get("location_type", "unknown")
        by_type[lt] = round(by_type.get(lt, 0) + loc.get("balance", 0), 2)
        branch = loc.get("branch_id") or "unassigned"
        by_branch[branch] = round(by_branch.get(branch, 0) + loc.get("balance", 0), 2)

    open_variances = [c for c in counts if c.get("status") == "draft" and abs(c.get("variance", 0)) > 0]
    open_closings = [c for c in closings if c.get("status") == "open"]
    pending_recon = [r for r in reconciliations if r.get("status") == "variance"]

    return {
        "summary": {
            "location_count": len(active),
            "total_cash_balance": total_balance,
            "transaction_count": len(transactions),
            "open_count_variances": len(open_variances),
            "open_closing_sessions": len(open_closings),
            "pending_reconciliations": len(pending_recon),
            "forecast_count": len(forecasts),
        },
        "balances_by_location_type": by_type,
        "balances_by_branch": by_branch,
        "locations": active,
        "recent_transactions": transactions[:10],
        "recent_counts": counts[:5],
        "recent_closings": closings[:5],
        "recent_reconciliations": reconciliations[:5],
        "forecasts": forecasts[:5],
    }
