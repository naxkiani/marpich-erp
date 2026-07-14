"""Identity Fabric Mesh / Trust Graph / Zero Trust Federation API (P198-C1)."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from contexts.identity.presentation.dependencies import (
    get_correlation_id,
    get_tenant_id,
    require_permissions,
)
from contexts.identity_federation.container import get_fabric_security_service
from contexts.identity_federation.presentation.fabric_schemas import (
    BrokerIntelRequest,
    DuplicateDetectRequest,
    EnterpriseTrustRequest,
    FederateSessionRequest,
    GlobalLogoutRequest,
    MeshRouteRequest,
    MeshSyncRequest,
    RecalculateTrustRequest,
    RiskFederationRequest,
    SecurityValidateRequest,
    TokenExchangeRequest,
    TokenTranslateRequest,
    TrustContractRequest,
    TrustEdgeRequest,
    TrustNeighborsRequest,
    TrustNodeRequest,
    TrustPathRequest,
    TrustPropagateRequest,
    ZeroTrustFederationRequest,
)

fabric_security_router = APIRouter(prefix="/federation/fabric", tags=["Identity Fabric Security"])


def _fail(result):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result.error or "request_failed")


@fabric_security_router.get("/mesh")
async def get_mesh(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("federation.read"))],
):
    return {"data": (await get_fabric_security_service().get_mesh(tenant_id)).unwrap()}


@fabric_security_router.post("/mesh/route")
async def route_mesh(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: MeshRouteRequest,
    _user: Annotated[dict, Depends(require_permissions("federation.broker.execute"))],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
):
    result = await get_fabric_security_service().route_mesh(
        tenant_id, email=body.email, node_hint=body.node_hint, correlation_id=correlation_id
    )
    if not result.succeeded:
        _fail(result)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@fabric_security_router.post("/mesh/sync")
async def sync_mesh(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: MeshSyncRequest,
    _user: Annotated[dict, Depends(require_permissions("federation.sync.execute"))],
):
    return {"data": (await get_fabric_security_service().sync_mesh_node(
        tenant_id, node_id=body.node_id, direction=body.direction
    )).unwrap()}


@fabric_security_router.get("/trust-graph/catalog")
async def trust_graph_catalog(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("federation.read"))],
):
    return {"data": (await get_fabric_security_service().trust_graph_catalog()).unwrap()}


@fabric_security_router.post("/trust-graph/nodes")
async def upsert_trust_node(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: TrustNodeRequest,
    _user: Annotated[dict, Depends(require_permissions("federation.trust.write"))],
):
    return {"data": (await get_fabric_security_service().upsert_trust_node(
        tenant_id, node_id=body.node_id, node_type=body.node_type, attributes=body.attributes
    )).unwrap()}


@fabric_security_router.post("/trust-graph/edges")
async def add_trust_edge(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: TrustEdgeRequest,
    _user: Annotated[dict, Depends(require_permissions("federation.trust.write"))],
):
    return {"data": (await get_fabric_security_service().add_trust_edge(
        tenant_id,
        edge_id=body.edge_id,
        from_id=body.from_id,
        to_id=body.to_id,
        relation=body.relation,
        weight=body.weight,
        metadata=body.metadata,
    )).unwrap()}


@fabric_security_router.post("/trust-graph/neighbors")
async def trust_neighbors(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: TrustNeighborsRequest,
    _user: Annotated[dict, Depends(require_permissions("federation.read"))],
):
    return {"data": (await get_fabric_security_service().query_trust_neighbors(
        tenant_id, node_id=body.node_id, relation=body.relation, depth=body.depth
    )).unwrap()}


@fabric_security_router.post("/trust-graph/path")
async def trust_path(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: TrustPathRequest,
    _user: Annotated[dict, Depends(require_permissions("federation.read"))],
):
    return {"data": (await get_fabric_security_service().find_trust_path(
        tenant_id, source=body.source, target=body.target
    )).unwrap()}


@fabric_security_router.post("/trust-graph/propagate")
async def trust_propagate(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: TrustPropagateRequest,
    _user: Annotated[dict, Depends(require_permissions("federation.trust.write"))],
):
    return {"data": (await get_fabric_security_service().propagate_trust(
        tenant_id, source=body.source, base_score=body.base_score
    )).unwrap()}


@fabric_security_router.post("/trust/evaluate")
async def evaluate_enterprise_trust(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: EnterpriseTrustRequest,
    _user: Annotated[dict, Depends(require_permissions("federation.read"))],
):
    return {"data": (await get_fabric_security_service().evaluate_enterprise_trust(
        tenant_id, **body.model_dump()
    )).unwrap()}


@fabric_security_router.post("/trust/recalculate")
async def recalculate_trust(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: RecalculateTrustRequest,
    _user: Annotated[dict, Depends(require_permissions("federation.trust.write"))],
):
    return {"data": (await get_fabric_security_service().recalculate_trust(
        tenant_id, prior_score=body.prior_score, delta=body.delta, reason=body.reason
    )).unwrap()}


@fabric_security_router.get("/trust/history")
async def trust_history(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("federation.read"))],
):
    return {"data": (await get_fabric_security_service().trust_history(tenant_id)).unwrap()}


@fabric_security_router.post("/trust/contracts")
async def create_trust_contract(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: TrustContractRequest,
    _user: Annotated[dict, Depends(require_permissions("federation.trust.write"))],
):
    return {"data": (await get_fabric_security_service().create_trust_contract(
        tenant_id,
        partner_type=body.partner_type,
        source_org=body.source_org,
        target_org=body.target_org,
        legal_policy_ref=body.legal_policy_ref,
    )).unwrap()}


@fabric_security_router.post("/zero-trust/evaluate")
async def evaluate_zero_trust(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: ZeroTrustFederationRequest,
    _user: Annotated[dict, Depends(require_permissions("federation.broker.execute"))],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
):
    result = await get_fabric_security_service().evaluate_zero_trust_federation(
        tenant_id,
        user_id=body.user_id,
        identity_verified=body.identity_verified,
        device_trusted=body.device_trusted,
        application_trusted=body.application_trusted,
        location_allowed=body.location_allowed,
        behavior_anomaly=body.behavior_anomaly,
        session_valid=body.session_valid,
        network_trusted=body.network_trusted,
        organization_trusted=body.organization_trusted,
        risk_score=body.risk_score,
        trust_score=body.trust_score,
        correlation_id=correlation_id,
        use_adaptive_pdp=body.use_adaptive_pdp,
    )
    if not result.succeeded:
        _fail(result)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@fabric_security_router.post("/security/validate")
async def validate_security(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: SecurityValidateRequest,
    _user: Annotated[dict, Depends(require_permissions("federation.read"))],
):
    return {"data": (await get_fabric_security_service().validate_security(
        tenant_id, **body.model_dump()
    )).unwrap()}


@fabric_security_router.post("/risk/decide")
async def risk_decide(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: RiskFederationRequest,
    _user: Annotated[dict, Depends(require_permissions("federation.broker.execute"))],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
):
    result = await get_fabric_security_service().risk_based_decision(
        tenant_id,
        protocol=body.protocol,
        device_risk=body.device_risk,
        behavior_risk=body.behavior_risk,
        network_risk=body.network_risk,
        organization_risk=body.organization_risk,
        certificate_risk=body.certificate_risk,
        country_risk=body.country_risk,
        transaction_risk=body.transaction_risk,
        trust_score=body.trust_score,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        _fail(result)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@fabric_security_router.post("/broker/intelligence")
async def broker_intelligence(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: BrokerIntelRequest,
    _user: Annotated[dict, Depends(require_permissions("federation.broker.execute"))],
):
    return {"data": (await get_fabric_security_service().broker_intelligence_route(
        tenant_id, email=body.email, risk_score=body.risk_score, trust_score=body.trust_score
    )).unwrap()}


@fabric_security_router.post("/broker/duplicates")
async def detect_duplicates(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: DuplicateDetectRequest,
    _user: Annotated[dict, Depends(require_permissions("federation.read"))],
):
    return {"data": (await get_fabric_security_service().detect_duplicates(
        tenant_id,
        email=body.email,
        external_subject=body.external_subject,
        candidates=body.candidates,
    )).unwrap()}


@fabric_security_router.post("/tokens/exchange")
async def exchange_token(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: TokenExchangeRequest,
    _user: Annotated[dict, Depends(require_permissions("federation.write"))],
):
    return {"data": (await get_fabric_security_service().exchange_token(
        tenant_id,
        source_type=body.source_type,
        target_type=body.target_type,
        subject=body.subject,
        audience=body.audience,
        scopes=body.scopes,
        claims=body.claims,
    )).unwrap()}


@fabric_security_router.post("/tokens/translate")
async def translate_claims(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: TokenTranslateRequest,
    _user: Annotated[dict, Depends(require_permissions("federation.read"))],
):
    return {"data": (await get_fabric_security_service().translate_token_claims(
        tenant_id, protocol=body.protocol, claims=body.claims
    )).unwrap()}


@fabric_security_router.post("/sessions/federate")
async def federate_session(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: FederateSessionRequest,
    _user: Annotated[dict, Depends(require_permissions("federation.write"))],
):
    return {"data": (await get_fabric_security_service().federate_session(
        tenant_id,
        session_ref=body.session_ref,
        user_id=body.user_id,
        provider_ref=body.provider_ref,
        protocol=body.protocol,
        apps=body.apps,
    )).unwrap()}


@fabric_security_router.post("/sessions/global-logout")
async def global_logout(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: GlobalLogoutRequest,
    _user: Annotated[dict, Depends(require_permissions("federation.write"))],
):
    return {"data": (await get_fabric_security_service().global_logout(
        tenant_id, user_id=body.user_id, sessions=body.sessions
    )).unwrap()}


@fabric_security_router.get("/security/dashboard")
async def security_dashboard(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("federation.read"))],
):
    return {"data": (await get_fabric_security_service().security_dashboard(tenant_id)).unwrap()}


@fabric_security_router.get("/audit")
async def list_audit(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("federation.read"))],
):
    return {"data": (await get_fabric_security_service().list_audit(tenant_id)).unwrap()}


@fabric_security_router.get("/metrics")
async def fabric_metrics(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("federation.read"))],
):
    return {"data": (await get_fabric_security_service().trust_metrics()).unwrap()}
