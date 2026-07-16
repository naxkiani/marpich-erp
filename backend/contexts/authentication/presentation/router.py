"""Authentication platform API."""
from __future__ import annotations

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status

from contexts.authentication.container import get_authentication_service
from contexts.authentication.presentation.schemas import (
    OidcAuthorizeRequest,
    OidcCallbackRequest,
    PasskeyLoginBeginRequest,
    PasskeyLoginVerifyRequest,
    PasskeyRegistrationVerifyRequest,
    RegisterOidcProviderRequest,
)
from contexts.identity.presentation.dependencies import (
    get_client_ip,
    get_correlation_id,
    get_current_user,
    get_tenant_id,
    require_permissions,
)

authentication_router = APIRouter(
    prefix="/authentication",
    tags=["Authentication"],
)


@authentication_router.get("/catalog")
async def catalog(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("authentication.read"))],
):
    return {"data": (await get_authentication_service().list_catalog()).unwrap()}


@authentication_router.post("/seed")
async def seed(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("authentication.write"))],
):
    return {"data": (await get_authentication_service().seed(tenant_id)).unwrap()}


@authentication_router.get("/dashboard")
async def dashboard(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("authentication.read"))],
):
    return {"data": (await get_authentication_service().get_dashboard(tenant_id)).unwrap()}


@authentication_router.get("/webauthn/credentials")
async def list_passkeys(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[dict, Depends(require_permissions("authentication.webauthn.manage"))],
):
    return {
        "data": (
            await get_authentication_service().list_passkeys(tenant_id, user["sub"])
        ).unwrap()
    }


@authentication_router.post("/webauthn/register/options")
async def passkey_register_options(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[dict, Depends(require_permissions("authentication.webauthn.manage"))],
):
    result = await get_authentication_service().begin_passkey_registration(
        tenant_id,
        user["sub"],
        email=user.get("email", ""),
        display_name=user.get("display_name", user.get("email", "User")),
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@authentication_router.post("/webauthn/register/verify")
async def passkey_register_verify(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: PasskeyRegistrationVerifyRequest,
    user: Annotated[dict, Depends(require_permissions("authentication.webauthn.manage"))],
):
    result = await get_authentication_service().complete_passkey_registration(
        tenant_id,
        user["sub"],
        challenge_id=body.challenge_id,
        credential=body.credential,
        nickname=body.nickname,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@authentication_router.post("/webauthn/login/options")
async def passkey_login_options(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: PasskeyLoginBeginRequest,
):
    result = await get_authentication_service().begin_passkey_login(tenant_id, body.email)
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@authentication_router.post("/webauthn/login/verify")
async def passkey_login_verify(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: PasskeyLoginVerifyRequest,
    request: Request,
    correlation_id: Annotated[str, Depends(get_correlation_id)],
):
    result = await get_authentication_service().complete_passkey_login(
        tenant_id,
        challenge_id=body.challenge_id,
        credential=body.credential,
        correlation_id=correlation_id,
        ip_address=get_client_ip(request),
        user_agent=request.headers.get("user-agent"),
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"tenant_id": tenant_id, "correlation_id": correlation_id}}


@authentication_router.delete("/webauthn/credentials/{credential_ref}")
async def revoke_passkey(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    credential_ref: str,
    user: Annotated[dict, Depends(require_permissions("authentication.webauthn.manage"))],
):
    result = await get_authentication_service().revoke_passkey(tenant_id, user["sub"], credential_ref)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@authentication_router.get("/federation/providers")
async def list_oidc_providers(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("authentication.read"))],
):
    return {"data": (await get_authentication_service().list_oidc_providers(tenant_id)).unwrap()}


@authentication_router.post("/federation/providers")
async def register_oidc_provider(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: RegisterOidcProviderRequest,
    _user: Annotated[dict, Depends(require_permissions("authentication.federation.write"))],
):
    result = await get_authentication_service().register_oidc_provider(
        tenant_id,
        name=body.name,
        issuer_url=body.issuer_url,
        client_id=body.client_id,
        client_secret=body.client_secret,
        redirect_uri=body.redirect_uri,
        scopes=body.scopes,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@authentication_router.post("/federation/oidc/authorize")
async def oidc_authorize(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: OidcAuthorizeRequest,
):
    result = await get_authentication_service().begin_oidc_authorize(tenant_id, body.provider_ref)
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@authentication_router.post("/federation/oidc/callback")
async def oidc_callback(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: OidcCallbackRequest,
    request: Request,
    correlation_id: Annotated[str, Depends(get_correlation_id)] = "",
):
    correlation_id = correlation_id or str(uuid.uuid4())
    result = await get_authentication_service().complete_oidc_callback(
        tenant_id,
        code=body.code,
        state=body.state,
        correlation_id=correlation_id,
        ip_address=get_client_ip(request),
        user_agent=request.headers.get("user-agent"),
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"tenant_id": tenant_id, "correlation_id": correlation_id}}
