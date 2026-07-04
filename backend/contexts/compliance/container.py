"""Compliance DI + event subscriptions."""
from __future__ import annotations

from contexts.compliance.application.service import ComplianceApplicationService
from contexts.compliance.infrastructure.persistence.memory_store import (
    InMemoryComplianceControlRepository,
    InMemoryComplianceReportRepository,
    InMemoryComplianceViolationRepository,
)
from shared.infrastructure.messaging.event_bus import InProcessEventBus

_service: ComplianceApplicationService | None = None
_registered = False


def get_compliance_service() -> ComplianceApplicationService:
    global _service, _registered
    if _service is None:
        _service = ComplianceApplicationService(
            controls=InMemoryComplianceControlRepository(),
            violations=InMemoryComplianceViolationRepository(),
            reports=InMemoryComplianceReportRepository(),
        )
    if not _registered:
        InProcessEventBus.subscribe(
            "platform.tenant.provisioned",
            _service.handle_tenant_provisioned,
        )
        for event_name in (
            "policy.evaluation.denied",
            "authorization.access.denied",
            "identity.login.failed",
            "audit.retention.applied",
            "hospital.patient.accessed",
            "university.student.record.accessed",
        ):
            InProcessEventBus.subscribe(event_name, _service.handle_integration_event)
        _registered = True
    return _service


def reset_compliance_service() -> None:
    global _service, _registered
    _service = None
    _registered = False
