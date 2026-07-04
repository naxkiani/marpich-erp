"""Workflow DI + event subscriptions."""
from __future__ import annotations

from contexts.workflow.application.service import WorkflowApplicationService
from contexts.workflow.infrastructure.acl.platform_events import PlatformModuleActivationAdapter
from contexts.workflow.infrastructure.persistence.memory_store import (
    InMemoryDefinitionRepository,
    InMemoryInstanceRepository,
    InMemoryTaskRepository,
)
from contexts.workflow.infrastructure.persistence.postgres_store import (
    PostgresDefinitionRepository,
    PostgresInstanceRepository,
    PostgresTaskRepository,
)
from shared.infrastructure.messaging.event_bus import InProcessEventBus
from shared.infrastructure.settings import use_postgres

_service: WorkflowApplicationService | None = None
_registered = False


def get_workflow_service() -> WorkflowApplicationService:
    global _service, _registered
    if _service is None:
        if use_postgres():
            _service = WorkflowApplicationService(
                definitions=PostgresDefinitionRepository(),
                instances=PostgresInstanceRepository(),
                tasks=PostgresTaskRepository(),
                module_activation=PlatformModuleActivationAdapter(),
            )
        else:
            _service = WorkflowApplicationService(
                definitions=InMemoryDefinitionRepository(),
                instances=InMemoryInstanceRepository(),
                tasks=InMemoryTaskRepository(),
                module_activation=PlatformModuleActivationAdapter(),
            )
    if not _registered:
        InProcessEventBus.subscribe(
            "platform.module.activated",
            _service.handle_module_activated,
        )
        _registered = True
    return _service


def reset_workflow_service() -> None:
    global _service, _registered
    _service = None
    _registered = False
