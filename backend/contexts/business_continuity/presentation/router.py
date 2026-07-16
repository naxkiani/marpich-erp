"""Enterprise Business Continuity Platform API."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from contexts.business_continuity.container import get_business_continuity_service
from contexts.business_continuity.presentation.schemas import (
    ActivateEmergencyOpsRequest,
    CreateBackupRequest,
    CreatePlanRequest,
    InitiateFailoverRequest,
    ScheduleTestRequest,
)
from contexts.identity.presentation.dependencies import get_correlation_id, get_tenant_id, require_permissions

business_continuity_router = APIRouter(
    prefix="/business-continuity",
    tags=["Enterprise Business Continuity Platform"],
)


@business_continuity_router.get("/catalog")
async def catalog(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("continuity.read"))],
):
    return {"data": (await get_business_continuity_service().list_catalog()).unwrap()}


@business_continuity_router.get("/dependency-map")
async def dependency_map(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("continuity.read"))],
):
    return {"data": (await get_business_continuity_service().get_dependency_map()).unwrap()}


@business_continuity_router.post("/seed")
async def seed(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("continuity.write"))],
):
    return {"data": (await get_business_continuity_service().seed(tenant_id)).unwrap()}


@business_continuity_router.get("/dashboard")
async def dashboard(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("continuity.read"))],
):
    return {"data": (await get_business_continuity_service().get_dashboard(tenant_id)).unwrap()}


@business_continuity_router.get("/plans")
async def list_plans(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("continuity.read"))],
):
    return {"data": (await get_business_continuity_service().list_plans(tenant_id)).unwrap()}


@business_continuity_router.post("/plans", status_code=status.HTTP_201_CREATED)
async def create_plan(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: CreatePlanRequest,
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    user: Annotated[dict, Depends(require_permissions("continuity.write"))],
):
    result = await get_business_continuity_service().create_plan(
        tenant_id,
        title=body.title,
        plan_type=body.plan_type,
        criticality_tier=body.criticality_tier,
        rpo_hours=body.rpo_hours,
        rto_hours=body.rto_hours,
        recovery_steps=body.recovery_steps,
        owner_id=user.get("sub", ""),
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@business_continuity_router.get("/backups")
async def list_backups(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("continuity.read"))],
):
    return {"data": (await get_business_continuity_service().list_backups(tenant_id)).unwrap()}


@business_continuity_router.post("/backups", status_code=status.HTTP_201_CREATED)
async def create_backup(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: CreateBackupRequest,
    _user: Annotated[dict, Depends(require_permissions("continuity.write"))],
):
    result = await get_business_continuity_service().create_backup(
        tenant_id,
        name=body.name,
        backup_type=body.backup_type,
        frequency_hours=body.frequency_hours,
        retention_days=body.retention_days,
        rpo_hours=body.rpo_hours,
        encrypted=body.encrypted,
    )
    return {"data": result.unwrap()}


@business_continuity_router.post("/backups/nightly-cloud", status_code=status.HTTP_201_CREATED)
async def schedule_nightly_cloud_backup(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("continuity.write"))],
):
    result = await get_business_continuity_service().schedule_nightly_cloud_backup(tenant_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@business_continuity_router.get("/rpo-rto")
async def get_rpo_rto(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("continuity.read"))],
):
    return {"data": (await get_business_continuity_service().get_rpo_rto(tenant_id)).unwrap()}


@business_continuity_router.get("/high-availability")
async def get_high_availability(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("continuity.read"))],
):
    return {"data": (await get_business_continuity_service().get_high_availability(tenant_id)).unwrap()}


@business_continuity_router.get("/replication")
async def get_replication(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("continuity.read"))],
):
    return {"data": (await get_business_continuity_service().get_replication(tenant_id)).unwrap()}


@business_continuity_router.post("/failover", status_code=status.HTTP_201_CREATED)
async def initiate_failover(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: InitiateFailoverRequest,
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    user: Annotated[dict, Depends(require_permissions("continuity.write"))],
):
    result = await get_business_continuity_service().initiate_failover(
        tenant_id,
        source_system=body.source_system,
        target_system=body.target_system,
        trigger_reason=body.trigger_reason,
        initiated_by=user.get("sub", ""),
        correlation_id=correlation_id,
    )
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@business_continuity_router.get("/failover")
async def list_failovers(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("continuity.read"))],
):
    return {"data": (await get_business_continuity_service().list_failovers(tenant_id)).unwrap()}


@business_continuity_router.post("/emergency-ops")
async def activate_emergency_ops(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: ActivateEmergencyOpsRequest,
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("continuity.write"))],
):
    result = await get_business_continuity_service().activate_emergency_ops(
        tenant_id, plan_ref=body.plan_ref, correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@business_continuity_router.post("/tests", status_code=status.HTTP_201_CREATED)
async def schedule_test(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: ScheduleTestRequest,
    user: Annotated[dict, Depends(require_permissions("continuity.test"))],
):
    result = await get_business_continuity_service().schedule_test(
        tenant_id,
        plan_ref=body.plan_ref,
        test_type=body.test_type,
        executed_by=user.get("sub", ""),
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@business_continuity_router.post("/tests/{test_ref}/run")
async def run_test(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    test_ref: str,
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("continuity.test"))],
):
    result = await get_business_continuity_service().run_test(
        tenant_id, test_ref, correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@business_continuity_router.get("/tests")
async def list_tests(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("continuity.read"))],
):
    return {"data": (await get_business_continuity_service().list_tests(tenant_id)).unwrap()}
