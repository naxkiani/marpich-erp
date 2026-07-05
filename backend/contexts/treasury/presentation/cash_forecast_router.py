"""Enterprise Cash Forecast API routes."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from contexts.identity.presentation.dependencies import (
    get_correlation_id,
    get_tenant_id,
    require_permissions,
)
from contexts.treasury.container import get_cash_forecast_service
from contexts.treasury.presentation.cash_forecast_schemas import (
    AIForecastRequest,
    CreateForecastPlanRequest,
    ScenarioSimulationRequest,
)

cash_forecast_router = APIRouter(
    prefix="/treasury/cash-forecast",
    tags=["Enterprise Cash Forecast"],
)


@cash_forecast_router.get("/catalog")
async def forecast_catalog(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.forecast.read"))],
):
    return {"data": (await get_cash_forecast_service().list_catalog()).unwrap()}


@cash_forecast_router.get("/categories")
async def forecast_categories(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.forecast.read"))],
):
    return {"data": (await get_cash_forecast_service().list_categories()).unwrap()}


@cash_forecast_router.get("/dashboard")
async def forecast_dashboard(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.forecast.read"))],
):
    return {"data": (await get_cash_forecast_service().get_dashboard(tenant_id)).unwrap()}


@cash_forecast_router.get("/daily")
async def daily_cash(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.forecast.read"))],
    days: int = Query(30, ge=7, le=90),
    scenario: str = Query("base"),
):
    return {
        "data": (
            await get_cash_forecast_service().get_period_forecast(
                tenant_id, "daily", days, scenario
            )
        ).unwrap()
    }


@cash_forecast_router.get("/weekly")
async def weekly_cash(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.forecast.read"))],
    weeks: int = Query(12, ge=4, le=52),
    scenario: str = Query("base"),
):
    return {
        "data": (
            await get_cash_forecast_service().get_period_forecast(
                tenant_id, "weekly", weeks, scenario
            )
        ).unwrap()
    }


@cash_forecast_router.get("/monthly")
async def monthly_cash(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.forecast.read"))],
    months: int = Query(12, ge=3, le=24),
    scenario: str = Query("base"),
):
    return {
        "data": (
            await get_cash_forecast_service().get_period_forecast(
                tenant_id, "monthly", months, scenario
            )
        ).unwrap()
    }


@cash_forecast_router.get("/quarterly")
async def quarterly_cash(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.forecast.read"))],
    quarters: int = Query(4, ge=2, le=8),
    scenario: str = Query("base"),
):
    return {
        "data": (
            await get_cash_forecast_service().get_period_forecast(
                tenant_id, "quarterly", quarters, scenario
            )
        ).unwrap()
    }


@cash_forecast_router.get("/annual")
async def annual_cash(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.forecast.read"))],
    years: int = Query(3, ge=1, le=5),
    scenario: str = Query("base"),
):
    return {
        "data": (
            await get_cash_forecast_service().get_period_forecast(
                tenant_id, "annual", years, scenario
            )
        ).unwrap()
    }


@cash_forecast_router.get("/categories/breakdown")
async def category_breakdown(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.forecast.read"))],
):
    return {"data": (await get_cash_forecast_service().get_category_breakdown(tenant_id)).unwrap()}


@cash_forecast_router.post("/plans", status_code=status.HTTP_201_CREATED)
async def create_plan(
    body: CreateForecastPlanRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.forecast.write"))],
):
    result = await get_cash_forecast_service().create_plan(
        tenant_id=tenant_id,
        name=body.name,
        period_type=body.period_type,
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


@cash_forecast_router.get("/plans")
async def list_plans(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.forecast.read"))],
):
    return {"data": (await get_cash_forecast_service().list_plans(tenant_id)).unwrap()}


@cash_forecast_router.get("/plans/{plan_id}")
async def get_plan(
    plan_id: str,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.forecast.read"))],
):
    result = await get_cash_forecast_service().get_plan(plan_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@cash_forecast_router.post("/ai/forecast")
async def ai_forecast(
    body: AIForecastRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.forecast.analyze"))],
):
    result = await get_cash_forecast_service().run_ai_forecast(
        tenant_id=tenant_id,
        horizon_days=body.horizon_days,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@cash_forecast_router.post("/plans/{plan_id}/simulate")
async def scenario_simulation(
    plan_id: str,
    body: ScenarioSimulationRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.forecast.analyze"))],
):
    result = await get_cash_forecast_service().run_scenario_simulation(
        tenant_id=tenant_id,
        plan_id=plan_id,
        name=body.name,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@cash_forecast_router.get("/simulations")
async def list_simulations(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.forecast.read"))],
):
    return {"data": (await get_cash_forecast_service().list_simulations(tenant_id)).unwrap()}
