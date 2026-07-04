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
