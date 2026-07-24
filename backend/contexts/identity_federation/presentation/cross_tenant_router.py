"""Cross-Tenant Trust & Delegation REST surface (P200-B8)."""
from __future__ import annotations

from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException

from contexts.identity.presentation.dependencies import get_tenant_id, require_permissions
from contexts.identity_federation.application.commands.cross_tenant_commands import (
    ActivateExternalIdentityCommand,
    ActivateTenantTrustCommand,
    ApproveDelegationCommand,
    ApproveTenantTrustCommand,
    AssignPartnerAccessCommand,
    CreateDelegationCommand,
    InviteExternalIdentityCommand,
    RegisterPartnerCommand,
    RemoveExternalIdentityCommand,
    RequestTenantTrustCommand,
    RevokeDelegationCommand,
    RevokeTenantTrustCommand,
    SuspendTenantTrustCommand,
    handle_activate_external_identity,
    handle_activate_tenant_trust,
    handle_approve_delegation,
    handle_approve_tenant_trust,
    handle_assign_partner_access,
    handle_create_delegation,
    handle_invite_external_identity,
    handle_register_partner,
    handle_remove_external_identity,
    handle_request_tenant_trust,
    handle_revoke_delegation,
    handle_revoke_tenant_trust,
    handle_suspend_tenant_trust,
)
from contexts.identity_federation.application.queries.cross_tenant_queries import (
    GetDelegationAuditQuery,
    GetDelegationsQuery,
    GetExternalIdentitiesQuery,
    GetPartnerAccessQuery,
    GetTenantTrustQuery,
    GetTrustHistoryQuery,
    handle_get_cross_tenant_surface,
    handle_get_delegation_audit,
    handle_get_delegations,
    handle_get_external_identities,
    handle_get_partner_access,
    handle_get_tenant_trust,
    handle_get_trust_history,
)
from contexts.identity_federation.container import (
    get_delegation_repository,
    get_external_identity_repository,
    get_partner_access_repository,
    get_tenant_federation_repository,
)

cross_tenant_router = APIRouter(prefix="/federation/cross-tenant", tags=["federation-cross-tenant"])


@cross_tenant_router.get(
    "/surface",
    dependencies=[Depends(require_permissions("federation.read"))],
)
async def surface() -> dict:
    return {"data": handle_get_cross_tenant_surface()}


@cross_tenant_router.post(
    "/trust/request",
    dependencies=[Depends(require_permissions("federation.write"))],
)
async def request_trust(
    body: dict[str, Any],
    tenant_id: Annotated[str, Depends(get_tenant_id)],
) -> dict:
    try:
        result = await handle_request_tenant_trust(
            RequestTenantTrustCommand(
                tenant_id=tenant_id,
                partner_tenant_id=str(body.get("partner_tenant_id") or ""),
                federation_ref=body.get("federation_ref"),
                federation_mode=str(body.get("federation_mode") or "partner"),
                agreement=dict(body.get("agreement") or {}),
                effective_until=body.get("effective_until"),
                assess_inputs=dict(body.get("assess_inputs") or {}),
                cross_tenant_enabled=bool(body.get("cross_tenant_enabled", True)),
            ),
            tenant_feds=get_tenant_federation_repository(),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"data": result}


@cross_tenant_router.post(
    "/trust/{federation_ref}/approve",
    dependencies=[Depends(require_permissions("federation.write"))],
)
async def approve_trust(
    federation_ref: str,
    body: dict[str, Any] | None = None,
    tenant_id: Annotated[str, Depends(get_tenant_id)] = "",
) -> dict:
    body = body or {}
    try:
        result = await handle_approve_tenant_trust(
            ApproveTenantTrustCommand(
                tenant_id=tenant_id,
                federation_ref=federation_ref,
                actor_id=body.get("actor_id"),
            ),
            tenant_feds=get_tenant_federation_repository(),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"data": result}


@cross_tenant_router.post(
    "/trust/{federation_ref}/activate",
    dependencies=[Depends(require_permissions("federation.write"))],
)
async def activate_trust(
    federation_ref: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
) -> dict:
    try:
        result = await handle_activate_tenant_trust(
            ActivateTenantTrustCommand(tenant_id=tenant_id, federation_ref=federation_ref),
            tenant_feds=get_tenant_federation_repository(),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"data": result}


