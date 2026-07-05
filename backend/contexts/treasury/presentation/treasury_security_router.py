"""Treasury Security API routes."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from contexts.identity.presentation.dependencies import (
    get_tenant_id,
    require_permissions,
)
from contexts.treasury.container import get_treasury_security_service
from contexts.treasury.presentation.treasury_security_schemas import (
    ApproveOperationRequest,
    CreateAccessRuleRequest,
    CreateApprovalMatrixRequest,
    CreateSecurityOperationRequest,
    CreateSecurityPolicyRequest,
    CreateTransactionLimitRequest,
    EmergencyFreezeRequest,
    EvaluateAccessRequest,
    LockTransactionRequest,
    RejectOperationRequest,
)

treasury_security_router = APIRouter(
    prefix="/treasury/security",
    tags=["Treasury Security"],
)


@treasury_security_router.get("/catalog")
async def security_catalog(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.security.read"))],
):
    return {"data": (await get_treasury_security_service().list_catalog()).unwrap()}


@treasury_security_router.get("/dashboard")
async def security_dashboard(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.security.read"))],
):
    return {"data": (await get_treasury_security_service().get_dashboard(tenant_id)).unwrap()}


@treasury_security_router.get("/policies")
async def list_policies(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.security.read"))],
):
    return {"data": (await get_treasury_security_service().list_policies(tenant_id)).unwrap()}


@treasury_security_router.get("/policies/view")
async def policies_view(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.security.read"))],
):
    return {"data": (await get_treasury_security_service().get_policies_view(tenant_id)).unwrap()}


@treasury_security_router.post("/policies", status_code=status.HTTP_201_CREATED)
async def create_policy(
    body: CreateSecurityPolicyRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[dict, Depends(require_permissions("treasury.security.admin"))],
):
    result = await get_treasury_security_service().create_policy(
        tenant_id=tenant_id,
        name=body.name,
        policy_type=body.policy_type,
        rules=body.rules,
        description=body.description,
        actor_id=str(user.get("id", user.get("sub"))),
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@treasury_security_router.get("/limits")
async def list_limits(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.security.read"))],
):
    return {"data": (await get_treasury_security_service().list_limits(tenant_id)).unwrap()}


@treasury_security_router.post("/limits", status_code=status.HTTP_201_CREATED)
async def create_limit(
    body: CreateTransactionLimitRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[dict, Depends(require_permissions("treasury.security.admin"))],
):
    result = await get_treasury_security_service().create_limit(
        tenant_id=tenant_id,
        operation_type=body.operation_type,
        name=body.name,
        max_amount=body.max_amount,
        currency=body.currency,
        daily_limit=body.daily_limit,
        actor_id=str(user.get("id", user.get("sub"))),
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@treasury_security_router.get("/matrix")
async def list_matrix(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.security.read"))],
):
    return {"data": (await get_treasury_security_service().list_matrix(tenant_id)).unwrap()}


@treasury_security_router.post("/matrix", status_code=status.HTTP_201_CREATED)
async def create_matrix_entry(
    body: CreateApprovalMatrixRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[dict, Depends(require_permissions("treasury.security.admin"))],
):
    result = await get_treasury_security_service().create_matrix_entry(
        tenant_id=tenant_id,
        operation_type=body.operation_type,
        role=body.role,
        min_amount=body.min_amount,
        max_amount=body.max_amount,
        approval_level=body.approval_level,
        currency=body.currency,
        actor_id=str(user.get("id", user.get("sub"))),
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@treasury_security_router.get("/access-rules")
async def list_access_rules(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.security.read"))],
):
    return {"data": (await get_treasury_security_service().list_access_rules(tenant_id)).unwrap()}


@treasury_security_router.post("/access-rules", status_code=status.HTTP_201_CREATED)
async def create_access_rule(
    body: CreateAccessRuleRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[dict, Depends(require_permissions("treasury.security.admin"))],
):
    result = await get_treasury_security_service().create_access_rule(
        tenant_id=tenant_id,
        rule_type=body.rule_type,
        name=body.name,
        roles=body.roles,
        attributes=body.attributes,
        allowed_operations=body.allowed_operations,
        denied_operations=body.denied_operations,
        actor_id=str(user.get("id", user.get("sub"))),
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@treasury_security_router.post("/evaluate")
async def evaluate_access(
    body: EvaluateAccessRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[dict, Depends(require_permissions("treasury.security.read"))],
):
    result = await get_treasury_security_service().evaluate_access(
        tenant_id=tenant_id,
        maker_id=body.maker_id,
        checker_id=body.checker_id,
        roles=body.roles,
        attributes=body.attributes,
        operation_type=body.operation_type,
        amount=body.amount,
        risk_score=body.risk_score,
        device_verified=body.device_verified,
        actor_id=str(user.get("id", user.get("sub"))),
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@treasury_security_router.get("/operations")
async def list_operations(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.security.read"))],
):
    return {"data": (await get_treasury_security_service().list_operations(tenant_id)).unwrap()}


@treasury_security_router.post("/operations", status_code=status.HTTP_201_CREATED)
async def create_operation(
    body: CreateSecurityOperationRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[dict, Depends(require_permissions("treasury.security.write"))],
):
    result = await get_treasury_security_service().create_operation(
        tenant_id=tenant_id,
        operation_type=body.operation_type,
        subject_ref=body.subject_ref,
        amount=body.amount,
        currency=body.currency,
        maker_id=str(user.get("id", user.get("sub"))),
        roles=body.roles,
        attributes=body.attributes,
        risk_score=body.risk_score,
        device_verified=body.device_verified,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@treasury_security_router.get("/operations/{operation_id}")
async def get_operation(
    operation_id: str,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.security.read"))],
):
    result = await get_treasury_security_service().get_operation(operation_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@treasury_security_router.post("/operations/{operation_id}/submit")
async def submit_operation(
    operation_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[dict, Depends(require_permissions("treasury.security.write"))],
):
    result = await get_treasury_security_service().submit_operation(
        operation_id,
        tenant_id=tenant_id,
        actor_id=str(user.get("id", user.get("sub"))),
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@treasury_security_router.post("/operations/{operation_id}/approve")
async def approve_operation(
    operation_id: str,
    body: ApproveOperationRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[dict, Depends(require_permissions("treasury.security.approve"))],
):
    result = await get_treasury_security_service().approve_operation(
        operation_id,
        tenant_id=tenant_id,
        checker_id=str(user.get("id", user.get("sub"))),
        with_signature=body.with_signature,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@treasury_security_router.post("/operations/{operation_id}/reject")
async def reject_operation(
    operation_id: str,
    body: RejectOperationRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[dict, Depends(require_permissions("treasury.security.approve"))],
):
    result = await get_treasury_security_service().reject_operation(
        operation_id,
        tenant_id=tenant_id,
        checker_id=str(user.get("id", user.get("sub"))),
        reason=body.reason,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@treasury_security_router.get("/locks")
async def list_locks(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.security.read"))],
):
    return {"data": (await get_treasury_security_service().list_locks(tenant_id)).unwrap()}


@treasury_security_router.post("/locks", status_code=status.HTTP_201_CREATED)
async def lock_transaction(
    body: LockTransactionRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[dict, Depends(require_permissions("treasury.security.write"))],
):
    result = await get_treasury_security_service().lock_transaction(
        tenant_id=tenant_id,
        subject_ref=body.subject_ref,
        subject_type=body.subject_type,
        reason=body.reason,
        locked_by=str(user.get("id", user.get("sub"))),
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@treasury_security_router.post("/locks/{lock_id}/release")
async def release_lock(
    lock_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[dict, Depends(require_permissions("treasury.security.admin"))],
):
    result = await get_treasury_security_service().release_lock(
        lock_id,
        tenant_id=tenant_id,
        released_by=str(user.get("id", user.get("sub"))),
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@treasury_security_router.post("/freeze", status_code=status.HTTP_201_CREATED)
async def emergency_freeze(
    body: EmergencyFreezeRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[dict, Depends(require_permissions("treasury.security.admin"))],
):
    result = await get_treasury_security_service().emergency_freeze(
        tenant_id=tenant_id,
        reason=body.reason,
        locked_by=str(user.get("id", user.get("sub"))),
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@treasury_security_router.post("/freeze/{lock_id}/release")
async def release_emergency_freeze(
    lock_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[dict, Depends(require_permissions("treasury.security.admin"))],
):
    result = await get_treasury_security_service().release_emergency_freeze(
        lock_id,
        tenant_id=tenant_id,
        released_by=str(user.get("id", user.get("sub"))),
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@treasury_security_router.get("/audit")
async def audit_trail(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.security.audit"))],
    subject_ref: str | None = None,
):
    return {
        "data": (
            await get_treasury_security_service().get_audit_trail(
                tenant_id, subject_ref=subject_ref
            )
        ).unwrap()
    }


@treasury_security_router.get("/check-lock/{subject_ref}")
async def check_lock(
    subject_ref: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.security.read"))],
):
    return {
        "data": (
            await get_treasury_security_service().check_subject_locked(tenant_id, subject_ref)
        ).unwrap()
    }
