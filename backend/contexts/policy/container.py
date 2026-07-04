"""Policy DI + event subscriptions."""
from __future__ import annotations

from contexts.policy.application.service import PolicyApplicationService
from contexts.policy.infrastructure.adapters.policy_evaluator_client import PolicyEvaluatorClient
from contexts.policy.infrastructure.persistence.memory_store import (
    InMemoryPolicyRepository,
    InMemoryPolicyVersionRepository,
)
from contexts.policy.infrastructure.persistence.postgres_store import (
    PostgresPolicyRepository,
    PostgresPolicyVersionRepository,
)
from shared.application.ports.policy import IPolicyEvaluator
from shared.infrastructure.messaging.event_bus import InProcessEventBus
from shared.infrastructure.settings import use_postgres

_service: PolicyApplicationService | None = None
_evaluator: PolicyEvaluatorClient | None = None
_registered = False


def get_policy_service() -> PolicyApplicationService:
    global _service, _evaluator, _registered
    if _service is None:
        if use_postgres():
            _service = PolicyApplicationService(
                policies=PostgresPolicyRepository(),
                versions=PostgresPolicyVersionRepository(),
            )
        else:
            _service = PolicyApplicationService(
                policies=InMemoryPolicyRepository(),
                versions=InMemoryPolicyVersionRepository(),
            )
        _evaluator = PolicyEvaluatorClient(_service)
    if not _registered:
        InProcessEventBus.subscribe(
            "platform.tenant.provisioned",
            _service.handle_tenant_provisioned,
        )
        InProcessEventBus.subscribe(
            "workflow.process.completed",
            _service.handle_workflow_process_completed,
        )
        _registered = True
    return _service


def get_policy_evaluator() -> IPolicyEvaluator:
    get_policy_service()
    assert _evaluator is not None
    return _evaluator


def reset_policy_service() -> None:
    global _service, _evaluator, _registered
    _service = None
    _evaluator = None
    _registered = False
