"""Enterprise Financial Workflow API routes."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from contexts.financial_kernel.container import get_financial_workflow_service
from contexts.financial_kernel.presentation.financial_workflow_schemas import (
    EscalateWorkflowRequest,
    SignWorkflowRequest,
    StartFinancialWorkflowRequest,
    WorkflowActionRequest,
)
from contexts.identity.presentation.dependencies import (
    get_correlation_id,
    get_current_user,
    get_tenant_id,
    require_permissions,
)

financial_workflows_router = APIRouter(
    prefix="/financial-kernel/workflows",
    tags=["Financial Workflow"],
)


@financial_workflows_router.get("/types")
async def list_workflow_types(
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.workflows.read"))],
):
    return {"data": (await get_financial_workflow_service().list_workflow_types()).unwrap()}


@financial_workflows_router.post("", status_code=status.HTTP_201_CREATED)
async def start_financial_workflow(
    body: StartFinancialWorkflowRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    user: Annotated[dict, Depends(require_permissions("financial_kernel.workflows.write"))],
):
    key = body.idempotency_key or f"{body.source_context}:{body.source_document_id}:{body.workflow_type}"
    result = await get_financial_workflow_service().start_workflow(
        tenant_id=tenant_id,
        workflow_type=body.workflow_type,
        source_context=body.source_context,
        source_document_id=body.source_document_id,
        idempotency_key=key,
        assignee_id=body.assignee_id,
        started_by=user.get("sub") or "system",
        amount=body.amount,
        currency=body.currency,
        sla_hours=body.sla_hours,
        metadata=body.metadata,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@financial_workflows_router.get("")
async def list_financial_workflows(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.workflows.read"))],
    workflow_type: str | None = Query(default=None),
):
    result = await get_financial_workflow_service().list_workflows(tenant_id, workflow_type=workflow_type)
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@financial_workflows_router.post("/sla/auto-escalate")
async def auto_escalate_sla_breached(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.workflows.escalate"))],
):
    result = await get_financial_workflow_service().auto_escalate_sla_breached(
        tenant_id, correlation_id=correlation_id
    )
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@financial_workflows_router.get("/{workflow_id}")
async def get_financial_workflow(
    workflow_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.workflows.read"))],
):
    result = await get_financial_workflow_service().get_workflow(tenant_id, workflow_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@financial_workflows_router.get("/{workflow_id}/history")
async def get_workflow_history(
    workflow_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.workflows.read"))],
):
    result = await get_financial_workflow_service().get_history(tenant_id, workflow_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@financial_workflows_router.get("/{workflow_id}/ai-recommendation")
async def get_workflow_ai_recommendation(
    workflow_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.workflows.read"))],
):
    result = await get_financial_workflow_service().get_ai_recommendation(tenant_id, workflow_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@financial_workflows_router.post("/{workflow_id}/approve")
async def approve_financial_workflow(
    workflow_id: str,
    body: WorkflowActionRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    user: Annotated[dict, Depends(require_permissions("financial_kernel.workflows.approve"))],
):
    result = await get_financial_workflow_service().approve_workflow(
        tenant_id=tenant_id,
        workflow_id=workflow_id,
        actor_id=user.get("sub") or "system",
        comment=body.comment,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@financial_workflows_router.post("/{workflow_id}/reject")
async def reject_financial_workflow(
    workflow_id: str,
    body: WorkflowActionRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    user: Annotated[dict, Depends(require_permissions("financial_kernel.workflows.approve"))],
):
    result = await get_financial_workflow_service().reject_workflow(
        tenant_id=tenant_id,
        workflow_id=workflow_id,
        actor_id=user.get("sub") or "system",
        comment=body.comment,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@financial_workflows_router.post("/{workflow_id}/escalate")
async def escalate_financial_workflow(
    workflow_id: str,
    body: EscalateWorkflowRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    user: Annotated[dict, Depends(require_permissions("financial_kernel.workflows.escalate"))],
):
    result = await get_financial_workflow_service().escalate_workflow(
        tenant_id=tenant_id,
        workflow_id=workflow_id,
        actor_id=user.get("sub") or "system",
        escalated_to=body.escalated_to,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@financial_workflows_router.post("/{workflow_id}/sign")
async def sign_financial_workflow(
    workflow_id: str,
    body: SignWorkflowRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    user: Annotated[dict, Depends(require_permissions("financial_kernel.workflows.sign"))],
):
    signer_id = body.signer_id or user.get("sub") or "system"
    result = await get_financial_workflow_service().sign_workflow(
        tenant_id=tenant_id,
        workflow_id=workflow_id,
        signer_id=signer_id,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@financial_workflows_router.post("/{workflow_id}/complete")
async def complete_financial_workflow(
    workflow_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[dict, Depends(require_permissions("financial_kernel.workflows.approve"))],
):
    result = await get_financial_workflow_service().complete_workflow(
        tenant_id=tenant_id,
        workflow_id=workflow_id,
        actor_id=user.get("sub") or "system",
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}
