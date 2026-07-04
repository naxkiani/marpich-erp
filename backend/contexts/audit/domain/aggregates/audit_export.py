"""Compliance export job."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot


class ExportStatus(StrEnum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


class ExportFormat(StrEnum):
    JSON = "json"
    CSV = "csv"


@dataclass(eq=False, kw_only=True)
class AuditExport(AggregateRoot):
    tenant_id: str
    status: ExportStatus
    format: ExportFormat
    filters: dict
    entry_count: int = 0
    data: list[dict] = field(default_factory=list)
    error: str | None = None
    requested_by: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    completed_at: datetime | None = None

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        export_format: ExportFormat,
        filters: dict,
        requested_by: str | None,
    ) -> AuditExport:
        from shared.domain.value_objects.unique_id import UniqueId

        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            status=ExportStatus.PENDING,
            format=export_format,
            filters=filters,
            requested_by=requested_by,
        )

    def mark_completed(self, entries: list[dict]) -> None:
        self.status = ExportStatus.COMPLETED
        self.entry_count = len(entries)
        self.data = entries
        self.completed_at = datetime.now(UTC)

    def mark_failed(self, error: str) -> None:
        self.status = ExportStatus.FAILED
        self.error = error
        self.completed_at = datetime.now(UTC)

    def to_dict(self, *, include_data: bool = True) -> dict:
        result = {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "status": self.status.value,
            "format": self.format.value,
            "filters": self.filters,
            "entry_count": self.entry_count,
            "error": self.error,
            "requested_by": self.requested_by,
            "created_at": self.created_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }
        if include_data and self.status == ExportStatus.COMPLETED:
            result["data"] = self.data
        return result
