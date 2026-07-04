"""Finance FastAPI router."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from contexts.finance.container import get_finance_service
from contexts.finance.presentation.schemas import CreateAccountRequest, OpenFiscalPeriodRequest
from contexts.identity.presentation.dependencies import (
    get_correlation_id,
    get_tenant_id,
    require_permissions,
)

router = APIRouter(prefix="/finance", tags=["Finance"])


@router.get("/accounts")
async def list_accounts(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("finance.accounts.read"))],
):
    result = await get_finance_service().list_accounts(tenant_id)
    return {"data": result.unwrap()}


@router.post("/accounts", status_code=status.HTTP_201_CREATED)
async def create_account(
    body: CreateAccountRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("finance.accounts.write"))],
):
    result = await get_finance_service().create_account(
        tenant_id=tenant_id,
        code=body.code,
        name=body.name,
        account_type=body.account_type,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.get("/fiscal-periods")
async def list_fiscal_periods(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("finance.periods.read"))],
):
    result = await get_finance_service().list_periods(tenant_id)
    return {"data": result.unwrap()}


@router.post("/fiscal-periods", status_code=status.HTTP_201_CREATED)
async def open_fiscal_period(
    body: OpenFiscalPeriodRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("finance.periods.write"))],
):
    result = await get_finance_service().open_fiscal_period(
        tenant_id=tenant_id,
        name=body.name,
        start_date=body.start_date,
        end_date=body.end_date,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.post("/fiscal-periods/{period_id}/close")
async def close_fiscal_period(
    period_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("finance.periods.write"))],
):
    result = await get_finance_service().close_fiscal_period(tenant_id, period_id, correlation_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.get("/journal-entries")
async def list_journal_entries(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("finance.journal.read"))],
):
    result = await get_finance_service().list_journal_entries(tenant_id)
    return {"data": result.unwrap()}


@router.get("/journal-entries/by-source/{source_type}/{source_id}")
async def get_journal_by_source(
    source_type: str,
    source_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("finance.journal.read"))],
):
    result = await get_finance_service().find_journal_by_source(tenant_id, source_type, source_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@router.get("/trial-balance")
async def trial_balance(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("finance.reports.read"))],
):
    result = await get_finance_service().trial_balance(tenant_id)
    return {"data": result.unwrap()}
