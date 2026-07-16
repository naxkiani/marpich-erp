"""Enterprise Connector Framework DI + event subscriptions."""
from __future__ import annotations

from contexts.enterprise_connector_framework.application.service import EnterpriseConnectorFrameworkApplicationService
from contexts.enterprise_connector_framework.infrastructure.adapters.connector_sdk_bridge import (
    ConnectorSdkBridge,
    get_connector_sdk_bridge,
)
from contexts.enterprise_connector_framework.infrastructure.persistence.enterprise_connector_framework_memory_store import (
    InMemoryConnectorFrameworkProfileRepository,
    InMemoryConnectorHealthRepository,
    InMemoryConnectorInstanceRepository,
    InMemoryOperationExecutionRepository,
    InMemoryPluginConnectorBindingRepository,
)
from contexts.policy.container import get_policy_evaluator
from shared.infrastructure.messaging.event_bus import InProcessEventBus

_service: EnterpriseConnectorFrameworkApplicationService | None = None
_registered = False


def get_enterprise_connector_framework_service() -> EnterpriseConnectorFrameworkApplicationService:
    global _service, _registered
    if _service is None:
        _service = EnterpriseConnectorFrameworkApplicationService(
            profiles=InMemoryConnectorFrameworkProfileRepository(),
            instances=InMemoryConnectorInstanceRepository(),
            health=InMemoryConnectorHealthRepository(),
            executions=InMemoryOperationExecutionRepository(),
            plugin_bindings=InMemoryPluginConnectorBindingRepository(),
            policy_evaluator=get_policy_evaluator(),
            sdk_bridge=get_connector_sdk_bridge(),
        )
    if not _registered:
        InProcessEventBus.subscribe("platform.tenant.provisioned", _service.handle_tenant_provisioned)
        _registered = True
    return _service


def reset_enterprise_connector_framework_service() -> None:
    global _service, _registered
    _service = None
    _registered = False
    ConnectorSdkBridge.reset()
    InMemoryConnectorFrameworkProfileRepository.reset()
    InMemoryConnectorInstanceRepository.reset()
    InMemoryConnectorHealthRepository.reset()
    InMemoryOperationExecutionRepository.reset()
    InMemoryPluginConnectorBindingRepository.reset()
