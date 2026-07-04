"""Integration delivery log."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class LogStatus(StrEnum):
    DELIVERED = "delivered"
    FAILED = "failed"


@dataclass(eq=False, kw_only=True)
class IntegrationLog(AggregateRoot):
    tenant_id: str
    log_type: str
    status: LogStatus
    reference_id: str
    event_name: str | None
    detail: dict
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def record(
        cls,
        *,
        tenant_id: str,
        log_type: str,
        status: LogStatus,
        reference_id: str,
        event_name: str | None = None,
        detail: dict | None = None,
    ) -> IntegrationLog:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            log_type=log_type,
            status=status,
            reference_id=reference_id,
            event_name=event_name,
            detail=detail or {},
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "log_type": self.log_type,
            "status": self.status.value,
            "reference_id": self.reference_id,
            "event_name": self.event_name,
            "detail": self.detail,
            "created_at": self.created_at.isoformat(),
        }
