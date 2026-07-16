"""Enterprise Identity Governance Platform API."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from contexts.identity.presentation.dependencies import get_correlation_id, get_tenant_id, require_permissions
from contexts.identity_governance.container import get_identity_governance_service
from contexts.identity_governance.presentation.schemas import (
    CertifyPrivilegesRequest,
    CompleteAccessReviewRequest,
    GrantEmergencyAccessRequest,
    GrantTemporaryAccessRequest,
    InitiateCertificationRequest,
    ScheduleAccessReviewRequest,
    SodCheckRequest,
    SubmitAccessRequest,
)

identity_governance_router = APIRouter(
    prefix="/identity-governance",
    tags=["Enterprise Identity Governance Platform"],
)


@identity_governance_router.get("/catalog")
async def catalog(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("identity_governance.read"))],
):
    return {"data": (await get_identity_governance_service().list_catalog()).unwrap()}


@identity_governance_router.get("/dependency-map")
async def dependency_map(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("identity_governance.read"))],
):
    return {"data": (await get_identity_governance_service().get_dependency_map()).unwrap()}


@identity_governance_router.post("/seed")
async def seed(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("identity_governance.write"))],
):
    return {"data": (await get_identity_governance_service().seed(tenant_id)).unwrap()}


@identity_governance_router.get("/dashboard")
async def dashboard(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("identity_governance.read"))],
):
    return {"data": (await get_identity_governance_service().get_dashboard(tenant_id)).unwrap()}


@identity_governance_router.post("/sod/check")
async def check_sod(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: SodCheckRequest,
    _user: Annotated[dict, Depends(require_permissions("identity_governance.read"))],
):
    return {"data": (await get_identity_governance_service().check_sod(
        tenant_id, existing_roles=body.existing_roles, requested_roles=body.requested_roles,
    )).unwrap()}


@identity_governance_router.get("/access-requests")
async def list_access_requests(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("identity_governance.read"))],
):
    return {"data": (await get_identity_governance_service().list_access_requests(tenant_id)).unwrap()}


@identity_governance_router.post("/access-requests", status_code=status.HTTP_201_CREATED)
async def submit_access_request(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: SubmitAccessRequest,
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    user: Annotated[dict, Depends(require_permissions("identity_governance.write"))],
):
    result = await get_identity_governance_service().submit_access_request(
        tenant_id,
        requester_id=user.get("sub", ""),
        target_user_id=body.target_user_id,
        requested_roles=body.requested_roles,
        justification=body.justification,
        existing_roles=body.existing_roles,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@identity_governance_router.post("/access-requests/{request_ref}/approve")
async def approve_access_request(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    request_ref: str,
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    user: Annotated[dict, Depends(require_permissions("identity_governance.approve"))],
):
    result = await get_identity_governance_service().approve_access_request(
        tenant_id, request_ref, approver_id=user.get("sub", ""), correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@identity_governance_router.post("/access-requests/{request_ref}/reject")
async def reject_access_request(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    request_ref: str,
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    user: Annotated[dict, Depends(require_permissions("identity_governance.approve"))],
):
    result = await get_identity_governance_service().reject_access_request(
        tenant_id, request_ref, approver_id=user.get("sub", ""), correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@identity_governance_router.get("/access-reviews")
async def list_access_reviews(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("identity_governance.read"))],
):
    return {"data": (await get_identity_governance_service().list_access_reviews(tenant_id)).unwrap()}


@identity_governance_router.post("/access-reviews", status_code=status.HTTP_201_CREATED)
async def schedule_access_review(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: ScheduleAccessReviewRequest,
    user: Annotated[dict, Depends(require_permissions("identity_governance.write"))],
):
    result = await get_identity_governance_service().schedule_access_review(
        tenant_id,
        title=body.title,
        reviewer_id=body.reviewer_id or user.get("sub", ""),
        scope_user_ids=body.scope_user_ids,
    )
    return {"data": result.unwrap()}


@identity_governance_router.post("/access-reviews/{review_ref}/complete")
async def complete_access_review(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    review_ref: str,
    body: CompleteAccessReviewRequest,
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    user: Annotated[dict, Depends(require_permissions("identity_governance.approve"))],
):
    result = await get_identity_governance_service().complete_access_review(
        tenant_id, review_ref, findings=body.findings,
        reviewer_id=user.get("sub", ""), correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@identity_governance_router.get("/certifications")
async def list_certifications(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("identity_governance.read"))],
):
    return {"data": (await get_identity_governance_service().list_certifications(tenant_id)).unwrap()}


@identity_governance_router.post("/certifications", status_code=status.HTTP_201_CREATED)
async def initiate_certification(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: InitiateCertificationRequest,
    _user: Annotated[dict, Depends(require_permissions("identity_governance.write"))],
):
    result = await get_identity_governance_service().initiate_certification(
        tenant_id, user_id=body.user_id, role_ids=body.role_ids,
    )
    return {"data": result.unwrap()}


@identity_governance_router.post("/certifications/{certification_ref}/certify")
async def certify_privileges(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    certification_ref: str,
    body: CertifyPrivilegesRequest,
    user: Annotated[dict, Depends(require_permissions("identity_governance.approve"))],
):
    result = await get_identity_governance_service().certify_privileges(
        tenant_id, certification_ref, certifier_id=user.get("sub", ""), notes=body.notes,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@identity_governance_router.post("/temporary-access", status_code=status.HTTP_201_CREATED)
async def grant_temporary_access(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: GrantTemporaryAccessRequest,
    user: Annotated[dict, Depends(require_permissions("identity_governance.write"))],
):
    result = await get_identity_governance_service().grant_temporary_access(
        tenant_id,
        user_id=body.user_id,
        roles=body.roles,
        granted_by=user.get("sub", ""),
        hours=body.hours,
        justification=body.justification,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@identity_governance_router.get("/temporary-access")
async def list_temporary_access(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("identity_governance.read"))],
):
    return {"data": (await get_identity_governance_service().list_temporary_access(tenant_id)).unwrap()}


@identity_governance_router.post("/emergency-access", status_code=status.HTTP_201_CREATED)
async def grant_emergency_access(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: GrantEmergencyAccessRequest,
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    user: Annotated[dict, Depends(require_permissions("identity_governance.approve"))],
):
    result = await get_identity_governance_service().grant_emergency_access(
        tenant_id,
        user_id=body.user_id,
        roles=body.roles,
        granted_by=user.get("sub", ""),
        incident_ref=body.incident_ref,
        justification=body.justification,
        correlation_id=correlation_id,
    )
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@identity_governance_router.get("/emergency-access")
async def list_emergency_access(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("identity_governance.read"))],
):
    return {"data": (await get_identity_governance_service().list_emergency_access(tenant_id)).unwrap()}


@identity_governance_router.get("/audit")
async def list_audit_log(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("identity_governance.read"))],
):
    return {"data": (await get_identity_governance_service().list_audit_log(tenant_id)).unwrap()}
