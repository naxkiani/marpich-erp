"""In-memory integration repositories."""
from __future__ import annotations

from contexts.integration.domain.aggregates.connector import Connector
from contexts.integration.domain.aggregates.integration_log import IntegrationLog
from contexts.integration.domain.aggregates.sync_job import SyncJob
from contexts.integration.domain.aggregates.webhook_subscription import WebhookSubscription
from contexts.integration.domain.ports.repositories import (
    IConnectorRepository,
    IIntegrationLogRepository,
    ISyncJobRepository,
    IWebhookRepository,
)
from shared.domain.value_objects.unique_id import UniqueId


class IntegrationMemoryStore:
    connectors: dict[str, Connector] = {}
    webhooks: dict[str, WebhookSubscription] = {}
    sync_jobs: dict[str, SyncJob] = {}
    logs: list[IntegrationLog] = []

    @classmethod
    def reset(cls) -> None:
        cls.connectors.clear()
        cls.webhooks.clear()
        cls.sync_jobs.clear()
        cls.logs.clear()


class InMemoryConnectorRepository(IConnectorRepository):
    async def save(self, connector: Connector) -> None:
        IntegrationMemoryStore.connectors[str(connector.id)] = connector

    async def find_by_id(self, tenant_id: str, connector_id: UniqueId) -> Connector | None:
        connector = IntegrationMemoryStore.connectors.get(str(connector_id))
        return connector if connector and connector.tenant_id == tenant_id else None

    async def list_by_tenant(self, tenant_id: str) -> list[Connector]:
        return [c for c in IntegrationMemoryStore.connectors.values() if c.tenant_id == tenant_id]


class InMemoryWebhookRepository(IWebhookRepository):
    async def save(self, webhook: WebhookSubscription) -> None:
        IntegrationMemoryStore.webhooks[str(webhook.id)] = webhook

    async def find_by_id(self, tenant_id: str, webhook_id: UniqueId) -> WebhookSubscription | None:
        webhook = IntegrationMemoryStore.webhooks.get(str(webhook_id))
        return webhook if webhook and webhook.tenant_id == tenant_id else None

    async def list_by_tenant(self, tenant_id: str) -> list[WebhookSubscription]:
        return [w for w in IntegrationMemoryStore.webhooks.values() if w.tenant_id == tenant_id]

    async def list_active_for_event(self, tenant_id: str, event_name: str) -> list[WebhookSubscription]:
        return [
            w
            for w in IntegrationMemoryStore.webhooks.values()
            if w.tenant_id == tenant_id and w.matches(event_name)
        ]


class InMemorySyncJobRepository(ISyncJobRepository):
    async def save(self, job: SyncJob) -> None:
        IntegrationMemoryStore.sync_jobs[str(job.id)] = job

    async def find_by_id(self, tenant_id: str, job_id: UniqueId) -> SyncJob | None:
        job = IntegrationMemoryStore.sync_jobs.get(str(job_id))
        return job if job and job.tenant_id == tenant_id else None


class InMemoryIntegrationLogRepository(IIntegrationLogRepository):
    async def append(self, log: IntegrationLog) -> None:
        IntegrationMemoryStore.logs.append(log)

    async def list_by_tenant(self, tenant_id: str, limit: int = 100) -> list[IntegrationLog]:
        items = [log for log in IntegrationMemoryStore.logs if log.tenant_id == tenant_id]
        return items[-limit:]
