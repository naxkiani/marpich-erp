"""Compliance report job."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class ReportStatus(StrEnum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass(eq=False, kw_only=True)
class ComplianceReport(AggregateRoot):
    tenant_id: str
    report_type: str
    domain: str | None
    format: str
    status: ReportStatus
    filters: dict
    data: dict
    requested_by: str | None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    completed_at: datetime | None = None
    error: str | None = None

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        report_type: str,
        domain: str | None,
        export_format: str,
        filters: dict,
        requested_by: str | None,
    ) -> ComplianceReport:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            report_type=report_type,
            domain=domain,
            format=export_format,
            status=ReportStatus.PENDING,
            filters=filters,
            data={},
            requested_by=requested_by,
        )

    def complete(self, data: dict) -> None:
        self.status = ReportStatus.COMPLETED
        self.data = data
        self.completed_at = datetime.now(UTC)

    def fail(self, error: str) -> None:
        self.status = ReportStatus.FAILED
        self.error = error
        self.completed_at = datetime.now(UTC)

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "report_type": self.report_type,
            "domain": self.domain,
            "format": self.format,
            "status": self.status.value,
            "filters": self.filters,
            "data": self.data,
            "requested_by": self.requested_by,
            "created_at": self.created_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "error": self.error,
        }
