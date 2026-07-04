"""Identity domain events → integration events (published language)."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.events.integration_event import IntegrationEvent
from shared.domain.value_objects.tenant_id import TenantId
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(frozen=True, kw_only=True)
class UserCreatedIntegration(IntegrationEvent):
    user_id: UniqueId = field(default=...)
    email: str = field(default=...)
    display_name: str = field(default=...)

    @property
    def event_name(self) -> str:
        return "identity.user.created"

    @property
    def source_context(self) -> str:
        return "identity"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "user_id": str(self.user_id),
            "email": self.email,
            "display_name": self.display_name,
        }


@dataclass(frozen=True, kw_only=True)
class UserLoggedInIntegration(IntegrationEvent):
    user_id: UniqueId = field(default=...)
    email: str = field(default=...)
    ip_address: str | None = None

    @property
    def event_name(self) -> str:
        return "identity.user.logged_in"

    @property
    def source_context(self) -> str:
        return "identity"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "user_id": str(self.user_id),
            "email": self.email,
            "ip_address": self.ip_address,
        }


@dataclass(frozen=True, kw_only=True)
class MfaEnabledIntegration(IntegrationEvent):
    user_id: UniqueId = field(default=...)

    @property
    def event_name(self) -> str:
        return "identity.mfa.enabled"

    @property
    def source_context(self) -> str:
        return "identity"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"user_id": str(self.user_id)}
