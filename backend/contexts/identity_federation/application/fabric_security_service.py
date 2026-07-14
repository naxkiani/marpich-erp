"""Identity Fabric security service — mesh, trust graph, ZT, risk (P198-C1)."""
from __future__ import annotations

from contexts.identity_federation.domain.events.federation_integration_events import (
    MeshRouteResolvedIntegration,
    TrustDecisionIntegration,
    ZeroTrustFederationDecisionIntegration,
)
from contexts.identity_federation.domain.ports.federation_repositories import (
    IFederationPartnerRepository,
    IFederationSessionRepository,
    IIdentityProviderRepository,
    ITenantFederationRepository,
    ITrustRelationshipRepository,
)
from contexts.identity_federation.domain.services import broker_intelligence_engine
from contexts.identity_federation.domain.services import federation_security_engine
from contexts.identity_federation.domain.services import identity_fabric_mesh_engine
from contexts.identity_federation.domain.services import risk_based_federation_engine
from contexts.identity_federation.domain.services import session_federation_engine
from contexts.identity_federation.domain.services import token_federation_engine
from contexts.identity_federation.domain.services import trust_graph_engine
from contexts.identity_federation.domain.services import trust_management_engine
from contexts.identity_federation.domain.services import zero_trust_federation_engine
from contexts.identity_federation.infrastructure.adapters.adaptive_auth_acl import AdaptiveAuthAcl
from contexts.identity_federation.infrastructure.adapters.identity_risk_acl import IdentityRiskAcl
from contexts.identity_federation.infrastructure.observability import federation_trust_metrics
from contexts.identity_federation.infrastructure.persistence.federation_audit_store import (
    FederationAuditStore,
)
from shared.application.ports.policy import IPolicyEvaluator
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.infrastructure.messaging.event_bus import publish_integration_event

# Per-tenant in-memory trust graph projection (directory graph sync via events in prod)
_TRUST_GRAPHS: dict[str, dict] = {}
_TRUST_HISTORY: dict[str, list[dict]] = {}
_REPLAY_KEYS: set[str] = set()


