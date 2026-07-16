"""Data isolation API."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends

from contexts.data_isolation.container import get_data_isolation_service
from contexts.identity.presentation.dependencies import get_tenant_id, require_permissions

data_isolation_router = APIRouter(
    prefix="/data-isolation",
    tags=["Data Isolation"],
)


@data_isolation_router.get("/catalog")
async def catalog(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("data_isolation.read"))],
):
    return {"data": (await get_data_isolation_service().list_catalog()).unwrap()}


@data_isolation_router.post("/seed")
async def seed(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("data_isolation.write"))],
):
    return {"data": (await get_data_isolation_service().seed(tenant_id)).unwrap()}


@data_isolation_router.get("/dashboard")
async def dashboard(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("data_isolation.read"))],
):
    return {"data": (await get_data_isolation_service().get_dashboard(tenant_id)).unwrap()}


@data_isolation_router.get("/principals")
async def list_principals(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("data_isolation.read"))],
):
    return {"data": (await get_data_isolation_service().list_principals(tenant_id)).unwrap()}


@data_isolation_router.post("/principals/sync")
async def sync_principals(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("data_isolation.principals.write"))],
):
    return {"data": (await get_data_isolation_service().sync_principals(tenant_id)).unwrap()}


@data_isolation_router.post("/verify")
async def verify_isolation(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("data_isolation.verify"))],
):
    return {"data": (await get_data_isolation_service().verify_isolation(tenant_id)).unwrap()}


@data_isolation_router.get("/partitions")
async def partition_map(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("data_isolation.read"))],
):
    return {"data": (await get_data_isolation_service().get_partition_map(tenant_id)).unwrap()}
