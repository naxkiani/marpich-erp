"""Directory platform API."""
from __future__ import annotations

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException, Request, status

from contexts.directory.container import get_directory_service
from contexts.directory.presentation.schemas import (
    LdapSyncRequest,
    RegisterLdapConnectorRequest,
    RegisterSamlProviderRequest,
    RegisterScimProviderRequest,
    SamlAcsRequest,
    SamlAuthorizeRequest,
    ScimCreateUserRequest,
)
from contexts.identity.presentation.dependencies import (
    get_client_ip,
    get_correlation_id,
    get_tenant_id,
    require_permissions,
)

directory_router = APIRouter(
    prefix="/directory",
    tags=["Directory"],
)


@directory_router.get("/catalog")
async def catalog(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("directory.read"))],
):
    return {"data": (await get_directory_service().list_catalog()).unwrap()}


@directory_router.post("/seed")
async def seed(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("directory.write"))],
):
    return {"data": (await get_directory_service().seed(tenant_id)).unwrap()}


@directory_router.get("/dashboard")
async def dashboard(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("directory.read"))],
):
    return {"data": (await get_directory_service().get_dashboard(tenant_id)).unwrap()}


@directory_router.get("/federation/saml/providers")
async def list_saml_providers(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("directory.read"))],
):
    return {"data": (await get_directory_service().list_saml_providers(tenant_id)).unwrap()}


@directory_router.post("/federation/saml/providers")
async def register_saml_provider(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: RegisterSamlProviderRequest,
    _user: Annotated[dict, Depends(require_permissions("directory.saml.write"))],
):
    result = await get_directory_service().register_saml_provider(
        tenant_id,
        name=body.name,
        entity_id=body.entity_id,
        sso_url=body.sso_url,
        x509_cert=body.x509_cert,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@directory_router.post("/federation/saml/authorize")
async def saml_authorize(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: SamlAuthorizeRequest,
):
    result = await get_directory_service().begin_saml_login(tenant_id, body.provider_ref)
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@directory_router.post("/federation/saml/acs")
async def saml_acs(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: SamlAcsRequest,
    request: Request,
    correlation_id: Annotated[str, Depends(get_correlation_id)] = "",
):
    correlation_id = correlation_id or str(uuid.uuid4())
    result = await get_directory_service().complete_saml_acs(
        saml_response=body.SAMLResponse,
        relay_state=body.RelayState,
        correlation_id=correlation_id,
        ip_address=get_client_ip(request),
        user_agent=request.headers.get("user-agent"),
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"tenant_id": tenant_id, "correlation_id": correlation_id}}


@directory_router.get("/ldap/connectors")
async def list_ldap_connectors(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("directory.read"))],
):
    return {"data": (await get_directory_service().list_ldap_connectors(tenant_id)).unwrap()}


@directory_router.post("/ldap/connectors")
async def register_ldap_connector(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: RegisterLdapConnectorRequest,
    _user: Annotated[dict, Depends(require_permissions("directory.ldap.write"))],
):
    result = await get_directory_service().register_ldap_connector(
        tenant_id,
        name=body.name,
        host=body.host,
        port=body.port,
        bind_dn=body.bind_dn,
        bind_password=body.bind_password,
        base_dn=body.base_dn,
        user_filter=body.user_filter,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@directory_router.post("/ldap/sync")
async def ldap_sync(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: LdapSyncRequest,
    _user: Annotated[dict, Depends(require_permissions("directory.sync.execute"))],
):
    result = await get_directory_service().sync_ldap(tenant_id, body.connector_ref)
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@directory_router.post("/sync/enqueue")
async def enqueue_sync(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: LdapSyncRequest,
    _user: Annotated[dict, Depends(require_permissions("directory.sync.execute"))],
):
    result = await get_directory_service().enqueue_ldap_sync(tenant_id, body.connector_ref)
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@directory_router.post("/sync/run")
async def run_sync_worker(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("directory.sync.execute"))],
):
    return {"data": (await get_directory_service().run_sync_worker(tenant_id)).unwrap()}


@directory_router.get("/sync/jobs")
async def list_sync_jobs(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("directory.read"))],
):
    return {"data": (await get_directory_service().list_sync_jobs(tenant_id)).unwrap()}


@directory_router.get("/scim/providers")
async def list_scim_providers(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("directory.read"))],
):
    return {"data": (await get_directory_service().list_scim_providers(tenant_id)).unwrap()}


@directory_router.post("/scim/providers")
async def register_scim_provider(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: RegisterScimProviderRequest,
    _user: Annotated[dict, Depends(require_permissions("directory.scim.write"))],
):
    result = await get_directory_service().register_scim_provider(
        tenant_id,
        name=body.name,
        bearer_token=body.bearer_token,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@directory_router.post("/scim/v2/Users")
async def scim_create_user(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: ScimCreateUserRequest,
    authorization: Annotated[str | None, Header()] = None,
    correlation_id: Annotated[str, Depends(get_correlation_id)] = "",
):
    correlation_id = correlation_id or str(uuid.uuid4())
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "directory.errors.scim_unauthorized")
    bearer_token = authorization.split(" ", 1)[1].strip()
    result = await get_directory_service().provision_scim_user(
        tenant_id,
        bearer_token,
        body.model_dump(),
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        status_code = status.HTTP_401_UNAUTHORIZED if "unauthorized" in (result.error or "") else status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code, result.error)
    return result.unwrap()
