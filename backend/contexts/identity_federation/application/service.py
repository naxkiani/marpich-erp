"""Identity Federation application service — enterprise SSO & identity fabric."""
from __future__ import annotations

from datetime import UTC, datetime, timedelta

from contexts.identity_federation.domain.aggregates.federation_platform import (
    ClaimsMapping,
    FederationPartner,
    FederationProfile,
    FederationSession,
    IdentityLink,
    IdentityProvider,
    ProvisioningPolicy,
    SynchronizationJob,
    TenantFederation,
    TrustRelationship,
)
from contexts.identity_federation.domain.events.federation_integration_events import (
    CertificateRotatedIntegration,
    ClaimsMappedIntegration,
    ExternalAuthenticationFailedIntegration,
    ExternalAuthenticationSucceededIntegration,
    FederatedLogoutIntegration,
    IdentityFederatedIntegration,
    IdentityLinkedIntegration,
    IdentityProviderRegisteredIntegration,
    IdentityProvisionedIntegration,
    TokenExchangedIntegration,
    TrustRelationshipEstablishedIntegration,
)
from contexts.identity_federation.domain.services import protocol_engine
from contexts.identity_federation.infrastructure.adapters.protocol_bridge_adapter import (
    ProtocolBridgeAdapter,
)
from contexts.identity_federation.infrastructure.certificates.certificate_manager import (
    CertificateManager,
)
from contexts.identity_federation.infrastructure.observability import federation_protocol_metrics
from contexts.identity_federation.infrastructure.protocols.oauth2_server import OAuth2AuthorizationServer
from contexts.identity_federation.infrastructure.protocols.oidc_provider import OidcProvider
from contexts.identity_federation.infrastructure.protocols.scim_server import ScimServer
from shared.infrastructure.settings import settings
from contexts.identity_federation.domain.ports.federation_repositories import (
    IClaimsMappingRepository,
    IFederationPartnerRepository,
    IFederationProfileRepository,
    IFederationSessionRepository,
    IIdentityLinkRepository,
    IIdentityProviderRepository,
    IProvisioningPolicyRepository,
    ISynchronizationJobRepository,
    ITenantFederationRepository,
    ITrustRelationshipRepository,
)
from contexts.identity_federation.domain.services import broker_engine
from contexts.identity_federation.domain.services import claims_transformation_engine
from contexts.identity_federation.domain.services import federation_engine
from contexts.identity_federation.domain.services import federation_plugin_registry
from contexts.identity_federation.domain.services import provisioning_engine
from contexts.identity_federation.domain.services import trust_management_engine
from shared.application.ports.policy import IPolicyEvaluator
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.domain.value_objects.unique_id import UniqueId
from shared.infrastructure.messaging.event_bus import publish_integration_event