class FabricSecurityApplicationService:
    def __init__(
        self,
        providers: IIdentityProviderRepository,
        partners: IFederationPartnerRepository,
        trusts: ITrustRelationshipRepository,
        sessions: IFederationSessionRepository,
        tenant_feds: ITenantFederationRepository,
        policy_evaluator: IPolicyEvaluator,
        adaptive_acl: AdaptiveAuthAcl | None = None,
        risk_acl: IdentityRiskAcl | None = None,
    ) -> None:
        self._providers = providers
        self._partners = partners
        self._trusts = trusts
        self._sessions = sessions
        self._tenant_feds = tenant_feds
        self._policy = policy_evaluator
        self._adaptive = adaptive_acl or AdaptiveAuthAcl()
        self._risk = risk_acl or IdentityRiskAcl()

    def _graph(self, tenant_id: str) -> dict:
        if tenant_id not in _TRUST_GRAPHS:
            _TRUST_GRAPHS[tenant_id] = trust_graph_engine.empty_graph(tenant_id)
        return _TRUST_GRAPHS[tenant_id]

    async def _policy_params(self, tenant_id: str) -> dict:
        params = {
            "zero_trust_enabled": True,
            "mesh_enabled": True,
            "risk_federation_enabled": True,
            "step_up_threshold": 70,
            "deny_threshold": 90,
            "cross_tenant_enabled": False,
        }
        pmap = {
            "federation.zero_trust.enabled": ("zero_trust_enabled", "enabled"),
            "federation.mesh.enabled": ("mesh_enabled", "enabled"),
            "federation.risk.enabled": ("risk_federation_enabled", "enabled"),
            "federation.risk.step_up.threshold": ("step_up_threshold", "threshold"),
            "federation.risk.deny.threshold": ("deny_threshold", "threshold"),
            "federation.cross_tenant.enabled": ("cross_tenant_enabled", "enabled"),
        }
        for key, (target, field) in pmap.items():
            decision = await self._policy.evaluate(
                tenant_id=tenant_id, domain="platform", policy_key=key, facts={}
            )
            if decision.parameters and field in decision.parameters:
                params[target] = decision.parameters[field]
        return params

    async def get_mesh(self, tenant_id: str) -> Result[dict]:
        providers = [p.to_dict() for p in await self._providers.list_by_tenant(tenant_id)]
        partners = [p.to_dict() for p in await self._partners.list_by_tenant(tenant_id)]
        tenants = [t.to_dict() for t in await self._tenant_feds.list_by_tenant(tenant_id)]
        topology = identity_fabric_mesh_engine.build_mesh_topology(
            providers=providers, partners=partners, tenants=tenants
        )
        health = identity_fabric_mesh_engine.mesh_health(topology=topology)
        return Result.ok({**topology, "health": health})

    async def route_mesh(
        self,
        tenant_id: str,
        *,
        email: str | None = None,
        node_hint: str | None = None,
        correlation_id: str | None = None,
    ) -> Result[dict]:
        params = await self._policy_params(tenant_id)
        if not params.get("mesh_enabled", True):
            return Result.fail("federation.errors.mesh_disabled")
        mesh = (await self.get_mesh(tenant_id)).unwrap()
        route = identity_fabric_mesh_engine.discover_mesh_route(
            email=email, node_hint=node_hint, topology=mesh
        )
        federation_trust_metrics.increment("mesh_route_total")
        if route.get("routed") and route.get("target"):
            await publish_integration_event(
                MeshRouteResolvedIntegration(
                    tenant_id=TenantId(tenant_id),
                    correlation_id=correlation_id or "",
                    node_id=route["target"].get("node_id", ""),
                    method=route.get("method", ""),
                )
            )
            FederationAuditStore.append(
                tenant_id=tenant_id,
                event_type="mesh.route",
                resource=route["target"].get("node_id", ""),
                decision="routed",
                detail=route,
                correlation_id=correlation_id or "",
            )
        return Result.ok(route)

    async def sync_mesh_node(self, tenant_id: str, *, node_id: str, direction: str = "inbound") -> Result[dict]:
        return Result.ok(identity_fabric_mesh_engine.synchronize_mesh_node(node_id=node_id, direction=direction))

    async def trust_graph_catalog(self) -> Result[dict]:
        return Result.ok(trust_graph_engine.catalog())

    async def upsert_trust_node(
        self,
        tenant_id: str,
        *,
        node_id: str,
        node_type: str,
        attributes: dict | None = None,
    ) -> Result[dict]:
        graph = self._graph(tenant_id)
        node = trust_graph_engine.upsert_node(
            graph, node_id=node_id, node_type=node_type, attributes=attributes
        )
        return Result.ok(node)

    async def add_trust_edge(
        self,
        tenant_id: str,
        *,
        edge_id: str,
        from_id: str,
        to_id: str,
        relation: str,
        weight: float = 1.0,
        metadata: dict | None = None,
    ) -> Result[dict]:
        graph = self._graph(tenant_id)
        if from_id not in graph["nodes"]:
            trust_graph_engine.upsert_node(graph, node_id=from_id, node_type="identity")
        if to_id not in graph["nodes"]:
            trust_graph_engine.upsert_node(graph, node_id=to_id, node_type="identity")
        edge = trust_graph_engine.add_edge(
            graph,
            edge_id=edge_id,
            from_id=from_id,
            to_id=to_id,
            relation=relation,
            weight=weight,
            metadata=metadata,
        )
        FederationAuditStore.append(
            tenant_id=tenant_id,
            event_type="trust.edge.added",
            resource=edge_id,
            detail=edge,
        )
        return Result.ok(edge)

    async def query_trust_neighbors(
        self, tenant_id: str, *, node_id: str, relation: str | None = None, depth: int = 1
    ) -> Result[dict]:
        return Result.ok(
            trust_graph_engine.query_neighbors(
                self._graph(tenant_id), node_id=node_id, relation=relation, depth=depth
            )
        )

    async def find_trust_path(self, tenant_id: str, *, source: str, target: str) -> Result[dict]:
        return Result.ok(trust_graph_engine.find_path(self._graph(tenant_id), source=source, target=target))

    async def propagate_trust(self, tenant_id: str, *, source: str, base_score: int = 80) -> Result[dict]:
        federation_trust_metrics.increment("trust_propagate_total")
        return Result.ok(
            trust_graph_engine.propagate_trust(self._graph(tenant_id), source=source, base_score=base_score)
        )

    async def evaluate_enterprise_trust(self, tenant_id: str, **dims: int) -> Result[dict]:
        federation_trust_metrics.increment("trust_eval_total")
        result = trust_management_engine.evaluate_enterprise_trust(**{
            k: dims.get(k, 50) for k in trust_management_engine.TRUST_DIMENSIONS
        })
        hist = _TRUST_HISTORY.setdefault(tenant_id, [])
        _TRUST_HISTORY[tenant_id] = trust_management_engine.append_trust_history(
            hist, score=result["trust_score"], level=result["trust_level"], reason="evaluate"
        )
        result["history_count"] = len(_TRUST_HISTORY[tenant_id])
        FederationAuditStore.append(
            tenant_id=tenant_id,
            event_type="trust.evaluated",
            decision=result["trust_level"],
            detail={"trust_score": result["trust_score"]},
        )
        return Result.ok(result)

    async def recalculate_trust(self, tenant_id: str, *, prior_score: int, delta: int, reason: str) -> Result[dict]:
        result = trust_management_engine.recalculate_trust(
            prior_score=prior_score, delta=delta, reason=reason
        )
        hist = _TRUST_HISTORY.setdefault(tenant_id, [])
        _TRUST_HISTORY[tenant_id] = trust_management_engine.append_trust_history(
            hist, score=result["trust_score"], level=result["trust_level"], reason=reason
        )
        return Result.ok(result)

    async def trust_history(self, tenant_id: str) -> Result[list[dict]]:
        return Result.ok(list(_TRUST_HISTORY.get(tenant_id, [])))

    async def create_trust_contract(
        self,
        tenant_id: str,
        *,
        partner_type: str,
        source_org: str,
        target_org: str,
        legal_policy_ref: str | None = None,
    ) -> Result[dict]:
        contract = trust_management_engine.cross_organization_trust_contract(
            partner_type=partner_type,
            source_org=source_org,
            target_org=target_org,
            legal_policy_ref=legal_policy_ref,
        )
        FederationAuditStore.append(
            tenant_id=tenant_id,
            event_type="trust.contract.created",
            resource=f"{source_org}->{target_org}",
            detail=contract,
        )
        return Result.ok(contract)

    async def evaluate_zero_trust_federation(
        self,
        tenant_id: str,
        *,
        user_id: str = "anonymous",
        identity_verified: bool = True,
        device_trusted: bool = False,
        application_trusted: bool = True,
        location_allowed: bool = True,
        behavior_anomaly: bool = False,
        session_valid: bool = True,
        network_trusted: bool = True,
        organization_trusted: bool = True,
        risk_score: int = 0,
        trust_score: int = 50,
        correlation_id: str | None = None,
        use_adaptive_pdp: bool = True,
    ) -> Result[dict]:
        params = await self._policy_params(tenant_id)
        if not params.get("zero_trust_enabled", True):
            return Result.ok({"allowed": True, "action": "allow", "zero_trust_disabled": True})

        decision = zero_trust_federation_engine.evaluate_federation_zero_trust(
            identity_verified=identity_verified,
            device_trusted=device_trusted,
            application_trusted=application_trusted,
            location_allowed=location_allowed,
            behavior_anomaly=behavior_anomaly,
            session_valid=session_valid,
            network_trusted=network_trusted,
            organization_trusted=organization_trusted,
            risk_score=risk_score,
            trust_score=trust_score,
            policy_allowed=True,
            step_up_threshold=int(params.get("step_up_threshold", 70)),
            deny_threshold=int(params.get("deny_threshold", 90)),
        )
        if use_adaptive_pdp:
            adaptive = await self._adaptive.evaluate_zero_trust(
                tenant_id=tenant_id,
                user_id=user_id,
                device_trusted=device_trusted,
                session_risk_score=decision["risk_score"],
            )
            decision["adaptive_pdp"] = adaptive
            if adaptive.get("outcome") == "step_up" and decision["action"] == "allow":
                decision["action"] = "step_up"
                decision["allowed"] = False

        federation_trust_metrics.increment("zt_decision_total")
        await publish_integration_event(
            ZeroTrustFederationDecisionIntegration(
                tenant_id=TenantId(tenant_id),
                correlation_id=correlation_id or "",
                action=decision["action"],
                risk_score=decision["risk_score"],
                failed_dimensions=tuple(decision.get("failed_dimensions") or ()),
            )
        )
        await publish_integration_event(
            TrustDecisionIntegration(
                tenant_id=TenantId(tenant_id),
                correlation_id=correlation_id or "",
                decision=decision["action"],
                trust_score=trust_score,
                risk_score=decision["risk_score"],
            )
        )
        FederationAuditStore.append(
            tenant_id=tenant_id,
            event_type="zero_trust.decision",
            actor=user_id,
            decision=decision["action"],
            detail=decision,
            correlation_id=correlation_id or "",
        )
        return Result.ok(decision)

    async def validate_security(
        self,
        tenant_id: str,
        *,
        state: str | None = None,
        expected_state: str | None = None,
        nonce: str | None = None,
        expected_nonce: str | None = None,
        audience: str | None = None,
        expected_audience: str | None = None,
        origin: str | None = None,
        allowed_origins: list[str] | None = None,
        signature_valid: bool = True,
        replay_key: str | None = None,
        token_exp: int | None = None,
    ) -> Result[dict]:
        result = federation_security_engine.validate_federation_request(
            state=state,
            expected_state=expected_state,
            nonce=nonce,
            expected_nonce=expected_nonce,
            audience=audience,
            expected_audience=expected_audience,
            origin=origin,
            allowed_origins=allowed_origins,
            signature_valid=signature_valid,
            replay_key=replay_key,
            seen_replays=_REPLAY_KEYS,
            token_exp=token_exp,
        )
        if replay_key and result["valid"]:
            _REPLAY_KEYS.add(replay_key)
        federation_trust_metrics.increment("cert_validate_total")
        return Result.ok({
            **result,
            "secure_defaults": zero_trust_federation_engine.secure_defaults(),
        })

    async def risk_based_decision(
        self,
        tenant_id: str,
        *,
        protocol: str = "oidc",
        device_risk: int = 0,
        behavior_risk: int = 0,
        network_risk: int = 0,
        organization_risk: int = 0,
        certificate_risk: int = 0,
        country_risk: int = 0,
        transaction_risk: int = 0,
        trust_score: int = 50,
        correlation_id: str | None = None,
    ) -> Result[dict]:
        params = await self._policy_params(tenant_id)
        if not params.get("risk_federation_enabled", True):
            return Result.fail("federation.errors.risk_disabled")
        scored = risk_based_federation_engine.score_federation_risk(
            device_risk=device_risk,
            behavior_risk=behavior_risk,
            network_risk=network_risk,
            organization_risk=organization_risk,
            certificate_risk=certificate_risk,
            country_risk=country_risk,
            transaction_risk=transaction_risk,
        )
        platform = await self._risk.score_federation(
            tenant_id=tenant_id,
            auth_method=protocol,
            correlation_id=correlation_id or "",
        )
        risk_score = max(scored["risk_score"], int(platform.get("score", platform.get("risk_score", 0)) or 0))
        decision = risk_based_federation_engine.adaptive_federation_decision(
            risk_score=risk_score,
            trust_score=trust_score,
            step_up_threshold=int(params.get("step_up_threshold", 70)),
            deny_threshold=int(params.get("deny_threshold", 90)),
        )
        federation_trust_metrics.increment("risk_decision_total")
        if risk_score >= 70:
            federation_trust_metrics.increment("high_risk_total")
        FederationAuditStore.append(
            tenant_id=tenant_id,
            event_type="risk.decision",
            decision=decision["action"],
            detail={**scored, **decision, "platform_score": platform},
            correlation_id=correlation_id or "",
        )
        return Result.ok({**decision, "signals": scored, "platform_risk": platform})

    async def broker_intelligence_route(
        self,
        tenant_id: str,
        *,
        email: str | None = None,
        risk_score: int = 0,
        trust_score: int = 50,
    ) -> Result[dict]:
        providers = [p.to_dict() for p in await self._providers.list_by_tenant(tenant_id)]
        federation_trust_metrics.increment("broker_intel_total")
        return Result.ok(
            broker_intelligence_engine.dynamic_route(
                email=email,
                risk_score=risk_score,
                trust_score=trust_score,
                providers=providers,
            )
        )

    async def detect_duplicates(
        self,
        tenant_id: str,
        *,
        email: str | None = None,
        external_subject: str | None = None,
        candidates: list[dict] | None = None,
    ) -> Result[dict]:
        return Result.ok(
            broker_intelligence_engine.detect_duplicates(
                candidates=candidates or [],
                email=email,
                external_subject=external_subject,
            )
        )

    async def exchange_token(
        self,
        tenant_id: str,
        *,
        source_type: str,
        target_type: str,
        subject: str,
        audience: str,
        scopes: list[str] | None = None,
        claims: dict | None = None,
    ) -> Result[dict]:
        return Result.ok(
            token_federation_engine.exchange_token(
                source_type=source_type,
                target_type=target_type,
                subject=subject,
                audience=audience,
                scopes=scopes,
                claims=claims,
            )
        )

    async def translate_token_claims(
        self, tenant_id: str, *, protocol: str, claims: dict
    ) -> Result[dict]:
        return Result.ok({
            "protocol": protocol,
            "claims": token_federation_engine.translate_claims_for_protocol(
                protocol=protocol, claims=claims
            ),
        })

    async def federate_session(
        self,
        tenant_id: str,
        *,
        session_ref: str,
        user_id: str,
        provider_ref: str,
        protocol: str,
        apps: list[str] | None = None,
    ) -> Result[dict]:
        session = session_federation_engine.create_federated_session(
            session_ref=session_ref,
            user_id=user_id,
            provider_ref=provider_ref,
            protocol=protocol,
            apps=apps,
            tenant_scope=[tenant_id],
        )
        FederationAuditStore.append(
            tenant_id=tenant_id,
            event_type="session.federated",
            actor=user_id,
            resource=session_ref,
            detail=session,
        )
        return Result.ok(session)

    async def global_logout(
        self, tenant_id: str, *, user_id: str, sessions: list[dict] | None = None
    ) -> Result[dict]:
        result = session_federation_engine.global_logout(sessions or [], user_id=user_id)
        FederationAuditStore.append(
            tenant_id=tenant_id,
            event_type="session.global_logout",
            actor=user_id,
            decision="revoked",
            detail=result,
        )
        return Result.ok(result)

    async def security_dashboard(self, tenant_id: str) -> Result[dict]:
        providers = await self._providers.list_by_tenant(tenant_id)
        trusts = await self._trusts.list_by_tenant(tenant_id)
        partners = await self._partners.list_by_tenant(tenant_id)
        audit = FederationAuditStore.list_by_tenant(tenant_id, limit=20)
        metrics = federation_trust_metrics.snapshot()
        graph = self._graph(tenant_id)
        failed = [a for a in audit if a.get("decision") in ("deny", "rejected", "failed")]
        return Result.ok({
            "identity_trust": {
                "providers": len(providers),
                "enabled_providers": sum(1 for p in providers if p.enabled),
            },
            "organization_trust": {
                "partners": len(partners),
                "trust_relationships": len(trusts),
                "graph_nodes": len(graph.get("nodes", {})),
                "graph_edges": len(graph.get("edges", [])),
            },
            "federation_health": (await self.get_mesh(tenant_id)).unwrap().get("health"),
            "certificate_health": federation_security_engine.certificate_security_posture(
                mtls=True, pinned=True, rotated_recently=True
            ),
            "policy_violations": len(failed),
            "failed_federations": failed[:10],
            "threat_detection": {
                "high_risk_events": metrics["risk_metrics"]["high_risk"],
                "zt_decisions": metrics["federation_metrics"]["zt_decisions"],
            },
            "real_time_alerts": failed[:5],
            "metrics": metrics,
            "audit_tail": audit[:10],
        })

    async def list_audit(self, tenant_id: str, *, limit: int = 50) -> Result[list[dict]]:
        return Result.ok(FederationAuditStore.list_by_tenant(tenant_id, limit=limit))

    async def trust_metrics(self) -> Result[dict]:
        return Result.ok(federation_trust_metrics.snapshot())


def reset_fabric_security_state() -> None:
    _TRUST_GRAPHS.clear()
    _TRUST_HISTORY.clear()
    _REPLAY_KEYS.clear()
    FederationAuditStore.reset()
    federation_trust_metrics.reset()
