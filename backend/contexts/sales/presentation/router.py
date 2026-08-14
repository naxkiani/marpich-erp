"""Sales FastAPI router — CAP-ENT-002 Sales Lifecycle."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from contexts.identity.presentation.dependencies import (
    get_correlation_id,
    get_tenant_id,
    require_permissions,
)
from contexts.sales.container import get_sales_service
from contexts.sales.presentation.schemas import CreateQuotationRequest

router = APIRouter(prefix="/sales", tags=["Sales"])


@router.post("/quotations", status_code=status.HTTP_201_CREATED)
async def create_quotation(
    body: CreateQuotationRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("sales.quotations.write"))],
):
    result = await get_sales_service().create_quotation(
        tenant_id=tenant_id,
        contact_id=body.contact_id,
        title=body.title,
        amount=body.amount,
        currency=body.currency,
        opportunity_id=body.opportunity_id,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.get("/quotations")
async def list_quotations(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("sales.quotations.read"))],
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
):
    result = await get_sales_service().list_quotations(tenant_id, limit=limit, offset=offset)
    return {"data": result.unwrap()}


@router.post("/quotations/{quotation_id}/send")
async def send_quotation(
    quotation_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("sales.quotations.write"))],
):
    result = await get_sales_service().send_quotation(
        tenant_id=tenant_id,
        quotation_id=quotation_id,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.post("/quotations/{quotation_id}/convert")
async def convert_quotation(
    quotation_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("sales.orders.write"))],
):
    result = await get_sales_service().convert_quotation_to_order(
        tenant_id=tenant_id,
        quotation_id=quotation_id,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.get("/orders")
async def list_orders(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("sales.orders.read"))],
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
):
    result = await get_sales_service().list_orders(tenant_id, limit=limit, offset=offset)
    return {"data": result.unwrap()}
