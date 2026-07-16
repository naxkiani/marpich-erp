"""Identity Federation DI container."""
from __future__ import annotations

from contexts.identity_federation.application.ai_service import IdentityFederationAIService
from contexts.identity_federation.application.fabric_intelligence_service import (
    FabricIntelligenceApplicationService,
)
from contexts.identity_federation.application.fabric_security_service import (
    FabricSecurityApplicationService,
    reset_fabric_security_state,
)
from contexts.identity_federation.application.service import IdentityFederationApplicationService
from contexts.identity_federation.infrastructure.adapters.adaptive_auth_acl import AdaptiveAuthAcl
from contexts.identity_federation.infrastructure.adapters.identity_risk_acl import IdentityRiskAcl
from contexts.identity_federation.infrastructure.adapters.protocol_bridge_adapter import ProtocolBridgeAdapter
from contexts.identity_federation.infrastructure.certificates.certificate_manager import CertificateManager
from contexts.identity_federation.infrastructure.observability import federation_ai_metrics
from contexts.identity_federation.infrastructure.observability import federation_protocol_metrics
from contexts.identity_federation.infrastructure.persistence.federation_memory_store import (
    InMemoryClaimsMappingRepository,
    InMemoryFederationPartnerRepository,
    InMemoryFederationProfileRepository,
    InMemoryFederationSessionRepository,
    InMemoryFederationStore,
    InMemoryIdentityLinkRepository,
    InMemoryIdentityProviderRepository,
    InMemoryProvisioningPolicyRepository,
    InMemorySynchronizationJobRepository,
    InMemoryTenantFederationRepository,
    InMemoryTrustRelationshipRepository,
)
from contexts.identity_federation.infrastructure.protocols.oauth2_server import OAuth2AuthorizationServer
from contexts.identity_federation.infrastructure.protocols.oidc_provider import OidcProvider
from contexts.identity_federation.infrastructure.protocols.scim_server import ScimServer
from contexts.policy.container import get_policy_evaluator
from shared.infrastructure.messaging.event_bus import InProcessEventBus

_service: IdentityFederationApplicationService | None = None
_fabric: FabricSecurityApplicationService | None = None
_intel: FabricIntelligenceApplicationService | None = None
_ai: IdentityFederationAIService | None = None
_registered = False

_providers = InMemoryIdentityProviderRepository()
_partners = InMemoryFederationPartnerRepository()
_trusts = InMemoryTrustRelationshipRepository()
_sessions = InMemoryFederationSessionRepository()
_tenant_feds = InMemoryTenantFederationRepository()
_mappings = InMemoryClaimsMappingRepository()


def get_identity_federation_service() -> IdentityFederationApplicationService:
    global _service, _registered
    if _service is None:
        _service = IdentityFederationApplicationService(
            profiles=InMemoryFederationProfileRepository(),
            providers=_providers,
            partners=_partners,
            trusts=_trusts,
            mappings=_mappings,
            links=InMemoryIdentityLinkRepository(),
            prov_policies=InMemoryProvisioningPolicyRepository(),
            sync_jobs=InMemorySynchronizationJobRepository(),
            sessions=_sessions,
            tenant_feds=_tenant_feds,
            policy_evaluator=get_policy_evaluator(),
            oauth2=OAuth2AuthorizationServer(),
            oidc=OidcProvider(),
            scim=ScimServer(),
            cert_manager=CertificateManager(),
            protocol_bridge=ProtocolBridgeAdapter(),
        )
    if not _registered:
        InProcessEventBus.subscribe("platform.tenant.provisioned", _service.handle_tenant_provisioned)
        _registered = True
    return _service


def get_fabric_security_service() -> FabricSecurityApplicationService:
    global _fabric
    get_identity_federation_service()
    if _fabric is None:
        _fabric = FabricSecurityApplicationService(
            providers=_providers,
            partners=_partners,
            trusts=_trusts,
            sessions=_sessions,
            tenant_feds=_tenant_feds,
            policy_evaluator=get_policy_evaluator(),
            adaptive_acl=AdaptiveAuthAcl(),
            risk_acl=IdentityRiskAcl(),
        )
    return _fabric


def get_fabric_intelligence_service() -> FabricIntelligenceApplicationService:
    global _intel
    get_identity_federation_service()
    if _intel is None:
        _intel = FabricIntelligenceApplicationService(
            providers=_providers,
            partners=_partners,
            trusts=_trusts,
            sessions=_sessions,
            mappings=_mappings,
            policy_evaluator=get_policy_evaluator(),
        )
    return _intel


def get_identity_federation_ai_service() -> IdentityFederationAIService:
    global _ai
    if _ai is None:
        _ai = IdentityFederationAIService(get_fabric_intelligence_service())
    return _ai


def reset_identity_federation_service() -> None:
    global _service, _fabric, _intel, _ai, _registered
    _service = None
    _fabric = None
    _intel = None
    _ai = None
    _registered = False
    InMemoryFederationStore.reset()
    OAuth2AuthorizationServer.reset()
    ScimServer.reset()
    CertificateManager.reset()
    federation_protocol_metrics.reset()
    federation_ai_metrics.reset()
    reset_fabric_security_state()
