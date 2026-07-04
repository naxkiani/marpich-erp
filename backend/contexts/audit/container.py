"""Audit DI + event subscriptions."""
from __future__ import annotations

from contexts.audit.application.service import AuditApplicationService
from contexts.audit.infrastructure.acl.event_mapper import IntegrationEventMapper
from contexts.audit.infrastructure.persistence.memory_store import (
    InMemoryAuditEntryRepository,
    InMemoryAuditExportRepository,
    InMemoryRetentionPolicyRepository,
)
from contexts.audit.infrastructure.persistence.postgres_store import (
    PostgresAuditEntryRepository,
    PostgresAuditExportRepository,
    PostgresRetentionPolicyRepository,
)
from shared.infrastructure.messaging.event_bus import InProcessEventBus
from shared.infrastructure.settings import use_postgres

_service: AuditApplicationService | None = None
_registered = False


def get_audit_service() -> AuditApplicationService:
    global _service, _registered
    if _service is None:
        if use_postgres():
            _service = AuditApplicationService(
                entries=PostgresAuditEntryRepository(),
                exports=PostgresAuditExportRepository(),
                retention=PostgresRetentionPolicyRepository(),
                event_mapper=IntegrationEventMapper(),
            )
        else:
            _service = AuditApplicationService(
                entries=InMemoryAuditEntryRepository(),
                exports=InMemoryAuditExportRepository(),
                retention=InMemoryRetentionPolicyRepository(),
                event_mapper=IntegrationEventMapper(),
            )
    if not _registered:
        InProcessEventBus.subscribe("*", _service.handle_integration_event)
        InProcessEventBus.subscribe(
            "platform.tenant.provisioned",
            _service.handle_tenant_provisioned,
        )
        _registered = True
    return _service


def reset_audit_service() -> None:
    global _service, _registered
    _service = None
    _registered = False
