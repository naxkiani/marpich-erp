"""PostgreSQL repositories — Workflow bounded context."""
from __future__ import annotations

from uuid import UUID

from sqlalchemy import select

from contexts.workflow.domain.aggregates.process_definition import ProcessDefinition
from contexts.workflow.domain.aggregates.process_instance import ProcessInstance, ProcessStatus
from contexts.workflow.domain.aggregates.task import Task, TaskOutcome, TaskStatus
from contexts.workflow.domain.ports.repositories import (
    IDefinitionRepository,
    IInstanceRepository,
    ITaskRepository,
)
from shared.domain.value_objects.unique_id import UniqueId
from shared.infrastructure.database.engine import session_scope
from shared.infrastructure.database.orm import ProcessDefinitionRow, ProcessInstanceRow, TaskRow


class PostgresDefinitionRepository(IDefinitionRepository):
    async def save(self, definition: ProcessDefinition) -> None:
        async with session_scope() as session:
            row = await session.scalar(
                select(ProcessDefinitionRow).where(
                    ProcessDefinitionRow.tenant_id == definition.tenant_id,
                    ProcessDefinitionRow.key == definition.key,
                )
            )
            if row is None:
                session.add(
                    ProcessDefinitionRow(
                        id=UUID(str(definition.id)),
                        tenant_id=definition.tenant_id,
                        key=definition.key,
                        name=definition.name,
                        version=definition.version,
                        steps=definition.steps,
                        is_active=definition.is_active,
                        created_at=definition.created_at,
                    )
                )
            else:
                row.name = definition.name
                row.version = definition.version
                row.steps = definition.steps
                row.is_active = definition.is_active

    async def find_by_key(self, tenant_id: str, key: str) -> ProcessDefinition | None:
        async with session_scope() as session:
            row = await session.scalar(
                select(ProcessDefinitionRow).where(
                    ProcessDefinitionRow.tenant_id == tenant_id,
                    ProcessDefinitionRow.key == key.lower(),
                )
            )
            return _definition_from_row(row) if row else None

    async def list_by_tenant(self, tenant_id: str) -> list[ProcessDefinition]:
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(ProcessDefinitionRow).where(ProcessDefinitionRow.tenant_id == tenant_id)
                )
            ).all()
        return [_definition_from_row(r) for r in rows]


class PostgresInstanceRepository(IInstanceRepository):
    async def save(self, instance: ProcessInstance) -> None:
        async with session_scope() as session:
            row = await session.get(ProcessInstanceRow, UUID(str(instance.id)))
            if row is None:
                session.add(
                    ProcessInstanceRow(
                        id=UUID(str(instance.id)),
                        tenant_id=instance.tenant_id,
                        definition_id=UUID(str(instance.definition_id)),
                        definition_key=instance.definition_key,
                        status=instance.status.value,
                        current_step_index=instance.current_step_index,
                        context=instance.context,
                        started_by=instance.started_by,
                        started_at=instance.started_at,
                        completed_at=instance.completed_at,
                    )
                )
            else:
                row.status = instance.status.value
                row.current_step_index = instance.current_step_index
                row.context = instance.context
                row.completed_at = instance.completed_at

    async def find_by_id(self, tenant_id: str, instance_id: UniqueId) -> ProcessInstance | None:
        async with session_scope() as session:
            row = await session.get(ProcessInstanceRow, UUID(str(instance_id)))
            if row and row.tenant_id == tenant_id:
                return _instance_from_row(row)
            return None


class PostgresTaskRepository(ITaskRepository):
    async def save(self, task: Task) -> None:
        async with session_scope() as session:
            row = await session.get(TaskRow, UUID(str(task.id)))
            if row is None:
                session.add(
                    TaskRow(
                        id=UUID(str(task.id)),
                        tenant_id=task.tenant_id,
                        instance_id=UUID(str(task.instance_id)),
                        step_key=task.step_key,
                        step_name=task.step_name,
                        assignee_id=task.assignee_id,
                        status=task.status.value,
                        outcome=task.outcome.value if task.outcome else None,
                        comment=task.comment,
                        delegated_from=task.delegated_from,
                        created_at=task.created_at,
                        completed_at=task.completed_at,
                    )
                )
            else:
                row.assignee_id = task.assignee_id
                row.status = task.status.value
                row.outcome = task.outcome.value if task.outcome else None
                row.comment = task.comment
                row.delegated_from = task.delegated_from
                row.completed_at = task.completed_at

    async def find_by_id(self, tenant_id: str, task_id: UniqueId) -> Task | None:
        async with session_scope() as session:
            row = await session.get(TaskRow, UUID(str(task_id)))
            if row and row.tenant_id == tenant_id:
                return _task_from_row(row)
            return None

    async def list_for_assignee(self, tenant_id: str, assignee_id: str) -> list[Task]:
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(TaskRow).where(
                        TaskRow.tenant_id == tenant_id,
                        TaskRow.assignee_id == assignee_id,
                        TaskRow.status == TaskStatus.PENDING.value,
                    )
                )
            ).all()
        return [_task_from_row(r) for r in rows]

    async def list_by_instance(self, tenant_id: str, instance_id: UniqueId) -> list[Task]:
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(TaskRow).where(
                        TaskRow.tenant_id == tenant_id,
                        TaskRow.instance_id == UUID(str(instance_id)),
                    )
                )
            ).all()
        return [_task_from_row(r) for r in rows]


def _definition_from_row(row: ProcessDefinitionRow) -> ProcessDefinition:
    return ProcessDefinition(
        id=UniqueId(str(row.id)),
        tenant_id=row.tenant_id,
        key=row.key,
        name=row.name,
        version=row.version,
        steps=row.steps,
        is_active=row.is_active,
        created_at=row.created_at,
    )


def _instance_from_row(row: ProcessInstanceRow) -> ProcessInstance:
    return ProcessInstance(
        id=UniqueId(str(row.id)),
        tenant_id=row.tenant_id,
        definition_id=UniqueId(str(row.definition_id)),
        definition_key=row.definition_key,
        status=ProcessStatus(row.status),
        current_step_index=row.current_step_index,
        context=row.context,
        started_by=row.started_by,
        started_at=row.started_at,
        completed_at=row.completed_at,
    )


def _task_from_row(row: TaskRow) -> Task:
    return Task(
        id=UniqueId(str(row.id)),
        tenant_id=row.tenant_id,
        instance_id=UniqueId(str(row.instance_id)),
        step_key=row.step_key,
        step_name=row.step_name,
        assignee_id=row.assignee_id,
        status=TaskStatus(row.status),
        outcome=TaskOutcome(row.outcome) if row.outcome else None,
        comment=row.comment,
        delegated_from=row.delegated_from,
        created_at=row.created_at,
        completed_at=row.completed_at,
    )
