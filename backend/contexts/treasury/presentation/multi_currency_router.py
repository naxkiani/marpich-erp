"""Multi-Currency Treasury API routes."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from contexts.identity.presentation.dependencies import (
    get_correlation_id,
    get_tenant_id,
    require_permissions,
)
from contexts.treasury.container import get_multi_currency_service
from contexts.treasury.presentation.multi_currency_schemas import (
    ConvertCurrencyRequest,
    CreateRateRequest,
    CrossCurrencyTransferRequest,
    RevaluationRequest,
)

multi_currency_router = APIRouter(
    prefix="/treasury/multi-currency",
    tags=["Multi-Currency Treasury"],
)


@multi_currency_router.get("/catalog")
async def multi_currency_catalog(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.fx.read"))],
):
    return {"data": (await get_multi_currency_service().list_catalog()).unwrap()}


@multi_currency_router.get("/dashboard")
async def fx_dashboard(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.fx.read"))],
):
    return {"data": (await get_multi_currency_service().get_dashboard(tenant_id)).unwrap()}


@multi_currency_router.get("/positions")
async def currency_positions(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.fx.read"))],
):
    return {"data": (await get_multi_currency_service().get_positions(tenant_id)).unwrap()}


@multi_currency_router.get("/rates")
async def list_exchange_rates(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.fx.read"))],
    rate_type: str | None = Query(default=None),
):
    return {"data": (await get_multi_currency_service().list_rates(tenant_id, rate_type)).unwrap()}


@multi_currency_router.post("/rates", status_code=status.HTTP_201_CREATED)
async def create_exchange_rate(
    body: CreateRateRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.fx.write"))],
):
    result = await get_multi_currency_service().create_rate(
        tenant_id=tenant_id,
        quote_currency=body.quote_currency,
        rate=body.rate,
        rate_type=body.rate_type,
        effective_date=body.effective_date,
        source=body.source,
        base_currency=body.base_currency,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@multi_currency_router.post("/convert", status_code=status.HTTP_201_CREATED)
async def convert_currency(
    body: ConvertCurrencyRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.fx.write"))],
):
    result = await get_multi_currency_service().convert_currency(
        tenant_id=tenant_id,
        from_currency=body.from_currency,
        to_currency=body.to_currency,
        amount=body.amount,
        rate_type=body.rate_type,
        transaction_date=body.transaction_date,
        notes=body.notes,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@multi_currency_router.post("/transfers", status_code=status.HTTP_201_CREATED)
async def cross_currency_transfer(
    body: CrossCurrencyTransferRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.fx.write"))],
):
    result = await get_multi_currency_service().cross_currency_transfer(
        tenant_id=tenant_id,
        from_account_id=body.from_account_id,
        to_account_id=body.to_account_id,
        amount=body.amount,
        rate_type=body.rate_type,
        transaction_date=body.transaction_date,
        notes=body.notes,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@multi_currency_router.post("/revaluations", status_code=status.HTTP_201_CREATED)
async def run_revaluation(
    body: RevaluationRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.fx.write"))],
):
    result = await get_multi_currency_service().run_revaluation(
        tenant_id=tenant_id,
        currency=body.currency,
        new_rate=body.new_rate,
        rate_type=body.rate_type,
        transaction_date=body.transaction_date,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@multi_currency_router.get("/report")
async def fx_report(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.fx.read"))],
):
    return {"data": (await get_multi_currency_service().get_fx_report(tenant_id)).unwrap()}


@multi_currency_router.get("/transactions")
async def list_fx_transactions(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.fx.read"))],
):
    return {"data": (await get_multi_currency_service().list_transactions(tenant_id)).unwrap()}


@multi_currency_router.post("/ai/recommendations")
async def ai_fx_recommendations(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.fx.analyze"))],
):
    result = await get_multi_currency_service().run_ai_recommendations(
        tenant_id,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}
