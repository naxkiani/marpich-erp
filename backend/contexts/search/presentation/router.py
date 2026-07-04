"""Search FastAPI router."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from contexts.identity.presentation.dependencies import (
    get_correlation_id,
    get_tenant_id,
    require_permissions,
)
from contexts.search.container import get_search_service

router = APIRouter(prefix="/search", tags=["Search"])


@router.get("/query")
async def search_query(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("search.query.read"))],
    q: str = Query(default="", max_length=512),
    types: Annotated[list[str] | None, Query()] = None,
    limit: int = Query(default=50, ge=1, le=200),
):
    result = await get_search_service().query(tenant_id, q, entity_types=types, limit=limit)
    return {"data": result.unwrap()}


@router.get("/suggest")
async def search_suggest(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("search.query.read"))],
    q: str = Query(min_length=1, max_length=128),
    limit: int = Query(default=10, ge=1, le=50),
):
    result = await get_search_service().suggest(tenant_id, q, limit=limit)
    return {"data": result.unwrap()}


@router.get("/indices")
async def list_indices(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("search.admin.read"))],
):
    result = await get_search_service().list_indices(tenant_id)
    return {"data": result.unwrap()}


@router.post("/reindex", status_code=status.HTTP_202_ACCEPTED)
async def trigger_reindex(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("search.admin.write"))],
):
    result = await get_search_service().reindex(tenant_id, correlation_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}
