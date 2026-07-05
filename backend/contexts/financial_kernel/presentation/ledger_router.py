"""Enterprise General Ledger API routes."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from contexts.financial_kernel.container import get_financial_kernel_service
from contexts.financial_kernel.presentation.schemas import (
    AdjustingEntryRequest,
    ClosingEntryRequest,
    CreateAccountRequest,
    CreateBudgetRequest,
    CreateFiscalYearRequest,
    CreatePeriodRequest,
    CreateRecurringRequest,
    IntercompanyEntryRequest,
    OpeningBalanceRequest,
    PostingPreviewRequest,
    PostingRuleRequest,
    PostJournalRequest,
    RollbackRequest,
    SingleEntryRequest,
)
from contexts.identity.presentation.dependencies import (
    get_correlation_id,
    get_tenant_id,
    require_permissions,
)

ledger_router = APIRouter(prefix="/financial-kernel/ledger", tags=["General Ledger"])


@ledger_router.post("/accounts", status_code=status.HTTP_201_CREATED)
async def create_account(
    body: CreateAccountRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.ledger.accounts.write"))],
):
    result = await get_financial_kernel_service().create_account(
        tenant_id=tenant_id,
        code=body.code,
        name=body.name,
        account_type=body.account_type,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@ledger_router.get("/accounts")
async def list_ledger_accounts(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.ledger.accounts.read"))],
):
    return {"data": (await get_financial_kernel_service().list_accounts(tenant_id)).unwrap()}


@ledger_router.post("/fiscal-years", status_code=status.HTTP_201_CREATED)
async def create_fiscal_year(
    body: CreateFiscalYearRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.ledger.periods.write"))],
):
    result = await get_financial_kernel_service().create_fiscal_year(
        tenant_id=tenant_id,
        organization_id=body.organization_id,
        name=body.name,
        start_date=body.start_date,
        end_date=body.end_date,
    )
    return {"data": result.unwrap()}


@ledger_router.get("/fiscal-years")
async def list_fiscal_years(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.ledger.periods.read"))],
):
    return {"data": (await get_financial_kernel_service().list_fiscal_years(tenant_id)).unwrap()}


@ledger_router.post("/periods", status_code=status.HTTP_201_CREATED)
async def create_period(
    body: CreatePeriodRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.ledger.periods.write"))],
):
    result = await get_financial_kernel_service().create_period(
        tenant_id=tenant_id,
        organization_id=body.organization_id,
        branch_id=body.branch_id,
        fiscal_year_id=body.fiscal_year_id,
        name=body.name,
        start_date=body.start_date,
        end_date=body.end_date,
    )
    return {"data": result.unwrap()}


@ledger_router.get("/periods")
async def list_periods(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.ledger.periods.read"))],
):
    return {"data": (await get_financial_kernel_service().list_periods(tenant_id)).unwrap()}


@ledger_router.post("/journals/automatic", status_code=status.HTTP_201_CREATED)
async def post_automatic_journal(
    body: PostJournalRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.ledger.journals.post"))],
):
    result = await get_financial_kernel_service().post_journal(
        tenant_id=tenant_id,
        source_context=body.source_context,
        source_document_id=body.source_document_id,
        lines=[line.model_dump() for line in body.lines],
        currency=body.currency,
        base_currency=body.base_currency,
        exchange_rate=body.exchange_rate,
        correlation_id=correlation_id,
        idempotency_key=body.idempotency_key,
        organization_id=body.organization_id,
        branch_id=body.branch_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@ledger_router.post("/journals/manual", status_code=status.HTTP_201_CREATED)
async def post_manual_journal(
    body: PostJournalRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.ledger.journals.manual"))],
):
    result = await get_financial_kernel_service().post_manual_journal(
        tenant_id=tenant_id,
        source_context=body.source_context,
        source_document_id=body.source_document_id,
        lines=[line.model_dump() for line in body.lines],
        currency=body.currency,
        base_currency=body.base_currency,
        exchange_rate=body.exchange_rate,
        correlation_id=correlation_id,
        organization_id=body.organization_id,
        branch_id=body.branch_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@ledger_router.post("/journals/{journal_id}/submit")
async def submit_journal(
    journal_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.ledger.journals.manual"))],
):
    result = await get_financial_kernel_service().submit_journal_for_approval(journal_id, correlation_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@ledger_router.post("/journals/{journal_id}/approve")
async def approve_journal(
    journal_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.ledger.journals.approve"))],
):
    result = await get_financial_kernel_service().approve_journal(journal_id, correlation_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@ledger_router.post("/journals/{journal_id}/reverse", status_code=status.HTTP_201_CREATED)
async def reverse_journal(
    journal_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.ledger.journals.reverse"))],
):
    result = await get_financial_kernel_service().reverse_journal(journal_id, correlation_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@ledger_router.get("/journals")
async def list_journals(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.ledger.journals.read"))],
):
    return {"data": (await get_financial_kernel_service().list_journals(tenant_id)).unwrap()}


@ledger_router.get("/journals/{journal_id}")
async def get_journal(
    journal_id: str,
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.ledger.journals.read"))],
):
    result = await get_financial_kernel_service().get_journal(journal_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@ledger_router.post("/recurring", status_code=status.HTTP_201_CREATED)
async def create_recurring(
    body: CreateRecurringRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.ledger.recurring.write"))],
):
    result = await get_financial_kernel_service().create_recurring_journal(
        tenant_id=tenant_id,
        organization_id=body.organization_id,
        name=body.name,
        schedule=body.schedule,
        currency=body.currency,
        base_currency=body.base_currency,
        lines=[line.model_dump() for line in body.lines],
        requires_approval=body.requires_approval,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@ledger_router.get("/recurring")
async def list_recurring(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.ledger.recurring.write"))],
):
    return {"data": (await get_financial_kernel_service().list_recurring_journals(tenant_id)).unwrap()}


@ledger_router.post("/recurring/{template_id}/run", status_code=status.HTTP_201_CREATED)
async def run_recurring(
    template_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.ledger.recurring.run"))],
):
    result = await get_financial_kernel_service().run_recurring_journal(template_id, correlation_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@ledger_router.post("/budgets", status_code=status.HTTP_201_CREATED)
async def create_budget(
    body: CreateBudgetRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.ledger.budgets.write"))],
):
    result = await get_financial_kernel_service().create_budget(
        tenant_id=tenant_id,
        organization_id=body.organization_id,
        period_id=body.period_id,
        account_code=body.account_code,
        amount=body.amount,
        cost_center=body.cost_center,
        currency=body.currency,
    )
    return {"data": result.unwrap()}


@ledger_router.get("/budgets")
async def list_budgets(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.ledger.budgets.read"))],
):
    return {"data": (await get_financial_kernel_service().list_budgets(tenant_id)).unwrap()}


@ledger_router.get("/trial-balance")
async def ledger_trial_balance(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.ledger.journals.read"))],
):
    return {"data": (await get_financial_kernel_service().get_trial_balance(tenant_id)).unwrap()}


@ledger_router.get("/posting-rules")
async def list_posting_rules(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.ledger.journals.read"))],
):
    return {"data": (await get_financial_kernel_service().list_posting_rules_catalog()).unwrap()}


@ledger_router.post("/posting/preview")
async def posting_preview(
    body: PostingPreviewRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.ledger.journals.read"))],
):
    result = await get_financial_kernel_service().preview_posting(
        tenant_id=tenant_id,
        lines=[line.model_dump() for line in body.lines],
        currency=body.currency,
        base_currency=body.base_currency,
        journal_entry_type=body.journal_entry_type,
        period_id=body.period_id,
        requires_approval=body.requires_approval,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@ledger_router.post("/journals/single-entry", status_code=status.HTTP_201_CREATED)
async def post_single_entry_journal(
    body: SingleEntryRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.ledger.journals.post"))],
):
    result = await get_financial_kernel_service().post_single_entry(
        tenant_id=tenant_id,
        source_context=body.source_context,
        source_document_id=body.source_document_id,
        amount=body.amount,
        primary_account_code=body.primary_account_code,
        offset_account_code=body.offset_account_code,
        side=body.side,
        currency=body.currency,
        correlation_id=correlation_id,
        description=body.description,
        organization_id=body.organization_id,
        branch_id=body.branch_id,
        cost_center=body.cost_center,
        profit_center=body.profit_center,
        idempotency_key=body.idempotency_key,
        require_approval=body.require_approval,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@ledger_router.post("/journals/adjusting", status_code=status.HTTP_201_CREATED)
async def post_adjusting_journal(
    body: AdjustingEntryRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.ledger.journals.manual"))],
):
    result = await get_financial_kernel_service().post_adjusting_entry(
        tenant_id=tenant_id,
        source_document_id=body.source_document_id,
        debit_account=body.debit_account,
        credit_account=body.credit_account,
        amount=body.amount,
        currency=body.currency,
        correlation_id=correlation_id,
        description=body.description,
        organization_id=body.organization_id,
        require_approval=body.require_approval,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@ledger_router.post("/journals/closing", status_code=status.HTTP_201_CREATED)
async def post_closing_journal(
    body: ClosingEntryRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.ledger.journals.post"))],
):
    result = await get_financial_kernel_service().post_closing_entry(
        tenant_id=tenant_id,
        source_document_id=body.source_document_id,
        retained_earnings_account=body.retained_earnings_account,
        income_summary_account=body.income_summary_account,
        revenue_closes=[item.model_dump() for item in body.revenue_closes],
        expense_closes=[item.model_dump() for item in body.expense_closes],
        currency=body.currency,
        correlation_id=correlation_id,
        organization_id=body.organization_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@ledger_router.post("/journals/opening-balance", status_code=status.HTTP_201_CREATED)
async def post_opening_balance_journal(
    body: OpeningBalanceRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.ledger.journals.manual"))],
):
    result = await get_financial_kernel_service().post_opening_balance(
        tenant_id=tenant_id,
        source_document_id=body.source_document_id,
        balances=[line.model_dump() for line in body.balances],
        currency=body.currency,
        correlation_id=correlation_id,
        organization_id=body.organization_id,
        require_approval=body.require_approval,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@ledger_router.post("/journals/intercompany", status_code=status.HTTP_201_CREATED)
async def post_intercompany_journal(
    body: IntercompanyEntryRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.ledger.journals.post"))],
):
    result = await get_financial_kernel_service().post_intercompany_entry(
        tenant_id=tenant_id,
        source_document_id=body.source_document_id,
        originating_org_id=body.originating_org_id,
        counterparty_org_id=body.counterparty_org_id,
        amount=body.amount,
        due_from_account=body.due_from_account,
        due_to_account=body.due_to_account,
        expense_account=body.expense_account,
        revenue_account=body.revenue_account,
        currency=body.currency,
        correlation_id=correlation_id,
        description=body.description,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@ledger_router.post("/journals/{journal_id}/rollback", status_code=status.HTTP_201_CREATED)
async def rollback_journal(
    journal_id: str,
    body: RollbackRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.ledger.journals.reverse"))],
):
    result = await get_financial_kernel_service().rollback_journal(
        journal_id, correlation_id, reason=body.reason
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@ledger_router.post("/journals/posting-rule", status_code=status.HTTP_201_CREATED)
async def post_with_posting_rule(
    body: PostingRuleRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.ledger.journals.post"))],
):
    result = await get_financial_kernel_service().post_with_rule(
        tenant_id=tenant_id,
        rule_id=body.rule_id,
        source_context=body.source_context,
        source_document_id=body.source_document_id,
        amount=body.amount,
        debit_account=body.debit_account,
        credit_account=body.credit_account,
        currency=body.currency,
        correlation_id=correlation_id,
        description=body.description,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}
