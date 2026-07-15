"""Enterprise Identity Lifecycle Platform API."""
from __future__ import annotations

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from contexts.identity.presentation.dependencies import get_correlation_id, get_tenant_id, require_permissions
from contexts.identity_lifecycle.container import get_identity_lifecycle_service
from contexts.identity_lifecycle.presentation.schemas import (
    ConsentRequest,
    DeleteIdentityRequest,
    MergeIdentityRequest,
    ReasonRequest,
    RegisterLifecycleRequest,
    SplitIdentityRequest,
    VerificationRequest,
)

identity_lifecycle_router = APIRouter(
    prefix="/identity-lifecycle",
    tags=["Identity Lifecycle"],
)


@identity_lifecycle_router.get("/catalog")
async def catalog(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("identity_lifecycle.read"))],
):
    return {"data": (await get_identity_lifecycle_service().list_catalog()).unwrap()}


@identity_lifecycle_router.post("/seed")
async def seed(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("identity_lifecycle.write"))],
):
    return {"data": (await get_identity_lifecycle_service().seed(tenant_id)).unwrap()}


@identity_lifecycle_router.get("/dashboard")
async def dashboard(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("identity_lifecycle.read"))],
):
    return {"data": (await get_identity_lifecycle_service().get_dashboard(tenant_id)).unwrap()}


@identity_lifecycle_router.get("/cases")
async def list_cases(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("identity_lifecycle.read"))],
):
    return {"data": (await get_identity_lifecycle_service().list_cases(tenant_id)).unwrap()}


