"""Identity resilience platform API."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from contexts.identity_resilience.container import get_identity_resilience_service
from contexts.identity_resilience.presentation.schemas import (
    DeployWorkerRequest,
    FailoverRequest,
    RegisterRegionRequest,
)
from contexts.identity.presentation.dependencies import get_tenant_id, require_permissions

identity_resilience_router = APIRouter(
    prefix="/identity-resilience",
    tags=["Identity Resilience"],
)


@identity_resilience_router.get("/catalog")
async def catalog(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("identity_resilience.read"))],
):
    return {"data": (await get_identity_resilience_service().list_catalog()).unwrap()}


@identity_resilience_router.post("/seed")
async def seed(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("identity_resilience.write"))],
):
    return {"data": (await get_identity_resilience_service().seed(tenant_id)).unwrap()}


@identity_resilience_router.get("/dashboard")
async def dashboard(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("identity_resilience.read"))],
):
    return {"data": (await get_identity_resilience_service().get_dashboard(tenant_id)).unwrap()}


@identity_resilience_router.get("/regions")
async def list_regions(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("identity_resilience.read"))],
):
    return {"data": (await get_identity_resilience_service().list_regions(tenant_id)).unwrap()}


@identity_resilience_router.post("/regions")
async def register_region(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: RegisterRegionRequest,
    _user: Annotated[dict, Depends(require_permissions("identity_resilience.regions.write"))],
):
    result = await get_identity_resilience_service().register_region(
        tenant_id,
        region_id=body.region_id,
        display_name=body.display_name,
        is_primary=body.is_primary,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@identity_resilience_router.get("/workers")
async def list_workers(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("identity_resilience.read"))],
):
    return {"data": (await get_identity_resilience_service().list_workers(tenant_id)).unwrap()}


@identity_resilience_router.post("/workers")
async def deploy_worker(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: DeployWorkerRequest,
    _user: Annotated[dict, Depends(require_permissions("identity_resilience.workers.write"))],
):
    result = await get_identity_resilience_service().deploy_worker(
        tenant_id,
        worker_type=body.worker_type,
        region_id=body.region_id,
        role=body.role,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@identity_resilience_router.post("/workers/{worker_ref}/heartbeat")
async def worker_heartbeat(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    worker_ref: str,
    _user: Annotated[dict, Depends(require_permissions("identity_resilience.workers.write"))],
):
    result = await get_identity_resilience_service().heartbeat(tenant_id, worker_ref)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@identity_resilience_router.get("/replication")
async def replication_health(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("identity_resilience.read"))],
):
    return {"data": (await get_identity_resilience_service().check_replication_health(tenant_id)).unwrap()}


@identity_resilience_router.post("/failover")
async def initiate_failover(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: FailoverRequest,
    _user: Annotated[dict, Depends(require_permissions("identity_resilience.failover.execute"))],
):
    result = await get_identity_resilience_service().initiate_failover(
        tenant_id,
        worker_type=body.worker_type,
        reason=body.reason,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@identity_resilience_router.post("/health-check")
async def run_health_check(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("identity_resilience.failover.execute"))],
):
    return {"data": (await get_identity_resilience_service().run_health_check(tenant_id)).unwrap()}


@identity_resilience_router.post("/workers/directory-sync/run")
async def run_directory_sync_ha(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("identity_resilience.workers.execute"))],
):
    result = await get_identity_resilience_service().run_directory_sync_ha(tenant_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@identity_resilience_router.get("/failovers")
async def list_failovers(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("identity_resilience.read"))],
):
    return {"data": (await get_identity_resilience_service().list_failovers(tenant_id)).unwrap()}
