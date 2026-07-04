"""Financial Kernel FastAPI router."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from contexts.financial_kernel.container import get_financial_kernel_service
from contexts.financial_kernel.presentation.schemas import (
    CalculateTaxRequest,
    ConvertCurrencyRequest,
    PostJournalRequest,
)
from contexts.identity.presentation.dependencies import (
    get_correlation_id,
    get_tenant_id,
    require_permissions,
)

router = APIRouter(prefix="/financial-kernel", tags=["Financial Kernel"])


@router.get("/accounts")
async def list_accounts(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.accounts.read"))],
):
    return {"data": (await get_financial_kernel_service().list_accounts(tenant_id)).unwrap()}


@router.get("/cost-centers")
async def list_cost_centers(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.dimensions.read"))],
):
    return {"data": (await get_financial_kernel_service().list_cost_centers(tenant_id)).unwrap()}


@router.post("/journals", status_code=status.HTTP_201_CREATED)
async def post_journal(
    body: PostJournalRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.journals.post"))],
):
    result = await get_financial_kernel_service().post_journal(
        tenant_id=tenant_id,
        source_context=body.source_context,
        source_document_id=body.source_document_id,
        lines=[line.model_dump() for line in body.lines],
        currency=body.currency,
        correlation_id=correlation_id,
        idempotency_key=body.idempotency_key,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.get("/ledger/trial-balance")
async def trial_balance(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.ledger.read"))],
):
    return {"data": (await get_financial_kernel_service().get_trial_balance(tenant_id)).unwrap()}


@router.post("/currency/convert")
async def convert_currency(
    body: ConvertCurrencyRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.currency.convert"))],
):
    return {"data": (await get_financial_kernel_service().convert_currency(
        tenant_id=tenant_id,
        amount=body.amount,
        from_currency=body.from_currency,
        to_currency=body.to_currency,
    )).unwrap()}


@router.post("/tax/calculate")
async def calculate_tax(
    body: CalculateTaxRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.tax.calculate"))],
):
    return {"data": (await get_financial_kernel_service().calculate_tax(
        tenant_id=tenant_id,
        amount=body.amount,
        tax_code=body.tax_code,
        jurisdiction=body.jurisdiction,
    )).unwrap()}
