"""In-memory notification repositories."""
from __future__ import annotations

from contexts.notifications.domain.aggregates.inbox_message import InboxMessage, InboxStatus
from contexts.notifications.domain.aggregates.notification_delivery import NotificationDelivery
from contexts.notifications.domain.ports.repositories import IDeliveryRepository, IInboxRepository
from shared.domain.value_objects.unique_id import UniqueId


class NotificationMemoryStore:
    inbox: dict[str, InboxMessage] = {}
    deliveries: dict[str, NotificationDelivery] = {}

    @classmethod
    def reset(cls) -> None:
        cls.inbox.clear()
        cls.deliveries.clear()


class InMemoryInboxRepository(IInboxRepository):
    async def save(self, message: InboxMessage) -> None:
        NotificationMemoryStore.inbox[str(message.id)] = message

    async def find_by_id(self, tenant_id: str, message_id: UniqueId) -> InboxMessage | None:
        msg = NotificationMemoryStore.inbox.get(str(message_id))
        return msg if msg and msg.tenant_id == tenant_id else None

    async def list_for_user(
        self, tenant_id: str, user_id: str, *, unread_only: bool = False
    ) -> list[InboxMessage]:
        items = [
            m
            for m in NotificationMemoryStore.inbox.values()
            if m.tenant_id == tenant_id and (m.user_id == user_id or m.user_id is None)
        ]
        if unread_only:
            items = [m for m in items if m.status == InboxStatus.UNREAD]
        return sorted(items, key=lambda m: m.created_at, reverse=True)

    async def list_tenant_broadcasts(self, tenant_id: str) -> list[InboxMessage]:
        return [
            m
            for m in NotificationMemoryStore.inbox.values()
            if m.tenant_id == tenant_id and m.user_id is None
        ]


class InMemoryDeliveryRepository(IDeliveryRepository):
    async def save(self, delivery: NotificationDelivery) -> None:
        NotificationMemoryStore.deliveries[str(delivery.id)] = delivery

    async def list_deliveries(self, tenant_id: str) -> list[NotificationDelivery]:
        return [d for d in NotificationMemoryStore.deliveries.values() if d.tenant_id == tenant_id]
