"""POS FastAPI router."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from contexts.identity.presentation.dependencies import (
    get_correlation_id,
    get_tenant_id,
    require_permissions,
)
from contexts.pos.container import get_pos_service
from contexts.pos.presentation.schemas import CompleteSaleRequest, OpenShiftRequest, RegisterTerminalRequest

router = APIRouter(prefix="/pos", tags=["POS"])


@router.post("/terminals", status_code=status.HTTP_201_CREATED)
async def register_terminal(
    body: RegisterTerminalRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("pos.terminals.write"))],
):
    result = await get_pos_service().register_terminal(
        tenant_id=tenant_id,
        terminal_code=body.terminal_code,
        store_name=body.store_name,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.post("/shifts", status_code=status.HTTP_201_CREATED)
async def open_shift(
    body: OpenShiftRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("pos.shifts.write"))],
):
    result = await get_pos_service().open_shift(
        tenant_id=tenant_id,
        terminal_id=body.terminal_id,
        cashier_name=body.cashier_name,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.post("/sales", status_code=status.HTTP_201_CREATED)
async def complete_sale(
    body: CompleteSaleRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("pos.sales.write"))],
):
    items = [item.model_dump() for item in body.items]
    result = await get_pos_service().complete_sale(
        tenant_id=tenant_id,
        shift_id=body.shift_id,
        items=items,
        subtotal=body.subtotal,
        tax=body.tax,
        payment_method=body.payment_method,
        correlation_id=correlation_id,
        issue_receipt=body.issue_receipt,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.post("/shifts/{shift_id}/close")
async def close_shift(
    shift_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("pos.shifts.write"))],
):
    result = await get_pos_service().close_shift(
        tenant_id=tenant_id, shift_id=shift_id, correlation_id=correlation_id
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}
