"""Audit metadata primitives — Audit Service owns persistence."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum


class AuditAction(StrEnum):
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    EXECUTE = "execute"


@dataclass(frozen=True, slots=True)
class AuditActor:
    user_id: str
    display_name: str | None = None
    ip_address: str | None = None


@dataclass(frozen=True, slots=True)
class AuditResource:
    resource_type: str
    resource_id: str


@dataclass(frozen=True, slots=True)
class AuditRecord:
    tenant_id: str
    action: AuditAction
    resource: AuditResource
    correlation_id: str
    actor: AuditActor
    occurred_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    payload: dict | None = None

    def to_dict(self) -> dict:
        return {
            "tenant_id": self.tenant_id,
            "action": self.action.value,
            "resource_type": self.resource.resource_type,
            "resource_id": self.resource.resource_id,
            "correlation_id": self.correlation_id,
            "actor_id": self.actor.user_id,
            "actor_name": self.actor.display_name,
            "ip_address": self.actor.ip_address,
            "occurred_at": self.occurred_at.isoformat(),
            "payload": self.payload or {},
        }
