"""Domain event — internal to a bounded context."""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.value_objects.tenant_id import TenantId
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(frozen=True, kw_only=True)
class DomainEvent(ABC):
    event_id: UniqueId = field(default_factory=UniqueId.generate)
    aggregate_id: UniqueId = field(default=...)
    tenant_id: TenantId = field(default=...)
    organization_id: str | None = None
    correlation_id: str = field(default=...)
    occurred_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    actor_user_id: str | None = None
    security_context: dict | None = None

    @property
    @abstractmethod
    def event_name(self) -> str: ...

    @property
    @abstractmethod
    def event_version(self) -> int: ...

    @abstractmethod
    def to_payload(self) -> dict: ...
