"""Enterprise subledger engine — catalog, posting, idempotency, reconciliation."""
from __future__ import annotations

from contexts.financial_kernel.domain.aggregates.subledger import (
    Subledger,
    SubledgerEntry,
    SubledgerEntryStatus,
    SubledgerType,
)

SUBLEDGER_CATALOG: dict[str, dict] = {
    SubledgerType.ACCOUNTS_RECEIVABLE.value: {
        "label": "Accounts Receivable",
        "posting_rule_id": "sales",
        "control_account_key": "accounts_receivable",
        "source_context": "subledger.ar",
        "journal_type": "sales",
        "normal_balance": "debit",
        "module": "accounting",
    },
    SubledgerType.ACCOUNTS_PAYABLE.value: {
        "label": "Accounts Payable",
        "posting_rule_id": "purchase",
        "control_account_key": "accounts_payable",
        "source_context": "subledger.ap",
        "journal_type": "purchase",
        "normal_balance": "credit",
        "module": "accounting",
    },
    SubledgerType.INVENTORY.value: {
        "label": "Inventory",
        "posting_rule_id": "inventory",
        "control_account_key": "inventory",
        "source_context": "subledger.inventory",
        "journal_type": "inventory",
        "normal_balance": "debit",
        "module": "inventory",
    },
    SubledgerType.PAYROLL.value: {
        "label": "Payroll",
        "posting_rule_id": "payroll",
        "control_account_key": "payroll_payable",
        "source_context": "subledger.payroll",
        "journal_type": "payroll",
        "normal_balance": "credit",
        "module": "hr",
    },
    SubledgerType.TREASURY.value: {
        "label": "Treasury",
        "posting_rule_id": "bank_deposit",
        "control_account_key": "bank",
        "source_context": "subledger.treasury",
        "journal_type": "bank",
        "normal_balance": "debit",
        "module": "treasury",
    },
    SubledgerType.ASSETS.value: {
        "label": "Fixed Assets",
        "posting_rule_id": "asset",
        "control_account_key": "fixed_assets",
        "source_context": "subledger.assets",
        "journal_type": "general",
        "normal_balance": "debit",
        "module": "fixed_assets",
    },
    SubledgerType.LOANS.value: {
        "label": "Loans",
        "posting_rule_id": "loan",
        "control_account_key": "loan_payable",
        "source_context": "subledger.loans",
        "journal_type": "general",
        "normal_balance": "credit",
        "module": "treasury",
    },
    SubledgerType.PROJECTS.value: {
        "label": "Projects",
        "posting_rule_id": "construction_cost",
        "control_account_key": "construction_wip",
        "source_context": "subledger.projects",
        "journal_type": "purchase",
        "normal_balance": "debit",
        "module": "construction",
    },
    SubledgerType.STUDENTS.value: {
        "label": "Students",
        "posting_rule_id": "university_tuition",
        "control_account_key": "student_receivables",
        "source_context": "subledger.students",
        "journal_type": "sales",
        "normal_balance": "debit",
        "module": "university",
    },
    SubledgerType.PATIENTS.value: {
        "label": "Patients",
        "posting_rule_id": "hospital_billing",
        "control_account_key": "patient_receivables",
        "source_context": "subledger.patients",
        "journal_type": "sales",
        "normal_balance": "debit",
        "module": "hospital",
    },
    SubledgerType.TAXES.value: {
        "label": "Taxes",
        "posting_rule_id": "tax",
        "control_account_key": "tax_payable",
        "source_context": "subledger.taxes",
        "journal_type": "tax",
        "normal_balance": "credit",
        "module": "tax",
    },
    SubledgerType.CURRENCY_EXCHANGE.value: {
        "label": "Currency Exchange",
        "posting_rule_id": "exchange_transaction",
        "control_account_key": "fx_asset",
        "source_context": "subledger.fx",
        "journal_type": "foreign_currency",
        "normal_balance": "debit",
        "module": "treasury",
    },
}


def list_subledger_catalog() -> list[dict]:
    return [
        {"subledger_type": key, **meta}
        for key, meta in SUBLEDGER_CATALOG.items()
    ]


def get_subledger_definition(subledger_type: str) -> dict:
    definition = SUBLEDGER_CATALOG.get(subledger_type)
    if not definition:
        raise KeyError(f"unknown_subledger_type:{subledger_type}")
    return definition


def build_subledger_from_catalog(tenant_id: str, subledger_type: str) -> Subledger:
    meta = get_subledger_definition(subledger_type)
    return Subledger.create(
        tenant_id=tenant_id,
        subledger_type=subledger_type,
        name=meta["label"],
        control_account_key=meta["control_account_key"],
        posting_rule_id=meta["posting_rule_id"],
        source_context=meta["source_context"],
        journal_type=meta["journal_type"],
        normal_balance=meta["normal_balance"],
    )


