"""Enterprise Business Continuity Platform DI + event subscriptions."""
from __future__ import annotations

from contexts.business_continuity.application.service import BusinessContinuityApplicationService
from contexts.business_continuity.infrastructure.persistence.continuity_memory_store import (
    InMemoryBackupStrategyRepository,
    InMemoryContinuityPlanRepository,
    InMemoryContinuityTenantProfileRepository,
    InMemoryFailoverRecordRepository,
    InMemoryRecoveryTestRepository,
)
from contexts.policy.container import get_policy_evaluator
from shared.infrastructure.messaging.event_bus import InProcessEventBus

_service: BusinessContinuityApplicationService | None = None
_registered = False


def get_business_continuity_service() -> BusinessContinuityApplicationService:
    global _service, _registered
    if _service is None:
        _service = BusinessContinuityApplicationService(
            profiles=InMemoryContinuityTenantProfileRepository(),
            plans=InMemoryContinuityPlanRepository(),
            backups=InMemoryBackupStrategyRepository(),
            failovers=InMemoryFailoverRecordRepository(),
            tests=InMemoryRecoveryTestRepository(),
            policy_evaluator=get_policy_evaluator(),
        )
    if not _registered:
        InProcessEventBus.subscribe(
            "platform.tenant.provisioned",
            _service.handle_tenant_provisioned,
        )
        _registered = True
    return _service


def reset_business_continuity_service() -> None:
    global _service, _registered
    _service = None
    _registered = False
    InMemoryContinuityTenantProfileRepository.reset()
    InMemoryContinuityPlanRepository.reset()
    InMemoryBackupStrategyRepository.reset()
    InMemoryFailoverRecordRepository.reset()
    InMemoryRecoveryTestRepository.reset()
