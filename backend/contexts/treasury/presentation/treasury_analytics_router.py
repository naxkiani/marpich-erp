"""Treasury Analytics API routes."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends

from contexts.identity.presentation.dependencies import (
    get_correlation_id,
    get_tenant_id,
    require_permissions,
)
from contexts.treasury.container import get_treasury_analytics_service

treasury_analytics_router = APIRouter(
    prefix="/treasury/analytics",
    tags=["Treasury Analytics"],
)


@treasury_analytics_router.get("/catalog")
async def analytics_catalog(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.analytics.read"))],
):
    return {"data": (await get_treasury_analytics_service().list_catalog()).unwrap()}


@treasury_analytics_router.get("/dashboard")
async def analytics_dashboard(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.analytics.read"))],
):
    return {"data": (await get_treasury_analytics_service().get_dashboard(tenant_id)).unwrap()}


@treasury_analytics_router.get("/cash-flow")
async def cash_flow_analysis(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.analytics.read"))],
):
    return {"data": (await get_treasury_analytics_service().get_cash_flow_analysis(tenant_id)).unwrap()}


@treasury_analytics_router.get("/liquidity-trends")
async def liquidity_trends(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.analytics.read"))],
):
    return {"data": (await get_treasury_analytics_service().get_liquidity_trends(tenant_id)).unwrap()}


@treasury_analytics_router.get("/kpis")
async def treasury_kpis(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.analytics.read"))],
):
    return {"data": (await get_treasury_analytics_service().get_treasury_kpis(tenant_id)).unwrap()}


@treasury_analytics_router.get("/bank-balances")
async def bank_balance_analysis(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.analytics.read"))],
):
    return {"data": (await get_treasury_analytics_service().get_bank_balance_analysis(tenant_id)).unwrap()}


@treasury_analytics_router.get("/forecast-accuracy")
async def forecast_accuracy(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.analytics.read"))],
):
    return {"data": (await get_treasury_analytics_service().get_forecast_accuracy(tenant_id)).unwrap()}


@treasury_analytics_router.get("/investment-performance")
async def investment_performance(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.analytics.read"))],
):
    return {"data": (await get_treasury_analytics_service().get_investment_performance(tenant_id)).unwrap()}


@treasury_analytics_router.get("/funding")
async def funding_analysis(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.analytics.read"))],
):
    return {"data": (await get_treasury_analytics_service().get_funding_analysis(tenant_id)).unwrap()}


@treasury_analytics_router.get("/currency-exposure")
async def currency_exposure(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.analytics.read"))],
):
    return {"data": (await get_treasury_analytics_service().get_currency_exposure(tenant_id)).unwrap()}


@treasury_analytics_router.get("/working-capital")
async def working_capital_kpis(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.analytics.read"))],
):
    return {"data": (await get_treasury_analytics_service().get_working_capital_kpis(tenant_id)).unwrap()}


@treasury_analytics_router.get("/executive")
async def executive_dashboard(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.analytics.read"))],
):
    return {"data": (await get_treasury_analytics_service().get_executive_dashboard(tenant_id)).unwrap()}


@treasury_analytics_router.get("/cfo")
async def cfo_dashboard(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.analytics.read"))],
):
    return {"data": (await get_treasury_analytics_service().get_cfo_dashboard(tenant_id)).unwrap()}


@treasury_analytics_router.get("/recommendations")
async def treasury_recommendations(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.analytics.read"))],
):
    return {"data": (await get_treasury_analytics_service().get_recommendations(tenant_id)).unwrap()}


@treasury_analytics_router.post("/ai/assistant")
async def ai_treasury_assistant(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.analytics.analyze"))],
):
    return {
        "data": (
            await get_treasury_analytics_service().run_ai_assistant(
                tenant_id, correlation_id=correlation_id
            )
        ).unwrap()
    }
