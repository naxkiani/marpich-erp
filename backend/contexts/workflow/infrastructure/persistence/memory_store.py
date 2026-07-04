"""In-memory workflow repositories."""
from __future__ import annotations

from contexts.workflow.domain.aggregates.process_definition import ProcessDefinition
from contexts.workflow.domain.aggregates.process_instance import ProcessInstance
from contexts.workflow.domain.aggregates.task import Task, TaskStatus
from contexts.workflow.domain.ports.repositories import (
    IDefinitionRepository,
    IInstanceRepository,
    ITaskRepository,
)
from shared.domain.value_objects.unique_id import UniqueId


class WorkflowMemoryStore:
    definitions: dict[str, ProcessDefinition] = {}
    instances: dict[str, ProcessInstance] = {}
    tasks: dict[str, Task] = {}

    @classmethod
    def reset(cls) -> None:
        cls.definitions.clear()
        cls.instances.clear()
        cls.tasks.clear()


class InMemoryDefinitionRepository(IDefinitionRepository):
    def _key(self, tenant_id: str, definition_key: str) -> str:
        return f"{tenant_id}:{definition_key}"

    async def save(self, definition: ProcessDefinition) -> None:
        WorkflowMemoryStore.definitions[self._key(definition.tenant_id, definition.key)] = definition

    async def find_by_key(self, tenant_id: str, key: str) -> ProcessDefinition | None:
        return WorkflowMemoryStore.definitions.get(self._key(tenant_id, key.lower()))

    async def list_by_tenant(self, tenant_id: str) -> list[ProcessDefinition]:
        return [d for d in WorkflowMemoryStore.definitions.values() if d.tenant_id == tenant_id]


class InMemoryInstanceRepository(IInstanceRepository):
    async def save(self, instance: ProcessInstance) -> None:
        WorkflowMemoryStore.instances[str(instance.id)] = instance

    async def find_by_id(self, tenant_id: str, instance_id: UniqueId) -> ProcessInstance | None:
        instance = WorkflowMemoryStore.instances.get(str(instance_id))
        return instance if instance and instance.tenant_id == tenant_id else None


class InMemoryTaskRepository(ITaskRepository):
    async def save(self, task: Task) -> None:
        WorkflowMemoryStore.tasks[str(task.id)] = task

    async def find_by_id(self, tenant_id: str, task_id: UniqueId) -> Task | None:
        task = WorkflowMemoryStore.tasks.get(str(task_id))
        return task if task and task.tenant_id == tenant_id else None

    async def list_for_assignee(self, tenant_id: str, assignee_id: str) -> list[Task]:
        return [
            t
            for t in WorkflowMemoryStore.tasks.values()
            if t.tenant_id == tenant_id
            and t.assignee_id == assignee_id
            and t.status == TaskStatus.PENDING
        ]

    async def list_by_instance(self, tenant_id: str, instance_id: UniqueId) -> list[Task]:
        return [
            t
            for t in WorkflowMemoryStore.tasks.values()
            if t.tenant_id == tenant_id and str(t.instance_id) == str(instance_id)
        ]
