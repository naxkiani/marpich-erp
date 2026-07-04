"""Workflow FastAPI router."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from contexts.identity.presentation.dependencies import (
    get_correlation_id,
    get_current_user,
    get_tenant_id,
    require_permissions,
)
from contexts.workflow.container import get_workflow_service
from contexts.workflow.presentation.schemas import (
    CompleteTaskRequest,
    DelegateTaskRequest,
    DeployDefinitionRequest,
    StartInstanceRequest,
)

router = APIRouter(prefix="/workflow", tags=["Workflow"])


@router.post("/definitions", status_code=status.HTTP_201_CREATED)
async def deploy_definition(
    body: DeployDefinitionRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("workflow.definitions.write"))],
):
    result = await get_workflow_service().deploy_definition(
        tenant_id=tenant_id,
        key=body.key,
        name=body.name,
        steps=[s.model_dump() for s in body.steps],
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@router.get("/definitions")
async def list_definitions(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("workflow.definitions.read"))],
):
    result = await get_workflow_service().list_definitions(tenant_id)
    return {"data": result.unwrap()}


@router.post("/instances", status_code=status.HTTP_201_CREATED)
async def start_instance(
    body: StartInstanceRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    user: Annotated[dict, Depends(require_permissions("workflow.instances.write"))],
):
    result = await get_workflow_service().start_instance(
        tenant_id=tenant_id,
        correlation_id=correlation_id,
        definition_key=body.definition_key,
        context=body.context,
        assignees=body.assignees,
        started_by=user["sub"],
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.get("/instances/{instance_id}")
async def get_instance(
    instance_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("workflow.instances.read"))],
):
    result = await get_workflow_service().get_instance(tenant_id, instance_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@router.get("/tasks")
async def list_my_tasks(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[dict, Depends(get_current_user)],
):
    result = await get_workflow_service().list_tasks(tenant_id, user["sub"])
    return {"data": result.unwrap()}


@router.post("/tasks/{task_id}/complete")
async def complete_task(
    task_id: str,
    body: CompleteTaskRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    user: Annotated[dict, Depends(get_current_user)],
):
    result = await get_workflow_service().complete_task(
        tenant_id=tenant_id,
        correlation_id=correlation_id,
        task_id=task_id,
        outcome=body.outcome,
        comment=body.comment,
        completed_by=user["sub"],
    )
    if not result.succeeded:
        code = status.HTTP_403_FORBIDDEN if "forbidden" in (result.error or "") else status.HTTP_400_BAD_REQUEST
        raise HTTPException(code, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.post("/tasks/{task_id}/delegate")
async def delegate_task(
    task_id: str,
    body: DelegateTaskRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    user: Annotated[dict, Depends(get_current_user)],
):
    result = await get_workflow_service().delegate_task(
        tenant_id=tenant_id,
        correlation_id=correlation_id,
        task_id=task_id,
        to_user_id=body.to_user_id,
        delegated_by=user["sub"],
    )
    if not result.succeeded:
        code = status.HTTP_403_FORBIDDEN if "forbidden" in (result.error or "") else status.HTTP_400_BAD_REQUEST
        raise HTTPException(code, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}
