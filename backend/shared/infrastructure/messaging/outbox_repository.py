"""Transactional outbox repository — memory + postgres."""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy import select, update

from shared.infrastructure.database.engine import session_scope
from shared.infrastructure.settings import use_postgres


@dataclass
class OutboxMessage:
    id: str
    envelope: dict
    retry_count: int = 0


class OutboxMemoryStore:
    _messages: dict[str, OutboxMessage] = {}
    _order: list[str] = []

    @classmethod
    def reset(cls) -> None:
        cls._messages = {}
        cls._order = []


class IOutboxRepository(ABC):
    @abstractmethod
    async def enqueue(self, envelope: dict) -> str: ...

    @abstractmethod
    async def fetch_pending(self, limit: int) -> list[OutboxMessage]: ...

    @abstractmethod
    async def mark_published(self, message_id: str) -> None: ...

    @abstractmethod
    async def mark_failed(self, message_id: str, error: str) -> None: ...


class InMemoryOutboxRepository(IOutboxRepository):
    async def enqueue(self, envelope: dict) -> str:
        msg_id = str(uuid4())
        OutboxMemoryStore._messages[msg_id] = OutboxMessage(id=msg_id, envelope=envelope)
        OutboxMemoryStore._order.append(msg_id)
        return msg_id

    async def fetch_pending(self, limit: int) -> list[OutboxMessage]:
        pending: list[OutboxMessage] = []
        for msg_id in OutboxMemoryStore._order:
            msg = OutboxMemoryStore._messages.get(msg_id)
            if msg is not None:
                pending.append(msg)
            if len(pending) >= limit:
                break
        return pending

    async def mark_published(self, message_id: str) -> None:
        OutboxMemoryStore._messages.pop(message_id, None)
        if message_id in OutboxMemoryStore._order:
            OutboxMemoryStore._order.remove(message_id)

    async def mark_failed(self, message_id: str, error: str) -> None:
        msg = OutboxMemoryStore._messages.get(message_id)
        if msg is not None:
            msg.retry_count += 1


def _get_outbox_row_class():
    from shared.infrastructure.database.orm import OutboxRow

    return OutboxRow


class PostgresOutboxRepository(IOutboxRepository):
    async def enqueue(self, envelope: dict) -> str:
        OutboxRow = _get_outbox_row_class()
        row_id = uuid4()
        event_id = envelope.get("event_id")
        async with session_scope() as session:
            session.add(
                OutboxRow(
                    id=row_id,
                    tenant_id=str(envelope.get("tenant_id", "")),
                    event_id=UUID(event_id) if event_id else None,
                    event_name=str(envelope.get("event_name", "")),
                    event_version=int(envelope.get("event_version", 1)),
                    correlation_id=envelope.get("correlation_id"),
                    source_context=envelope.get("source_context"),
                    payload=envelope.get("payload", {}),
                    envelope=envelope,
                    published=False,
                )
            )
        return str(row_id)

    async def fetch_pending(self, limit: int) -> list[OutboxMessage]:
        OutboxRow = _get_outbox_row_class()
        async with session_scope() as session:
            result = await session.execute(
                select(OutboxRow)
                .where(OutboxRow.published.is_(False))
                .order_by(OutboxRow.created_at)
                .limit(limit)
            )
            rows = result.scalars().all()
        return [
            OutboxMessage(
                id=str(row.id),
                envelope=row.envelope or {
                    "event_id": str(row.event_id) if row.event_id else "",
                    "event_name": row.event_name,
                    "event_version": row.event_version,
                    "tenant_id": row.tenant_id,
                    "correlation_id": row.correlation_id or "",
                    "source_context": row.source_context or "",
                    "payload": row.payload,
                },
                retry_count=row.retry_count,
            )
            for row in rows
        ]

    async def mark_published(self, message_id: str) -> None:
        OutboxRow = _get_outbox_row_class()
        async with session_scope() as session:
            await session.execute(
                update(OutboxRow)
                .where(OutboxRow.id == UUID(message_id))
                .values(published=True, published_at=datetime.now(UTC))
            )

    async def mark_failed(self, message_id: str, error: str) -> None:
        OutboxRow = _get_outbox_row_class()
        async with session_scope() as session:
            result = await session.execute(select(OutboxRow).where(OutboxRow.id == UUID(message_id)))
            row = result.scalar_one_or_none()
            if row is None:
                return
            await session.execute(
                update(OutboxRow)
                .where(OutboxRow.id == UUID(message_id))
                .values(retry_count=row.retry_count + 1, last_error=error[:4000])
            )


_outbox_repository: IOutboxRepository | None = None


def get_outbox_repository() -> IOutboxRepository:
    global _outbox_repository
    if _outbox_repository is None:
        _outbox_repository = PostgresOutboxRepository() if use_postgres() else InMemoryOutboxRepository()
    return _outbox_repository


def reset_outbox_repository() -> None:
    global _outbox_repository
    _outbox_repository = None
