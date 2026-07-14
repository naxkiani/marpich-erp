"""Enterprise Identity Federation & SSO Platform API."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status

from contexts.identity.presentation.dependencies import (
    get_correlation_id,
    get_tenant_id,
    require_permissions,
)
from contexts.identity_federation.container import get_identity_federation_service
from contexts.identity_federation.presentation.schemas import (
    BrokerAuthRequest,
    ClaimsMappingRequest,
    CreateTrustRequest,
    DiscoverIdentityRequest,
    EvaluateTrustRequest,
    FederatedLogoutRequest,
    JitProvisionRequest,
    LinkIdentityRequest,
    RegisterPartnerRequest,
    RegisterProviderRequest,
    SyncJobRequest,
    TenantFederationRequest,
    TransformClaimsRequest,
)

identity_federation_router = APIRouter(prefix="/federation", tags=["Identity Federation & SSO"])


def _fail(result):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result.error or "request_failed")


@identity_federation_router.get("/catalog")
async def catalog(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("federation.read"))],
):
    return {"data": (await get_identity_federation_service().list_catalog()).unwrap()}


@identity_federation_router.post("/seed")
async def seed(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("federation.write"))],
):
    return {"data": (await get_identity_federation_service().seed(tenant_id)).unwrap()}


@identity_federation_router.get("/dashboard")
async def dashboard(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("federation.read"))],
):
    return {"data": (await get_identity_federation_service().get_dashboard(tenant_id)).unwrap()}


@identity_federation_router.get("/providers")
async def list_providers(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("federation.read"))],
):
    return {"data": (await get_identity_federation_service().list_providers(tenant_id)).unwrap()}


@identity_federation_router.post("/providers")
async def register_provider(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: RegisterProviderRequest,
    _user: Annotated[dict, Depends(require_permissions("federation.write"))],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
):
    result = await get_identity_federation_service().register_provider(
        tenant_id,
        protocol=body.protocol,
        name=body.name,
        config=body.config,
        plugin_id=body.plugin_id,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        _fail(result)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@identity_federation_router.post("/partners")
async def register_partner(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: RegisterPartnerRequest,
    _user: Annotated[dict, Depends(require_permissions("federation.write"))],
):
    result = await get_identity_federation_service().register_partner(
        tenant_id,
        name=body.name,
        partner_type=body.partner_type,
        trust_level=body.trust_level,
        metadata=body.metadata,
    )
    if not result.succeeded:
        _fail(result)
    return {"data": result.unwrap()}


@identity_federation_router.post("/trust")
async def create_trust(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: CreateTrustRequest,
    _user: Annotated[dict, Depends(require_permissions("federation.trust.write"))],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
):
    result = await get_identity_federation_service().create_trust_relationship(
        tenant_id,
        source_entity_type=body.source_entity_type,
        source_entity_id=body.source_entity_id,
        target_entity_type=body.target_entity_type,
        target_entity_id=body.target_entity_id,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        _fail(result)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@identity_federation_router.post("/claims/mappings")
async def create_claims_mapping(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: ClaimsMappingRequest,
    _user: Annotated[dict, Depends(require_permissions("federation.write"))],
):
    result = await get_identity_federation_service().create_claims_mapping(
        tenant_id,
        provider_ref=body.provider_ref,
        source_claim=body.source_claim,
        target_claim=body.target_claim,
        transform_type=body.transform_type,
        transform_config=body.transform_config,
        priority=body.priority,
    )
    if not result.succeeded:
        _fail(result)
    return {"data": result.unwrap()}


@identity_federation_router.post("/claims/transform")
async def transform_claims(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: TransformClaimsRequest,
    _user: Annotated[dict, Depends(require_permissions("federation.read"))],
):
    result = await get_identity_federation_service().transform_claims(
        tenant_id,
        provider_ref=body.provider_ref,
        raw_claims=body.raw_claims,
    )
    if not result.succeeded:
        _fail(result)
    return {"data": result.unwrap()}


@identity_federation_router.post("/discover")
async def discover_identity(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: DiscoverIdentityRequest,
    _user: Annotated[dict, Depends(require_permissions("federation.read"))],
):
    result = await get_identity_federation_service().discover_identity(tenant_id, email=body.email)
    if not result.succeeded:
        _fail(result)
    return {"data": result.unwrap()}


@identity_federation_router.post("/broker/authenticate")
async def broker_authenticate(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: BrokerAuthRequest,
    _user: Annotated[dict, Depends(require_permissions("federation.broker.execute"))],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
):
    result = await get_identity_federation_service().broker_authenticate(
        tenant_id,
        email=body.email,
        provider_hint=body.provider_hint,
        raw_claims=body.raw_claims,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        _fail(result)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@identity_federation_router.post("/links")
async def link_identity(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: LinkIdentityRequest,
    _user: Annotated[dict, Depends(require_permissions("federation.write"))],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
):
    result = await get_identity_federation_service().link_identity(
        tenant_id,
        user_id=body.user_id,
        provider_ref=body.provider_ref,
        external_subject=body.external_subject,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        _fail(result)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@identity_federation_router.post("/provision/jit")
async def provision_jit(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: JitProvisionRequest,
    _user: Annotated[dict, Depends(require_permissions("federation.provision.execute"))],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
):
    result = await get_identity_federation_service().provision_jit(
        tenant_id,
        provider_ref=body.provider_ref,
        claims=body.claims,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        _fail(result)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@identity_federation_router.post("/sessions/logout")
async def federated_logout(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: FederatedLogoutRequest,
    _user: Annotated[dict, Depends(require_permissions("federation.read"))],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
):
    result = await get_identity_federation_service().federated_logout(
        tenant_id,
        session_ref=body.session_ref,
        user_id=body.user_id,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        _fail(result)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@identity_federation_router.post("/jobs/sync")
async def start_sync(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: SyncJobRequest,
    _user: Annotated[dict, Depends(require_permissions("federation.sync.execute"))],
):
    result = await get_identity_federation_service().start_sync_job(
        tenant_id,
        provider_ref=body.provider_ref,
        direction=body.direction,
    )
    if not result.succeeded:
        _fail(result)
    return {"data": result.unwrap()}


@identity_federation_router.post("/tenant-federation")
async def configure_tenant_federation(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: TenantFederationRequest,
    _user: Annotated[dict, Depends(require_permissions("federation.admin"))],
):
    result = await get_identity_federation_service().configure_tenant_federation(
        tenant_id,
        federation_mode=body.federation_mode,
        partner_tenant_id=body.partner_tenant_id,
        region=body.region,
        shared_providers=body.shared_providers,
    )
    if not result.succeeded:
        _fail(result)
    return {"data": result.unwrap()}


@identity_federation_router.post("/trust/evaluate")
async def evaluate_trust(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: EvaluateTrustRequest,
    _user: Annotated[dict, Depends(require_permissions("federation.read"))],
):
    return {"data": (await get_identity_federation_service().evaluate_trust(
        organization_trust=body.organization_trust,
        partner_trust=body.partner_trust,
        identity_trust=body.identity_trust,
        device_trust=body.device_trust,
    )).unwrap()}
