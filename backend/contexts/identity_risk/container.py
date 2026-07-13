"""Identity risk DI container."""
from __future__ import annotations

from contexts.identity_risk.application.service import IdentityRiskApplicationService
from contexts.identity_risk.infrastructure.persistence.identity_risk_memory_store import (
    InMemoryAnomalyAlertRepository,
    InMemoryIdentityRiskStore,
    InMemoryRiskProfileRepository,
    InMemoryRiskScoreRepository,
    InMemoryRiskSignalRepository,
)
from contexts.policy.container import get_policy_evaluator
from shared.infrastructure.messaging.event_bus import InProcessEventBus

_service: IdentityRiskApplicationService | None = None
_registered = False


def get_identity_risk_service() -> IdentityRiskApplicationService:
    global _service, _registered
    if _service is None:
        _service = IdentityRiskApplicationService(
            profiles=InMemoryRiskProfileRepository(),
            signals=InMemoryRiskSignalRepository(),
            scores=InMemoryRiskScoreRepository(),
            alerts=InMemoryAnomalyAlertRepository(),
            policy_evaluator=get_policy_evaluator(),
        )
    if not _registered:
        bus = InProcessEventBus
        bus.subscribe("platform.tenant.provisioned", _service.handle_tenant_provisioned)
        bus.subscribe("authentication.login.success", _service.handle_authentication_login_success)
        bus.subscribe("directory.sync.completed", _service.handle_directory_sync_completed)
        bus.subscribe("integration.directory.synced", _service.handle_directory_sync_completed)
        bus.subscribe("directory.scim.user.provisioned", _service.handle_scim_user_provisioned)
        _registered = True
    return _service


def reset_identity_risk_service() -> None:
    global _service, _registered
    _service = None
    _registered = False
    InMemoryIdentityRiskStore.reset()
