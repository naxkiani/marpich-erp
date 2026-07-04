"""Workflow integration events."""
from __future__ import annotations

from dataclasses import dataclass

from shared.domain.events.integration_event import IntegrationEvent
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(frozen=True, kw_only=True)
class ProcessStartedIntegration(IntegrationEvent):
    instance_id: UniqueId
    definition_key: str
    started_by: str

    @property
    def event_name(self) -> str:
        return "workflow.process.started"

    @property
    def source_context(self) -> str:
        return "workflow"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "instance_id": str(self.instance_id),
            "definition_key": self.definition_key,
            "started_by": self.started_by,
        }


@dataclass(frozen=True, kw_only=True)
class TaskAssignedIntegration(IntegrationEvent):
    task_id: UniqueId
    instance_id: UniqueId
    assignee_id: str
    step_key: str
    step_name: str

    @property
    def event_name(self) -> str:
        return "workflow.task.assigned"

    @property
    def source_context(self) -> str:
        return "workflow"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "task_id": str(self.task_id),
            "instance_id": str(self.instance_id),
            "assignee_id": self.assignee_id,
            "step_key": self.step_key,
            "step_name": self.step_name,
        }


@dataclass(frozen=True, kw_only=True)
class TaskCompletedIntegration(IntegrationEvent):
    task_id: UniqueId
    instance_id: UniqueId
    outcome: str
    completed_by: str

    @property
    def event_name(self) -> str:
        return "workflow.task.completed"

    @property
    def source_context(self) -> str:
        return "workflow"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "task_id": str(self.task_id),
            "instance_id": str(self.instance_id),
            "outcome": self.outcome,
            "completed_by": self.completed_by,
        }


@dataclass(frozen=True, kw_only=True)
class ProcessCompletedIntegration(IntegrationEvent):
    instance_id: UniqueId
    definition_key: str
    status: str

    @property
    def event_name(self) -> str:
        return "workflow.process.completed"

    @property
    def source_context(self) -> str:
        return "workflow"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "instance_id": str(self.instance_id),
            "definition_key": self.definition_key,
            "status": self.status,
        }
