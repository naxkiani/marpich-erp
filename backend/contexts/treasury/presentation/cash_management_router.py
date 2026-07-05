"""Enterprise Cash Management API routes."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from contexts.identity.presentation.dependencies import (
    get_correlation_id,
    get_tenant_id,
    require_permissions,
)
from contexts.treasury.container import get_cash_management_service
from contexts.treasury.presentation.cash_management_schemas import (
    CashCloseRequest,
    CashCountRequest,
    CashForecastRequest,
    CashReconcileRequest,
    CashTransactionRequest,
    CashVerifyRequest,
    CreateCashLocationRequest,
    OpenClosingRequest,
)

cash_management_router = APIRouter(
    prefix="/treasury/cash-management",
    tags=["Enterprise Cash Management"],
)


@cash_management_router.get("/catalog")
async def list_cash_catalog(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.cash.read"))],
):
    return {"data": (await get_cash_management_service().list_catalog()).unwrap()}


@cash_management_router.get("/dashboard")
async def cash_dashboard(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.cash.read"))],
):
    return {"data": (await get_cash_management_service().get_dashboard(tenant_id)).unwrap()}


@cash_management_router.post("/locations", status_code=status.HTTP_201_CREATED)
async def create_cash_location(
    body: CreateCashLocationRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.cash.write"))],
):
    result = await get_cash_management_service().create_location(
        tenant_id=tenant_id,
        code=body.code,
        name=body.name,
        location_type=body.location_type,
        currency=body.currency,
        organization_id=body.organization_id,
        branch_id=body.branch_id,
        department_id=body.department_id,
        opening_balance=body.opening_balance,
        gl_account_code=body.gl_account_code,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@cash_management_router.get("/locations")
async def list_cash_locations(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.cash.read"))],
    organization_id: str | None = Query(None),
):
    return {
        "data": (await get_cash_management_service().list_locations(tenant_id, organization_id)).unwrap()
    }


@cash_management_router.get("/locations/{location_id}")
async def get_cash_location(
    location_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.cash.read"))],
):
    result = await get_cash_management_service().get_location(tenant_id, location_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@cash_management_router.post("/transactions", status_code=status.HTTP_201_CREATED)
async def record_cash_transaction(
    body: CashTransactionRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    user: Annotated[dict, Depends(require_permissions("treasury.cash.write"))],
):
    result = await get_cash_management_service().record_transaction(
        tenant_id=tenant_id,
        location_id=body.location_id,
        transaction_type=body.transaction_type,
        amount=body.amount,
        reference=body.reference,
        description=body.description,
        counterpart_location_id=body.counterpart_location_id,
        created_by=user.get("sub"),
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@cash_management_router.get("/transactions")
async def list_cash_transactions(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.cash.read"))],
    location_id: str | None = Query(None),
):
    return {"data": (await get_cash_management_service().list_transactions(tenant_id, location_id)).unwrap()}


@cash_management_router.post("/counts", status_code=status.HTTP_201_CREATED)
async def create_cash_count(
    body: CashCountRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[dict, Depends(require_permissions("treasury.cash.write"))],
):
    result = await get_cash_management_service().create_count(
        tenant_id=tenant_id,
        location_id=body.location_id,
        counted_amount=body.counted_amount,
        counted_by=user.get("sub", "system"),
        notes=body.notes,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@cash_management_router.post("/counts/{count_id}/verify")
async def verify_cash_count(
    count_id: str,
    body: CashVerifyRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[dict, Depends(require_permissions("treasury.cash.approve"))],
):
    result = await get_cash_management_service().verify_count(
        tenant_id=tenant_id,
        count_id=count_id,
        verified_by=user.get("sub", "system"),
        approved=body.approved,
        notes=body.notes,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@cash_management_router.get("/counts")
async def list_cash_counts(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.cash.read"))],
    location_id: str | None = Query(None),
):
    return {"data": (await get_cash_management_service().list_counts(tenant_id, location_id)).unwrap()}


@cash_management_router.post("/closings", status_code=status.HTTP_201_CREATED)
async def open_cash_closing(
    body: OpenClosingRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[dict, Depends(require_permissions("treasury.cash.write"))],
):
    result = await get_cash_management_service().open_closing(
        tenant_id=tenant_id,
        location_id=body.location_id,
        closed_by=user.get("sub", "system"),
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@cash_management_router.post("/closings/{closing_id}/close")
async def close_cash_session(
    closing_id: str,
    body: CashCloseRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.cash.write"))],
):
    result = await get_cash_management_service().close_session(
        tenant_id=tenant_id,
        closing_id=closing_id,
        counted_amount=body.counted_amount,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@cash_management_router.get("/closings")
async def list_cash_closings(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.cash.read"))],
):
    return {"data": (await get_cash_management_service().list_closings(tenant_id)).unwrap()}


@cash_management_router.post("/reconciliations", status_code=status.HTTP_201_CREATED)
async def reconcile_cash(
    body: CashReconcileRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[dict, Depends(require_permissions("treasury.cash.write"))],
):
    result = await get_cash_management_service().reconcile_cash(
        tenant_id=tenant_id,
        location_id=body.location_id,
        period_start=body.period_start,
        period_end=body.period_end,
        counted_balance=body.counted_balance,
        reconciled_by=user.get("sub"),
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@cash_management_router.get("/reconciliations")
async def list_cash_reconciliations(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.cash.read"))],
):
    return {"data": (await get_cash_management_service().list_reconciliations(tenant_id)).unwrap()}


@cash_management_router.post("/forecasts", status_code=status.HTTP_201_CREATED)
async def create_cash_forecast(
    body: CashForecastRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.cash.write"))],
):
    result = await get_cash_management_service().create_forecast(
        tenant_id=tenant_id,
        name=body.name,
        period_start=body.period_start,
        period_end=body.period_end,
        scenario=body.scenario,
        currency=body.currency,
        opening_balance=body.opening_balance,
        projected_lines=[line.model_dump() for line in body.projected_lines],
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@cash_management_router.get("/forecasts")
async def list_cash_forecasts(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.cash.read"))],
):
    return {"data": (await get_cash_management_service().list_forecasts(tenant_id)).unwrap()}
