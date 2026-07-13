"""Identity resilience DI container."""
from __future__ import annotations

from contexts.identity_resilience.application.service import IdentityResilienceApplicationService
from contexts.identity_resilience.infrastructure.adapters.worker_delegates import (
    DirectoryWorkerAdapter,
    RiskWorkerAdapter,
)
from contexts.identity_resilience.infrastructure.persistence.identity_resilience_memory_store import (
    InMemoryFailoverEventRepository,
    InMemoryIdentityResilienceStore,
    InMemoryRegionRepository,
    InMemoryResilienceProfileRepository,
    InMemoryWorkerDeploymentRepository,
)
from contexts.policy.container import get_policy_evaluator
from shared.infrastructure.messaging.event_bus import InProcessEventBus

_service: IdentityResilienceApplicationService | None = None
_registered = False


def get_identity_resilience_service() -> IdentityResilienceApplicationService:
    global _service, _registered
    if _service is None:
        _service = IdentityResilienceApplicationService(
            profiles=InMemoryResilienceProfileRepository(),
            regions=InMemoryRegionRepository(),
            workers=InMemoryWorkerDeploymentRepository(),
            failovers=InMemoryFailoverEventRepository(),
            directory_workers=DirectoryWorkerAdapter(),
            risk_workers=RiskWorkerAdapter(),
            policy_evaluator=get_policy_evaluator(),
        )
    if not _registered:
        bus = InProcessEventBus
        bus.subscribe("platform.tenant.provisioned", _service.handle_tenant_provisioned)
        bus.subscribe("directory.sync.completed", _service.handle_worker_activity)
        bus.subscribe("identity_risk.score.computed", _service.handle_worker_activity)
        _registered = True
    return _service


def reset_identity_resilience_service() -> None:
    global _service, _registered
    _service = None
    _registered = False
    InMemoryIdentityResilienceStore.reset()
