"""Financial Kernel API schemas."""
from __future__ import annotations

from pydantic import BaseModel, Field


class JournalLineRequest(BaseModel):
    account_code: str
    debit: float = 0
    credit: float = 0
    cost_center: str | None = None
    profit_center: str | None = None
    description: str | None = None
    dimensions: dict[str, str] = Field(default_factory=dict)


class PostJournalRequest(BaseModel):
    source_context: str
    source_document_id: str
    currency: str = "USD"
    base_currency: str = "USD"
    exchange_rate: float = 1.0
    organization_id: str | None = None
    branch_id: str | None = None
    lines: list[JournalLineRequest]
    idempotency_key: str | None = None


class CreateAccountRequest(BaseModel):
    code: str
    name: str
    account_type: str | None = None
    account_category: str | None = None
    account_key: str | None = None
    parent_account_id: str | None = None
    account_group: str | None = None
    is_posting: bool = True


class CreateCoaAccountRequest(BaseModel):
    code: str
    name: str
    account_type: str | None = None
    account_category: str | None = None
    account_key: str | None = None
    parent_account_id: str | None = None
    account_group: str | None = None
    is_posting: bool = True
    currency: str | None = None
    is_control_account: bool = False
    reconciliation_required: bool = False
    tax_code: str | None = None
    budget_code: str | None = None
    effective_date: str | None = None


class ApplyCoaTemplateRequest(BaseModel):
    template_key: str
    template_type: str = "industry"
    code_overrides: dict[str, str] | None = None
    code_prefix: str = ""
    country_code: str | None = None
    merge: bool = False


class CreateFiscalYearRequest(BaseModel):
    name: str
    start_date: str
    end_date: str
    organization_id: str | None = None


class CreatePeriodRequest(BaseModel):
    fiscal_year_id: str
    name: str
    start_date: str
    end_date: str
    organization_id: str | None = None
    branch_id: str | None = None


class CreateRecurringRequest(BaseModel):
    name: str
    schedule: str
    currency: str = "USD"
    base_currency: str = "USD"
    organization_id: str | None = None
    requires_approval: bool = False
    lines: list[JournalLineRequest]


class CreateBudgetRequest(BaseModel):
    period_id: str
    account_code: str
    amount: float
    cost_center: str | None = None
    currency: str = "USD"
    organization_id: str | None = None


class ConvertCurrencyRequest(BaseModel):
    amount: str
    from_currency: str
    to_currency: str
    rate_type: str | None = None
    as_of_date: str | None = None


class UpdateCurrencyConfigRequest(BaseModel):
    base_currency: str | None = None
    reporting_currency: str | None = None
    auto_update_enabled: bool | None = None
    auto_update_provider: str | None = None


class AddCurrencyRequest(BaseModel):
    code: str


class CreateManualRateRequest(BaseModel):
    from_currency: str
    to_currency: str
    rate: float
    effective_date: str | None = None


class ImportCentralBankRatesRequest(BaseModel):
    central_bank: str = "fed"


class RevaluationBalance(BaseModel):
    currency: str
    foreign_balance: float
    base_balance: float


class RevaluationRequest(BaseModel):
    period_id: str | None = None
    revaluation_date: str | None = None
    rate_type: str = "spot"
    balances: list[RevaluationBalance] | None = None


class CalculateTaxRequest(BaseModel):
    amount: str
    tax_code: str
    jurisdiction: str


class PostingPreviewRequest(BaseModel):
    lines: list[JournalLineRequest]
    currency: str = "USD"
    base_currency: str = "USD"
    journal_entry_type: str = "standard"
    period_id: str | None = None
    requires_approval: bool = False


class SingleEntryRequest(BaseModel):
    source_context: str
    source_document_id: str
    amount: float
    primary_account_code: str
    offset_account_code: str
    side: str = Field(description="debit or credit — side for primary account")
    currency: str = "USD"
    description: str = ""
    organization_id: str | None = None
    branch_id: str | None = None
    cost_center: str | None = None
    profit_center: str | None = None
    idempotency_key: str | None = None
    require_approval: bool = False