class IdentityFederationApplicationService:
    def __init__(
        self,
        profiles: IFederationProfileRepository,
        providers: IIdentityProviderRepository,
        partners: IFederationPartnerRepository,
        trusts: ITrustRelationshipRepository,
        mappings: IClaimsMappingRepository,
        links: IIdentityLinkRepository,
        prov_policies: IProvisioningPolicyRepository,
        sync_jobs: ISynchronizationJobRepository,
        sessions: IFederationSessionRepository,
        tenant_feds: ITenantFederationRepository,
        policy_evaluator: IPolicyEvaluator,
        oauth2: OAuth2AuthorizationServer | None = None,
        oidc: OidcProvider | None = None,
        scim: ScimServer | None = None,
        cert_manager: CertificateManager | None = None,
        protocol_bridge: ProtocolBridgeAdapter | None = None,
    ) -> None:
        self._profiles = profiles
        self._providers = providers
        self._partners = partners
        self._trusts = trusts
        self._mappings = mappings
        self._links = links
        self._prov_policies = prov_policies
        self._sync_jobs = sync_jobs
        self._sessions = sessions
        self._tenant_feds = tenant_feds
        self._policy = policy_evaluator
        self._oauth2 = oauth2 or OAuth2AuthorizationServer()
        self._oidc = oidc or OidcProvider()
        self._scim = scim or ScimServer()
        self._certs = cert_manager or CertificateManager()
        self._bridge = protocol_bridge or ProtocolBridgeAdapter()

    async def _policy_params(self, tenant_id: str) -> dict:
        profile = await self._profiles.find_by_tenant(tenant_id)
        params = {
            "federation_enabled": profile.federation_enabled if profile else True,
            "broker_enabled": profile.broker_enabled if profile else True,
            "jit_provisioning_enabled": profile.jit_provisioning_enabled if profile else True,
            "identity_discovery_enabled": profile.identity_discovery_enabled if profile else True,
            "single_logout_enabled": profile.single_logout_enabled if profile else True,
            "cross_tenant_enabled": profile.cross_tenant_enabled if profile else False,
        }
        pmap = {
            "federation.enabled": ("federation_enabled", "enabled"),
            "federation.broker.enabled": ("broker_enabled", "enabled"),
            "federation.jit_provisioning.enabled": ("jit_provisioning_enabled", "enabled"),
            "federation.identity_discovery.enabled": ("identity_discovery_enabled", "enabled"),
            "federation.single_logout.enabled": ("single_logout_enabled", "enabled"),
            "federation.cross_tenant.enabled": ("cross_tenant_enabled", "enabled"),
        }
        for key, (target, field) in pmap.items():
            decision = await self._policy.evaluate(tenant_id=tenant_id, domain="platform", policy_key=key, facts={})
            if decision.parameters and field in decision.parameters:
                params[target] = decision.parameters[field]
        return params

    async def _ensure_profile(self, tenant_id: str) -> FederationProfile:
        profile = await self._profiles.find_by_tenant(tenant_id)
        if profile:
            return profile
        profile = FederationProfile.create(
            tenant_id=tenant_id,
            profile_ref=self._profiles.next_profile_ref(tenant_id),
        )
        await self._profiles.save(profile)
        return profile

    async def handle_tenant_provisioned(self, envelope: dict) -> None:
        tenant_id = envelope.get("tenant_id", "")
        if tenant_id:
            await self._ensure_profile(tenant_id)

    async def list_catalog(self) -> Result[dict]:
        catalog = federation_engine.build_federation_catalog()
        catalog["provider_plugins"] = federation_plugin_registry.list_provider_plugins()
        return Result.ok(catalog)

    async def seed(self, tenant_id: str) -> Result[dict]:
        profile = await self._ensure_profile(tenant_id)
        return Result.ok({"profile_ref": profile.profile_ref, "seeded": True})

    async def get_dashboard(self, tenant_id: str) -> Result[dict]:
        providers = await self._providers.list_by_tenant(tenant_id)
        partners = await self._partners.list_by_tenant(tenant_id)
        trusts = await self._trusts.list_by_tenant(tenant_id)
        return Result.ok({
            "providers_count": len(providers),
            "partners_count": len(partners),
            "trust_relationships_count": len(trusts),
            "enabled_providers": sum(1 for p in providers if p.enabled),
            "federation_modes": [f.to_dict() for f in await self._tenant_feds.list_by_tenant(tenant_id)],
        })

    async def register_provider(
        self,
        tenant_id: str,
        *,
        protocol: str,
        name: str,
        config: dict | None = None,
        plugin_id: str | None = None,
        correlation_id: str | None = None,
    ) -> Result[dict]:
        params = await self._policy_params(tenant_id)
        if not params.get("federation_enabled", True):
            return Result.fail("federation.errors.disabled")
        plugin = federation_plugin_registry.resolve_plugin(protocol)
        provider = IdentityProvider.register(
            tenant_id=tenant_id,
            provider_ref=self._providers.next_provider_ref(tenant_id),
            protocol=protocol,
            name=name,
            config=config,
            plugin_id=plugin_id or (plugin.plugin_id if plugin else "builtin.custom"),
        )
        await self._providers.save(provider)
        await publish_integration_event(
            IdentityProviderRegisteredIntegration(
                tenant_id=TenantId(tenant_id),
                correlation_id=correlation_id or "",
                provider_ref=provider.provider_ref,
                protocol=protocol,
                name=name,
            )
        )
        return Result.ok(provider.to_dict())

    async def list_providers(self, tenant_id: str) -> Result[list[dict]]:
        items = await self._providers.list_by_tenant(tenant_id)
        return Result.ok([p.to_dict() for p in items])

    async def register_partner(
        self,
        tenant_id: str,
        *,
        name: str,
        partner_type: str = "organization",
        trust_level: str = "medium",
        metadata: dict | None = None,
    ) -> Result[dict]:
        partner = FederationPartner(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            partner_ref=self._partners.next_partner_ref(tenant_id),
            name=name,
            partner_type=partner_type,
            trust_level=trust_level,
            metadata=metadata or {},
        )
        await self._partners.save(partner)
        return Result.ok(partner.to_dict())

    async def create_trust_relationship(
        self,
        tenant_id: str,
        *,
        source_entity_type: str,
        source_entity_id: str,
        target_entity_type: str,
        target_entity_id: str,
        correlation_id: str | None = None,
    ) -> Result[dict]:
        trust_eval = trust_management_engine.compute_trust_score(partner_verified=True)
        trust = TrustRelationship(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            trust_ref=self._trusts.next_trust_ref(tenant_id),
            source_entity_type=source_entity_type,
            source_entity_id=source_entity_id,
            target_entity_type=target_entity_type,
            target_entity_id=target_entity_id,
            trust_score=trust_eval["trust_score"],
            trust_level=trust_eval["trust_level"],
        )
        await self._trusts.save(trust)
        await publish_integration_event(
            TrustRelationshipEstablishedIntegration(
                tenant_id=TenantId(tenant_id),
                correlation_id=correlation_id or "",
                trust_ref=trust.trust_ref,
                source_entity_id=source_entity_id,
                target_entity_id=target_entity_id,
                trust_score=trust.trust_score,
            )
        )
        return Result.ok(trust.to_dict())

    async def create_claims_mapping(
        self,
        tenant_id: str,
        *,
        provider_ref: str,
        source_claim: str,
        target_claim: str,
        transform_type: str = "direct",
        transform_config: dict | None = None,
        priority: int = 100,
    ) -> Result[dict]:
        provider = await self._providers.find_by_ref(tenant_id, provider_ref)
        if not provider:
            return Result.fail("federation.errors.provider_not_found")
        mapping = ClaimsMapping(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            mapping_ref=self._mappings.next_mapping_ref(tenant_id),
            provider_id=str(provider.id),
            source_claim=source_claim,
            target_claim=target_claim,
            transform_type=transform_type,
            transform_config=transform_config or {},
            priority=priority,
        )
        await self._mappings.save(mapping)
        return Result.ok(mapping.to_dict())

    async def transform_claims(
        self,
        tenant_id: str,
        *,
        provider_ref: str,
        raw_claims: dict,
    ) -> Result[dict]:
        provider = await self._providers.find_by_ref(tenant_id, provider_ref)
        if not provider:
            return Result.fail("federation.errors.provider_not_found")
        mappings = await self._mappings.list_by_provider(tenant_id, str(provider.id))
        transformed = claims_transformation_engine.transform_claims(
            raw_claims=raw_claims,
            mappings=[m.to_dict() for m in mappings],
        )
        return Result.ok({"transformed_claims": transformed, "provider_ref": provider_ref})

    async def discover_identity(
        self,
        tenant_id: str,
        *,
        email: str | None = None,
    ) -> Result[dict]:
        params = await self._policy_params(tenant_id)
        if not params.get("identity_discovery_enabled", True):
            return Result.fail("federation.errors.discovery_disabled")
        providers = [p.to_dict() for p in await self._providers.list_by_tenant(tenant_id)]
        return Result.ok(broker_engine.discover_identity_providers(email=email, tenant_id=tenant_id, providers=providers))

    async def broker_authenticate(
        self,
        tenant_id: str,
        *,
        email: str | None = None,
        provider_hint: str | None = None,
        raw_claims: dict | None = None,
        correlation_id: str | None = None,
    ) -> Result[dict]:
        params = await self._policy_params(tenant_id)
        if not params.get("broker_enabled", True):
            return Result.fail("federation.errors.broker_disabled")
        providers = [p.to_dict() for p in await self._providers.list_by_tenant(tenant_id)]
        route = broker_engine.route_authentication(
            tenant_id=tenant_id,
            email=email,
            hint=provider_hint,
            providers=providers,
        )
        if not route.get("routed"):
            return Result.fail("federation.errors.no_provider_routed")
        provider_dict = route["provider"]
        provider = await self._providers.find_by_ref(tenant_id, provider_dict["provider_ref"])
        if not provider:
            return Result.fail("federation.errors.provider_not_found")
        claims = raw_claims or {}
        mappings = await self._mappings.list_by_provider(tenant_id, str(provider.id))
        transformed = claims_transformation_engine.transform_claims(
            raw_claims=claims,
            mappings=[m.to_dict() for m in mappings],
        )
        brokered = broker_engine.broker_federation_flow(
            provider=provider.to_dict(),
            raw_claims=claims,
            transformed_claims=transformed,
        )
        session_ref = self._sessions.next_session_ref(tenant_id)
        session = FederationSession(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            session_ref=session_ref,
            provider_id=str(provider.id),
            protocol=provider.protocol,
            expires_at=datetime.now(UTC) + timedelta(hours=8),
        )
        await self._sessions.save(session)
        await publish_integration_event(
            IdentityFederatedIntegration(
                tenant_id=TenantId(tenant_id),
                correlation_id=correlation_id or "",
                user_id=brokered.get("external_subject") or "",
                provider_ref=provider.provider_ref,
                session_ref=session_ref,
                protocol=provider.protocol,
            )
        )
        return Result.ok({**brokered, "session_ref": session_ref, "routing_method": route["routing_method"]})

    async def link_identity(
        self,
        tenant_id: str,
        *,
        user_id: str,
        provider_ref: str,
        external_subject: str,
        correlation_id: str | None = None,
    ) -> Result[dict]:
        provider = await self._providers.find_by_ref(tenant_id, provider_ref)
        if not provider:
            return Result.fail("federation.errors.provider_not_found")
        link = IdentityLink(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            link_ref=self._links.next_link_ref(tenant_id),
            user_id=user_id,
            provider_id=str(provider.id),
            external_subject=external_subject,
        )
        await self._links.save(link)
        await publish_integration_event(
            IdentityLinkedIntegration(
                tenant_id=TenantId(tenant_id),
                correlation_id=correlation_id or "",
                user_id=user_id,
                provider_ref=provider_ref,
                external_subject=external_subject,
            )
        )
        return Result.ok(link.to_dict())

    async def provision_jit(
        self,
        tenant_id: str,
        *,
        provider_ref: str,
        claims: dict,
        correlation_id: str | None = None,
    ) -> Result[dict]:
        params = await self._policy_params(tenant_id)
        if not params.get("jit_provisioning_enabled", True):
            return Result.fail("federation.errors.jit_disabled")
        provider = await self._providers.find_by_ref(tenant_id, provider_ref)
        if not provider:
            return Result.fail("federation.errors.provider_not_found")
        policy = await self._prov_policies.find_by_provider(tenant_id, str(provider.id))
        decision = provisioning_engine.evaluate_jit_provisioning(
            jit_enabled=policy.jit_enabled if policy else True,
            claims=claims,
            rules=policy.rules if policy else [],
            default_roles=policy.default_roles if policy else [],
        )
        if not decision.get("provision"):
            return Result.fail(f"federation.errors.{decision.get('reason', 'provision_denied')}")
        user_id = claims.get("sub") or claims.get("email", "jit-user")
        await publish_integration_event(
            IdentityProvisionedIntegration(
                tenant_id=TenantId(tenant_id),
                correlation_id=correlation_id or "",
                user_id=str(user_id),
                provider_ref=provider_ref,
                provisioning_mode="jit",
            )
        )
        return Result.ok(decision)

    async def federated_logout(
        self,
        tenant_id: str,
        *,
        session_ref: str,
        user_id: str,
        correlation_id: str | None = None,
    ) -> Result[dict]:
        params = await self._policy_params(tenant_id)
        session = await self._sessions.find_by_ref(tenant_id, session_ref)
        if not session:
            return Result.fail("federation.errors.session_not_found")
        provider = None
        for p in await self._providers.list_by_tenant(tenant_id):
            if str(p.id) == session.provider_id:
                provider = p
                break
        logout = federation_engine.orchestrate_federated_logout(
            session_ref=session_ref,
            provider_protocol=session.protocol,
            single_logout_enabled=params.get("single_logout_enabled", True),
        )
        session.status = "logged_out"
        await self._sessions.save(session)
        if provider:
            await publish_integration_event(
                FederatedLogoutIntegration(
                    tenant_id=TenantId(tenant_id),
                    correlation_id=correlation_id or "",
                    session_ref=session_ref,
                    user_id=user_id,
                    provider_ref=provider.provider_ref,
                )
            )
        return Result.ok(logout)

    async def start_sync_job(
        self,
        tenant_id: str,
        *,
        provider_ref: str,
        direction: str = "inbound",
    ) -> Result[dict]:
        provider = await self._providers.find_by_ref(tenant_id, provider_ref)
        if not provider:
            return Result.fail("federation.errors.provider_not_found")
        job = SynchronizationJob(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            job_ref=self._sync_jobs.next_job_ref(tenant_id),
            provider_id=str(provider.id),
            direction=direction,
            status="running",
            started_at=datetime.now(UTC),
        )
        await self._sync_jobs.save(job)
        summary = provisioning_engine.sync_provisioning_action(direction=direction, records=[])
        job.status = "completed"
        job.completed_at = datetime.now(UTC)
        job.records_processed = summary["records_processed"]
        await self._sync_jobs.save(job)
        return Result.ok({**job.to_dict(), "summary": summary})

    async def configure_tenant_federation(
        self,
        tenant_id: str,
        *,
        federation_mode: str,
        partner_tenant_id: str | None = None,
        region: str | None = None,
        shared_providers: list[str] | None = None,
    ) -> Result[dict]:
        params = await self._policy_params(tenant_id)
        if federation_mode in ("shared", "cross_region") and not params.get("cross_tenant_enabled"):
            return Result.fail("federation.errors.cross_tenant_disabled")
        fed = TenantFederation(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            federation_ref=self._tenant_feds.next_federation_ref(tenant_id),
            federation_mode=federation_mode,
            partner_tenant_id=partner_tenant_id,
            region=region,
            shared_providers=shared_providers or [],
        )
        await self._tenant_feds.save(fed)
        return Result.ok(fed.to_dict())

    async def evaluate_trust(
        self,
        *,
        organization_trust: int = 50,
        partner_trust: int = 50,
        identity_trust: int = 50,
        device_trust: int = 50,
    ) -> Result[dict]:
        return Result.ok(
            trust_management_engine.evaluate_trust_hierarchy(
                organization_trust=organization_trust,
                partner_trust=partner_trust,
                identity_trust=identity_trust,
                device_trust=device_trust,
            )
        )

    def _issuer_base(self, tenant_id: str) -> str:
        return f"{settings.jwt_issuer.rstrip('/')}/tenants/{tenant_id}/federation"

    async def federation_login(
        self,
        tenant_id: str,
        *,
        protocol: str | None = None,
        email: str | None = None,
        provider_ref: str | None = None,
        client_id: str | None = None,
        redirect_uri: str | None = None,
        scope: str = "openid profile email",
        state: str = "",
        code_challenge: str | None = None,
        code_challenge_method: str | None = None,
        user_id: str | None = None,
        callback_code: str | None = None,
        callback_state: str | None = None,
        saml_response: str | None = None,
        relay_state: str | None = None,
        correlation_id: str | None = None,
    ) -> Result[dict]:
        params = await self._policy_params(tenant_id)
        if not params.get("federation_enabled", True):
            return Result.fail("federation.errors.disabled")
        negotiation = protocol_engine.negotiate_protocol(requested=protocol)
        negotiated = negotiation["negotiated_protocol"]
        federation_protocol_metrics.increment("federation_login_total")

        if callback_code and negotiated in ("oidc", "oauth2"):
            bridge_result = await self._bridge.complete_oidc_callback(
                tenant_id=tenant_id,
                code=callback_code,
                state=callback_state or "",
                correlation_id=correlation_id or "",
            )
            if bridge_result.get("error"):
                await publish_integration_event(
                    ExternalAuthenticationFailedIntegration(
                        tenant_id=TenantId(tenant_id),
                        correlation_id=correlation_id or "",
                        protocol=negotiated,
                        reason=str(bridge_result["error"]),
                    )
                )
                return Result.fail(bridge_result["error"])
            raw_claims = bridge_result.get("claims") or bridge_result.get("user") or {}
            provider = provider_ref or bridge_result.get("provider_ref")
            if provider and raw_claims:
                broker = await self.broker_authenticate(
                    tenant_id,
                    email=raw_claims.get("email"),
                    provider_hint=provider,
                    raw_claims=raw_claims,
                    correlation_id=correlation_id,
                )
                if broker.succeeded:
                    federation_protocol_metrics.increment("federation_sso_total")
                    await publish_integration_event(
                        ExternalAuthenticationSucceededIntegration(
                            tenant_id=TenantId(tenant_id),
                            correlation_id=correlation_id or "",
                            user_id=broker.unwrap().get("external_subject", ""),
                            protocol=negotiated,
                            provider_ref=provider,
                        )
                    )
                return broker
            return Result.ok({"authenticated": True, "protocol": negotiated, **bridge_result})

        if saml_response and negotiated == "saml":
            bridge_result = await self._bridge.complete_saml_acs(
                saml_response=saml_response,
                relay_state=relay_state or "",
                correlation_id=correlation_id or "",
            )
            if bridge_result.get("error"):
                await publish_integration_event(
                    ExternalAuthenticationFailedIntegration(
                        tenant_id=TenantId(tenant_id),
                        correlation_id=correlation_id or "",
                        protocol="saml",
                        reason=str(bridge_result["error"]),
                    )
                )
                return Result.fail(bridge_result["error"])
            federation_protocol_metrics.increment("federation_sso_total")
            return Result.ok({"authenticated": True, "protocol": "saml", **bridge_result})

        if negotiated in ("oidc", "oauth2", "saml") and (provider_ref or email):
            resolved_ref = provider_ref
            if not resolved_ref and email:
                discovery = broker_engine.discover_identity_providers(
                    email=email,
                    tenant_id=tenant_id,
                    providers=[p.to_dict() for p in await self._providers.list_by_tenant(tenant_id)],
                )
                recommended = discovery.get("recommended_provider") or {}
                resolved_ref = recommended.get("provider_ref")
            if not resolved_ref:
                return Result.fail("federation.errors.no_provider_routed")
            provider = await self._providers.find_by_ref(tenant_id, resolved_ref)
            if not provider:
                return Result.fail("federation.errors.provider_not_found")
            if provider.protocol in ("oidc", "oauth2"):
                bridge_result = await self._bridge.begin_oidc_login(
                    tenant_id=tenant_id, provider_ref=resolved_ref
                )
            else:
                bridge_result = await self._bridge.begin_saml_login(
                    tenant_id=tenant_id, provider_ref=resolved_ref
                )
            if bridge_result.get("error"):
                return Result.fail(bridge_result["error"])
            return Result.ok(
                {
                    "protocol": provider.protocol,
                    "provider_ref": resolved_ref,
                    "negotiation": negotiation,
                    **bridge_result,
                }
            )

        if client_id and redirect_uri and negotiated in ("oidc", "oauth2"):
            auth = self._oauth2.authorize(
                tenant_id=tenant_id,
                client_id=client_id,
                redirect_uri=redirect_uri,
                scope=scope,
                state=state,
                code_challenge=code_challenge,
                code_challenge_method=code_challenge_method,
                user_id=user_id,
            )
            if auth.get("error"):
                return Result.fail(auth["error"])
            return Result.ok({"protocol": negotiated, "mode": "authorization_server", **auth})

        return Result.fail("federation.errors.login_parameters_invalid")

    async def federation_logout_gateway(
        self,
        tenant_id: str,
        *,
        session_ref: str | None = None,
        id_token_hint: str | None = None,
        post_logout_redirect_uri: str | None = None,
        correlation_id: str | None = None,
    ) -> Result[dict]:
        params = await self._policy_params(tenant_id)
        if not params.get("single_logout_enabled", True):
            return Result.fail("federation.errors.single_logout_disabled")
        if session_ref:
            return await self.federated_logout(
                tenant_id,
                session_ref=session_ref,
                user_id="",
                correlation_id=correlation_id,
            )
        return Result.ok(
            {
                "logged_out": True,
                "end_session_endpoint": f"{self._issuer_base(tenant_id)}/logout",
                "id_token_hint_received": bool(id_token_hint),
                "post_logout_redirect_uri": post_logout_redirect_uri,
            }
        )

    async def federation_token(
        self,
        tenant_id: str,
        *,
        grant_type: str,
        client_id: str,
        client_secret: str | None = None,
        code: str | None = None,
        redirect_uri: str | None = None,
        code_verifier: str | None = None,
        refresh_token: str | None = None,
        scope: str | None = None,
        user_id: str | None = None,
        nonce: str | None = None,
        correlation_id: str | None = None,
    ) -> Result[dict]:
        params = await self._policy_params(tenant_id)
        if not params.get("federation_enabled", True):
            return Result.fail("federation.errors.disabled")
        token_result = self._oauth2.token(
            tenant_id=tenant_id,
            grant_type=grant_type,
            client_id=client_id,
            client_secret=client_secret,
            code=code,
            redirect_uri=redirect_uri,
            code_verifier=code_verifier,
            refresh_token=refresh_token,
            scope=scope,
            user_id=user_id,
        )
        if token_result.get("error"):
            return Result.fail(token_result.get("error_description") or token_result["error"])
        federation_protocol_metrics.increment("federation_token_total")
        if "openid" in (scope or token_result.get("scope", "")):
            sub = user_id or "user"
            token_result["id_token"] = self._oidc.id_token(
                sub=sub,
                tenant_id=tenant_id,
                client_id=client_id,
                nonce=nonce,
            )
        await publish_integration_event(
            TokenExchangedIntegration(
                tenant_id=TenantId(tenant_id),
                correlation_id=correlation_id or "",
                client_id=client_id,
                grant_type=grant_type,
            )
        )
        return Result.ok(token_result)

    async def federation_introspect(self, tenant_id: str, *, token: str) -> Result[dict]:
        return Result.ok(self._oauth2.introspect(token=token))

    async def federation_revoke(
        self,
        tenant_id: str,
        *,
        token: str,
        token_type_hint: str | None = None,
    ) -> Result[dict]:
        return Result.ok(self._oauth2.revoke(token=token, token_type_hint=token_type_hint))

    async def federation_provision(
        self,
        tenant_id: str,
        *,
        resource_type: str,
        operation: str,
        payload: dict | None = None,
        resource_id: str | None = None,
        correlation_id: str | None = None,
    ) -> Result[dict]:
        params = await self._policy_params(tenant_id)
        if not params.get("jit_provisioning_enabled", True):
            return Result.fail("federation.errors.provisioning_disabled")
        payload = payload or {}
        federation_protocol_metrics.increment("federation_scim_total")
        if resource_type == "User":
            if operation == "create":
                user = self._scim.create_user(tenant_id=tenant_id, payload=payload)
                await publish_integration_event(
                    IdentityProvisionedIntegration(
                        tenant_id=TenantId(tenant_id),
                        correlation_id=correlation_id or "",
                        user_id=user["id"],
                        provider_ref="scim",
                        provisioning_mode="scim",
                    )
                )
                return Result.ok(user)
            if operation == "patch" and resource_id:
                user = self._scim.patch_user(
                    tenant_id=tenant_id, user_id=resource_id, operations=payload.get("Operations", [])
                )
                if not user:
                    return Result.fail("federation.errors.resource_not_found")
                return Result.ok(user)
            if operation == "delete" and resource_id:
                ok = self._scim.delete_user(tenant_id=tenant_id, user_id=resource_id)
                return Result.ok({"deleted": ok}) if ok else Result.fail("federation.errors.resource_not_found")
        if resource_type == "Group" and operation == "create":
            return Result.ok(self._scim.create_group(tenant_id=tenant_id, payload=payload))
        if operation == "bulk":
            return Result.ok(self._scim.bulk(tenant_id=tenant_id, operations=payload.get("Operations", [])))
        return Result.fail("federation.errors.unsupported_provision_operation")

    async def federation_sync_gateway(
        self,
        tenant_id: str,
        *,
        provider_ref: str,
        connector_ref: str | None = None,
    ) -> Result[dict]:
        params = await self._policy_params(tenant_id)
        if not params.get("federation_enabled", True):
            return Result.fail("federation.errors.disabled")
        provider = await self._providers.find_by_ref(tenant_id, provider_ref)
        if not provider:
            return Result.fail("federation.errors.provider_not_found")
        if provider.protocol in ("ldap", "ldaps", "ad"):
            bridge_result = await self._bridge.ldap_sync(
                tenant_id=tenant_id,
                connector_ref=connector_ref or provider_ref,
            )
            if bridge_result.get("error"):
                return Result.fail(bridge_result["error"])
            return Result.ok(bridge_result)
        return await self.start_sync_job(tenant_id, provider_ref=provider_ref, direction="inbound")

    async def oidc_discovery(self, tenant_id: str) -> Result[dict]:
        issuer = self._issuer_base(tenant_id)
        return Result.ok(self._oidc.discovery(issuer=issuer))

    async def oidc_jwks(self, tenant_id: str) -> Result[dict]:
        return Result.ok(self._certs.jwks_for_tenant(tenant_id=tenant_id))

    async def identity_providers_public(self, tenant_id: str) -> Result[list[dict]]:
        providers = await self._providers.list_by_tenant(tenant_id)
        return Result.ok(
            [
                {
                    "provider_ref": p.provider_ref,
                    "name": p.name,
                    "protocol": p.protocol,
                    "enabled": p.enabled,
                }
                for p in providers
                if p.enabled
            ]
        )

    async def identity_claims_catalog(self, tenant_id: str) -> Result[dict]:
        providers = await self._providers.list_by_tenant(tenant_id)
        mapped: list[dict] = []
        for provider in providers:
            for mapping in await self._mappings.list_by_provider(tenant_id, str(provider.id)):
                mapped.append({"source": mapping.source_claim, "target": mapping.target_claim})
        return Result.ok(
            {
                "standard_claims": ["sub", "email", "name", "preferred_username", "tenant_id"],
                "mapped_claims": mapped,
            }
        )

    async def identity_metadata(self, tenant_id: str) -> Result[dict]:
        profile = await self._profiles.find_by_tenant(tenant_id)
        return Result.ok(
            {
                "tenant_id": tenant_id,
                "issuer": self._issuer_base(tenant_id),
                "profile": profile.to_dict() if profile else {},
                "protocol_catalog": protocol_engine.build_protocol_catalog(),
                "capabilities": federation_engine.build_federation_catalog(),
            }
        )

    async def register_oauth_client(
        self,
        tenant_id: str,
        *,
        client_name: str,
        redirect_uris: list[str],
        grant_types: list[str] | None = None,
        scopes: list[str] | None = None,
        require_pkce: bool = True,
    ) -> Result[dict]:
        return Result.ok(
            self._oauth2.register_client(
                tenant_id=tenant_id,
                client_name=client_name,
                redirect_uris=redirect_uris,
                grant_types=grant_types,
                scopes=scopes,
                require_pkce=require_pkce,
            )
        )

    async def rotate_certificates(
        self,
        tenant_id: str,
        *,
        correlation_id: str | None = None,
    ) -> Result[dict]:
        rotation = self._certs.rotate_jwks(tenant_id=tenant_id)
        await publish_integration_event(
            CertificateRotatedIntegration(
                tenant_id=TenantId(tenant_id),
                correlation_id=correlation_id or "",
                cert_ref="jwks",
                kid=rotation["new_kid"],
            )
        )
        return Result.ok(rotation)

    async def map_claims_and_publish(
        self,
        tenant_id: str,
        *,
        provider_ref: str,
        raw_claims: dict,
        correlation_id: str | None = None,
    ) -> Result[dict]:
        result = await self.transform_claims(tenant_id, provider_ref=provider_ref, raw_claims=raw_claims)
        if result.succeeded:
            await publish_integration_event(
                ClaimsMappedIntegration(
                    tenant_id=TenantId(tenant_id),
                    correlation_id=correlation_id or "",
                    provider_ref=provider_ref,
                    claims_count=len(result.unwrap().get("transformed_claims", {})),
                )
            )
        return result

    async def protocol_metrics_snapshot(self) -> Result[dict]:
        return Result.ok(federation_protocol_metrics.snapshot())
