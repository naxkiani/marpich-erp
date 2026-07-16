"""Enterprise Regulatory Reporting Platform DI + event subscriptions."""
from __future__ import annotations

from contexts.policy.container import get_policy_evaluator
from contexts.regulatory_reporting.application.service import EnterpriseRegulatoryReportingApplicationService
from contexts.regulatory_reporting.infrastructure.acl.reporting_acl import ReportingRegulatoryAcl
from contexts.regulatory_reporting.infrastructure.persistence.regulatory_reporting_memory_store import (
    InMemoryCountryAdapterRepository,
    InMemoryDigitalSubmissionRepository,
    InMemoryRegulatoryTenantProfileRepository,
)
from shared.infrastructure.messaging.event_bus import InProcessEventBus

_service: EnterpriseRegulatoryReportingApplicationService | None = None
_registered = False


def get_enterprise_regulatory_reporting_service() -> EnterpriseRegulatoryReportingApplicationService:
    global _service, _registered
    if _service is None:
        _service = EnterpriseRegulatoryReportingApplicationService(
            profiles=InMemoryRegulatoryTenantProfileRepository(),
            adapters=InMemoryCountryAdapterRepository(),
            submissions=InMemoryDigitalSubmissionRepository(),
            reporting_acl=ReportingRegulatoryAcl(),
            policy_evaluator=get_policy_evaluator(),
        )
    if not _registered:
        InProcessEventBus.subscribe(
            "platform.tenant.provisioned",
            _service.handle_tenant_provisioned,
        )
        _registered = True
    return _service


def reset_enterprise_regulatory_reporting_service() -> None:
    global _service, _registered
    _service = None
    _registered = False
    InMemoryRegulatoryTenantProfileRepository.reset()
    InMemoryCountryAdapterRepository.reset()
    InMemoryDigitalSubmissionRepository.reset()