class AdjustingEntryRequest(BaseModel):
    source_document_id: str
    debit_account: str
    credit_account: str
    amount: float
    currency: str = "USD"
    description: str = "Adjusting entry"
    organization_id: str | None = None
    require_approval: bool = True


class ClosingBalanceItem(BaseModel):
    account_code: str
    balance: float


class ClosingEntryRequest(BaseModel):
    source_document_id: str
    retained_earnings_account: str
    income_summary_account: str
    revenue_closes: list[ClosingBalanceItem]
    expense_closes: list[ClosingBalanceItem]
    currency: str = "USD"
    organization_id: str | None = None


class OpeningBalanceLine(BaseModel):
    account_code: str
    debit: float = 0
    credit: float = 0
    description: str | None = None


class OpeningBalanceRequest(BaseModel):
    source_document_id: str
    balances: list[OpeningBalanceLine]
    currency: str = "USD"
    organization_id: str | None = None
    require_approval: bool = True


class IntercompanyEntryRequest(BaseModel):
    source_document_id: str
    originating_org_id: str
    counterparty_org_id: str
    amount: float
    due_from_account: str
    due_to_account: str
    expense_account: str
    revenue_account: str
    currency: str = "USD"
    description: str = "Intercompany entry"


class PostingRuleRequest(BaseModel):
    rule_id: str
    source_context: str
    source_document_id: str
    amount: float
    debit_account: str
    credit_account: str
    currency: str = "USD"
    description: str = ""


class RollbackRequest(BaseModel):
    reason: str = "rollback"


class TypedJournalRequest(BaseModel):
    journal_type: str = "general"
    source_context: str
    source_document_id: str
    currency: str = "USD"
    base_currency: str = "USD"
    exchange_rate: float = 1.0
    organization_id: str | None = None
    branch_id: str | None = None
    lines: list[JournalLineRequest]
    idempotency_key: str | None = None
    require_approval: bool | None = None


class BatchJournalEntryRequest(BaseModel):
    journal_type: str = "general"
    source_context: str
    source_document_id: str
    currency: str = "USD"
    base_currency: str = "USD"
    exchange_rate: float = 1.0
    organization_id: str | None = None
    branch_id: str | None = None
    lines: list[JournalLineRequest]
    idempotency_key: str | None = None
    require_approval: bool | None = None


class BatchJournalRequest(BaseModel):
    batch_id: str | None = None
    entries: list[BatchJournalEntryRequest]


class SignJournalRequest(BaseModel):
    signer_id: str


class CreateJournalVersionRequest(BaseModel):
    lines: list[JournalLineRequest]


class PostingRuleSlotRequest(BaseModel):
    label: str
    account_key: str | None = None
    role: str | None = None
    required: bool = True


class PostingRuleLineTemplateRequest(BaseModel):
    side: str
    account_slot: str
    amount_field: str = "amount"
    description: str = ""


class RuleBuilderRequest(BaseModel):
    rule_id: str
    label: str
    module: str
    journal_type: str = "general"
    pattern: str = "debit_credit"
    account_slots: dict[str, PostingRuleSlotRequest] = Field(default_factory=dict)
    line_templates: list[PostingRuleLineTemplateRequest] = Field(default_factory=list)
    approval_required: bool = False
    tax_amount_field: str | None = None
    tax_account_slot: str | None = None
    dimensions: list[str] = Field(default_factory=list)
    description: str = ""


class UpdatePostingRuleRequest(BaseModel):
    label: str | None = None
    account_slots: dict[str, PostingRuleSlotRequest] | None = None
    line_templates: list[PostingRuleLineTemplateRequest] | None = None
    approval_required: bool | None = None
    description: str | None = None
    is_active: bool | None = None


