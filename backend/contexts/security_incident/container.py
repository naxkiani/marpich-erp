"""Enterprise Security Incident Platform DI + event subscriptions."""
from __future__ import annotations

from contexts.policy.container import get_policy_evaluator
from contexts.security_incident.application.service import SecurityIncidentApplicationService
from contexts.security_incident.infrastructure.persistence.incident_memory_store import (
    InMemoryIncidentEvidenceRepository,
    InMemoryIncidentLessonLearnedRepository,
    InMemoryIncidentNotificationRepository,
    InMemoryIncidentTenantProfileRepository,
    InMemorySecurityIncidentRepository,
)
from shared.infrastructure.messaging.event_bus import InProcessEventBus

_service: SecurityIncidentApplicationService | None = None
_registered = False


def get_security_incident_service() -> SecurityIncidentApplicationService:
    global _service, _registered
    if _service is None:
        _service = SecurityIncidentApplicationService(
            profiles=InMemoryIncidentTenantProfileRepository(),
            incidents=InMemorySecurityIncidentRepository(),
            evidence=InMemoryIncidentEvidenceRepository(),
            notifications=InMemoryIncidentNotificationRepository(),
            lessons=InMemoryIncidentLessonLearnedRepository(),
            policy_evaluator=get_policy_evaluator(),
        )
    if not _registered:
        InProcessEventBus.subscribe(
            "platform.tenant.provisioned",
            _service.handle_tenant_provisioned,
        )
        InProcessEventBus.subscribe(
            "security.attack.detected",
            _service.handle_security_attack_detected,
        )
        _registered = True
    return _service


def reset_security_incident_service() -> None:
    global _service, _registered
    _service = None
    _registered = False
    InMemoryIncidentTenantProfileRepository.reset()
    InMemorySecurityIncidentRepository.reset()
    InMemoryIncidentEvidenceRepository.reset()
    InMemoryIncidentNotificationRepository.reset()
    InMemoryIncidentLessonLearnedRepository.reset()
