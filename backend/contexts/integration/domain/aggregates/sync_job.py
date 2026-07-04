"""Sync job — event-driven or manual external sync."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class SyncStatus(StrEnum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass(eq=False, kw_only=True)
class SyncJob(AggregateRoot):
    tenant_id: str
    connector_id: UniqueId
    job_type: str
    status: SyncStatus
    result: dict
    error: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    completed_at: datetime | None = None

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        connector_id: UniqueId,
        job_type: str,
    ) -> SyncJob:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            connector_id=connector_id,
            job_type=job_type.strip(),
            status=SyncStatus.PENDING,
            result={},
        )

    def complete(self, result: dict) -> None:
        self.status = SyncStatus.COMPLETED
        self.result = result
        self.completed_at = datetime.now(UTC)

    def fail(self, error: str) -> None:
        self.status = SyncStatus.FAILED
        self.error = error
        self.completed_at = datetime.now(UTC)

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "connector_id": str(self.connector_id),
            "job_type": self.job_type,
            "status": self.status.value,
            "result": self.result,
            "error": self.error,
            "created_at": self.created_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }
