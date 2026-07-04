from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID, uuid4

from .unique_id import UniqueId
from .tenant_id import TenantId


@dataclass(frozen=True, slots=True)
class EventMetadata:
    correlation_id: UUID
    tenant_id: TenantId
    occurred_at: datetime
    causation_id: UUID | None = None
    user_id: UUID | None = None

    @classmethod
    def create(
        cls,
        tenant_id: TenantId,
        correlation_id: UUID | None = None,
        user_id: UUID | None = None,
        causation_id: UUID | None = None,
    ) -> EventMetadata:
        return cls(
            correlation_id=correlation_id or uuid4(),
            tenant_id=tenant_id,
            occurred_at=datetime.now(timezone.utc),
            causation_id=causation_id,
            user_id=user_id,
        )


class DomainEvent:
    """Internal domain event — never leaves the bounded context boundary directly."""

    __slots__ = ("event_id", "aggregate_id", "metadata", "event_version")

    def __init__(
        self,
        aggregate_id: UniqueId,
        metadata: EventMetadata,
        event_version: int = 1,
        event_id: UniqueId | None = None,
    ) -> None:
        self.event_id = event_id or UniqueId.generate()
        self.aggregate_id = aggregate_id
        self.metadata = metadata
        self.event_version = event_version

    @property
    def event_name(self) -> str:
        raise NotImplementedError

    def to_integration_payload(self) -> dict:
        raise NotImplementedError
