"""Async transcode job."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class TranscodeStatus(StrEnum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass(eq=False, kw_only=True)
class TranscodeJob(AggregateRoot):
    tenant_id: str
    asset_id: UniqueId
    profile: str
    status: TranscodeStatus
    error: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    completed_at: datetime | None = None

    @classmethod
    def create(cls, *, tenant_id: str, asset_id: UniqueId, profile: str) -> TranscodeJob:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            asset_id=asset_id,
            profile=profile.strip().lower(),
            status=TranscodeStatus.PENDING,
        )

    def complete(self) -> None:
        self.status = TranscodeStatus.COMPLETED
        self.completed_at = datetime.now(UTC)

    def fail(self, error: str) -> None:
        self.status = TranscodeStatus.FAILED
        self.error = error
        self.completed_at = datetime.now(UTC)

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "asset_id": str(self.asset_id),
            "profile": self.profile,
            "status": self.status.value,
            "error": self.error,
            "created_at": self.created_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }
