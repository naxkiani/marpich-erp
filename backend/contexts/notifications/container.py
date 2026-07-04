"""Notifications DI + event subscriptions."""
from __future__ import annotations

from contexts.notifications.application.service import NotificationApplicationService
from contexts.notifications.infrastructure.acl.event_routes import NotificationEventAdapter
from contexts.notifications.infrastructure.channels.email_console import ConsoleEmailChannel
from contexts.notifications.infrastructure.persistence.memory_store import (
    InMemoryDeliveryRepository,
    InMemoryInboxRepository,
)
from contexts.notifications.infrastructure.persistence.postgres_store import (
    PostgresDeliveryRepository,
    PostgresInboxRepository,
)
from shared.infrastructure.messaging.event_bus import InProcessEventBus
from shared.infrastructure.settings import use_postgres

_service: NotificationApplicationService | None = None
_registered = False

_SUBSCRIBED_EVENTS = (
    "identity.user.created",
    "platform.tenant.provisioned",
    "hospital.encounter.completed",
    "finance.journal.recorded",
    "workflow.task.assigned",
)


def get_notification_service() -> NotificationApplicationService:
    global _service, _registered
    if _service is None:
        if use_postgres():
            _service = NotificationApplicationService(
                inbox=PostgresInboxRepository(),
                deliveries=PostgresDeliveryRepository(),
                event_adapter=NotificationEventAdapter(),
                email=ConsoleEmailChannel(),
            )
        else:
            _service = NotificationApplicationService(
                inbox=InMemoryInboxRepository(),
                deliveries=InMemoryDeliveryRepository(),
                event_adapter=NotificationEventAdapter(),
                email=ConsoleEmailChannel(),
            )
    if not _registered:
        for event_name in _SUBSCRIBED_EVENTS:
            InProcessEventBus.subscribe(event_name, _service.handle_integration_event)
        _registered = True
    return _service


def reset_notification_service() -> None:
    global _service, _registered
    _service = None
    _registered = False
