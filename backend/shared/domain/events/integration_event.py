"""Integration event — cross bounded context; published language."""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.value_objects.tenant_id import TenantId
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(frozen=True, kw_only=True)
class IntegrationEvent(ABC):
    """
    Published between bounded contexts via event bus.
    Producers and consumers MUST NOT share domain models.
    Envelope is immutable — corrections use compensating events.
    """

    event_id: UniqueId = field(default_factory=UniqueId.generate)
    tenant_id: TenantId = field(default=...)
    organization_id: str | None = None
    correlation_id: str = field(default=...)
    causation_id: str | None = None
    occurred_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    actor_user_id: str | None = None
    security_context: dict | None = None

    @property
    @abstractmethod
    def event_name(self) -> str: ...

    @property
    @abstractmethod
    def source_context(self) -> str: ...

    @property
    @abstractmethod
    def event_version(self) -> int: ...

    @abstractmethod
    def to_payload(self) -> dict: ...

    def _default_security_context(self) -> dict:
        return {
            "auth_method": "system",
            "ip_address": None,
            "user_agent": None,
            "scopes": [],
            "session_id": None,
        }

    def envelope(self) -> dict:
        return {
            "event_id": str(self.event_id),
            "event_name": self.event_name,
            "event_version": self.event_version,
            "source_context": self.source_context,
            "tenant_id": str(self.tenant_id),
            "organization_id": self.organization_id,
            "correlation_id": self.correlation_id,
            "causation_id": self.causation_id,
            "occurred_at": self.occurred_at.isoformat(),
            "user_id": self.actor_user_id,
            "security_context": self.security_context or self._default_security_context(),
            "payload": self.to_payload(),
        }
