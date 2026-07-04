"""Workflow repository ports."""
from __future__ import annotations

from abc import ABC, abstractmethod

from contexts.workflow.domain.aggregates.process_definition import ProcessDefinition
from contexts.workflow.domain.aggregates.process_instance import ProcessInstance
from contexts.workflow.domain.aggregates.task import Task
from shared.domain.value_objects.unique_id import UniqueId


class IDefinitionRepository(ABC):
    @abstractmethod
    async def save(self, definition: ProcessDefinition) -> None: ...

    @abstractmethod
    async def find_by_key(self, tenant_id: str, key: str) -> ProcessDefinition | None: ...

    @abstractmethod
    async def list_by_tenant(self, tenant_id: str) -> list[ProcessDefinition]: ...


class IInstanceRepository(ABC):
    @abstractmethod
    async def save(self, instance: ProcessInstance) -> None: ...

    @abstractmethod
    async def find_by_id(self, tenant_id: str, instance_id: UniqueId) -> ProcessInstance | None: ...


class ITaskRepository(ABC):
    @abstractmethod
    async def save(self, task: Task) -> None: ...

    @abstractmethod
    async def find_by_id(self, tenant_id: str, task_id: UniqueId) -> Task | None: ...

    @abstractmethod
    async def list_for_assignee(self, tenant_id: str, assignee_id: str) -> list[Task]: ...

    @abstractmethod
    async def list_by_instance(self, tenant_id: str, instance_id: UniqueId) -> list[Task]: ...