def build_subledger_idempotency_key(
    subledger_type: str, source_document_id: str, *, suffix: str = ""
) -> str:
    base = f"subledger:{subledger_type}:{source_document_id}"
    return f"{base}:{suffix}" if suffix else base


def validate_no_duplicate_entry(
    existing: SubledgerEntry | None,
) -> tuple[bool, str]:
    if existing and existing.status in (
        SubledgerEntryStatus.POSTED.value,
        SubledgerEntryStatus.RECONCILED.value,
    ):
        return False, "duplicate_subledger_entry"
    return True, ""


def compute_subledger_balance(
    entries: list[SubledgerEntry],
    *,
    normal_balance: str = "debit",
) -> float:
    total = 0.0
    for entry in entries:
        if entry.status not in (
            SubledgerEntryStatus.POSTED.value,
            SubledgerEntryStatus.RECONCILED.value,
        ):
            continue
        if normal_balance == "debit":
            total += entry.amount if entry.side == "debit" else -entry.amount
        else:
            total += entry.amount if entry.side == "credit" else -entry.amount
    return round(total, 2)


def build_reconciliation_items(entries: list[SubledgerEntry]) -> list[dict]:
    items: list[dict] = []
    for entry in entries:
        if entry.status not in (
            SubledgerEntryStatus.POSTED.value,
            SubledgerEntryStatus.RECONCILED.value,
        ):
            continue
        items.append(
            {
                "entry_id": str(entry.id),
                "source_document_id": entry.source_document_id,
                "reference": entry.reference,
                "amount": entry.amount,
                "entry_date": entry.entry_date,
                "journal_id": entry.journal_id,
                "counterparty": entry.counterparty,
            }
        )
    return items


def build_gl_items_from_journals(journals: list[dict], control_account_code: str) -> list[dict]:
    items: list[dict] = []
    for journal in journals:
        for line in journal.get("lines", []):
            if line.get("account_code") != control_account_code:
                continue
            debit = float(line.get("debit", 0))
            credit = float(line.get("credit", 0))
            amount = debit if debit else credit
            items.append(
                {
                    "journal_id": journal.get("id"),
                    "source_document_id": journal.get("source_document_id"),
                    "reference": journal.get("source_document_id", ""),
                    "amount": round(amount, 2),
                    "debit": debit,
                    "credit": credit,
                    "entry_date": journal.get("created_at", ""),
                }
            )
    return items


def reconcile_balances(
    *,
    subledger_balance: float,
    gl_control_balance: float,
    tolerance: float = 0.01,
) -> dict:
    variance = round(gl_control_balance - subledger_balance, 2)
    return {
        "subledger_balance": subledger_balance,
        "gl_control_balance": gl_control_balance,
        "variance": variance,
        "balanced": abs(variance) <= tolerance,
    }


def resolve_entry_side(subledger_type: str, *, is_reversal: bool = False) -> str:
    meta = get_subledger_definition(subledger_type)
    side = "debit" if meta["normal_balance"] == "debit" else "credit"
    if is_reversal:
        return "credit" if side == "debit" else "debit"
    return side


def update_subledger_stats(subledger: Subledger, entries: list[SubledgerEntry]) -> None:
    posted = [
        e
        for e in entries
        if e.status
        in (SubledgerEntryStatus.POSTED.value, SubledgerEntryStatus.RECONCILED.value)
    ]
    subledger.entry_count = len(posted)
    subledger.posted_balance = compute_subledger_balance(
        entries, normal_balance=subledger.normal_balance
    )


def build_subledger_account_mappings(
    rule_slots: tuple,
    accounts: list,
    *,
    provided: dict[str, str] | None = None,
) -> dict[str, str]:
    """Resolve posting slots from COA keys with category fallbacks."""
    key_to_code = {
        a.account_key: a.code for a in accounts if getattr(a, "account_key", None)
    }
    mappings: dict[str, str] = dict(provided or {})
    for slot in rule_slots:
        slot_name = slot.slot if hasattr(slot, "slot") else slot.get("slot", "")
        account_key = slot.account_key if hasattr(slot, "account_key") else slot.get("account_key")
        if slot_name in mappings:
            continue
        if account_key and account_key in key_to_code:
            mappings[slot_name] = key_to_code[account_key]

    def _first_posting(category_value: str) -> str | None:
        for account in accounts:
            cat = (
                account.account_category.value
                if hasattr(account.account_category, "value")
                else account.account_category
            )
            if cat == category_value and account.is_posting:
                return account.code
        return None

    if "debit" not in mappings:
        code = _first_posting("expense") or _first_posting("asset")
        if code:
            mappings["debit"] = code
    if "credit" not in mappings:
        code = _first_posting("liability") or _first_posting("revenue")
        if code:
            mappings["credit"] = code
    return mappings
