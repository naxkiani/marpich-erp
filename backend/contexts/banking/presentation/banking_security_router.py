"""Banking Security Platform API routes."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from contexts.banking.container import get_banking_security_platform_service
from contexts.banking.presentation.banking_security_schemas import (
    ActivateFreezeRequest,
    ApproveRequestRequest,
    AssessRiskRequest,
    AuthorizeActionRequest,
    CheckLimitsRequest,
    EncryptDataRequest,
    EvaluateAccessRequest,
    MonitorTransactionRequest,
    RegisterDeviceRequest,
    RegisterSessionRequest,
    ReleaseFreezeRequest,
    SessionHeartbeatRequest,
    SignPayloadRequest,
    SubmitApprovalRequest,
    VerifyDeviceRequest,
)
from contexts.identity.presentation.dependencies import (
    get_tenant_id,
    require_permissions,
)

banking_security_router = APIRouter(
    prefix="/banking/security",
    tags=["Banking Security Platform"],
)


def _raise(result) -> None:
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)


@banking_security_router.get("/catalog")
async def security_catalog(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.security.read"))],
):
    return {"data": (await get_banking_security_platform_service().list_catalog()).unwrap()}


@banking_security_router.get("/policy-keys")
async def security_policy_keys(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.security.read"))],
):
    return {"data": (await get_banking_security_platform_service().list_policy_keys()).unwrap()}


@banking_security_router.get("/dashboard")
async def security_dashboard(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.security.read"))],
):
    return {"data": (await get_banking_security_platform_service().get_dashboard(tenant_id)).unwrap()}


@banking_security_router.post("/access/evaluate")
async def evaluate_access(
    body: EvaluateAccessRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.security.read"))],
):
    result = await get_banking_security_platform_service().evaluate_access(
        tenant_id=tenant_id, **body.model_dump()
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_security_router.post("/limits/check")
async def check_limits(
    body: CheckLimitsRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.security.read"))],
):
    result = await get_banking_security_platform_service().check_limits(
        tenant_id=tenant_id, **body.model_dump()
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_security_router.post("/devices/register", status_code=status.HTTP_201_CREATED)
async def register_device(
    body: RegisterDeviceRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.security.write"))],
):
    result = await get_banking_security_platform_service().register_device(
        tenant_id=tenant_id, **body.model_dump()
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_security_router.post("/devices/verify")
async def verify_device(
    body: VerifyDeviceRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.security.write"))],
):
    result = await get_banking_security_platform_service().verify_device(
        tenant_id=tenant_id, **body.model_dump()
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_security_router.post("/sessions/register", status_code=status.HTTP_201_CREATED)
async def register_session(
    body: RegisterSessionRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.security.write"))],
):
    result = await get_banking_security_platform_service().register_session(
        tenant_id=tenant_id, **body.model_dump()
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_security_router.post("/sessions/{session_id}/heartbeat")
async def session_heartbeat(
    session_id: str,
    body: SessionHeartbeatRequest,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.security.write"))],
):
    result = await get_banking_security_platform_service().session_heartbeat(
        session_id=session_id, **body.model_dump()
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_security_router.post("/transactions/monitor")
async def monitor_transaction(
    body: MonitorTransactionRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.security.write"))],
):
    result = await get_banking_security_platform_service().monitor_transaction(
        tenant_id=tenant_id, **body.model_dump()
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_security_router.post("/risk/assess")
async def assess_risk(
    body: AssessRiskRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.security.read"))],
):
    result = await get_banking_security_platform_service().assess_risk_auth(
        tenant_id=tenant_id, **body.model_dump()
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_security_router.post("/approvals", status_code=status.HTTP_201_CREATED)
async def submit_approval(
    body: SubmitApprovalRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.security.write"))],
):
    result = await get_banking_security_platform_service().submit_approval(
        tenant_id=tenant_id, **body.model_dump()
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_security_router.post("/approvals/{request_id}/approve")
async def approve_request(
    request_id: str,
    body: ApproveRequestRequest,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.security.approve"))],
):
    result = await get_banking_security_platform_service().approve_request(
        request_id=request_id, approver_id=body.approver_id
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_security_router.post("/authorize")
async def authorize_critical_action(
    body: AuthorizeActionRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.security.write"))],
):
    result = await get_banking_security_platform_service().authorize_critical_action(
        tenant_id=tenant_id, **body.model_dump()
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_security_router.post("/sign")
async def sign_payload(
    body: SignPayloadRequest,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.security.write"))],
):
    result = await get_banking_security_platform_service().sign_payload(**body.model_dump())
    _raise(result)
    return {"data": result.unwrap()}


@banking_security_router.post("/encrypt")
async def encrypt_data(
    body: EncryptDataRequest,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.security.write"))],
):
    result = await get_banking_security_platform_service().encrypt_data(payload=body.payload)
    _raise(result)
    return {"data": result.unwrap()}


@banking_security_router.post("/freeze", status_code=status.HTTP_201_CREATED)
async def activate_freeze(
    body: ActivateFreezeRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.security.admin"))],
):
    result = await get_banking_security_platform_service().activate_freeze(
        tenant_id=tenant_id, **body.model_dump()
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_security_router.post("/freeze/release")
async def release_freeze(
    body: ReleaseFreezeRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.security.admin"))],
):
    result = await get_banking_security_platform_service().release_freeze(
        tenant_id=tenant_id, released_by=body.released_by
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_security_router.get("/audit")
async def audit_trail(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.security.read"))],
):
    return {"data": (await get_banking_security_platform_service().get_audit_trail(tenant_id)).unwrap()}


@banking_security_router.get("/audit/verify")
async def verify_audit_trail(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.security.read"))],
):
    result = await get_banking_security_platform_service().verify_audit_trail(tenant_id)
    _raise(result)
    return {"data": result.unwrap()}
