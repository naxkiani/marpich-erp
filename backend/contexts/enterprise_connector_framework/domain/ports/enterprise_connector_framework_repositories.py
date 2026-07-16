"""Enterprise Connector Framework repository ports."""
from __future__ import annotations

from abc import ABC, abstractmethod

from contexts.enterprise_connector_framework.domain.aggregates.enterprise_connector_framework_platform import (
    ConnectorFrameworkProfile,
    ConnectorHealthRecord,
    ConnectorInstance,
    OperationExecution,
    PluginConnectorBinding,
)


class IConnectorFrameworkProfileRepository(ABC):
    @abstractmethod
    async def save(self, profile: ConnectorFrameworkProfile) -> None: ...

    @abstractmethod
    async def find_by_tenant(self, tenant_id: str) -> ConnectorFrameworkProfile | None: ...

    @abstractmethod
    def next_profile_ref(self, tenant_id: str) -> str: ...


class IConnectorInstanceRepository(ABC):
    @abstractmethod
    async def save(self, instance: ConnectorInstance) -> None: ...

    @abstractmethod
    async def list_by_tenant(self, tenant_id: str) -> list[ConnectorInstance]: ...

    @abstractmethod
    async def find_by_ref(self, tenant_id: str, instance_ref: str) -> ConnectorInstance | None: ...

    @abstractmethod
    def next_instance_ref(self, tenant_id: str) -> str: ...


class IConnectorHealthRepository(ABC):
    @abstractmethod
    async def save(self, record: ConnectorHealthRecord) -> None: ...

    @abstractmethod
    async def list_by_tenant(self, tenant_id: str) -> list[ConnectorHealthRecord]: ...

    @abstractmethod
    def next_health_ref(self, tenant_id: str) -> str: ...


class IOperationExecutionRepository(ABC):
    @abstractmethod
    async def save(self, execution: OperationExecution) -> None: ...

    @abstractmethod
    async def list_by_tenant(self, tenant_id: str) -> list[OperationExecution]: ...

    @abstractmethod
    def next_execution_ref(self, tenant_id: str) -> str: ...


class IPluginConnectorBindingRepository(ABC):
    @abstractmethod
    async def save(self, binding: PluginConnectorBinding) -> None: ...

    @abstractmethod
    async def list_by_tenant(self, tenant_id: str) -> list[PluginConnectorBinding]: ...

    @abstractmethod
    def next_binding_ref(self, tenant_id: str) -> str: ...