@identity_lifecycle_router.post("/cases")
async def register_case(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: RegisterLifecycleRequest,
    user: Annotated[dict, Depends(require_permissions("identity_lifecycle.cases.write"))],
    correlation_id: Annotated[str, Depends(get_correlation_id)] = "",
):
    correlation_id = correlation_id or str(uuid.uuid4())
    result = await get_identity_lifecycle_service().register(
        tenant_id,
        email=body.email,
        display_name=body.display_name,
        identity_ref=body.identity_ref,
        user_id=body.user_id,
        correlation_id=correlation_id,
        actor_id=str(user.get("id", "")),
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@identity_lifecycle_router.get("/cases/{case_ref}")
async def get_case(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    case_ref: str,
    _user: Annotated[dict, Depends(require_permissions("identity_lifecycle.read"))],
):
    result = await get_identity_lifecycle_service().get_case(tenant_id, case_ref)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@identity_lifecycle_router.post("/cases/{case_ref}/invite")
async def invite_case(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    case_ref: str,
    user: Annotated[dict, Depends(require_permissions("identity_lifecycle.cases.write"))],
    correlation_id: Annotated[str, Depends(get_correlation_id)] = "",
):
    correlation_id = correlation_id or str(uuid.uuid4())
    result = await get_identity_lifecycle_service().invite(
        tenant_id,
        case_ref,
        correlation_id=correlation_id,
        actor_id=str(user.get("id", "")),
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@identity_lifecycle_router.post("/cases/{case_ref}/verify")
async def verify_case(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    case_ref: str,
    body: VerificationRequest,
    user: Annotated[dict, Depends(require_permissions("identity_lifecycle.verify.execute"))],
    correlation_id: Annotated[str, Depends(get_correlation_id)] = "",
):
    correlation_id = correlation_id or str(uuid.uuid4())
    result = await get_identity_lifecycle_service().run_verification(
        tenant_id,
        case_ref,
        body.verification_type,
        correlation_id=correlation_id,
        actor_id=str(user.get("id", "")),
        payload=body.payload,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@identity_lifecycle_router.post("/cases/{case_ref}/activate")
async def activate_case(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    case_ref: str,
    user: Annotated[dict, Depends(require_permissions("identity_lifecycle.cases.write"))],
    correlation_id: Annotated[str, Depends(get_correlation_id)] = "",
):
    correlation_id = correlation_id or str(uuid.uuid4())
    result = await get_identity_lifecycle_service().activate(
        tenant_id,
        case_ref,
        correlation_id=correlation_id,
        actor_id=str(user.get("id", "")),
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@identity_lifecycle_router.post("/cases/{case_ref}/suspend")
async def suspend_case(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    case_ref: str,
    body: ReasonRequest,
    user: Annotated[dict, Depends(require_permissions("identity_lifecycle.cases.write"))],
    correlation_id: Annotated[str, Depends(get_correlation_id)] = "",
):
    correlation_id = correlation_id or str(uuid.uuid4())
    result = await get_identity_lifecycle_service().suspend(
        tenant_id,
        case_ref,
        reason=body.reason,
        correlation_id=correlation_id,
        actor_id=str(user.get("id", "")),
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@identity_lifecycle_router.post("/cases/{case_ref}/disable")
async def disable_case(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    case_ref: str,
    body: ReasonRequest,
    user: Annotated[dict, Depends(require_permissions("identity_lifecycle.cases.write"))],
    correlation_id: Annotated[str, Depends(get_correlation_id)] = "",
):
    correlation_id = correlation_id or str(uuid.uuid4())
    result = await get_identity_lifecycle_service().temporary_disable(
        tenant_id,
        case_ref,
        reason=body.reason,
        correlation_id=correlation_id,
        actor_id=str(user.get("id", "")),
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@identity_lifecycle_router.post("/cases/{case_ref}/reactivate")
async def reactivate_case(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    case_ref: str,
    user: Annotated[dict, Depends(require_permissions("identity_lifecycle.cases.write"))],
    correlation_id: Annotated[str, Depends(get_correlation_id)] = "",
):
    correlation_id = correlation_id or str(uuid.uuid4())
    result = await get_identity_lifecycle_service().reactivate(
        tenant_id,
        case_ref,
        correlation_id=correlation_id,
        actor_id=str(user.get("id", "")),
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@identity_lifecycle_router.post("/cases/{case_ref}/merge")
async def merge_case(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    case_ref: str,
    body: MergeIdentityRequest,
    user: Annotated[dict, Depends(require_permissions("identity_lifecycle.merge.execute"))],
    correlation_id: Annotated[str, Depends(get_correlation_id)] = "",
):
    correlation_id = correlation_id or str(uuid.uuid4())
    result = await get_identity_lifecycle_service().merge_identities(
        tenant_id,
        case_ref,
        target_case_ref=body.target_case_ref,
        correlation_id=correlation_id,
        actor_id=str(user.get("id", "")),
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@identity_lifecycle_router.post("/cases/{case_ref}/split")
async def split_case(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    case_ref: str,
    body: SplitIdentityRequest,
    user: Annotated[dict, Depends(require_permissions("identity_lifecycle.merge.execute"))],
    correlation_id: Annotated[str, Depends(get_correlation_id)] = "",
):
    correlation_id = correlation_id or str(uuid.uuid4())
    result = await get_identity_lifecycle_service().split_identity(
        tenant_id,
        case_ref,
        new_identity_ref=body.new_identity_ref,
        correlation_id=correlation_id,
        actor_id=str(user.get("id", "")),
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@identity_lifecycle_router.post("/cases/{case_ref}/archive")
async def archive_case(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    case_ref: str,
    body: ReasonRequest,
    user: Annotated[dict, Depends(require_permissions("identity_lifecycle.cases.write"))],
    correlation_id: Annotated[str, Depends(get_correlation_id)] = "",
):
    correlation_id = correlation_id or str(uuid.uuid4())
    result = await get_identity_lifecycle_service().archive(
        tenant_id,
        case_ref,
        reason=body.reason,
        correlation_id=correlation_id,
        actor_id=str(user.get("id", "")),
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@identity_lifecycle_router.post("/cases/{case_ref}/recover")
async def recover_case(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    case_ref: str,
    user: Annotated[dict, Depends(require_permissions("identity_lifecycle.recovery.execute"))],
    correlation_id: Annotated[str, Depends(get_correlation_id)] = "",
):
    correlation_id = correlation_id or str(uuid.uuid4())
    result = await get_identity_lifecycle_service().recover(
        tenant_id,
        case_ref,
        correlation_id=correlation_id,
        actor_id=str(user.get("id", "")),
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@identity_lifecycle_router.post("/cases/{case_ref}/delete")
async def delete_case(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    case_ref: str,
    body: DeleteIdentityRequest,
    user: Annotated[dict, Depends(require_permissions("identity_lifecycle.delete.execute"))],
    correlation_id: Annotated[str, Depends(get_correlation_id)] = "",
):
    correlation_id = correlation_id or str(uuid.uuid4())
    result = await get_identity_lifecycle_service().delete_identity(
        tenant_id,
        case_ref,
        deletion_type=body.deletion_type,
        reason=body.reason,
        correlation_id=correlation_id,
        actor_id=str(user.get("id", "")),
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@identity_lifecycle_router.post("/cases/{case_ref}/consent")
async def record_consent(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    case_ref: str,
    body: ConsentRequest,
    user: Annotated[dict, Depends(require_permissions("identity_lifecycle.consent.write"))],
    correlation_id: Annotated[str, Depends(get_correlation_id)] = "",
):
    correlation_id = correlation_id or str(uuid.uuid4())
    result = await get_identity_lifecycle_service().record_consent(
        tenant_id,
        case_ref,
        purpose=body.purpose,
        granted=body.granted,
        version=body.version,
        correlation_id=correlation_id,
        actor_id=str(user.get("id", "")),
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@identity_lifecycle_router.get("/cases/{case_ref}/audit")
async def list_audit(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    case_ref: str,
    _user: Annotated[dict, Depends(require_permissions("identity_lifecycle.audit.read"))],
):
    return {"data": (await get_identity_lifecycle_service().list_audit(tenant_id, case_ref)).unwrap()}


@identity_lifecycle_router.get("/cases/{case_ref}/workflow")
async def get_workflow(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    case_ref: str,
    _user: Annotated[dict, Depends(require_permissions("identity_lifecycle.read"))],
):
    result = await get_identity_lifecycle_service().get_workflow(tenant_id, case_ref)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@identity_lifecycle_router.get("/cases/{case_ref}/assistant")
async def assistant_recommend(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    case_ref: str,
    _user: Annotated[dict, Depends(require_permissions("identity_lifecycle.assistant.read"))],
):
    result = await get_identity_lifecycle_service().assistant_recommend(tenant_id, case_ref)
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}
