"""Treasury Transaction Engine — catalog, workflow, approval, posting rules."""
from __future__ import annotations

from contexts.treasury.domain.aggregates.treasury_transaction import (
    TransactionWorkflowStatus,
    TreasuryTransactionType,
)

TRANSACTION_ENGINE_CATALOG: dict[str, dict] = {
    TreasuryTransactionType.INTERNAL_TRANSFER.value: {
        "label": "Internal Transfers",
        "requires_accounts": True,
        "dual_account": True,
    },
    TreasuryTransactionType.BANK_TRANSFER.value: {
        "label": "Bank Transfers",
        "requires_accounts": True,
        "dual_account": True,
    },
    TreasuryTransactionType.WIRE_TRANSFER.value: {
        "label": "Wire Transfers",
        "requires_accounts": True,
        "dual_account": True,
        "always_approve": True,
    },
    TreasuryTransactionType.CASH_MOVEMENT.value: {
        "label": "Cash Movement",
        "requires_accounts": True,
        "dual_account": True,
    },
    TreasuryTransactionType.FUND_ALLOCATION.value: {
        "label": "Fund Allocation",
        "requires_accounts": True,
        "dual_account": True,
    },
    TreasuryTransactionType.TREASURY_SETTLEMENT.value: {
        "label": "Treasury Settlement",
        "requires_accounts": True,
        "dual_account": True,
        "always_approve": True,
    },
    TreasuryTransactionType.INVESTMENT_PURCHASE.value: {
        "label": "Investment Purchase",
        "requires_accounts": True,
        "dual_account": True,
        "always_approve": True,
    },
    TreasuryTransactionType.INVESTMENT_SALE.value: {
        "label": "Investment Sale",
        "requires_accounts": True,
        "dual_account": True,
        "always_approve": True,
    },
    TreasuryTransactionType.DEBT_PAYMENT.value: {
        "label": "Debt Payment",
        "requires_accounts": True,
        "dual_account": False,
        "always_approve": True,
    },
    TreasuryTransactionType.INTEREST_PAYMENT.value: {
        "label": "Interest Payment",
        "requires_accounts": True,
        "dual_account": False,
    },
    TreasuryTransactionType.LOAN_DISBURSEMENT.value: {
        "label": "Loan Disbursement",
        "requires_accounts": True,
        "dual_account": False,
        "always_approve": True,
    },
    TreasuryTransactionType.LOAN_REPAYMENT.value: {
        "label": "Loan Repayment",
        "requires_accounts": True,
        "dual_account": False,
    },
}

TRANSACTION_POSTING_RULE_MAP: dict[str, str] = {
    TreasuryTransactionType.INTERNAL_TRANSFER.value: "treasury_internal_transfer",
    TreasuryTransactionType.BANK_TRANSFER.value: "treasury_bank_transfer",
    TreasuryTransactionType.WIRE_TRANSFER.value: "treasury_wire_transfer",
    TreasuryTransactionType.CASH_MOVEMENT.value: "treasury_cash_movement",
    TreasuryTransactionType.FUND_ALLOCATION.value: "treasury_fund_allocation",
    TreasuryTransactionType.TREASURY_SETTLEMENT.value: "treasury_settlement",
    TreasuryTransactionType.INVESTMENT_PURCHASE.value: "treasury_investment_purchase",
    TreasuryTransactionType.INVESTMENT_SALE.value: "treasury_investment_sale",
    TreasuryTransactionType.DEBT_PAYMENT.value: "treasury_debt_payment",
    TreasuryTransactionType.INTEREST_PAYMENT.value: "treasury_interest_payment",
    TreasuryTransactionType.LOAN_DISBURSEMENT.value: "treasury_loan_disbursement",
    TreasuryTransactionType.LOAN_REPAYMENT.value: "treasury_loan_repayment",
}

APPROVAL_THRESHOLDS: list[tuple[float, float, int]] = [
    (0, 1_000, 0),
    (1_000, 10_000, 1),
    (10_000, 50_000, 2),
    (50_000, float("inf"), 3),
]

