"""Inventory FastAPI router — stock levels for retail/POS."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from contexts.identity.presentation.dependencies import (
    get_correlation_id,
    get_tenant_id,
    require_permissions,
)
from contexts.inventory.container import get_inventory_service
from contexts.inventory.presentation.schemas import UpsertStockRequest

router = APIRouter(prefix="/inventory", tags=["Inventory"])


@router.put("/stock", status_code=status.HTTP_200_OK)
async def upsert_stock(
    body: UpsertStockRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("inventory.stock.write"))],
):
    result = await get_inventory_service().upsert_stock(
        tenant_id=tenant_id,
        sku=body.sku,
        quantity=body.quantity,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.get("/stock")
async def list_stock(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("inventory.stock.read"))],
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
):
    result = await get_inventory_service().list_stock(tenant_id, limit=limit, offset=offset)
    return {"data": result.unwrap()}


@router.get("/stock/{sku}")
async def get_stock(
    sku: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("inventory.stock.read"))],
):
    result = await get_inventory_service().get_stock(tenant_id, sku)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}
