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
from contexts.identity_federation.infrastructure.persistence.postgres_store import (
    PostgresClaimsMappingRepository,
    PostgresFederationSessionRepository,
    PostgresIdentityLinkRepository,
    PostgresIdentityProviderRepository,
    PostgresTrustRelationshipRepository,
)
from contexts.identity_federation.infrastructure.protocols.oauth2_server import OAuth2AuthorizationServer
from contexts.identity_federation.infrastructure.protocols.oidc_provider import OidcProvider
from contexts.identity_federation.infrastructure.protocols.scim_server import ScimServer
from contexts.policy.container import get_policy_evaluator
from shared.infrastructure.messaging.event_bus import InProcessEventBus
from shared.infrastructure.settings import use_postgres

_service: IdentityFederationApplicationService | None = None
_fabric: FabricSecurityApplicationService | None = None
_intel: FabricIntelligenceApplicationService | None = None
_ai: IdentityFederationAIService | None = None
_registered = False

_providers = None
_partners = None
_trusts = None
_sessions = None
_tenant_feds = None
_mappings = None
_links = None


def _ensure_sor_repos() -> None:
    global _providers, _partners, _trusts, _sessions, _tenant_feds, _mappings, _links
    if _providers is not None:
        return
    if use_postgres():
        _providers = PostgresIdentityProviderRepository()
        _trusts = PostgresTrustRelationshipRepository()
        _sessions = PostgresFederationSessionRepository()
        _mappings = PostgresClaimsMappingRepository()
        _links = PostgresIdentityLinkRepository()
    else:
        _providers = InMemoryIdentityProviderRepository()
        _trusts = InMemoryTrustRelationshipRepository()
        _sessions = InMemoryFederationSessionRepository()
        _mappings = InMemoryClaimsMappingRepository()
        _links = InMemoryIdentityLinkRepository()
    _partners = InMemoryFederationPartnerRepository()
    _tenant_feds = InMemoryTenantFederationRepository()


def get_identity_federation_service() -> IdentityFederationApplicationService:
    global _service, _registered
    _ensure_sor_repos()
    if _service is None:
        _service = IdentityFederationApplicationService(
            profiles=InMemoryFederationProfileRepository(),
            providers=_providers,
            partners=_partners,
            trusts=_trusts,
            mappings=_mappings,
            links=_links,
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
    _ensure_sor_repos()
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
    _ensure_sor_repos()
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
    global _providers, _partners, _trusts, _sessions, _tenant_feds, _mappings, _links
    _service = None
    _fabric = None
    _intel = None
    _ai = None
    _registered = False
    _providers = None
    _partners = None
    _trusts = None
    _sessions = None
    _tenant_feds = None
    _mappings = None
    _links = None
    InMemoryFederationStore.reset()
    PostgresIdentityProviderRepository.reset_counters()
    PostgresTrustRelationshipRepository.reset_counters()
    PostgresClaimsMappingRepository.reset_counters()
    PostgresIdentityLinkRepository.reset_counters()
    PostgresFederationSessionRepository.reset_counters()
    OAuth2AuthorizationServer.reset()
    ScimServer.reset()
    CertificateManager.reset()
    federation_protocol_metrics.reset()
    federation_ai_metrics.reset()
    reset_fabric_security_state()