WORKFLOW_TRANSITIONS: dict[str, list[str]] = {
    TransactionWorkflowStatus.DRAFT.value: [
        TransactionWorkflowStatus.SUBMITTED.value,
        TransactionWorkflowStatus.CANCELLED.value,
    ],
    TransactionWorkflowStatus.SUBMITTED.value: [
        TransactionWorkflowStatus.PENDING_APPROVAL.value,
        TransactionWorkflowStatus.APPROVED.value,
        TransactionWorkflowStatus.REJECTED.value,
        TransactionWorkflowStatus.CANCELLED.value,
    ],
    TransactionWorkflowStatus.PENDING_APPROVAL.value: [
        TransactionWorkflowStatus.APPROVED.value,
        TransactionWorkflowStatus.REJECTED.value,
        TransactionWorkflowStatus.CANCELLED.value,
    ],
    TransactionWorkflowStatus.APPROVED.value: [TransactionWorkflowStatus.EXECUTED.value],
}


def list_transaction_catalog() -> list[dict]:
    return [
        {
            "transaction_type": ttype,
            "posting_rule_id": TRANSACTION_POSTING_RULE_MAP[ttype],
            **meta,
        }
        for ttype, meta in TRANSACTION_ENGINE_CATALOG.items()
    ]


def list_posting_rules() -> list[dict]:
    return [
        {"transaction_type": ttype, "rule_id": rule_id}
        for ttype, rule_id in TRANSACTION_POSTING_RULE_MAP.items()
    ]


def list_workflow_states() -> list[dict]:
    terminal = [
        TransactionWorkflowStatus.EXECUTED.value,
        TransactionWorkflowStatus.REJECTED.value,
        TransactionWorkflowStatus.CANCELLED.value,
    ]
    states = [
        {"status": status, "allowed_transitions": transitions}
        for status, transitions in WORKFLOW_TRANSITIONS.items()
    ]
    states.extend({"status": s, "allowed_transitions": []} for s in terminal)
    return states


def resolve_posting_rule(transaction_type: str) -> str:
    return TRANSACTION_POSTING_RULE_MAP.get(transaction_type, "treasury_internal_transfer")


def resolve_approval_levels(transaction_type: str, amount: float) -> int:
    meta = TRANSACTION_ENGINE_CATALOG.get(transaction_type, {})
    if meta.get("always_approve"):
        for low, high, levels in APPROVAL_THRESHOLDS:
            if low <= amount < high:
                return max(levels, 1)
        return 1
    for low, high, levels in APPROVAL_THRESHOLDS:
        if low <= amount < high:
            return levels
    return 1


def requires_approval(transaction_type: str, amount: float) -> bool:
    return resolve_approval_levels(transaction_type, amount) > 0


def can_auto_execute(transaction_type: str, amount: float) -> bool:
    return not requires_approval(transaction_type, amount)


def assert_transaction_type(transaction_type: str) -> None:
    if transaction_type not in {t.value for t in TreasuryTransactionType}:
        raise ValueError("invalid_treasury_transaction_type")


def build_transaction_dashboard(*, transactions: list[dict]) -> dict:
    by_type: dict[str, int] = {}
    by_status: dict[str, int] = {}
    pending_approval: list[dict] = []
    total_executed = 0.0

    for txn in transactions:
        ttype = txn.get("transaction_type", "unknown")
        status = txn.get("status", "unknown")
        by_type[ttype] = by_type.get(ttype, 0) + 1
        by_status[status] = by_status.get(status, 0) + 1
        if status in (
            TransactionWorkflowStatus.SUBMITTED.value,
            TransactionWorkflowStatus.PENDING_APPROVAL.value,
        ):
            pending_approval.append(txn)
        if status == TransactionWorkflowStatus.EXECUTED.value:
            total_executed += txn.get("amount", 0)

    return {
        "summary": {
            "transaction_count": len(transactions),
            "pending_approval_count": len(pending_approval),
            "total_executed_amount": round(total_executed, 2),
        },
        "by_transaction_type": by_type,
        "by_status": by_status,
        "pending_approval": pending_approval[:20],
        "recent_transactions": transactions[:15],
        "posting_rules": list_posting_rules(),
        "workflow_states": list_workflow_states(),
    }
