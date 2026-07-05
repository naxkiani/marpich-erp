"""Enterprise Double Entry Posting Engine."""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from uuid import uuid4


class JournalEntryType(StrEnum):
    STANDARD = "standard"
    SINGLE_ENTRY = "single_entry"
    COMPOUND = "compound"
    RECURRING = "recurring"
    ADJUSTING = "adjusting"
    CLOSING = "closing"
    OPENING_BALANCE = "opening_balance"
    REVERSING = "reversing"
    INTERCOMPANY = "intercompany"


class PostingRuleId(StrEnum):
    EXPENSE_PAYMENT = "expense_payment"
    REVENUE_RECEIPT = "revenue_receipt"
    ACCRUAL = "accrual"
    PREPAYMENT = "prepayment"
    DEPRECIATION = "depreciation"
    INTERCOMPANY_DUE = "intercompany_due"


POSTING_RULES: dict[str, dict] = {
    PostingRuleId.EXPENSE_PAYMENT.value: {
        "description": "Debit expense, credit cash/bank",
        "debit_role": "expense",
        "credit_role": "asset",
    },
    PostingRuleId.REVENUE_RECEIPT.value: {
        "description": "Debit cash/bank, credit revenue",
        "debit_role": "asset",
        "credit_role": "revenue",
    },
    PostingRuleId.ACCRUAL.value: {
        "description": "Debit expense, credit liability",
        "debit_role": "expense",
        "credit_role": "liability",
    },
    PostingRuleId.PREPAYMENT.value: {
        "description": "Debit prepaid asset, credit cash",
        "debit_role": "asset",
        "credit_role": "asset",
    },
    PostingRuleId.DEPRECIATION.value: {
        "description": "Debit depreciation expense, credit accumulated depreciation",
        "debit_role": "expense",
        "credit_role": "asset",
    },
    PostingRuleId.INTERCOMPANY_DUE.value: {
        "description": "Debit due-from, credit offset in originating org",
        "debit_role": "asset",
        "credit_role": "liability",
    },
}


@dataclass(frozen=True, slots=True)
class SingleEntryInput:
    amount: float
    primary_account_code: str
    offset_account_code: str
    side: str  # debit | credit — which side primary account receives
    description: str = ""
    cost_center: str | None = None
    profit_center: str | None = None
    department: str | None = None
    project: str | None = None


def expand_single_entry_to_double(entry: SingleEntryInput) -> list[dict]:
    """Single Entry UI → automatic double entry lines."""
    amount = round(float(entry.amount), 2)
    if amount <= 0:
        raise ValueError("amount_must_be_positive")

    dims = {
        k: v
        for k, v in {
            "cost_center": entry.cost_center,
            "profit_center": entry.profit_center,
            "department": entry.department,
            "project": entry.project,
        }.items()
        if v
    }

    if entry.side == "debit":
        return [
            {
                "account_code": entry.primary_account_code,
                "debit": amount,
                "credit": 0,
                "description": entry.description,
                **dims,
            },
            {
                "account_code": entry.offset_account_code,
                "debit": 0,
                "credit": amount,
                "description": entry.description,
                **dims,
            },
        ]

    return [
        {
            "account_code": entry.offset_account_code,
            "debit": amount,
            "credit": 0,
            "description": entry.description,
            **dims,
        },
        {
            "account_code": entry.primary_account_code,
            "debit": 0,
            "credit": amount,
            "description": entry.description,
            **dims,
        },
    ]


def classify_journal_entry_type(lines: list[dict], *, explicit_type: str | None = None) -> str:
    if explicit_type:
        return explicit_type
    if len(lines) > 2:
        return JournalEntryType.COMPOUND.value
    return JournalEntryType.STANDARD.value


def build_compound_journal(lines: list[dict]) -> list[dict]:
    """Compound journal — multiple debits and/or credits; must already balance."""
    return [dict(line) for line in lines]


def build_adjusting_entry(
    *,
    debit_account: str,
    credit_account: str,
    amount: float,
    description: str = "Adjusting entry",
    cost_center: str | None = None,
) -> list[dict]:
    amount = round(amount, 2)
    line_dims = {"cost_center": cost_center} if cost_center else {}
    return [
        {
            "account_code": debit_account,
            "debit": amount,
            "credit": 0,
            "description": description,
            "journal_entry_type": JournalEntryType.ADJUSTING.value,
            **line_dims,
        },
        {
            "account_code": credit_account,
            "debit": 0,
            "credit": amount,
            "description": description,
            "journal_entry_type": JournalEntryType.ADJUSTING.value,
            **line_dims,
        },
    ]


