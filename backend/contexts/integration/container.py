"""Integration DI + event subscriptions."""
from __future__ import annotations

from contexts.integration.application.service import IntegrationApplicationService
from contexts.integration.infrastructure.acl.platform_events import IntegrationPlatformAdapter
from contexts.integration.infrastructure.channels.console_webhook import ConsoleWebhookChannel
from contexts.integration.infrastructure.persistence.memory_store import (
    InMemoryConnectorRepository,
    InMemoryIntegrationLogRepository,
    InMemorySyncJobRepository,
    InMemoryWebhookRepository,
)
from contexts.integration.infrastructure.persistence.postgres_store import (
    PostgresConnectorRepository,
    PostgresIntegrationLogRepository,
    PostgresSyncJobRepository,
    PostgresWebhookRepository,
)
from shared.infrastructure.messaging.event_bus import InProcessEventBus
from shared.infrastructure.settings import use_postgres

_service: IntegrationApplicationService | None = None
_registered = False


def get_integration_service() -> IntegrationApplicationService:
    global _service, _registered
    if _service is None:
        if use_postgres():
            _service = IntegrationApplicationService(
                connectors=PostgresConnectorRepository(),
                webhooks=PostgresWebhookRepository(),
                sync_jobs=PostgresSyncJobRepository(),
                logs=PostgresIntegrationLogRepository(),
                platform_events=IntegrationPlatformAdapter(),
                webhook_channel=ConsoleWebhookChannel(),
            )
        else:
            _service = IntegrationApplicationService(
                connectors=InMemoryConnectorRepository(),
                webhooks=InMemoryWebhookRepository(),
                sync_jobs=InMemorySyncJobRepository(),
                logs=InMemoryIntegrationLogRepository(),
                platform_events=IntegrationPlatformAdapter(),
                webhook_channel=ConsoleWebhookChannel(),
            )
    if not _registered:
        InProcessEventBus.subscribe("*", _service.handle_integration_event)
        InProcessEventBus.subscribe(
            "platform.tenant.provisioned",
            _service.handle_tenant_provisioned,
        )
        _registered = True
    return _service


def reset_integration_service() -> None:
    global _service, _registered
    _service = None
    _registered = False
