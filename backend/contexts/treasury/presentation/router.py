"""Enterprise Treasury API routes."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from contexts.identity.presentation.dependencies import (
    get_correlation_id,
    get_tenant_id,
    require_permissions,
)
from contexts.treasury.container import get_treasury_service
from contexts.treasury.domain.services.treasury_platform_engine import (
    list_gl_rule_map,
    list_platform_catalog,
    pos_boundary_statement,
)
from contexts.treasury.presentation.schemas import (
    ApproveTransferRequest,
    CreateForecastRequest,
    CreateReconciliationRequest,
    CreateTransferRequest,
    CreateTreasuryAccountRequest,
)

router = APIRouter(prefix="/treasury", tags=["Enterprise Treasury"])


@router.get("/platform/catalog")
async def treasury_platform_catalog(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.dashboard.read"))],
):
    return {
        "data": list_platform_catalog(),
        "meta": {
            "gl_rule_map": list_gl_rule_map(),
            "pos_boundary": pos_boundary_statement(),
            "law": "treasury_manages_liquidity_gl_owned_by_kernel",
        },
    }


@router.get("/dashboard")
async def treasury_dashboard(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.dashboard.read"))],
):
    return {"data": (await get_treasury_service().get_dashboard(tenant_id)).unwrap()}


@router.get("/liquidity")
async def liquidity_analysis(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.dashboard.read"))],
):
    return {"data": (await get_treasury_service().get_liquidity_analysis(tenant_id)).unwrap()}


@router.post("/accounts", status_code=status.HTTP_201_CREATED)
async def create_account(
    body: CreateTreasuryAccountRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.accounts.write"))],
):
    result = await get_treasury_service().create_account(
        tenant_id=tenant_id,
        code=body.code,
        name=body.name,
        account_type=body.account_type,
        currency=body.currency,
        bank_name=body.bank_name,
        account_number=body.account_number,
        opening_balance=body.opening_balance,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@router.get("/accounts")
async def list_accounts(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.accounts.read"))],
):
    return {"data": (await get_treasury_service().list_accounts(tenant_id)).unwrap()}


@router.get("/accounts/{account_id}")
async def get_account(
    account_id: str,
    _user: Annotated[dict, Depends(require_permissions("treasury.accounts.read"))],
):
    result = await get_treasury_service().get_account(account_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@router.post("/transfers", status_code=status.HTTP_201_CREATED)
async def create_transfer(
    body: CreateTransferRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.transfers.write"))],
):
    result = await get_treasury_service().create_transfer(
        tenant_id=tenant_id,
        from_account_id=body.from_account_id,
        to_account_id=body.to_account_id,
        amount=body.amount,
        currency=body.currency,
        instrument=body.instrument,
        reference=body.reference,
        description=body.description,
        cheque_number=body.cheque_number,
        require_approval=body.require_approval,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@router.get("/transfers")
async def list_transfers(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.transfers.read"))],
):
    return {"data": (await get_treasury_service().list_transfers(tenant_id)).unwrap()}


@router.post("/transfers/{transfer_id}/submit")
async def submit_transfer(
    transfer_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.transfers.write"))],
):
    result = await get_treasury_service().submit_transfer(transfer_id, correlation_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.post("/transfers/{transfer_id}/approve")
async def approve_transfer(
    transfer_id: str,
    body: ApproveTransferRequest,
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.transfers.approve"))],
):
    result = await get_treasury_service().approve_transfer(
        transfer_id, correlation_id, workflow_instance_id=body.workflow_instance_id
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.post("/transfers/{transfer_id}/reject")
async def reject_transfer(
    transfer_id: str,
    _user: Annotated[dict, Depends(require_permissions("treasury.transfers.approve"))],
):
    result = await get_treasury_service().reject_transfer(transfer_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@router.post("/reconciliations", status_code=status.HTTP_201_CREATED)
async def create_reconciliation(
    body: CreateReconciliationRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.reconciliation.write"))],
):
    result = await get_treasury_service().create_reconciliation(
        tenant_id=tenant_id,
        treasury_account_id=body.treasury_account_id,
        statement_date=body.statement_date,
        statement_balance=body.statement_balance,
        statement_items=[i.model_dump() for i in body.statement_items],
        book_items=[i.model_dump() for i in body.book_items] if body.book_items else None,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@router.get("/reconciliations")
async def list_reconciliations(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.reconciliation.read"))],
):
    return {"data": (await get_treasury_service().list_reconciliations(tenant_id)).unwrap()}


@router.post("/forecasts", status_code=status.HTTP_201_CREATED)
async def create_forecast(
    body: CreateForecastRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.forecast.write"))],
):
    result = await get_treasury_service().create_forecast(
        tenant_id=tenant_id,
        name=body.name,
        period_start=body.period_start,
        period_end=body.period_end,
        scenario=body.scenario,
        currency=body.currency,
        opening_balance=body.opening_balance,
        projected_lines=[l.model_dump() for l in body.projected_lines],
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@router.get("/forecasts")
async def list_forecasts(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.forecast.read"))],
):
    return {"data": (await get_treasury_service().list_forecasts(tenant_id)).unwrap()}
