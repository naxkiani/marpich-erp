"""Registration & onboarding REST surface (P201-A)."""
from __future__ import annotations

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from contexts.identity.presentation.dependencies import (
    get_correlation_id,
    get_tenant_id,
    require_permissions,
)
from contexts.identity_lifecycle.container import get_registration_onboarding_service
from contexts.identity_lifecycle.presentation.schemas import (
    ApproveRegistrationRequest,
    DetectDuplicatesRequest,
    RegisterIdentityRequest,
    RejectRegistrationRequest,
)

registration_router = APIRouter(
    prefix="/identity-lifecycle",
    tags=["Identity Lifecycle Registration"],
)


@registration_router.get(
    "/eilmp/surface",
    dependencies=[Depends(require_permissions("identity_lifecycle.read"))],
)
async def eilmp_surface() -> dict:
    return {"data": get_registration_onboarding_service().surface()}


@registration_router.get(
    "/registration/catalog",
    dependencies=[Depends(require_permissions("identity_lifecycle.read"))],
)
async def registration_catalog() -> dict:
    from contexts.identity_lifecycle.domain.services import registration_onboarding_engine as eng

    return {"data": eng.catalog()}


@registration_router.post(
    "/registration/register",
    dependencies=[Depends(require_permissions("identity_lifecycle.cases.write"))],
)
async def register_identity(
    body: RegisterIdentityRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[dict, Depends(require_permissions("identity_lifecycle.cases.write"))],
    correlation_id: Annotated[str, Depends(get_correlation_id)] = "",
) -> dict:
    correlation_id = correlation_id or str(uuid.uuid4())
    result = await get_registration_onboarding_service().register_identity(
        tenant_id,
        email=body.email,
        display_name=body.display_name,
        identity_type=body.identity_type,
        channel=body.channel,
        source=body.source,
        method=body.method,
        national_id=body.national_id,
        employee_number=body.employee_number,
        phone=body.phone,
        organization_ref=body.organization_ref,
        approval_mode=body.approval_mode,
        zt_context=body.zt_context,
        metadata=body.metadata,
        correlation_id=correlation_id,
        actor_id=str(user.get("id", "")),
        auto_advance=body.auto_advance,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@registration_router.post(
    "/registration/{registration_ref}/validate",
    dependencies=[Depends(require_permissions("identity_lifecycle.cases.write"))],
)
async def validate_registration(
    registration_ref: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[dict, Depends(require_permissions("identity_lifecycle.cases.write"))],
    correlation_id: Annotated[str, Depends(get_correlation_id)] = "",
) -> dict:
    result = await get_registration_onboarding_service().validate_registration(
        tenant_id,
        registration_ref,
        correlation_id=correlation_id or str(uuid.uuid4()),
        actor_id=str(user.get("id", "")),
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@registration_router.post(
    "/registration/{registration_ref}/detect-duplicates",
    dependencies=[Depends(require_permissions("identity_lifecycle.read"))],
)
async def detect_duplicates(
    registration_ref: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: DetectDuplicatesRequest | None = None,
    correlation_id: Annotated[str, Depends(get_correlation_id)] = "",
) -> dict:
    body = body or DetectDuplicatesRequest()
    result = await get_registration_onboarding_service().detect_duplicates(
        tenant_id,
        registration_ref,
        threshold=body.threshold,
        correlation_id=correlation_id or str(uuid.uuid4()),
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@registration_router.post(
    "/registration/{registration_ref}/approve",
    dependencies=[Depends(require_permissions("identity_lifecycle.cases.write"))],
)
async def approve_registration(
    registration_ref: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[dict, Depends(require_permissions("identity_lifecycle.cases.write"))],
    body: ApproveRegistrationRequest | None = None,
    correlation_id: Annotated[str, Depends(get_correlation_id)] = "",
) -> dict:
    body = body or ApproveRegistrationRequest()
    result = await get_registration_onboarding_service().approve_registration(
        tenant_id,
        registration_ref,
        correlation_id=correlation_id or str(uuid.uuid4()),
        actor_id=str(user.get("id", "")),
        force=body.force,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@registration_router.post(
    "/registration/{registration_ref}/reject",
    dependencies=[Depends(require_permissions("identity_lifecycle.cases.write"))],
)
async def reject_registration(
    registration_ref: str,
    body: RejectRegistrationRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[dict, Depends(require_permissions("identity_lifecycle.cases.write"))],
    correlation_id: Annotated[str, Depends(get_correlation_id)] = "",
) -> dict:
    result = await get_registration_onboarding_service().reject_registration(
        tenant_id,
        registration_ref,
        reason=body.reason,
        correlation_id=correlation_id or str(uuid.uuid4()),
        actor_id=str(user.get("id", "")),
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@registration_router.post(
    "/registration/{registration_ref}/initialize-profile",
    dependencies=[Depends(require_permissions("identity_lifecycle.cases.write"))],
)
async def initialize_profile(
    registration_ref: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)] = "",
) -> dict:
    result = await get_registration_onboarding_service().initialize_profile(
        tenant_id,
        registration_ref,
        correlation_id=correlation_id or str(uuid.uuid4()),
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@registration_router.post(
    "/registration/{registration_ref}/start-onboarding",
    dependencies=[Depends(require_permissions("identity_lifecycle.cases.write"))],
)
async def start_onboarding(
    registration_ref: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)] = "",
) -> dict:
    result = await get_registration_onboarding_service().start_onboarding(
        tenant_id,
        registration_ref,
        correlation_id=correlation_id or str(uuid.uuid4()),
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@registration_router.post(
    "/registration/{registration_ref}/request-provisioning",
    dependencies=[Depends(require_permissions("identity_lifecycle.cases.write"))],
)
async def request_provisioning(
    registration_ref: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)] = "",
) -> dict:
    result = await get_registration_onboarding_service().request_provisioning(
        tenant_id,
        registration_ref,
        correlation_id=correlation_id or str(uuid.uuid4()),
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@registration_router.get(
    "/registration/{registration_ref}",
    dependencies=[Depends(require_permissions("identity_lifecycle.read"))],
)
async def get_registration(
    registration_ref: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
) -> dict:
    result = await get_registration_onboarding_service().get_registration(
        tenant_id, registration_ref
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@registration_router.get(
    "/registration/{registration_ref}/status",
    dependencies=[Depends(require_permissions("identity_lifecycle.read"))],
)
async def get_registration_status(
    registration_ref: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
) -> dict:
    result = await get_registration_onboarding_service().get_status(
        tenant_id, registration_ref
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}