@cross_tenant_router.post(
    "/trust/{federation_ref}/suspend",
    dependencies=[Depends(require_permissions("federation.write"))],
)
async def suspend_trust(
    federation_ref: str,
    body: dict[str, Any] | None = None,
    tenant_id: Annotated[str, Depends(get_tenant_id)] = "",
) -> dict:
    body = body or {}
    try:
        result = await handle_suspend_tenant_trust(
            SuspendTenantTrustCommand(
                tenant_id=tenant_id,
                federation_ref=federation_ref,
                reason=str(body.get("reason") or "suspended"),
            ),
            tenant_feds=get_tenant_federation_repository(),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"data": result}


@cross_tenant_router.post(
    "/trust/{federation_ref}/revoke",
    dependencies=[Depends(require_permissions("federation.write"))],
)
async def revoke_trust(
    federation_ref: str,
    body: dict[str, Any] | None = None,
    tenant_id: Annotated[str, Depends(get_tenant_id)] = "",
) -> dict:
    body = body or {}
    try:
        result = await handle_revoke_tenant_trust(
            RevokeTenantTrustCommand(
                tenant_id=tenant_id,
                federation_ref=federation_ref,
                reason=str(body.get("reason") or "revoked"),
            ),
            tenant_feds=get_tenant_federation_repository(),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"data": result}


@cross_tenant_router.get(
    "/trust/{federation_ref}",
    dependencies=[Depends(require_permissions("federation.read"))],
)
async def get_trust(
    federation_ref: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
) -> dict:
    try:
        result = await handle_get_tenant_trust(
            GetTenantTrustQuery(tenant_id=tenant_id, federation_ref=federation_ref),
            tenant_feds=get_tenant_federation_repository(),
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"data": result}


@cross_tenant_router.get(
    "/trust/{federation_ref}/history",
    dependencies=[Depends(require_permissions("federation.read"))],
)
async def get_trust_history(
    federation_ref: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
) -> dict:
    try:
        result = await handle_get_trust_history(
            GetTrustHistoryQuery(tenant_id=tenant_id, federation_ref=federation_ref),
            tenant_feds=get_tenant_federation_repository(),
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"data": result}


@cross_tenant_router.post(
    "/delegations",
    dependencies=[Depends(require_permissions("federation.write"))],
)
async def create_delegation(
    body: dict[str, Any],
    tenant_id: Annotated[str, Depends(get_tenant_id)],
) -> dict:
    try:
        result = await handle_create_delegation(
            CreateDelegationCommand(
                tenant_id=tenant_id,
                delegation_type=str(body.get("delegation_type") or "user"),
                owner_id=str(body.get("owner_id") or ""),
                delegate_id=str(body.get("delegate_id") or ""),
                scope=list(body.get("scope") or []),
                permissions=list(body.get("permissions") or []),
                conditions=dict(body.get("conditions") or {}),
                expires_at=body.get("expires_at"),
                delegation_ref=body.get("delegation_ref"),
                auto_approve=bool(body.get("auto_approve") or False),
            ),
            delegations=get_delegation_repository(),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"data": result}


@cross_tenant_router.post(
    "/delegations/{delegation_ref}/approve",
    dependencies=[Depends(require_permissions("federation.write"))],
)
async def approve_delegation(
    delegation_ref: str,
    body: dict[str, Any] | None = None,
    tenant_id: Annotated[str, Depends(get_tenant_id)] = "",
) -> dict:
    body = body or {}
    try:
        result = await handle_approve_delegation(
            ApproveDelegationCommand(
                tenant_id=tenant_id,
                delegation_ref=delegation_ref,
                actor_id=body.get("actor_id"),
                activate=bool(body.get("activate", True)),
            ),
            delegations=get_delegation_repository(),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"data": result}


@cross_tenant_router.post(
    "/delegations/{delegation_ref}/revoke",
    dependencies=[Depends(require_permissions("federation.write"))],
)
async def revoke_delegation(
    delegation_ref: str,
    body: dict[str, Any] | None = None,
    tenant_id: Annotated[str, Depends(get_tenant_id)] = "",
) -> dict:
    body = body or {}
    try:
        result = await handle_revoke_delegation(
            RevokeDelegationCommand(
                tenant_id=tenant_id,
                delegation_ref=delegation_ref,
                reason=str(body.get("reason") or "revoked"),
            ),
            delegations=get_delegation_repository(),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"data": result}


@cross_tenant_router.get(
    "/delegations",
    dependencies=[Depends(require_permissions("federation.read"))],
)
async def list_delegations(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    limit: int = 50,
) -> dict:
    result = await handle_get_delegations(
        GetDelegationsQuery(tenant_id=tenant_id, limit=limit),
        delegations=get_delegation_repository(),
    )
    return {"data": result}


