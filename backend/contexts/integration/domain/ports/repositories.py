"""Integration repository ports."""
from __future__ import annotations

from abc import ABC, abstractmethod

from contexts.integration.domain.aggregates.connector import Connector
from contexts.integration.domain.aggregates.integration_log import IntegrationLog
from contexts.integration.domain.aggregates.sync_job import SyncJob
from contexts.integration.domain.aggregates.webhook_subscription import WebhookSubscription
from shared.domain.value_objects.unique_id import UniqueId


class IConnectorRepository(ABC):
    @abstractmethod
    async def save(self, connector: Connector) -> None: ...

    @abstractmethod
    async def find_by_id(self, tenant_id: str, connector_id: UniqueId) -> Connector | None: ...

    @abstractmethod
    async def list_by_tenant(self, tenant_id: str) -> list[Connector]: ...


class IWebhookRepository(ABC):
    @abstractmethod
    async def save(self, webhook: WebhookSubscription) -> None: ...

    @abstractmethod
    async def find_by_id(self, tenant_id: str, webhook_id: UniqueId) -> WebhookSubscription | None: ...

    @abstractmethod
    async def list_by_tenant(self, tenant_id: str) -> list[WebhookSubscription]: ...

    @abstractmethod
    async def list_active_for_event(self, tenant_id: str, event_name: str) -> list[WebhookSubscription]: ...


class ISyncJobRepository(ABC):
    @abstractmethod
    async def save(self, job: SyncJob) -> None: ...

    @abstractmethod
    async def find_by_id(self, tenant_id: str, job_id: UniqueId) -> SyncJob | None: ...


class IIntegrationLogRepository(ABC):
    @abstractmethod
    async def append(self, log: IntegrationLog) -> None: ...

    @abstractmethod
    async def list_by_tenant(self, tenant_id: str, limit: int = 100) -> list[IntegrationLog]: ...
