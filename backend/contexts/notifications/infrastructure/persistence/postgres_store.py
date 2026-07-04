"""PostgreSQL repositories — Notifications bounded context."""
from __future__ import annotations

from uuid import UUID

from sqlalchemy import select

from contexts.notifications.domain.aggregates.inbox_message import InboxMessage, InboxStatus
from contexts.notifications.domain.aggregates.notification_delivery import (
    DeliveryStatus,
    NotificationDelivery,
)
from contexts.notifications.domain.ports.repositories import IDeliveryRepository, IInboxRepository
from shared.domain.value_objects.unique_id import UniqueId
from shared.infrastructure.database.engine import session_scope
from shared.infrastructure.database.orm import InboxMessageRow, NotificationDeliveryRow


def _parse_user_id(user_id: str | None) -> UUID | None:
    if not user_id:
        return None
    try:
        return UUID(user_id)
    except ValueError:
        return None


class PostgresInboxRepository(IInboxRepository):
    async def save(self, message: InboxMessage) -> None:
        async with session_scope() as session:
            row = await session.get(InboxMessageRow, UUID(str(message.id)))
            if row is None:
                session.add(
                    InboxMessageRow(
                        id=UUID(str(message.id)),
                        tenant_id=message.tenant_id,
                        user_id=_parse_user_id(message.user_id),
                        channel=message.channel,
                        title=message.title,
                        body=message.body,
                        category=message.category,
                        source_event=message.source_event,
                        status=message.status.value,
                        message_metadata=message.metadata,
                        created_at=message.created_at,
                        read_at=message.read_at,
                    )
                )
            else:
                row.status = message.status.value
                row.read_at = message.read_at

    async def find_by_id(self, tenant_id: str, message_id: UniqueId) -> InboxMessage | None:
        async with session_scope() as session:
            row = await session.get(InboxMessageRow, UUID(str(message_id)))
            if row and row.tenant_id == tenant_id:
                return _inbox_from_row(row)
            return None

    async def list_for_user(
        self, tenant_id: str, user_id: str, *, unread_only: bool = False
    ) -> list[InboxMessage]:
        async with session_scope() as session:
            uid = _parse_user_id(user_id)
            stmt = select(InboxMessageRow).where(InboxMessageRow.tenant_id == tenant_id)
            if uid is not None:
                stmt = stmt.where(
                    (InboxMessageRow.user_id == uid) | (InboxMessageRow.user_id.is_(None))
                )
            rows = (await session.scalars(stmt)).all()
        items = [_inbox_from_row(r) for r in rows]
        if unread_only:
            items = [m for m in items if m.status == InboxStatus.UNREAD]
        return sorted(items, key=lambda m: m.created_at, reverse=True)

    async def list_tenant_broadcasts(self, tenant_id: str) -> list[InboxMessage]:
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(InboxMessageRow).where(
                        InboxMessageRow.tenant_id == tenant_id,
                        InboxMessageRow.user_id.is_(None),
                    )
                )
            ).all()
        return [_inbox_from_row(r) for r in rows]


class PostgresDeliveryRepository(IDeliveryRepository):
    async def save(self, delivery: NotificationDelivery) -> None:
        async with session_scope() as session:
            row = await session.get(NotificationDeliveryRow, UUID(str(delivery.id)))
            if row is None:
                session.add(
                    NotificationDeliveryRow(
                        id=UUID(str(delivery.id)),
                        tenant_id=delivery.tenant_id,
                        channel=delivery.channel,
                        recipient=delivery.recipient,
                        template_key=delivery.template_key,
                        source_event=delivery.source_event,
                        status=delivery.status.value,
                        error=delivery.error,
                        payload=delivery.payload,
                        created_at=delivery.created_at,
                        delivered_at=delivery.delivered_at,
                    )
                )
            else:
                row.status = delivery.status.value
                row.error = delivery.error
                row.delivered_at = delivery.delivered_at

    async def list_deliveries(self, tenant_id: str) -> list[NotificationDelivery]:
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(NotificationDeliveryRow).where(
                        NotificationDeliveryRow.tenant_id == tenant_id
                    )
                )
            ).all()
        return [_delivery_from_row(r) for r in rows]


def _inbox_from_row(row: InboxMessageRow) -> InboxMessage:
    return InboxMessage(
        id=UniqueId(str(row.id)),
        tenant_id=row.tenant_id,
        user_id=str(row.user_id) if row.user_id else None,
        channel=row.channel,
        title=row.title,
        body=row.body,
        category=row.category,
        source_event=row.source_event,
        status=InboxStatus(row.status),
        metadata=row.message_metadata,
        created_at=row.created_at,
        read_at=row.read_at,
    )


def _delivery_from_row(row: NotificationDeliveryRow) -> NotificationDelivery:
    return NotificationDelivery(
        id=UniqueId(str(row.id)),
        tenant_id=row.tenant_id,
        channel=row.channel,
        recipient=row.recipient,
        template_key=row.template_key,
        source_event=row.source_event,
        status=DeliveryStatus(row.status),
        error=row.error,
        payload=row.payload,
        created_at=row.created_at,
        delivered_at=row.delivered_at,
    )
