"""Workflow application service."""
from __future__ import annotations

from contexts.workflow.application.commands.deploy_module_approval import (
    DeployModuleApprovalCommand,
)
from contexts.workflow.application.ports.module_activation import IModuleActivationAdapter
from contexts.workflow.domain.aggregates.process_definition import ProcessDefinition
from contexts.workflow.domain.aggregates.process_instance import ProcessInstance, ProcessStatus
from contexts.workflow.domain.aggregates.task import Task, TaskOutcome
from contexts.workflow.domain.events.integration_events import (
    ProcessCompletedIntegration,
    ProcessStartedIntegration,
    TaskAssignedIntegration,
    TaskCompletedIntegration,
)
from contexts.workflow.domain.ports.repositories import (
    IDefinitionRepository,
    IInstanceRepository,
    ITaskRepository,
)
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.domain.value_objects.unique_id import UniqueId
from shared.infrastructure.messaging.event_bus import publish_integration_event


class WorkflowApplicationService:
    def __init__(
        self,
        definitions: IDefinitionRepository,
        instances: IInstanceRepository,
        tasks: ITaskRepository,
        module_activation: IModuleActivationAdapter,
    ) -> None:
        self._definitions = definitions
        self._instances = instances
        self._tasks = tasks
        self._module_activation = module_activation

    async def handle_module_activated(self, envelope: dict) -> None:
        command = await self._module_activation.parse_module_activated(envelope)
        await self.deploy_module_approval(command)

    async def deploy_module_approval(self, command: DeployModuleApprovalCommand) -> Result[dict]:
        key = f"module.{command.module_id}.approval"
        existing = await self._definitions.find_by_key(command.tenant_id, key)
        if existing:
            return Result.ok(existing.to_dict())

        definition = ProcessDefinition.deploy(
            tenant_id=command.tenant_id,
            key=key,
            name=f"Approval for {command.module_id}",
            steps=[{"key": "module_review", "name": "Module activation review"}],
        )
        await self._definitions.save(definition)
        return Result.ok(definition.to_dict())

    async def deploy_definition(
        self,
        *,
        tenant_id: str,
        key: str,
        name: str,
        steps: list[dict],
    ) -> Result[dict]:
        if not steps:
            return Result.fail("workflow.errors.steps_required")

        existing = await self._definitions.find_by_key(tenant_id, key)
        version = (existing.version + 1) if existing else 1
        definition = ProcessDefinition.deploy(
            tenant_id=tenant_id,
            key=key,
            name=name,
            steps=steps,
            version=version,
        )
        await self._definitions.save(definition)
        return Result.ok(definition.to_dict())

    async def list_definitions(self, tenant_id: str) -> Result[list[dict]]:
        items = await self._definitions.list_by_tenant(tenant_id)
        return Result.ok([d.to_dict() for d in items])

    async def start_instance(
        self,
        *,
        tenant_id: str,
        correlation_id: str,
        definition_key: str,
        context: dict,
        assignees: dict[str, str],
        started_by: str,
    ) -> Result[dict]:
        definition = await self._definitions.find_by_key(tenant_id, definition_key)
        if not definition:
            return Result.fail("workflow.errors.definition_not_found")
        if not definition.steps:
            return Result.fail("workflow.errors.no_steps")

        instance = ProcessInstance.start(
            tenant_id=tenant_id,
            definition_id=definition.id,
            definition_key=definition.key,
            context=context,
            started_by=started_by,
        )
        await self._instances.save(instance)

        await publish_integration_event(
            ProcessStartedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                instance_id=instance.id,
                definition_key=definition.key,
                started_by=started_by,
            )
        )

        task_result = await self._create_task_for_step(
            tenant_id=tenant_id,
            correlation_id=correlation_id,
            instance=instance,
            definition=definition,
            assignees=assignees,
            started_by=started_by,
        )
        if not task_result.succeeded:
            return task_result

        return Result.ok(
            {
                "instance": instance.to_dict(),
                "task": task_result.unwrap(),
            }
        )

    async def _create_task_for_step(
        self,
        *,
        tenant_id: str,
        correlation_id: str,
        instance: ProcessInstance,
        definition: ProcessDefinition,
        assignees: dict[str, str],
        started_by: str,
    ) -> Result[dict]:
        if instance.current_step_index >= len(definition.steps):
            return Result.fail("workflow.errors.no_pending_step")

        step = definition.steps[instance.current_step_index]
        assignee_id = assignees.get(step["key"]) or assignees.get("*") or started_by

        task = Task.create(
            tenant_id=tenant_id,
            instance_id=instance.id,
            step_key=step["key"],
            step_name=step["name"],
            assignee_id=assignee_id,
        )
        await self._tasks.save(task)

        await publish_integration_event(
            TaskAssignedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                task_id=task.id,
                instance_id=instance.id,
                assignee_id=assignee_id,
                step_key=step["key"],
                step_name=step["name"],
            )
        )
        return Result.ok(task.to_dict())

    async def get_instance(self, tenant_id: str, instance_id: str) -> Result[dict]:
        instance = await self._instances.find_by_id(tenant_id, UniqueId.from_string(instance_id))
        if not instance:
            return Result.fail("workflow.errors.instance_not_found")

        tasks = await self._tasks.list_by_instance(tenant_id, instance.id)
        return Result.ok(
            {
                "instance": instance.to_dict(),
                "tasks": [t.to_dict() for t in tasks],
            }
        )

    async def list_tasks(self, tenant_id: str, assignee_id: str) -> Result[list[dict]]:
        tasks = await self._tasks.list_for_assignee(tenant_id, assignee_id)
        return Result.ok([t.to_dict() for t in tasks])

    async def complete_task(
        self,
        *,
        tenant_id: str,
        correlation_id: str,
        task_id: str,
        outcome: str,
        comment: str,
        completed_by: str,
    ) -> Result[dict]:
        task = await self._tasks.find_by_id(tenant_id, UniqueId.from_string(task_id))
        if not task:
            return Result.fail("workflow.errors.task_not_found")
        if task.assignee_id != completed_by:
            return Result.fail("workflow.errors.forbidden")
        if task.status.value != "pending":
            return Result.fail("workflow.errors.task_not_pending")

        try:
            task_outcome = TaskOutcome(outcome)
        except ValueError:
            return Result.fail("workflow.errors.invalid_outcome")

        task.complete(task_outcome, comment)
        await self._tasks.save(task)

        instance = await self._instances.find_by_id(tenant_id, task.instance_id)
        if not instance:
            return Result.fail("workflow.errors.instance_not_found")

        definition = await self._definitions.find_by_key(tenant_id, instance.definition_key)
        if not definition:
            return Result.fail("workflow.errors.definition_not_found")

        await publish_integration_event(
            TaskCompletedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                task_id=task.id,
                instance_id=instance.id,
                outcome=task_outcome.value,
                completed_by=completed_by,
            )
        )

        if task_outcome == TaskOutcome.REJECTED:
            instance.reject()
            await self._instances.save(instance)
            await publish_integration_event(
                ProcessCompletedIntegration(
                    tenant_id=TenantId.create(tenant_id),
                    correlation_id=correlation_id,
                    instance_id=instance.id,
                    definition_key=instance.definition_key,
                    status=instance.status.value,
                )
            )
            return Result.ok({"task": task.to_dict(), "instance": instance.to_dict()})

        instance.advance_step()
        if instance.current_step_index >= len(definition.steps):
            instance.complete()
            await self._instances.save(instance)
            await publish_integration_event(
                ProcessCompletedIntegration(
                    tenant_id=TenantId.create(tenant_id),
                    correlation_id=correlation_id,
                    instance_id=instance.id,
                    definition_key=instance.definition_key,
                    status=instance.status.value,
                )
            )
            return Result.ok({"task": task.to_dict(), "instance": instance.to_dict()})

        await self._instances.save(instance)
        next_task = await self._create_task_for_step(
            tenant_id=tenant_id,
            correlation_id=correlation_id,
            instance=instance,
            definition=definition,
            assignees={},
            started_by=completed_by,
        )
        return Result.ok(
            {
                "task": task.to_dict(),
                "instance": instance.to_dict(),
                "next_task": next_task.unwrap() if next_task.succeeded else None,
            }
        )

    async def delegate_task(
        self,
        *,
        tenant_id: str,
        correlation_id: str,
        task_id: str,
        to_user_id: str,
        delegated_by: str,
    ) -> Result[dict]:
        task = await self._tasks.find_by_id(tenant_id, UniqueId.from_string(task_id))
        if not task:
            return Result.fail("workflow.errors.task_not_found")
        if task.assignee_id != delegated_by:
            return Result.fail("workflow.errors.forbidden")
        if task.status.value != "pending":
            return Result.fail("workflow.errors.task_not_pending")

        task.delegate(to_user_id)
        await self._tasks.save(task)

        await publish_integration_event(
            TaskAssignedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                task_id=task.id,
                instance_id=task.instance_id,
                assignee_id=to_user_id,
                step_key=task.step_key,
                step_name=task.step_name,
            )
        )
        return Result.ok(task.to_dict())
