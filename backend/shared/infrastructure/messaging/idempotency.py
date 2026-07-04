"""Idempotent consumer ledger — memory + postgres."""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from shared.infrastructure.database.engine import session_scope
from shared.infrastructure.settings import use_postgres


@dataclass(frozen=True, slots=True)
class ProcessedEventKey:
    tenant_id: str
    event_id: str
    consumer_id: str


class ProcessedEventMemoryStore:
    keys: set[tuple[str, str, str]] = set()

    @classmethod
    def reset(cls) -> None:
        cls.keys.clear()


class IProcessedEventStore(ABC):
    @abstractmethod
    async def is_processed(self, key: ProcessedEventKey) -> bool: ...

    @abstractmethod
    async def mark_processed(self, key: ProcessedEventKey, event_name: str) -> None: ...


class InMemoryProcessedEventStore(IProcessedEventStore):
    async def is_processed(self, key: ProcessedEventKey) -> bool:
        return (key.tenant_id, key.event_id, key.consumer_id) in ProcessedEventMemoryStore.keys

    async def mark_processed(self, key: ProcessedEventKey, event_name: str) -> None:
        ProcessedEventMemoryStore.keys.add((key.tenant_id, key.event_id, key.consumer_id))


class ProcessedEventRow:
    """Lazy import avoids circular dependency with ORM module."""

    __table__ = None


def _get_processed_row_class():
    from shared.infrastructure.database.orm import ProcessedEventRow

    return ProcessedEventRow


class PostgresProcessedEventStore(IProcessedEventStore):
    async def is_processed(self, key: ProcessedEventKey) -> bool:
        ProcessedEventRow = _get_processed_row_class()
        async with session_scope() as session:
            result = await session.execute(
                select(ProcessedEventRow).where(
                    ProcessedEventRow.tenant_id == key.tenant_id,
                    ProcessedEventRow.event_id == UUID(key.event_id),
                    ProcessedEventRow.consumer_id == key.consumer_id,
                )
            )
            return result.scalar_one_or_none() is not None

    async def mark_processed(self, key: ProcessedEventKey, event_name: str) -> None:
        ProcessedEventRow = _get_processed_row_class()
        async with session_scope() as session:
            await session.execute(
                pg_insert(ProcessedEventRow)
                .values(
                    tenant_id=key.tenant_id,
                    event_id=UUID(key.event_id),
                    consumer_id=key.consumer_id,
                    event_name=event_name,
                    processed_at=datetime.now(UTC),
                )
                .on_conflict_do_nothing()
            )


def get_processed_event_store() -> IProcessedEventStore:
    if use_postgres():
        return PostgresProcessedEventStore()
    return InMemoryProcessedEventStore()


def consumer_id_for_handler(handler: object) -> str:
    module = getattr(handler, "__module__", "unknown")
    qualname = getattr(handler, "__qualname__", repr(handler))
    return f"{module}.{qualname}"
