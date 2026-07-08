"""Enterprise Risk Platform DI + event subscriptions."""
from __future__ import annotations

from contexts.policy.container import get_policy_evaluator
from contexts.risk.application.service import RiskApplicationService
from contexts.risk.infrastructure.persistence.risk_memory_store import (
    InMemoryEnterpriseRiskItemRepository,
    InMemoryRiskMatrixSnapshotRepository,
    InMemoryRiskPredictionRepository,
    InMemoryRiskTenantProfileRepository,
)
from shared.infrastructure.messaging.event_bus import InProcessEventBus

_service: RiskApplicationService | None = None
_registered = False


def get_risk_service() -> RiskApplicationService:
    global _service, _registered
    if _service is None:
        _service = RiskApplicationService(
            profiles=InMemoryRiskTenantProfileRepository(),
            risks=InMemoryEnterpriseRiskItemRepository(),
            matrices=InMemoryRiskMatrixSnapshotRepository(),
            predictions=InMemoryRiskPredictionRepository(),
            policy_evaluator=get_policy_evaluator(),
        )
    if not _registered:
        InProcessEventBus.subscribe(
            "platform.tenant.provisioned",
            _service.handle_tenant_provisioned,
        )
        _registered = True
    return _service


def reset_risk_service() -> None:
    global _service, _registered
    _service = None
    _registered = False
    InMemoryRiskTenantProfileRepository.reset()
    InMemoryEnterpriseRiskItemRepository.reset()
    InMemoryRiskMatrixSnapshotRepository.reset()
    InMemoryRiskPredictionRepository.reset()
