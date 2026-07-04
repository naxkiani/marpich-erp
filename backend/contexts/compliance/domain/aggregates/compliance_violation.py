"""Compliance violation record."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class ViolationSeverity(StrEnum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ViolationStatus(StrEnum):
    OPEN = "open"
    INVESTIGATING = "investigating"
    RESOLVED = "resolved"
    FALSE_POSITIVE = "false_positive"


@dataclass(eq=False, kw_only=True)
class ComplianceViolation(AggregateRoot):
    tenant_id: str
    domain: str
    control_id: str
    severity: ViolationSeverity
    status: ViolationStatus
    title: str
    description: str | None
    source_event: str | None
    correlation_id: str | None
    detected_at: datetime
    payload: dict = field(default_factory=dict)
    resolved_at: datetime | None = None
    resolved_by: str | None = None
    resolution_notes: str | None = None

    @classmethod
    def detect(
        cls,
        *,
        tenant_id: str,
        domain: str,
        control_id: str,
        severity: str,
        title: str,
        description: str | None = None,
        source_event: str | None = None,
        correlation_id: str | None = None,
        payload: dict | None = None,
    ) -> ComplianceViolation:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            domain=domain,
            control_id=control_id,
            severity=ViolationSeverity(severity),
            status=ViolationStatus.OPEN,
            title=title,
            description=description,
            source_event=source_event,
            correlation_id=correlation_id,
            detected_at=datetime.now(UTC),
            payload=payload or {},
        )

    def resolve(self, *, actor_id: str | None, notes: str) -> None:
        self.status = ViolationStatus.RESOLVED
        self.resolved_at = datetime.now(UTC)
        self.resolved_by = actor_id
        self.resolution_notes = notes

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "domain": self.domain,
            "control_id": self.control_id,
            "severity": self.severity.value,
            "status": self.status.value,
            "title": self.title,
            "description": self.description,
            "source_event": self.source_event,
            "correlation_id": self.correlation_id,
            "detected_at": self.detected_at.isoformat(),
            "resolved_at": self.resolved_at.isoformat() if self.resolved_at else None,
            "resolved_by": self.resolved_by,
            "resolution_notes": self.resolution_notes,
            "payload": self.payload,
        }
