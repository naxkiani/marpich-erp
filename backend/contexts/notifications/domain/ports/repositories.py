"""Repository ports — Notifications."""
from __future__ import annotations

from abc import ABC, abstractmethod

from contexts.notifications.domain.aggregates.inbox_message import InboxMessage
from contexts.notifications.domain.aggregates.notification_delivery import NotificationDelivery
from shared.domain.value_objects.unique_id import UniqueId


class IInboxRepository(ABC):
    @abstractmethod
    async def save(self, message: InboxMessage) -> None: ...

    @abstractmethod
    async def find_by_id(self, tenant_id: str, message_id: UniqueId) -> InboxMessage | None: ...

    @abstractmethod
    async def list_for_user(
        self, tenant_id: str, user_id: str, *, unread_only: bool = False
    ) -> list[InboxMessage]: ...

    @abstractmethod
    async def list_tenant_broadcasts(self, tenant_id: str) -> list[InboxMessage]: ...


class IDeliveryRepository(ABC):
    @abstractmethod
    async def save(self, delivery: NotificationDelivery) -> None: ...

    @abstractmethod
    async def list_deliveries(self, tenant_id: str) -> list[NotificationDelivery]: ...