def build_closing_entry(
    *,
    retained_earnings_account: str,
    income_summary_account: str,
    revenue_closes: list[dict],
    expense_closes: list[dict],
) -> list[dict]:
    """
    Closing entry: zero out revenue/expense into income summary, net to retained earnings.
    Each close item: {account_code, balance, account_category}
    """
    lines: list[dict] = []
    net_income = 0.0

    for item in revenue_closes:
        balance = round(float(item["balance"]), 2)
        if balance == 0:
            continue
        lines.append({
            "account_code": item["account_code"],
            "debit": balance,
            "credit": 0,
            "description": "Close revenue to income summary",
            "journal_entry_type": JournalEntryType.CLOSING.value,
        })
        lines.append({
            "account_code": income_summary_account,
            "debit": 0,
            "credit": balance,
            "description": "Close revenue to income summary",
            "journal_entry_type": JournalEntryType.CLOSING.value,
        })
        net_income += balance

    for item in expense_closes:
        balance = round(float(item["balance"]), 2)
        if balance == 0:
            continue
        lines.append({
            "account_code": income_summary_account,
            "debit": balance,
            "credit": 0,
            "description": "Close expense to income summary",
            "journal_entry_type": JournalEntryType.CLOSING.value,
        })
        lines.append({
            "account_code": item["account_code"],
            "debit": 0,
            "credit": balance,
            "description": "Close expense to income summary",
            "journal_entry_type": JournalEntryType.CLOSING.value,
        })
        net_income -= balance

    net_income = round(net_income, 2)
    if net_income > 0:
        lines.append({
            "account_code": income_summary_account,
            "debit": net_income,
            "credit": 0,
            "description": "Transfer net income to retained earnings",
            "journal_entry_type": JournalEntryType.CLOSING.value,
        })
        lines.append({
            "account_code": retained_earnings_account,
            "debit": 0,
            "credit": net_income,
            "description": "Transfer net income to retained earnings",
            "journal_entry_type": JournalEntryType.CLOSING.value,
        })
    elif net_income < 0:
        loss = abs(net_income)
        lines.append({
            "account_code": retained_earnings_account,
            "debit": loss,
            "credit": 0,
            "description": "Transfer net loss to retained earnings",
            "journal_entry_type": JournalEntryType.CLOSING.value,
        })
        lines.append({
            "account_code": income_summary_account,
            "debit": 0,
            "credit": loss,
            "description": "Transfer net loss to retained earnings",
            "journal_entry_type": JournalEntryType.CLOSING.value,
        })

    return lines


def build_opening_balance_entry(
    balances: list[dict],
) -> list[dict]:
    """
    Opening balances: [{account_code, debit?, credit?}]
    Must balance across all lines.
    """
    lines = []
    for item in balances:
        debit = round(float(item.get("debit", 0)), 2)
        credit = round(float(item.get("credit", 0)), 2)
        lines.append({
            "account_code": item["account_code"],
            "debit": debit,
            "credit": credit,
            "description": item.get("description", "Opening balance"),
            "opening_balance": True,
            "journal_entry_type": JournalEntryType.OPENING_BALANCE.value,
        })
    return lines


def build_reversal_lines(lines: list[dict]) -> list[dict]:
    reversed_lines = []
    for line in lines:
        reversed_lines.append({
            **line,
            "debit": line.get("credit", 0),
            "credit": line.get("debit", 0),
            "description": f"REVERSAL: {line.get('description', '')}".strip(),
            "journal_entry_type": JournalEntryType.REVERSING.value,
        })
    return reversed_lines


def build_rollback_plan(lines: list[dict], *, reason: str = "rollback") -> dict:
    """Rollback = compensating reversal with audit metadata."""
    return {
        "action": "rollback",
        "reason": reason,
        "reversal_lines": build_reversal_lines(lines),
        "journal_entry_type": JournalEntryType.REVERSING.value,
    }


def build_intercompany_entry(
    *,
    originating_org_id: str,
    counterparty_org_id: str,
    amount: float,
    due_from_account: str,
    due_to_account: str,
    expense_account: str,
    revenue_account: str,
    description: str = "Intercompany entry",
) -> tuple[list[dict], list[dict], str]:
    """
    Returns (org_a_lines, org_b_lines, intercompany_pair_id).
    Each org's lines balance independently.
    """
    amount = round(amount, 2)
    pair_id = str(uuid4())

    org_a_lines = [
        {
            "account_code": expense_account,
            "debit": amount,
            "credit": 0,
            "description": description,
            "organization_id": originating_org_id,
            "intercompany_pair_id": pair_id,
            "journal_entry_type": JournalEntryType.INTERCOMPANY.value,
        },
        {
            "account_code": due_to_account,
            "debit": 0,
            "credit": amount,
            "description": description,
            "organization_id": originating_org_id,
            "intercompany_pair_id": pair_id,
            "journal_entry_type": JournalEntryType.INTERCOMPANY.value,
        },
    ]

    org_b_lines = [
        {
            "account_code": due_from_account,
            "debit": amount,
            "credit": 0,
            "description": description,
            "organization_id": counterparty_org_id,
            "intercompany_pair_id": pair_id,
            "journal_entry_type": JournalEntryType.INTERCOMPANY.value,
        },
        {
            "account_code": revenue_account,
            "debit": 0,
            "credit": amount,
            "description": description,
            "organization_id": counterparty_org_id,
            "intercompany_pair_id": pair_id,
            "journal_entry_type": JournalEntryType.INTERCOMPANY.value,
        },
    ]

    return org_a_lines, org_b_lines, pair_id


def list_posting_rules() -> list[dict]:
    return [
        {"id": rule_id, **meta}
        for rule_id, meta in POSTING_RULES.items()
    ]


def apply_posting_rule(
    rule_id: str,
    *,
    amount: float,
    debit_account: str,
    credit_account: str,
    description: str = "",
) -> list[dict]:
    if rule_id not in POSTING_RULES:
        raise ValueError(f"unknown_posting_rule:{rule_id}")
    amount = round(amount, 2)
    return [
        {
            "account_code": debit_account,
            "debit": amount,
            "credit": 0,
            "description": description or POSTING_RULES[rule_id]["description"],
            "posting_rule_id": rule_id,
        },
        {
            "account_code": credit_account,
            "debit": 0,
            "credit": amount,
            "description": description or POSTING_RULES[rule_id]["description"],
            "posting_rule_id": rule_id,
        },
    ]


def build_audit_trail_entry(
    *,
    action: str,
    journal_id: str,
    actor_id: str | None,
    correlation_id: str,
    details: dict | None = None,
) -> dict:
    return {
        "action": action,
        "journal_id": journal_id,
        "actor_id": actor_id,
        "correlation_id": correlation_id,
        "details": details or {},
    }
