"""Banking Analytics Platform API routes."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from contexts.banking.container import get_banking_analytics_platform_service
from contexts.banking.presentation.banking_analytics_schemas import AIAssistantRequest, RunAnalysisRequest
from contexts.identity.presentation.dependencies import (
    get_correlation_id,
    get_tenant_id,
    require_permissions,
)

banking_analytics_router = APIRouter(
    prefix="/banking/analytics",
    tags=["Banking Analytics Platform"],
)


def _raise(result) -> None:
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)


@banking_analytics_router.get("/catalog")
async def analytics_catalog(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.analytics.read"))],
):
    return {"data": (await get_banking_analytics_platform_service().list_catalog()).unwrap()}


@banking_analytics_router.get("/policy-keys")
async def analytics_policy_keys(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.analytics.read"))],
):
    return {"data": (await get_banking_analytics_platform_service().list_policy_keys()).unwrap()}


@banking_analytics_router.get("/dashboard")
async def analytics_dashboard(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.analytics.read"))],
):
    return {"data": (await get_banking_analytics_platform_service().get_dashboard(tenant_id)).unwrap()}


@banking_analytics_router.get("/liquidity-kpis")
async def liquidity_kpis(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.analytics.read"))],
):
    return {"data": (await get_banking_analytics_platform_service().get_liquidity_kpis(tenant_id)).unwrap()}


@banking_analytics_router.get("/deposit-trends")
async def deposit_trends(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.analytics.read"))],
):
    return {"data": (await get_banking_analytics_platform_service().get_deposit_trends(tenant_id)).unwrap()}


@banking_analytics_router.get("/loan-portfolio")
async def loan_portfolio(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.analytics.read"))],
):
    return {"data": (await get_banking_analytics_platform_service().get_loan_portfolio(tenant_id)).unwrap()}


@banking_analytics_router.get("/customer-segmentation")
async def customer_segmentation(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.analytics.read"))],
):
    return {"data": (await get_banking_analytics_platform_service().get_customer_segmentation(tenant_id)).unwrap()}


@banking_analytics_router.get("/branch-performance")
async def branch_performance(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.analytics.read"))],
):
    return {"data": (await get_banking_analytics_platform_service().get_branch_performance(tenant_id)).unwrap()}


@banking_analytics_router.get("/revenue-analysis")
async def revenue_analysis(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.analytics.read"))],
):
    return {"data": (await get_banking_analytics_platform_service().get_revenue_analysis(tenant_id)).unwrap()}


@banking_analytics_router.get("/risk-indicators")
async def risk_indicators(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.analytics.read"))],
):
    return {"data": (await get_banking_analytics_platform_service().get_risk_indicators(tenant_id)).unwrap()}


@banking_analytics_router.get("/portfolio-quality")
async def portfolio_quality(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.analytics.read"))],
):
    return {"data": (await get_banking_analytics_platform_service().get_portfolio_quality(tenant_id)).unwrap()}


@banking_analytics_router.get("/delinquency-analysis")
async def delinquency_analysis(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.analytics.read"))],
):
    return {"data": (await get_banking_analytics_platform_service().get_delinquency_analysis(tenant_id)).unwrap()}


@banking_analytics_router.get("/forecasting")
async def forecasting(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.analytics.read"))],
):
    return {"data": (await get_banking_analytics_platform_service().get_forecasting(tenant_id)).unwrap()}


@banking_analytics_router.get("/fraud-detection")
async def fraud_detection(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.analytics.read"))],
):
    return {"data": (await get_banking_analytics_platform_service().get_fraud_detection(tenant_id)).unwrap()}


@banking_analytics_router.get("/customer-insights")
async def customer_insights(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.analytics.read"))],
):
    return {"data": (await get_banking_analytics_platform_service().get_customer_insights(tenant_id)).unwrap()}


@banking_analytics_router.get("/executive-dashboard")
async def executive_dashboard(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.analytics.read"))],
):
    return {"data": (await get_banking_analytics_platform_service().get_executive_dashboard(tenant_id)).unwrap()}


@banking_analytics_router.get("/recommendations")
async def recommendations(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.analytics.read"))],
):
    return {"data": (await get_banking_analytics_platform_service().get_recommendations(tenant_id)).unwrap()}


@banking_analytics_router.post("/ai-assistant")
async def ai_assistant(
    _body: AIAssistantRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.analytics.write"))],
):
    result = await get_banking_analytics_platform_service().run_ai_assistant(
        tenant_id, correlation_id=correlation_id
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_analytics_router.post("/analyze/{capability}", status_code=status.HTTP_201_CREATED)
async def analyze_capability(
    capability: str,
    body: RunAnalysisRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.analytics.write"))],
):
    result = await get_banking_analytics_platform_service().run_analysis(
        tenant_id,
        capability,
        correlation_id=correlation_id,
        input_data=body.input_data,
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_analytics_router.get("/jobs")
async def list_jobs(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.analytics.read"))],
    capability: str | None = None,
):
    return {"data": (await get_banking_analytics_platform_service().list_jobs(tenant_id, capability)).unwrap()}


@banking_analytics_router.get("/jobs/{job_id}")
async def get_job(
    job_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.analytics.read"))],
):
    result = await get_banking_analytics_platform_service().get_job(tenant_id, job_id)
    _raise(result)
    return {"data": result.unwrap()}