class ExecutePostingRequest(BaseModel):
    rule_id: str
    source_context: str
    source_document_id: str
    currency: str = "USD"
    amount: float | None = None
    account_mappings: dict[str, str] = Field(default_factory=dict)
    lines: list[JournalLineRequest] | None = None
    description: str = ""
    dimensions: dict[str, str] = Field(default_factory=dict)
    tax_amount: float | None = None
    idempotency_key: str | None = None
    organization_id: str | None = None
    branch_id: str | None = None
    use_default_accounts: bool = True
    require_approval: bool | None = None


class PreviewPostingRuleRequest(BaseModel):
    rule_id: str
    amount: float | None = None
    account_mappings: dict[str, str] = Field(default_factory=dict)
    lines: list[JournalLineRequest] | None = None
    description: str = ""
    dimensions: dict[str, str] = Field(default_factory=dict)
    tax_amount: float | None = None
    use_default_accounts: bool = True


class CreateFiscalCalendarRequest(BaseModel):
    name: str
    organization_id: str | None = None
    description: str = ""
    fiscal_year_start_month: int = 1
    is_default: bool = False


class CreateCalendarFiscalYearRequest(BaseModel):
    name: str
    start_date: str
    end_date: str
    organization_id: str | None = None


class PeriodCloseActionRequest(BaseModel):
    action_type: str
    reason: str = ""


class ApproveCloseActionRequest(BaseModel):
    approver_id: str | None = None


class CreateAccountTreeRequest(BaseModel):
    name: str
    description: str = ""
    tree_type: str = "primary"
    template_key: str | None = None
    template_type: str | None = None
    country_code: str | None = None
    is_default: bool = False


class MoveAccountInTreeRequest(BaseModel):
    account_id: str
    new_parent_id: str | None = None
    position: int | None = None


class CreateTreeVersionRequest(BaseModel):
    change_summary: str = "Manual snapshot"


class BulkImportAccountsRequest(BaseModel):
    rows: list[dict]


class ApplyTreeTemplateRequest(BaseModel):
    template_key: str
    template_type: str = "industry"
    code_overrides: dict[str, str] | None = None
    code_prefix: str = ""
    country_code: str | None = None
    merge: bool = False


class PostSubledgerEntryRequest(BaseModel):
    subledger_type: str
    source_document_id: str
    amount: float
    entry_date: str
    currency: str = "USD"
    reference: str = ""
    counterparty: str | None = None
    description: str = ""
    dimensions: dict | None = None
    account_mappings: dict | None = None
    idempotency_key: str | None = None
    tax_amount: float | None = None
    organization_id: str | None = None
    branch_id: str | None = None


class RunSubledgerReconciliationRequest(BaseModel):
    reconciliation_date: str
    period_id: str | None = None


class CreateReconciliationRunRequest(BaseModel):
    reconciliation_type: str
    reconciliation_date: str
    reference_id: str | None = None
    reference_label: str = ""
    left_items: list[dict]
    right_items: list[dict]
    period_id: str | None = None
    auto_match: bool = True


class ManualMatchRequest(BaseModel):
    left_item: dict
    right_item: dict


class RejectReconciliationRequest(BaseModel):
    reason: str = ""


class CreateDimensionValueRequest(BaseModel):
    dimension_type: str
    code: str
    name: str
    parent_id: str | None = None
    metadata: dict | None = None


class ValidateJournalDimensionsRequest(BaseModel):
    lines: list[dict]


class ValidateTransactionRequest(BaseModel):
    source_context: str
    source_document_id: str
    lines: list[dict]
    currency: str = "USD"
    base_currency: str = "USD"
    exchange_rate: float = 1.0
    period_id: str | None = None
    idempotency_key: str | None = None
    posting_mode: str = "automatic"
    requires_approval: bool = False
    journal_entry_type: str = "standard"
    persist: bool = True

