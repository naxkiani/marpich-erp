"""Enterprise Financial Dimensions API routes."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from contexts.financial_kernel.container import get_financial_kernel_service
from contexts.financial_kernel.presentation.schemas import (
    CreateDimensionValueRequest,
    ValidateJournalDimensionsRequest,
)
from contexts.identity.presentation.dependencies import (
    get_tenant_id,
    require_permissions,
)

financial_dimensions_router = APIRouter(
    prefix="/financial-kernel/dimensions", tags=["Financial Dimensions"]
)


@financial_dimensions_router.get("/catalog")
async def list_dimension_catalog(
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.dimensions.read"))],
):
    result = await get_financial_kernel_service().list_dimension_catalog()
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@financial_dimensions_router.get("/values")
async def list_dimension_values(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.dimensions.read"))],
    dimension_type: str | None = Query(None),
):
    result = await get_financial_kernel_service().list_dimension_values(
        tenant_id, dimension_type=dimension_type
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@financial_dimensions_router.post("/values", status_code=status.HTTP_201_CREATED)
async def create_dimension_value(
    body: CreateDimensionValueRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[dict, Depends(require_permissions("financial_kernel.dimensions.write"))],
):
    result = await get_financial_kernel_service().create_dimension_value(
        tenant_id=tenant_id,
        dimension_type=body.dimension_type,
        code=body.code,
        name=body.name,
        parent_id=body.parent_id,
        metadata=body.metadata,
        actor_id=user.get("sub", "system"),
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@financial_dimensions_router.get("/values/{value_id}")
async def get_dimension_value(
    value_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.dimensions.read"))],
):
    result = await get_financial_kernel_service().get_dimension_value(tenant_id, value_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@financial_dimensions_router.post("/values/{value_id}/deactivate")
async def deactivate_dimension_value(
    value_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[dict, Depends(require_permissions("financial_kernel.dimensions.write"))],
):
    result = await get_financial_kernel_service().deactivate_dimension_value(
        tenant_id, value_id, actor_id=user.get("sub", "system")
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@financial_dimensions_router.post("/validate")
async def validate_journal_dimensions(
    body: ValidateJournalDimensionsRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.dimensions.read"))],
):
    result = await get_financial_kernel_service().validate_journal_dimensions(
        tenant_id, body.lines
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@financial_dimensions_router.get("/values/{value_id}/audit")
async def list_dimension_audit_history(
    value_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.dimensions.read"))],
):
    result = await get_financial_kernel_service().list_dimension_audit_history(
        tenant_id, value_id
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}
