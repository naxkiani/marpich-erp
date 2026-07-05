"""Enterprise Investment Management API routes."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from contexts.identity.presentation.dependencies import (
    get_correlation_id,
    get_tenant_id,
    require_permissions,
)
from contexts.treasury.container import get_investment_service
from contexts.treasury.presentation.investments_schemas import (
    AccrueInterestRequest,
    CreateInvestmentRequest,
    MatureInvestmentRequest,
    RecordIncomeRequest,
)

investments_router = APIRouter(
    prefix="/treasury/investments",
    tags=["Enterprise Investment Management"],
)


@investments_router.get("/catalog")
async def investment_catalog(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.investments.read"))],
):
    return {"data": (await get_investment_service().list_catalog()).unwrap()}


@investments_router.get("/dashboard")
async def investment_dashboard(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.investments.read"))],
):
    return {"data": (await get_investment_service().get_dashboard(tenant_id)).unwrap()}


@investments_router.get("/portfolios")
async def list_portfolios(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.investments.read"))],
):
    return {"data": (await get_investment_service().list_portfolios(tenant_id)).unwrap()}


@investments_router.get("/performance")
async def portfolio_performance(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.investments.read"))],
):
    return {"data": (await get_investment_service().get_portfolio_performance(tenant_id)).unwrap()}


@investments_router.get("/maturities")
async def maturity_tracking(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.investments.read"))],
    horizon_days: int = Query(90, ge=7, le=365),
):
    return {
        "data": (await get_investment_service().get_maturity_tracking(tenant_id, horizon_days)).unwrap()
    }


@investments_router.get("/risk-ratings")
async def risk_ratings(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.investments.read"))],
):
    return {"data": (await get_investment_service().get_risk_ratings(tenant_id)).unwrap()}


@investments_router.post("/ai/analysis")
async def ai_investment_analysis(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.investments.analyze"))],
):
    result = await get_investment_service().run_ai_analysis(
        tenant_id,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@investments_router.get("")
async def list_investments(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.investments.read"))],
    portfolio_name: str | None = Query(default=None),
):
    return {
        "data": (await get_investment_service().list_investments(tenant_id, portfolio_name)).unwrap()
    }


@investments_router.post("", status_code=status.HTTP_201_CREATED)
async def create_investment(
    body: CreateInvestmentRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.investments.write"))],
):
    result = await get_investment_service().create_investment(
        tenant_id=tenant_id,
        portfolio_name=body.portfolio_name,
        investment_type=body.investment_type,
        name=body.name,
        instrument_code=body.instrument_code,
        principal_amount=body.principal_amount,
        currency=body.currency,
        interest_rate=body.interest_rate,
        purchase_date=body.purchase_date,
        maturity_date=body.maturity_date,
        risk_rating=body.risk_rating,
        treasury_account_id=body.treasury_account_id,
        notes=body.notes,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@investments_router.get("/{investment_id}")
async def get_investment(
    investment_id: str,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.investments.read"))],
):
    result = await get_investment_service().get_investment(investment_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@investments_router.post("/{investment_id}/accrue-interest")
async def accrue_interest(
    investment_id: str,
    body: AccrueInterestRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.investments.write"))],
):
    result = await get_investment_service().accrue_interest(
        investment_id,
        tenant_id=tenant_id,
        days=body.days,
        accrual_date=body.accrual_date,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@investments_router.post("/{investment_id}/record-income")
async def record_income(
    investment_id: str,
    body: RecordIncomeRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.investments.write"))],
):
    result = await get_investment_service().record_income(
        investment_id,
        tenant_id=tenant_id,
        amount=body.amount,
        transaction_date=body.transaction_date,
        notes=body.notes,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@investments_router.post("/{investment_id}/mature")
async def mature_investment(
    investment_id: str,
    body: MatureInvestmentRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.investments.write"))],
):
    result = await get_investment_service().mature_investment(
        investment_id,
        tenant_id=tenant_id,
        maturity_date=body.maturity_date,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@investments_router.get("/{investment_id}/income")
async def list_investment_income(
    investment_id: str,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.investments.read"))],
):
    return {"data": (await get_investment_service().list_income_transactions(investment_id)).unwrap()}
