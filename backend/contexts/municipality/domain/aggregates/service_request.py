"""Municipality citizen service request aggregate."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.tenant_id import TenantId
from shared.domain.value_objects.unique_id import UniqueId

from contexts.municipality.domain.events.integration_events import ServiceRequestClosedIntegration


class ServiceRequestStatus(StrEnum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    CLOSED = "closed"


@dataclass(eq=False, kw_only=True)
class ServiceRequest(AggregateRoot):
    tenant_id: str
    citizen_name: str
    category: str
    description: str
    status: ServiceRequestStatus = ServiceRequestStatus.OPEN
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    closed_at: datetime | None = None

    @classmethod
    def open(
        cls,
        *,
        tenant_id: str,
        citizen_name: str,
        category: str,
        description: str,
    ) -> ServiceRequest:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            citizen_name=citizen_name.strip(),
            category=category.strip(),
            description=description.strip(),
        )

    def close(self, *, correlation_id: str, resolution: str) -> ServiceRequestClosedIntegration:
        if self.status == ServiceRequestStatus.CLOSED:
            raise ValueError("municipality.errors.request_already_closed")
        self.status = ServiceRequestStatus.CLOSED
        self.closed_at = datetime.now(UTC)
        return ServiceRequestClosedIntegration(
            tenant_id=TenantId.create(self.tenant_id),
            correlation_id=correlation_id,
            request_id=self.id,
            category=self.category,
            resolution=resolution,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "citizen_name": self.citizen_name,
            "category": self.category,
            "description": self.description,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "closed_at": self.closed_at.isoformat() if self.closed_at else None,
        }
