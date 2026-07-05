"""Treasury Workflow API routes."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from contexts.identity.presentation.dependencies import (
    get_tenant_id,
    require_permissions,
)
from contexts.treasury.container import get_treasury_workflow_service
from contexts.treasury.presentation.treasury_workflow_schemas import (
    ApproveStepRequest,
    CreateWorkflowDefinitionRequest,
    CreateWorkflowLimitRequest,
    CreateWorkflowRequest,
    DelegateRequest,
    EscalateRequest,
    RejectRequest,
)

treasury_workflow_router = APIRouter(
    prefix="/treasury/workflows",
    tags=["Treasury Workflow"],
)


@treasury_workflow_router.get("/catalog")
async def workflow_catalog(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.workflows.read"))],
):
    return {"data": (await get_treasury_workflow_service().list_catalog()).unwrap()}


@treasury_workflow_router.get("/states")
async def workflow_states(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.workflows.read"))],
):
    return {"data": (await get_treasury_workflow_service().list_workflow()).unwrap()}


@treasury_workflow_router.get("/dashboard")
async def workflow_dashboard(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.workflows.read"))],
):
    return {"data": (await get_treasury_workflow_service().get_dashboard(tenant_id)).unwrap()}


@treasury_workflow_router.get("/designer")
async def workflow_designer(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.workflows.design"))],
):
    return {"data": (await get_treasury_workflow_service().get_designer(tenant_id)).unwrap()}


@treasury_workflow_router.get("/definitions")
async def list_definitions(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.workflows.read"))],
):
    return {"data": (await get_treasury_workflow_service().list_definitions(tenant_id)).unwrap()}


@treasury_workflow_router.post("/definitions", status_code=status.HTTP_201_CREATED)
async def create_definition(
    body: CreateWorkflowDefinitionRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.workflows.design"))],
):
    result = await get_treasury_workflow_service().create_definition(
        tenant_id=tenant_id,
        name=body.name,
        workflow_type=body.workflow_type,
        approval_mode=body.approval_mode,
        steps=[s.model_dump() for s in body.steps],
        sla_hours=body.sla_hours,
        description=body.description,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@treasury_workflow_router.get("/limits")
async def list_limits(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.workflows.read"))],
):
    return {"data": (await get_treasury_workflow_service().list_limits(tenant_id)).unwrap()}


@treasury_workflow_router.post("/limits", status_code=status.HTTP_201_CREATED)
async def create_limit(
    body: CreateWorkflowLimitRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.workflows.design"))],
):
    result = await get_treasury_workflow_service().create_limit(
        tenant_id=tenant_id,
        workflow_type=body.workflow_type,
        name=body.name,
        max_amount=body.max_amount,
        currency=body.currency,
        approval_levels=body.approval_levels,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@treasury_workflow_router.get("/sla")
async def sla_monitoring(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.workflows.read"))],
):
    return {"data": (await get_treasury_workflow_service().get_sla_monitoring(tenant_id)).unwrap()}


@treasury_workflow_router.get("/requests")
async def list_requests(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.workflows.read"))],
):
    return {"data": (await get_treasury_workflow_service().list_requests(tenant_id)).unwrap()}


@treasury_workflow_router.post("/requests", status_code=status.HTTP_201_CREATED)
async def create_request(
    body: CreateWorkflowRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[dict, Depends(require_permissions("treasury.workflows.write"))],
):
    result = await get_treasury_workflow_service().create_request(
        tenant_id=tenant_id,
        workflow_type=body.workflow_type,
        amount=body.amount,
        currency=body.currency,
        subject_ref=body.subject_ref,
        subject_type=body.subject_type,
        requester_id=str(user.get("id", user.get("sub"))),
        title=body.title,
        description=body.description,
        definition_id=body.definition_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@treasury_workflow_router.get("/requests/{request_id}")
async def get_request(
    request_id: str,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.workflows.read"))],
):
    result = await get_treasury_workflow_service().get_request(request_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@treasury_workflow_router.post("/requests/{request_id}/submit")
async def submit_request(
    request_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[dict, Depends(require_permissions("treasury.workflows.write"))],
):
    result = await get_treasury_workflow_service().submit_request(
        request_id,
        tenant_id=tenant_id,
        actor_id=str(user.get("id", user.get("sub"))),
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@treasury_workflow_router.post("/requests/{request_id}/approve")
async def approve_step(
    request_id: str,
    body: ApproveStepRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[dict, Depends(require_permissions("treasury.workflows.approve"))],
):
    result = await get_treasury_workflow_service().approve_step(
        request_id,
        tenant_id=tenant_id,
        step_id=body.step_id,
        approver_id=str(user.get("id", user.get("sub"))),
        comment=body.comment,
        with_signature=body.with_signature,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@treasury_workflow_router.post("/requests/{request_id}/reject")
async def reject_request(
    request_id: str,
    body: RejectRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[dict, Depends(require_permissions("treasury.workflows.approve"))],
):
    result = await get_treasury_workflow_service().reject_request(
        request_id,
        tenant_id=tenant_id,
        approver_id=str(user.get("id", user.get("sub"))),
        comment=body.comment,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@treasury_workflow_router.post("/requests/{request_id}/delegate")
async def delegate_step(
    request_id: str,
    body: DelegateRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[dict, Depends(require_permissions("treasury.workflows.approve"))],
):
    result = await get_treasury_workflow_service().delegate_step(
        request_id,
        tenant_id=tenant_id,
        step_id=body.step_id,
        from_user=str(user.get("id", user.get("sub"))),
        to_user=body.to_user,
        reason=body.reason,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@treasury_workflow_router.post("/requests/{request_id}/escalate")
async def escalate_request(
    request_id: str,
    body: EscalateRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[dict, Depends(require_permissions("treasury.workflows.approve"))],
):
    result = await get_treasury_workflow_service().escalate_request(
        request_id,
        tenant_id=tenant_id,
        escalated_to=body.escalated_to,
        actor_id=str(user.get("id", user.get("sub"))),
        reason=body.reason,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@treasury_workflow_router.post("/requests/{request_id}/execute")
async def execute_request(
    request_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[dict, Depends(require_permissions("treasury.workflows.write"))],
):
    result = await get_treasury_workflow_service().execute_request(
        request_id,
        tenant_id=tenant_id,
        actor_id=str(user.get("id", user.get("sub"))),
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@treasury_workflow_router.get("/requests/{request_id}/audit")
async def request_audit_trail(
    request_id: str,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.workflows.read"))],
):
    return {"data": (await get_treasury_workflow_service().get_audit_trail(request_id)).unwrap()}