@cross_tenant_router.get(
    "/delegations/{delegation_ref}/audit",
    dependencies=[Depends(require_permissions("federation.read"))],
)
async def delegation_audit(
    delegation_ref: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
) -> dict:
    try:
        result = await handle_get_delegation_audit(
            GetDelegationAuditQuery(tenant_id=tenant_id, delegation_ref=delegation_ref),
            delegations=get_delegation_repository(),
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"data": result}


@cross_tenant_router.post(
    "/partners",
    dependencies=[Depends(require_permissions("federation.write"))],
)
async def register_partner(
    body: dict[str, Any],
    tenant_id: Annotated[str, Depends(get_tenant_id)],
) -> dict:
    try:
        result = await handle_register_partner(
            RegisterPartnerCommand(
                tenant_id=tenant_id,
                partner_kind=str(body.get("partner_kind") or "partner"),
                organization_name=str(body.get("organization_name") or ""),
                partner_tenant_id=body.get("partner_tenant_id"),
                partner_ref=body.get("partner_ref"),
                expires_at=body.get("expires_at"),
            ),
            partners=get_partner_access_repository(),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"data": result}


@cross_tenant_router.post(
    "/partners/{partner_ref}/assign-access",
    dependencies=[Depends(require_permissions("federation.write"))],
)
async def assign_partner_access(
    partner_ref: str,
    body: dict[str, Any],
    tenant_id: Annotated[str, Depends(get_tenant_id)],
) -> dict:
    try:
        result = await handle_assign_partner_access(
            AssignPartnerAccessCommand(
                tenant_id=tenant_id,
                partner_ref=partner_ref,
                scopes=list(body.get("scopes") or []),
                policy_ref=body.get("policy_ref"),
            ),
            partners=get_partner_access_repository(),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"data": result}


@cross_tenant_router.get(
    "/partners",
    dependencies=[Depends(require_permissions("federation.read"))],
)
async def list_partners(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    limit: int = 50,
) -> dict:
    result = await handle_get_partner_access(
        GetPartnerAccessQuery(tenant_id=tenant_id, limit=limit),
        partners=get_partner_access_repository(),
    )
    return {"data": result}


@cross_tenant_router.post(
    "/external/invite",
    dependencies=[Depends(require_permissions("federation.write"))],
)
async def invite_external(
    body: dict[str, Any],
    tenant_id: Annotated[str, Depends(get_tenant_id)],
) -> dict:
    try:
        result = await handle_invite_external_identity(
            InviteExternalIdentityCommand(
                tenant_id=tenant_id,
                email=str(body.get("email") or ""),
                identity_kind=str(body.get("identity_kind") or "guest"),
                sponsor_id=body.get("sponsor_id"),
                access_scopes=list(body.get("access_scopes") or []),
                expires_at=body.get("expires_at"),
                external_ref=body.get("external_ref"),
            ),
            externals=get_external_identity_repository(),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"data": result}


@cross_tenant_router.post(
    "/external/{external_ref}/activate",
    dependencies=[Depends(require_permissions("federation.write"))],
)
async def activate_external(
    external_ref: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
) -> dict:
    try:
        result = await handle_activate_external_identity(
            ActivateExternalIdentityCommand(tenant_id=tenant_id, external_ref=external_ref),
            externals=get_external_identity_repository(),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"data": result}


@cross_tenant_router.post(
    "/external/{external_ref}/remove",
    dependencies=[Depends(require_permissions("federation.write"))],
)
async def remove_external(
    external_ref: str,
    body: dict[str, Any] | None = None,
    tenant_id: Annotated[str, Depends(get_tenant_id)] = "",
) -> dict:
    body = body or {}
    try:
        result = await handle_remove_external_identity(
            RemoveExternalIdentityCommand(
                tenant_id=tenant_id,
                external_ref=external_ref,
                reason=str(body.get("reason") or "removed"),
            ),
            externals=get_external_identity_repository(),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"data": result}


@cross_tenant_router.get(
    "/external",
    dependencies=[Depends(require_permissions("federation.read"))],
)
async def list_external(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    limit: int = 50,
) -> dict:
    result = await handle_get_external_identities(
        GetExternalIdentitiesQuery(tenant_id=tenant_id, limit=limit),
        externals=get_external_identity_repository(),
    )
    return {"data": result}
