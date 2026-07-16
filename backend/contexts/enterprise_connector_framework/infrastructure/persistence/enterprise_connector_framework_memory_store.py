"""In-memory Enterprise Connector Framework persistence."""
from __future__ import annotations

from contexts.enterprise_connector_framework.domain.aggregates.enterprise_connector_framework_platform import (
    ConnectorFrameworkProfile,
    ConnectorHealthRecord,
    ConnectorInstance,
    OperationExecution,
    PluginConnectorBinding,
)
from contexts.enterprise_connector_framework.domain.ports.enterprise_connector_framework_repositories import (
    IConnectorFrameworkProfileRepository,
    IConnectorHealthRepository,
    IConnectorInstanceRepository,
    IOperationExecutionRepository,
    IPluginConnectorBindingRepository,
)


class _RefCounter:
    _counters: dict[str, int] = {}

    @classmethod
    def reset(cls) -> None:
        cls._counters = {}

    @classmethod
    def next(cls, tenant_id: str, prefix: str) -> str:
        key = f"{tenant_id}:{prefix}"
        n = cls._counters.get(key, 0) + 1
        cls._counters[key] = n
        return f"{prefix}-{tenant_id[:4].upper()}-{n:05d}"


class InMemoryConnectorFrameworkProfileRepository(IConnectorFrameworkProfileRepository):
    _store: dict[str, ConnectorFrameworkProfile] = {}

    @classmethod
    def reset(cls) -> None:
        cls._store = {}

    async def save(self, profile: ConnectorFrameworkProfile) -> None:
        self._store[str(profile.id)] = profile

    async def find_by_tenant(self, tenant_id: str) -> ConnectorFrameworkProfile | None:
        for profile in self._store.values():
            if profile.tenant_id == tenant_id:
                return profile
        return None

    def next_profile_ref(self, tenant_id: str) -> str:
        return _RefCounter.next(tenant_id, "ERP-CF-PRF")


class InMemoryConnectorInstanceRepository(IConnectorInstanceRepository):
    _store: dict[str, ConnectorInstance] = {}

    @classmethod
    def reset(cls) -> None:
        cls._store = {}

    async def save(self, instance: ConnectorInstance) -> None:
        self._store[str(instance.id)] = instance

    async def list_by_tenant(self, tenant_id: str) -> list[ConnectorInstance]:
        items = [i for i in self._store.values() if i.tenant_id == tenant_id]
        return sorted(items, key=lambda i: i.created_at, reverse=True)

    async def find_by_ref(self, tenant_id: str, instance_ref: str) -> ConnectorInstance | None:
        for instance in self._store.values():
            if instance.tenant_id == tenant_id and instance.instance_ref == instance_ref:
                return instance
        return None

    def next_instance_ref(self, tenant_id: str) -> str:
        return _RefCounter.next(tenant_id, "ERP-CF-INS")


class InMemoryConnectorHealthRepository(IConnectorHealthRepository):
    _store: dict[str, ConnectorHealthRecord] = {}

    @classmethod
    def reset(cls) -> None:
        cls._store = {}

    async def save(self, record: ConnectorHealthRecord) -> None:
        self._store[str(record.id)] = record

    async def list_by_tenant(self, tenant_id: str) -> list[ConnectorHealthRecord]:
        items = [r for r in self._store.values() if r.tenant_id == tenant_id]
        return sorted(items, key=lambda r: r.checked_at, reverse=True)

    def next_health_ref(self, tenant_id: str) -> str:
        return _RefCounter.next(tenant_id, "ERP-CF-HLT")


class InMemoryOperationExecutionRepository(IOperationExecutionRepository):
    _store: dict[str, OperationExecution] = {}

    @classmethod
    def reset(cls) -> None:
        cls._store = {}

    async def save(self, execution: OperationExecution) -> None:
        self._store[str(execution.id)] = execution

    async def list_by_tenant(self, tenant_id: str) -> list[OperationExecution]:
        items = [e for e in self._store.values() if e.tenant_id == tenant_id]
        return sorted(items, key=lambda e: e.created_at, reverse=True)

    def next_execution_ref(self, tenant_id: str) -> str:
        return _RefCounter.next(tenant_id, "ERP-CF-EXE")


class InMemoryPluginConnectorBindingRepository(IPluginConnectorBindingRepository):
    _store: dict[str, PluginConnectorBinding] = {}

    @classmethod
    def reset(cls) -> None:
        cls._store = {}

    async def save(self, binding: PluginConnectorBinding) -> None:
        self._store[str(binding.id)] = binding

    async def list_by_tenant(self, tenant_id: str) -> list[PluginConnectorBinding]:
        items = [b for b in self._store.values() if b.tenant_id == tenant_id]
        return sorted(items, key=lambda b: b.created_at, reverse=True)

    def next_binding_ref(self, tenant_id: str) -> str:
        return _RefCounter.next(tenant_id, "ERP-CF-PLG")
