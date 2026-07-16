"""Enterprise Integration Studio DI + event subscriptions."""
from __future__ import annotations

from contexts.enterprise_integration_studio.application.service import EnterpriseIntegrationStudioApplicationService
from contexts.enterprise_integration_studio.infrastructure.persistence.enterprise_integration_studio_memory_store import (
    InMemoryMarketplaceListingRepository,
    InMemoryStudioArtifactRepository,
    InMemoryStudioDeploymentRepository,
    InMemoryStudioProfileRepository,
    InMemoryStudioProjectRepository,
    InMemoryStudioTestRunRepository,
    InMemoryStudioVersionRepository,
)
from contexts.policy.container import get_policy_evaluator
from shared.infrastructure.messaging.event_bus import InProcessEventBus

_service: EnterpriseIntegrationStudioApplicationService | None = None
_registered = False


def get_enterprise_integration_studio_service() -> EnterpriseIntegrationStudioApplicationService:
    global _service, _registered
    if _service is None:
        _service = EnterpriseIntegrationStudioApplicationService(
            profiles=InMemoryStudioProfileRepository(),
            projects=InMemoryStudioProjectRepository(),
            artifacts=InMemoryStudioArtifactRepository(),
            versions=InMemoryStudioVersionRepository(),
            deployments=InMemoryStudioDeploymentRepository(),
            tests=InMemoryStudioTestRunRepository(),
            marketplace=InMemoryMarketplaceListingRepository(),
            policy_evaluator=get_policy_evaluator(),
        )
    if not _registered:
        InProcessEventBus.subscribe("platform.tenant.provisioned", _service.handle_tenant_provisioned)
        _registered = True
    return _service


def reset_enterprise_integration_studio_service() -> None:
    global _service, _registered
    _service = None
    _registered = False
    InMemoryStudioProfileRepository.reset()
    InMemoryStudioProjectRepository.reset()
    InMemoryStudioArtifactRepository.reset()
    InMemoryStudioVersionRepository.reset()
    InMemoryStudioDeploymentRepository.reset()
    InMemoryStudioTestRunRepository.reset()
    InMemoryMarketplaceListingRepository.reset()
