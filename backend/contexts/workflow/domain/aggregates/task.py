"""Human workflow task."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class TaskStatus(StrEnum):
    PENDING = "pending"
    COMPLETED = "completed"
    DELEGATED = "delegated"


class TaskOutcome(StrEnum):
    APPROVED = "approved"
    REJECTED = "rejected"


@dataclass(eq=False, kw_only=True)
class Task(AggregateRoot):
    tenant_id: str
    instance_id: UniqueId
    step_key: str
    step_name: str
    assignee_id: str
    status: TaskStatus
    outcome: TaskOutcome | None = None
    comment: str = ""
    delegated_from: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    completed_at: datetime | None = None

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        instance_id: UniqueId,
        step_key: str,
        step_name: str,
        assignee_id: str,
    ) -> Task:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            instance_id=instance_id,
            step_key=step_key,
            step_name=step_name,
            assignee_id=assignee_id,
            status=TaskStatus.PENDING,
        )

    def complete(self, outcome: TaskOutcome, comment: str = "") -> None:
        self.status = TaskStatus.COMPLETED
        self.outcome = outcome
        self.comment = comment.strip()
        self.completed_at = datetime.now(UTC)

    def delegate(self, to_user_id: str) -> None:
        self.delegated_from = self.assignee_id
        self.assignee_id = to_user_id
        self.status = TaskStatus.PENDING

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "instance_id": str(self.instance_id),
            "step_key": self.step_key,
            "step_name": self.step_name,
            "assignee_id": self.assignee_id,
            "status": self.status.value,
            "outcome": self.outcome.value if self.outcome else None,
            "comment": self.comment,
            "delegated_from": self.delegated_from,
            "created_at": self.created_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }
