"""Enterprise Scheduler DI + event subscriptions."""
from __future__ import annotations

from contexts.enterprise_scheduler.application.service import EnterpriseSchedulerApplicationService
from contexts.enterprise_scheduler.infrastructure.persistence.enterprise_scheduler_memory_store import (
    InMemoryJobDependencyRepository,
    InMemoryJobExecutionRepository,
    InMemoryScheduledJobRepository,
    InMemorySchedulerProfileRepository,
)
from contexts.policy.container import get_policy_evaluator
from shared.infrastructure.messaging.event_bus import InProcessEventBus

_service: EnterpriseSchedulerApplicationService | None = None
_registered = False


def get_enterprise_scheduler_service() -> EnterpriseSchedulerApplicationService:
    global _service, _registered
    if _service is None:
        _service = EnterpriseSchedulerApplicationService(
            profiles=InMemorySchedulerProfileRepository(),
            jobs=InMemoryScheduledJobRepository(),
            dependencies=InMemoryJobDependencyRepository(),
            executions=InMemoryJobExecutionRepository(),
            policy_evaluator=get_policy_evaluator(),
        )
    if not _registered:
        InProcessEventBus.subscribe("platform.tenant.provisioned", _service.handle_tenant_provisioned)
        _registered = True
    return _service


def reset_enterprise_scheduler_service() -> None:
    global _service, _registered
    _service = None
    _registered = False
    InMemorySchedulerProfileRepository.reset()
    InMemoryScheduledJobRepository.reset()
    InMemoryJobDependencyRepository.reset()
    InMemoryJobExecutionRepository.reset()
