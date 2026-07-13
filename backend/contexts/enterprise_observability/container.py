"""Enterprise Observability DI + event subscriptions."""
from __future__ import annotations

from contexts.enterprise_observability.application.service import EnterpriseObservabilityApplicationService
from contexts.enterprise_observability.infrastructure.persistence.enterprise_observability_memory_store import (
    InMemoryHealthCheckResultRepository,
    InMemoryLogEntryRepository,
    InMemoryMetricSnapshotRepository,
    InMemoryMonitoringAlertRepository,
    InMemoryObservabilityIncidentRepository,
    InMemoryObservabilityProfileRepository,
    InMemoryTraceSpanRepository,
)
from contexts.policy.container import get_policy_evaluator
from shared.infrastructure.messaging.event_bus import InProcessEventBus

_service: EnterpriseObservabilityApplicationService | None = None
_registered = False


def get_enterprise_observability_service() -> EnterpriseObservabilityApplicationService:
    global _service, _registered
    if _service is None:
        _service = EnterpriseObservabilityApplicationService(
            profiles=InMemoryObservabilityProfileRepository(),
            traces=InMemoryTraceSpanRepository(),
            logs=InMemoryLogEntryRepository(),
            metrics=InMemoryMetricSnapshotRepository(),
            health_checks=InMemoryHealthCheckResultRepository(),
            alerts=InMemoryMonitoringAlertRepository(),
            incidents=InMemoryObservabilityIncidentRepository(),
            policy_evaluator=get_policy_evaluator(),
        )
    if not _registered:
        InProcessEventBus.subscribe("platform.tenant.provisioned", _service.handle_tenant_provisioned)
        _registered = True
    return _service


def reset_enterprise_observability_service() -> None:
    global _service, _registered
    _service = None
    _registered = False
    InMemoryObservabilityProfileRepository.reset()
    InMemoryTraceSpanRepository.reset()
    InMemoryLogEntryRepository.reset()
    InMemoryMetricSnapshotRepository.reset()
    InMemoryHealthCheckResultRepository.reset()
    InMemoryMonitoringAlertRepository.reset()
    InMemoryObservabilityIncidentRepository.reset()
