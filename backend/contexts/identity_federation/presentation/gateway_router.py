"""Enterprise Identity Federation Gateway — universal protocol endpoints."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import JSONResponse

from contexts.identity.presentation.dependencies import get_correlation_id, get_tenant_id
from contexts.identity_federation.container import get_identity_federation_service
from contexts.identity_federation.presentation.gateway_schemas import (
    FederationIntrospectRequest,
    FederationLoginRequest,
    FederationLogoutRequest,
    FederationProvisionRequest,
    FederationRevokeRequest,
    FederationSyncRequest,
    FederationTokenRequest,
    ProblemDetail,
    RegisterOAuthClientRequest,
)

federation_gateway_router = APIRouter(prefix="/federation", tags=["Federation Gateway"])
identity_gateway_router = APIRouter(prefix="/identity", tags=["Identity Gateway"])


def _problem(status_code: int, title: str, detail: str | None = None, error_code: str | None = None) -> JSONResponse:
    body = ProblemDetail(
        title=title,
        status=status_code,
        detail=detail,
        error_code=error_code,
    )
    return JSONResponse(status_code=status_code, content=body.model_dump(exclude_none=True), media_type="application/problem+json")


def _fail(result, *, instance: str = "") -> JSONResponse:
    code = result.error or "federation.errors.request_failed"
    return _problem(
        status.HTTP_400_BAD_REQUEST,
        title="Federation request failed",
        detail=code,
        error_code=code,
    )


@federation_gateway_router.post("/login")
async def federation_login(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: FederationLoginRequest,
    correlation_id: Annotated[str, Depends(get_correlation_id)],
):
    result = await get_identity_federation_service().federation_login(
        tenant_id,
        protocol=body.protocol,
        email=body.email,
        provider_ref=body.provider_ref,
        client_id=body.client_id,
        redirect_uri=body.redirect_uri,
        scope=body.scope,
        state=body.state,
        code_challenge=body.code_challenge,
        code_challenge_method=body.code_challenge_method,
        user_id=body.user_id,
        callback_code=body.callback_code,
        callback_state=body.callback_state,
        saml_response=body.saml_response,
        relay_state=body.relay_state,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        return _fail(result)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@federation_gateway_router.post("/logout")
async def federation_logout(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: FederationLogoutRequest,
    correlation_id: Annotated[str, Depends(get_correlation_id)],
):
    result = await get_identity_federation_service().federation_logout_gateway(
        tenant_id,
        session_ref=body.session_ref,
        id_token_hint=body.id_token_hint,
        post_logout_redirect_uri=body.post_logout_redirect_uri,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        return _fail(result)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@federation_gateway_router.post("/token")
async def federation_token(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: FederationTokenRequest,
    correlation_id: Annotated[str, Depends(get_correlation_id)],
):
    result = await get_identity_federation_service().federation_token(
        tenant_id,
        grant_type=body.grant_type,
        client_id=body.client_id,
        client_secret=body.client_secret,
        code=body.code,
        redirect_uri=body.redirect_uri,
        code_verifier=body.code_verifier,
        refresh_token=body.refresh_token,
        scope=body.scope,
        user_id=body.user_id,
        nonce=body.nonce,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        return _fail(result)
    return result.unwrap()


@federation_gateway_router.post("/introspect")
async def federation_introspect(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: FederationIntrospectRequest,
):
    result = await get_identity_federation_service().federation_introspect(tenant_id, token=body.token)
    return result.unwrap()


@federation_gateway_router.post("/revoke")
async def federation_revoke(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: FederationRevokeRequest,
):
    result = await get_identity_federation_service().federation_revoke(
        tenant_id, token=body.token, token_type_hint=body.token_type_hint
    )
    return result.unwrap()


@federation_gateway_router.post("/provision")
async def federation_provision(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: FederationProvisionRequest,
    correlation_id: Annotated[str, Depends(get_correlation_id)],
):
    result = await get_identity_federation_service().federation_provision(
        tenant_id,
        resource_type=body.resource_type,
        operation=body.operation,
        payload=body.payload,
        resource_id=body.resource_id,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        return _fail(result)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@federation_gateway_router.post("/sync")
async def federation_sync(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: FederationSyncRequest,
):
    result = await get_identity_federation_service().federation_sync_gateway(
        tenant_id,
        provider_ref=body.provider_ref,
        connector_ref=body.connector_ref,
    )
    if not result.succeeded:
        return _fail(result)
    return {"data": result.unwrap()}


@federation_gateway_router.get("/.well-known/openid-configuration")
async def oidc_discovery(tenant_id: Annotated[str, Depends(get_tenant_id)]):
    return (await get_identity_federation_service().oidc_discovery(tenant_id)).unwrap()


@federation_gateway_router.get("/jwks")
async def oidc_jwks(tenant_id: Annotated[str, Depends(get_tenant_id)]):
    return (await get_identity_federation_service().oidc_jwks(tenant_id)).unwrap()


@federation_gateway_router.post("/clients/register")
async def register_oauth_client(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: RegisterOAuthClientRequest,
):
    result = await get_identity_federation_service().register_oauth_client(
        tenant_id,
        client_name=body.client_name,
        redirect_uris=body.redirect_uris,
        grant_types=body.grant_types,
        scopes=body.scopes,
        require_pkce=body.require_pkce,
    )
    if not result.succeeded:
        return _fail(result)
    return {"data": result.unwrap()}


@federation_gateway_router.get("/metrics")
async def federation_metrics(_request: Request):
    return (await get_identity_federation_service().protocol_metrics_snapshot()).unwrap()


@identity_gateway_router.get("/providers")
async def identity_providers(tenant_id: Annotated[str, Depends(get_tenant_id)]):
    return {"data": (await get_identity_federation_service().identity_providers_public(tenant_id)).unwrap()}


@identity_gateway_router.get("/claims")
async def identity_claims(tenant_id: Annotated[str, Depends(get_tenant_id)]):
    return {"data": (await get_identity_federation_service().identity_claims_catalog(tenant_id)).unwrap()}


@identity_gateway_router.get("/metadata")
async def identity_metadata(tenant_id: Annotated[str, Depends(get_tenant_id)]):
    return {"data": (await get_identity_federation_service().identity_metadata(tenant_id)).unwrap()}
