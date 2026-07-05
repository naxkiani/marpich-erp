"""Enterprise Liquidity Engine API routes."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from contexts.identity.presentation.dependencies import (
    get_correlation_id,
    get_tenant_id,
    require_permissions,
)
from contexts.treasury.container import get_liquidity_service
from contexts.treasury.presentation.liquidity_schemas import (
    CreateCashPoolRequest,
    CreateFundingNeedRequest,
    LiquidityPredictionRequest,
)

liquidity_router = APIRouter(
    prefix="/treasury/liquidity",
    tags=["Enterprise Liquidity Engine"],
)


@liquidity_router.get("/catalog")
async def liquidity_catalog(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.liquidity.read"))],
):
    return {"data": (await get_liquidity_service().list_catalog()).unwrap()}


@liquidity_router.get("/dashboard")
async def liquidity_dashboard(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.liquidity.read"))],
):
    return {"data": (await get_liquidity_service().get_dashboard(tenant_id)).unwrap()}


@liquidity_router.get("/cash-position")
async def cash_position(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.liquidity.read"))],
):
    return {"data": (await get_liquidity_service().get_cash_position(tenant_id)).unwrap()}


@liquidity_router.get("/daily")
async def daily_liquidity(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.liquidity.read"))],
    days: int = Query(30, ge=7, le=90),
):
    return {"data": (await get_liquidity_service().get_daily_liquidity(tenant_id, days)).unwrap()}


@liquidity_router.get("/weekly")
async def weekly_liquidity(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.liquidity.read"))],
    weeks: int = Query(12, ge=4, le=52),
):
    return {"data": (await get_liquidity_service().get_weekly_liquidity(tenant_id, weeks)).unwrap()}


@liquidity_router.get("/monthly")
async def monthly_liquidity(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.liquidity.read"))],
    months: int = Query(12, ge=3, le=24),
):
    return {"data": (await get_liquidity_service().get_monthly_liquidity(tenant_id, months)).unwrap()}


@liquidity_router.get("/rolling-forecast")
async def rolling_forecast(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.liquidity.read"))],
    horizon_weeks: int = Query(13, ge=4, le=52),
):
    return {
        "data": (await get_liquidity_service().get_rolling_forecast(tenant_id, horizon_weeks)).unwrap()
    }


@liquidity_router.get("/pools")
async def list_pools(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.liquidity.read"))],
):
    return {"data": (await get_liquidity_service().list_cash_pools(tenant_id)).unwrap()}


@liquidity_router.post("/pools", status_code=status.HTTP_201_CREATED)
async def create_pool(
    body: CreateCashPoolRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.liquidity.write"))],
):
    result = await get_liquidity_service().create_cash_pool(
        tenant_id=tenant_id,
        code=body.code,
        name=body.name,
        currency=body.currency,
        target_balance=body.target_balance,
        minimum_balance=body.minimum_balance,
        member_account_ids=body.member_account_ids,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@liquidity_router.get("/funding-needs")
async def funding_needs(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.liquidity.read"))],
):
    return {"data": (await get_liquidity_service().get_funding_needs(tenant_id)).unwrap()}


@liquidity_router.post("/funding-needs", status_code=status.HTTP_201_CREATED)
async def create_funding_need(
    body: CreateFundingNeedRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.liquidity.write"))],
):
    result = await get_liquidity_service().create_funding_need(
        tenant_id=tenant_id,
        label=body.label,
        currency=body.currency,
        required_amount=body.required_amount,
        available_amount=body.available_amount,
        due_date=body.due_date,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@liquidity_router.get("/gap")
async def liquidity_gap(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.liquidity.read"))],
):
    return {"data": (await get_liquidity_service().get_liquidity_gap(tenant_id)).unwrap()}


@liquidity_router.get("/working-capital")
async def working_capital(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.liquidity.read"))],
):
    return {"data": (await get_liquidity_service().get_working_capital(tenant_id)).unwrap()}


@liquidity_router.post("/ai/predict")
async def ai_liquidity_prediction(
    body: LiquidityPredictionRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.liquidity.analyze"))],
):
    result = await get_liquidity_service().predict_liquidity(
        tenant_id=tenant_id,
        horizon_days=body.horizon_days,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@liquidity_router.get("/ai/optimization")
async def optimization_recommendations(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.liquidity.analyze"))],
):
    result = await get_liquidity_service().get_optimization_recommendations(
        tenant_id=tenant_id,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}
