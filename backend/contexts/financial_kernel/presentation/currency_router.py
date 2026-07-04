"""Enterprise Currency Engine API routes."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from contexts.financial_kernel.container import get_financial_kernel_service
from contexts.financial_kernel.presentation.schemas import (
    AddCurrencyRequest,
    ConvertCurrencyRequest,
    CreateManualRateRequest,
    ImportCentralBankRatesRequest,
    RevaluationRequest,
    UpdateCurrencyConfigRequest,
)
from contexts.identity.presentation.dependencies import (
    get_correlation_id,
    get_tenant_id,
    require_permissions,
)

currency_router = APIRouter(prefix="/financial-kernel/currency", tags=["Currency Engine"])


@currency_router.get("/config")
async def get_currency_config(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.currency.read"))],
):
    return {"data": (await get_financial_kernel_service().get_currency_config(tenant_id)).unwrap()}


@currency_router.put("/config")
async def update_currency_config(
    body: UpdateCurrencyConfigRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.currency.write"))],
):
    result = await get_financial_kernel_service().update_currency_config(
        tenant_id=tenant_id,
        base_currency=body.base_currency,
        reporting_currency=body.reporting_currency,
        auto_update_enabled=body.auto_update_enabled,
        auto_update_provider=body.auto_update_provider,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@currency_router.get("/currencies")
async def list_currencies(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.currency.read"))],
):
    return {"data": (await get_financial_kernel_service().list_currencies(tenant_id)).unwrap()}


@currency_router.post("/currencies", status_code=status.HTTP_201_CREATED)
async def add_currency(
    body: AddCurrencyRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.currency.write"))],
):
    result = await get_financial_kernel_service().add_currency(tenant_id, body.code)
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@currency_router.get("/rates")
async def list_exchange_rates(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.currency.read"))],
    from_currency: Annotated[str | None, Query()] = None,
    to_currency: Annotated[str | None, Query()] = None,
    rate_type: Annotated[str | None, Query()] = None,
):
    return {
        "data": (
            await get_financial_kernel_service().list_exchange_rates(
                tenant_id,
                from_currency=from_currency,
                to_currency=to_currency,
                rate_type=rate_type,
            )
        ).unwrap()
    }


@currency_router.get("/rates/history")
async def exchange_rate_history(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.currency.read"))],
    from_currency: Annotated[str | None, Query()] = None,
    to_currency: Annotated[str | None, Query()] = None,
    rate_type: Annotated[str | None, Query()] = None,
):
    return {
        "data": (
            await get_financial_kernel_service().get_exchange_history(
                tenant_id,
                from_currency=from_currency,
                to_currency=to_currency,
                rate_type=rate_type,
            )
        ).unwrap()
    }


@currency_router.post("/rates/manual", status_code=status.HTTP_201_CREATED)
async def create_manual_rate(
    body: CreateManualRateRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.currency.write"))],
):
    result = await get_financial_kernel_service().create_manual_rate(
        tenant_id=tenant_id,
        from_currency=body.from_currency,
        to_currency=body.to_currency,
        rate=body.rate,
        effective_date=body.effective_date,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@currency_router.post("/rates/central-bank", status_code=status.HTTP_201_CREATED)
async def import_central_bank_rates(
    body: ImportCentralBankRatesRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.currency.write"))],
):
    result = await get_financial_kernel_service().import_central_bank_rates(
        tenant_id=tenant_id,
        central_bank=body.central_bank,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@currency_router.post("/rates/fetch", status_code=status.HTTP_201_CREATED)
async def fetch_exchange_api_rates(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.currency.write"))],
):
    result = await get_financial_kernel_service().fetch_exchange_api_rates(tenant_id=tenant_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@currency_router.post("/convert")
async def convert_currency(
    body: ConvertCurrencyRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.currency.convert"))],
):
    result = await get_financial_kernel_service().convert_currency(
        tenant_id=tenant_id,
        amount=body.amount,
        from_currency=body.from_currency,
        to_currency=body.to_currency,
        rate_type=body.rate_type,
        as_of_date=body.as_of_date,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@currency_router.get("/snapshots")
async def list_rate_snapshots(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.currency.read"))],
):
    return {"data": (await get_financial_kernel_service().list_rate_snapshots(tenant_id)).unwrap()}


@currency_router.post("/revaluation", status_code=status.HTTP_201_CREATED)
async def run_revaluation(
    body: RevaluationRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.currency.write"))],
):
    result = await get_financial_kernel_service().run_revaluation(
        tenant_id=tenant_id,
        period_id=body.period_id,
        revaluation_date=body.revaluation_date,
        rate_type=body.rate_type,
        balances=[b.model_dump() for b in body.balances] if body.balances else None,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@currency_router.get("/revaluation")
async def list_revaluations(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.currency.read"))],
):
    return {"data": (await get_financial_kernel_service().list_revaluations(tenant_id)).unwrap()}


@currency_router.get("/gain-loss")
async def gain_loss_report(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.currency.read"))],
):
    return {"data": (await get_financial_kernel_service().get_gain_loss_report(tenant_id)).unwrap()}
