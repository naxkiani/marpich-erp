"""Running process instance."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class ProcessStatus(StrEnum):
    RUNNING = "running"
    COMPLETED = "completed"
    REJECTED = "rejected"


@dataclass(eq=False, kw_only=True)
class ProcessInstance(AggregateRoot):
    tenant_id: str
    definition_id: UniqueId
    definition_key: str
    status: ProcessStatus
    current_step_index: int
    context: dict
    started_by: str
    started_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    completed_at: datetime | None = None

    @classmethod
    def start(
        cls,
        *,
        tenant_id: str,
        definition_id: UniqueId,
        definition_key: str,
        context: dict,
        started_by: str,
    ) -> ProcessInstance:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            definition_id=definition_id,
            definition_key=definition_key,
            status=ProcessStatus.RUNNING,
            current_step_index=0,
            context=context,
            started_by=started_by,
        )

    def advance_step(self) -> None:
        self.current_step_index += 1

    def complete(self) -> None:
        self.status = ProcessStatus.COMPLETED
        self.completed_at = datetime.now(UTC)

    def reject(self) -> None:
        self.status = ProcessStatus.REJECTED
        self.completed_at = datetime.now(UTC)

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "definition_id": str(self.definition_id),
            "definition_key": self.definition_key,
            "status": self.status.value,
            "current_step_index": self.current_step_index,
            "context": self.context,
            "started_by": self.started_by,
            "started_at": self.started_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }
