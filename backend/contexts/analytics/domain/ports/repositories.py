"""Analytics repository ports."""
from __future__ import annotations

from abc import ABC, abstractmethod

from contexts.analytics.domain.aggregates.alert_rule import AlertRule
from contexts.analytics.domain.aggregates.dashboard import Dashboard
from contexts.analytics.domain.aggregates.metric_definition import MetricDefinition
from contexts.analytics.domain.aggregates.metric_snapshot import MetricSnapshot
from shared.domain.value_objects.unique_id import UniqueId


class IMetricDefinitionRepository(ABC):
    @abstractmethod
    async def save(self, metric: MetricDefinition) -> None: ...

    @abstractmethod
    async def find_by_key(self, tenant_id: str, key: str) -> MetricDefinition | None: ...

    @abstractmethod
    async def list_by_tenant(self, tenant_id: str) -> list[MetricDefinition]: ...


class IMetricSnapshotRepository(ABC):
    @abstractmethod
    async def append(self, snapshot: MetricSnapshot) -> None: ...

    @abstractmethod
    async def get_current_value(self, tenant_id: str, metric_key: str) -> int: ...

    @abstractmethod
    async def list_timeseries(self, tenant_id: str, metric_key: str, limit: int = 100) -> list[MetricSnapshot]: ...


class IDashboardRepository(ABC):
    @abstractmethod
    async def save(self, dashboard: Dashboard) -> None: ...

    @abstractmethod
    async def find_by_id(self, tenant_id: str, dashboard_id: UniqueId) -> Dashboard | None: ...

    @abstractmethod
    async def list_by_tenant(self, tenant_id: str) -> list[Dashboard]: ...

    @abstractmethod
    async def find_default(self, tenant_id: str) -> Dashboard | None: ...


class IAlertRuleRepository(ABC):
    @abstractmethod
    async def save(self, rule: AlertRule) -> None: ...

    @abstractmethod
    async def list_by_tenant(self, tenant_id: str) -> list[AlertRule]: ...

    @abstractmethod
    async def list_for_metric(self, tenant_id: str, metric_key: str) -> list[AlertRule]: ...
