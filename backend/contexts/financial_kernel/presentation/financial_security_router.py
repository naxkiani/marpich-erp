"""Enterprise Financial Security API routes."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from contexts.financial_kernel.container import get_financial_security_service
from contexts.financial_kernel.presentation.financial_security_schemas import (
    CreateSecurityPolicyRequest,
    EvaluateAccessRequest,
    GuardedModificationRequest,
    LockTransactionRequest,
    PeriodCloseRequestBody,
    SubmitMakerCheckerRequest,
)
from contexts.identity.presentation.dependencies import (
    get_correlation_id,
    get_current_user,
    get_tenant_id,
    require_permissions,
)

financial_security_router = APIRouter(
    prefix="/financial-kernel/security",
    tags=["Financial Security"],
)


@financial_security_router.post("/maker-checker", status_code=status.HTTP_201_CREATED)
async def submit_maker_checker(
    body: SubmitMakerCheckerRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    user: Annotated[dict, Depends(require_permissions("financial_kernel.security.write"))],
):
    key = body.idempotency_key or f"{body.resource_type}:{body.resource_id}:{body.control_type}"
    result = await get_financial_security_service().submit_maker_checker(
        tenant_id=tenant_id,
        control_type=body.control_type,
        resource_type=body.resource_type,
        resource_id=body.resource_id,
        idempotency_key=key,
        maker_id=user.get("sub") or "system",
        payload=body.payload,
        checker_id=body.checker_id,
        second_approver_id=body.second_approver_id,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@financial_security_router.get("/maker-checker")
async def list_maker_checker_requests(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.security.read"))],
):
    result = await get_financial_security_service().list_maker_checker_requests(tenant_id)
    return {"data": result.unwrap()}


@financial_security_router.post("/maker-checker/{request_id}/approve")
async def approve_maker_checker(
    request_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    user: Annotated[dict, Depends(require_permissions("financial_kernel.security.approve"))],
):
    result = await get_financial_security_service().approve_maker_checker(
        tenant_id=tenant_id,
        request_id=request_id,
        approver_id=user.get("sub") or "checker",
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@financial_security_router.post("/maker-checker/{request_id}/reject")
async def reject_maker_checker(
    request_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    user: Annotated[dict, Depends(require_permissions("financial_kernel.security.approve"))],
):
    result = await get_financial_security_service().reject_maker_checker(
        tenant_id=tenant_id,
        request_id=request_id,
        actor_id=user.get("sub") or "checker",
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@financial_security_router.post("/locks", status_code=status.HTTP_201_CREATED)
async def lock_transaction(
    body: LockTransactionRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    user: Annotated[dict, Depends(require_permissions("financial_kernel.security.lock"))],
):
    result = await get_financial_security_service().lock_transaction(
        tenant_id=tenant_id,
        resource_type=body.resource_type,
        resource_id=body.resource_id,
        locked_by=user.get("sub") or "system",
        reason=body.reason,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@financial_security_router.post("/locks/{lock_id}/release")
async def release_transaction_lock(
    lock_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    user: Annotated[dict, Depends(require_permissions("financial_kernel.security.lock"))],
):
    result = await get_financial_security_service().release_lock(
        tenant_id=tenant_id,
        lock_id=lock_id,
        actor_id=user.get("sub") or "system",
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@financial_security_router.post("/period-close", status_code=status.HTTP_201_CREATED)
async def request_period_close(
    body: PeriodCloseRequestBody,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    user: Annotated[dict, Depends(require_permissions("financial_kernel.security.close"))],
):
    result = await get_financial_security_service().request_period_close(
        tenant_id=tenant_id,
        close_type=body.close_type,
        target_id=body.target_id,
        requester_id=user.get("sub") or "system",
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@financial_security_router.post("/period-close/{request_id}/approve")
async def approve_period_close(
    request_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    user: Annotated[dict, Depends(require_permissions("financial_kernel.security.approve"))],
):
    result = await get_financial_security_service().approve_period_close(
        tenant_id=tenant_id,
        request_id=request_id,
        approver_id=user.get("sub") or "approver",
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@financial_security_router.post("/policies", status_code=status.HTTP_201_CREATED)
async def create_security_policy(
    body: CreateSecurityPolicyRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    user: Annotated[dict, Depends(require_permissions("financial_kernel.security.admin"))],
):
    result = await get_financial_security_service().create_policy(
        tenant_id=tenant_id,
        name=body.name,
        policy_type=body.policy_type,
        resource_type=body.resource_type,
        rules=body.rules,
        actor_id=user.get("sub") or "admin",
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@financial_security_router.post("/policies/evaluate")
async def evaluate_access_policy(
    body: EvaluateAccessRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.security.read"))],
):
    return {"data": (await get_financial_security_service().evaluate_access(
        tenant_id=tenant_id,
        resource_type=body.resource_type,
        permission=body.permission,
        role=body.role,
        attributes=body.attributes,
    )).unwrap()}


@financial_security_router.get("/audit")
async def list_security_audit_trail(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.security.audit"))],
    resource_type: str | None = Query(default=None),
    resource_id: str | None = Query(default=None),
):
    result = await get_financial_security_service().list_audit_trail(
        tenant_id,
        resource_type=resource_type,
        resource_id=resource_id,
    )
    return {"data": result.unwrap()}


@financial_security_router.get("/audit/{audit_id}/verify-tamper")
async def verify_audit_tamper(
    audit_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.security.audit"))],
):
    result = await get_financial_security_service().verify_tamper(
        tenant_id=tenant_id,
        audit_id=audit_id,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@financial_security_router.post("/guarded-modification")
async def guarded_financial_modification(
    body: GuardedModificationRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    user: Annotated[dict, Depends(require_permissions("financial_kernel.security.write"))],
):
    result = await get_financial_security_service().guarded_modification(
        tenant_id=tenant_id,
        resource_type=body.resource_type,
        resource_id=body.resource_id,
        actor_id=user.get("sub") or "system",
        action=body.action,
        payload=body.payload,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}
