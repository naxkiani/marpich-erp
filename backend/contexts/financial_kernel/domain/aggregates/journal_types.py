"""Enterprise journal types and configurable posting rules."""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class EnterpriseJournalType(StrEnum):
    GENERAL = "general"
    CASH = "cash"
    BANK = "bank"
    PURCHASE = "purchase"
    SALES = "sales"
    INVENTORY = "inventory"
    PAYROLL = "payroll"
    TAX = "tax"
    ADJUSTMENT = "adjustment"
    OPENING = "opening"
    CLOSING = "closing"
    REVERSING = "reversing"
    RECURRING = "recurring"
    FOREIGN_CURRENCY = "foreign_currency"
    INTERCOMPANY = "intercompany"


@dataclass(frozen=True, slots=True)
class JournalTypeRules:
    journal_type: str
    label: str
    journal_entry_type: str
    approval_workflow_required: bool = False
    digital_signature_required: bool = False
    ai_review_enabled: bool = False
    automatic_posting_allowed: bool = True
    batch_posting_allowed: bool = True
    rollback_allowed: bool = True
    lock_on_post: bool = True
    versioning_enabled: bool = True
    default_posting_mode: str = "automatic"
    description: str = ""


# Configurable posting rules — tenant policy engine may override per tenant
JOURNAL_TYPE_RULES: dict[str, JournalTypeRules] = {
    EnterpriseJournalType.GENERAL.value: JournalTypeRules(
        journal_type="general",
        label="General Journal",
        journal_entry_type="standard",
        ai_review_enabled=True,
        description="Manual and system general ledger entries",
    ),
    EnterpriseJournalType.CASH.value: JournalTypeRules(
        journal_type="cash",
        label="Cash Journal",
        journal_entry_type="standard",
        approval_workflow_required=True,
        digital_signature_required=True,
        ai_review_enabled=True,
        automatic_posting_allowed=False,
        description="Petty cash and cash disbursement entries",
    ),
    EnterpriseJournalType.BANK.value: JournalTypeRules(
        journal_type="bank",
        label="Bank Journal",
        journal_entry_type="standard",
        approval_workflow_required=True,
        digital_signature_required=True,
        ai_review_enabled=True,
        automatic_posting_allowed=False,
        description="Bank reconciliation and transfer entries",
    ),
    EnterpriseJournalType.PURCHASE.value: JournalTypeRules(
        journal_type="purchase",
        label="Purchase Journal",
        journal_entry_type="standard",
        approval_workflow_required=True,
        ai_review_enabled=True,
        automatic_posting_allowed=False,
        description="Accounts payable and procurement accruals",
    ),
    EnterpriseJournalType.SALES.value: JournalTypeRules(
        journal_type="sales",
        label="Sales Journal",
        journal_entry_type="standard",
        approval_workflow_required=True,
        ai_review_enabled=True,
        automatic_posting_allowed=False,
        description="Accounts receivable and revenue recognition",
    ),
    EnterpriseJournalType.INVENTORY.value: JournalTypeRules(
        journal_type="inventory",
        label="Inventory Journal",
        journal_entry_type="standard",
        approval_workflow_required=True,
        ai_review_enabled=True,
        automatic_posting_allowed=False,
        description="Stock movements, COGS, and valuation adjustments",
    ),
    EnterpriseJournalType.PAYROLL.value: JournalTypeRules(
        journal_type="payroll",
        label="Payroll Journal",
        journal_entry_type="standard",
        approval_workflow_required=True,
        digital_signature_required=True,
        ai_review_enabled=True,
        automatic_posting_allowed=False,
        batch_posting_allowed=False,
        description="Payroll accruals and disbursements",
    ),
    EnterpriseJournalType.TAX.value: JournalTypeRules(
        journal_type="tax",
        label="Tax Journal",
        journal_entry_type="standard",
        approval_workflow_required=True,
        digital_signature_required=True,
        ai_review_enabled=True,
        automatic_posting_allowed=False,
        batch_posting_allowed=False,
        description="Tax accruals, remittances, and adjustments",
    ),
    EnterpriseJournalType.ADJUSTMENT.value: JournalTypeRules(
        journal_type="adjustment",
        label="Adjustment Journal",
        journal_entry_type="adjusting",
        approval_workflow_required=True,
        digital_signature_required=True,
        ai_review_enabled=True,
        automatic_posting_allowed=False,
        batch_posting_allowed=False,
        description="Period-end and correcting adjustments",
    ),
    EnterpriseJournalType.OPENING.value: JournalTypeRules(
        journal_type="opening",
        label="Opening Journal",
        journal_entry_type="opening_balance",
        approval_workflow_required=True,
        digital_signature_required=True,
        ai_review_enabled=True,
        automatic_posting_allowed=False,
        rollback_allowed=False,
        batch_posting_allowed=False,
        description="Opening balance carry-forward entries",
    ),
    EnterpriseJournalType.CLOSING.value: JournalTypeRules(
        journal_type="closing",
        label="Closing Journal",
        journal_entry_type="closing",
        approval_workflow_required=True,
        digital_signature_required=True,
        ai_review_enabled=True,
        rollback_allowed=False,
        versioning_enabled=False,
        batch_posting_allowed=False,
        description="Period and year-end closing entries",
    ),
    EnterpriseJournalType.REVERSING.value: JournalTypeRules(
        journal_type="reversing",
        label="Reversing Journal",
        journal_entry_type="reversing",
        automatic_posting_allowed=True,
        approval_workflow_required=False,
        ai_review_enabled=False,
        versioning_enabled=False,
        default_posting_mode="reversing",
        description="Automatic reversal of prior-period accruals",
    ),
    EnterpriseJournalType.RECURRING.value: JournalTypeRules(
        journal_type="recurring",
        label="Recurring Journal",
        journal_entry_type="recurring",
        automatic_posting_allowed=True,
        default_posting_mode="recurring",
        description="Scheduled template-driven entries",
    ),
    EnterpriseJournalType.FOREIGN_CURRENCY.value: JournalTypeRules(
        journal_type="foreign_currency",
        label="Foreign Currency Journal",
        journal_entry_type="standard",
        approval_workflow_required=True,
        digital_signature_required=True,
        ai_review_enabled=True,
        automatic_posting_allowed=False,
        description="FX revaluation and translation entries",
    ),
    EnterpriseJournalType.INTERCOMPANY.value: JournalTypeRules(
        journal_type="intercompany",
        label="Intercompany Journal",
        journal_entry_type="intercompany",
        approval_workflow_required=True,
        digital_signature_required=True,
        ai_review_enabled=True,
        automatic_posting_allowed=False,
        batch_posting_allowed=False,
        description="Due-to/due-from inter-entity eliminations",
    ),
}
