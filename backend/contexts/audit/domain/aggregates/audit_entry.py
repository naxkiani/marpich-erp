"""Immutable audit log record."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot


class AuditSeverity(StrEnum):
    INFO = "info"
    SECURITY = "security"
    COMPLIANCE = "compliance"


@dataclass(eq=False, kw_only=True)
class AuditEntry(AggregateRoot):
    tenant_id: str
    event_name: str
    source_context: str
    correlation_id: str
    action: str
    resource_type: str
    resource_id: str | None
    actor_id: str | None
    severity: AuditSeverity
    payload: dict
    occurred_at: datetime
    recorded_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def from_integration_event(
        cls,
        *,
        tenant_id: str,
        event_name: str,
        source_context: str,
        correlation_id: str,
        action: str,
        resource_type: str,
        resource_id: str | None,
        actor_id: str | None,
        severity: AuditSeverity,
        payload: dict,
        occurred_at: datetime,
    ) -> AuditEntry:
        from shared.domain.value_objects.unique_id import UniqueId

        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            event_name=event_name,
            source_context=source_context,
            correlation_id=correlation_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            actor_id=actor_id,
            severity=severity,
            payload=payload,
            occurred_at=occurred_at,
        )

    @classmethod
    def record_direct(
        cls,
        *,
        tenant_id: str,
        correlation_id: str,
        action: str,
        resource_type: str,
        resource_id: str | None,
        actor_id: str | None,
        severity: AuditSeverity = AuditSeverity.INFO,
        payload: dict | None = None,
    ) -> AuditEntry:
        now = datetime.now(UTC)
        from shared.domain.value_objects.unique_id import UniqueId

        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            event_name="audit.direct",
            source_context="audit",
            correlation_id=correlation_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            actor_id=actor_id,
            severity=severity,
            payload=payload or {},
            occurred_at=now,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "event_name": self.event_name,
            "source_context": self.source_context,
            "correlation_id": self.correlation_id,
            "action": self.action,
            "resource_type": self.resource_type,
            "resource_id": self.resource_id,
            "actor_id": self.actor_id,
            "severity": self.severity.value,
            "payload": self.payload,
            "occurred_at": self.occurred_at.isoformat(),
            "recorded_at": self.recorded_at.isoformat(),
        }
