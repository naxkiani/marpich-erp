"""Tax FastAPI router — CAP-ENT-026 Tax Processing."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from contexts.identity.presentation.dependencies import (
    get_correlation_id,
    get_tenant_id,
    require_permissions,
)
from contexts.tax.container import get_tax_service
from contexts.tax.presentation.schemas import FileTaxReturnRequest

router = APIRouter(prefix="/tax", tags=["Tax"])


@router.get("/liabilities")
async def list_tax_liabilities(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("tax.liabilities.read"))],
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
):
    result = await get_tax_service().list_liabilities(tenant_id, limit=limit, offset=offset)
    return {"data": result.unwrap()}


@router.get("/returns")
async def list_tax_returns(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("tax.returns.read"))],
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
):
    result = await get_tax_service().list_returns(tenant_id, limit=limit, offset=offset)
    return {"data": result.unwrap()}


@router.post("/returns/file", status_code=status.HTTP_201_CREATED)
async def file_tax_return(
    body: FileTaxReturnRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("tax.returns.write"))],
):
    get_tax_service()
    result = await get_tax_service().file_return(
        tenant_id=tenant_id,
        period_label=body.period_label,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}
