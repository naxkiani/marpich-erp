"""Enterprise Scheduler Platform API."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from contexts.enterprise_scheduler.container import get_enterprise_scheduler_service
from contexts.enterprise_scheduler.presentation.schemas import CreateJobRequest, RegisterDependencyRequest
from contexts.identity.presentation.dependencies import get_correlation_id, get_tenant_id, require_permissions

enterprise_scheduler_router = APIRouter(
    prefix="/enterprise-scheduler",
    tags=["Enterprise Scheduler"],
)


@enterprise_scheduler_router.get("/catalog")
async def catalog(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("enterprise_scheduler.read"))],
):
    return {"data": (await get_enterprise_scheduler_service().list_catalog()).unwrap()}


@enterprise_scheduler_router.get("/dependency-map")
async def dependency_map(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("enterprise_scheduler.read"))],
):
    return {"data": (await get_enterprise_scheduler_service().get_dependency_map()).unwrap()}


@enterprise_scheduler_router.post("/seed")
async def seed(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("enterprise_scheduler.write"))],
):
    return {"data": (await get_enterprise_scheduler_service().seed(tenant_id)).unwrap()}


@enterprise_scheduler_router.get("/dashboard")
async def dashboard(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("enterprise_scheduler.read"))],
):
    return {"data": (await get_enterprise_scheduler_service().get_dashboard(tenant_id)).unwrap()}


@enterprise_scheduler_router.get("/jobs")
async def list_jobs(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("enterprise_scheduler.read"))],
):
    return {"data": (await get_enterprise_scheduler_service().list_jobs(tenant_id)).unwrap()}


@enterprise_scheduler_router.post("/jobs")
async def create_job(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: CreateJobRequest,
    _user: Annotated[dict, Depends(require_permissions("enterprise_scheduler.write"))],
):
    return {"data": (await get_enterprise_scheduler_service().create_job(
        tenant_id,
        name=body.name,
        job_type=body.job_type,
        cron_expression=body.cron_expression,
        calendar_rule=body.calendar_rule,
        recurrence_rule=body.recurrence_rule,
        event_pattern=body.event_pattern,
        workflow_ref=body.workflow_ref,
        priority=body.priority,
        max_retries=body.max_retries,
        depends_on=body.depends_on,
        payload=body.payload,
    )).unwrap()}


@enterprise_scheduler_router.get("/jobs/{job_ref}")
async def get_job(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    job_ref: str,
    _user: Annotated[dict, Depends(require_permissions("enterprise_scheduler.read"))],
):
    result = await get_enterprise_scheduler_service().get_job(tenant_id, job_ref)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@enterprise_scheduler_router.post("/jobs/{job_ref}/trigger")
async def trigger_job(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    job_ref: str,
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("enterprise_scheduler.write"))],
):
    result = await get_enterprise_scheduler_service().trigger_job(tenant_id, job_ref, correlation_id=correlation_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@enterprise_scheduler_router.post("/jobs/{job_ref}/pause")
async def pause_job(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    job_ref: str,
    _user: Annotated[dict, Depends(require_permissions("enterprise_scheduler.write"))],
):
    result = await get_enterprise_scheduler_service().pause_job(tenant_id, job_ref)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@enterprise_scheduler_router.post("/jobs/{job_ref}/resume")
async def resume_job(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    job_ref: str,
    _user: Annotated[dict, Depends(require_permissions("enterprise_scheduler.write"))],
):
    result = await get_enterprise_scheduler_service().resume_job(tenant_id, job_ref)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@enterprise_scheduler_router.get("/history")
async def list_history(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("enterprise_scheduler.read"))],
):
    return {"data": (await get_enterprise_scheduler_service().list_history(tenant_id)).unwrap()}


@enterprise_scheduler_router.get("/jobs/{job_ref}/history")
async def job_history(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    job_ref: str,
    _user: Annotated[dict, Depends(require_permissions("enterprise_scheduler.read"))],
):
    return {"data": (await get_enterprise_scheduler_service().list_history(tenant_id, job_ref)).unwrap()}


@enterprise_scheduler_router.get("/dependencies")
async def list_dependencies(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("enterprise_scheduler.read"))],
):
    return {"data": (await get_enterprise_scheduler_service().list_dependencies(tenant_id)).unwrap()}


@enterprise_scheduler_router.post("/dependencies")
async def register_dependency(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: RegisterDependencyRequest,
    _user: Annotated[dict, Depends(require_permissions("enterprise_scheduler.write"))],
):
    result = await get_enterprise_scheduler_service().register_dependency(
        tenant_id,
        job_ref=body.job_ref,
        depends_on_job_ref=body.depends_on_job_ref,
        required_status=body.required_status,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@enterprise_scheduler_router.get("/monitoring")
async def monitoring(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("enterprise_scheduler.read"))],
):
    return {"data": (await get_enterprise_scheduler_service().get_monitoring(tenant_id)).unwrap()}
