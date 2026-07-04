"""In-memory analytics repositories."""
from __future__ import annotations

from contexts.analytics.domain.aggregates.alert_rule import AlertRule
from contexts.analytics.domain.aggregates.dashboard import Dashboard
from contexts.analytics.domain.aggregates.metric_definition import MetricDefinition
from contexts.analytics.domain.aggregates.metric_snapshot import MetricSnapshot
from contexts.analytics.domain.ports.repositories import (
    IAlertRuleRepository,
    IDashboardRepository,
    IMetricDefinitionRepository,
    IMetricSnapshotRepository,
)
from shared.domain.value_objects.unique_id import UniqueId


class AnalyticsMemoryStore:
    metrics: dict[str, MetricDefinition] = {}
    snapshots: list[MetricSnapshot] = []
    dashboards: dict[str, Dashboard] = {}
    alerts: dict[str, AlertRule] = {}
    event_counts: dict[str, int] = {}

    @classmethod
    def reset(cls) -> None:
        cls.metrics.clear()
        cls.snapshots.clear()
        cls.dashboards.clear()
        cls.alerts.clear()
        cls.event_counts.clear()


class InMemoryMetricDefinitionRepository(IMetricDefinitionRepository):
    def _key(self, tenant_id: str, metric_key: str) -> str:
        return f"{tenant_id}:{metric_key}"

    async def save(self, metric: MetricDefinition) -> None:
        AnalyticsMemoryStore.metrics[self._key(metric.tenant_id, metric.key)] = metric

    async def find_by_key(self, tenant_id: str, key: str) -> MetricDefinition | None:
        return AnalyticsMemoryStore.metrics.get(self._key(tenant_id, key.lower()))

    async def list_by_tenant(self, tenant_id: str) -> list[MetricDefinition]:
        return [m for m in AnalyticsMemoryStore.metrics.values() if m.tenant_id == tenant_id]


class InMemoryMetricSnapshotRepository(IMetricSnapshotRepository):
    async def append(self, snapshot: MetricSnapshot) -> None:
        AnalyticsMemoryStore.snapshots.append(snapshot)

    async def get_current_value(self, tenant_id: str, metric_key: str) -> int:
        values = [
            s.value
            for s in AnalyticsMemoryStore.snapshots
            if s.tenant_id == tenant_id and s.metric_key == metric_key
        ]
        return values[-1] if values else 0

    async def list_timeseries(self, tenant_id: str, metric_key: str, limit: int = 100) -> list[MetricSnapshot]:
        items = [
            s
            for s in AnalyticsMemoryStore.snapshots
            if s.tenant_id == tenant_id and s.metric_key == metric_key
        ]
        return items[-limit:]


class InMemoryDashboardRepository(IDashboardRepository):
    async def save(self, dashboard: Dashboard) -> None:
        AnalyticsMemoryStore.dashboards[str(dashboard.id)] = dashboard

    async def find_by_id(self, tenant_id: str, dashboard_id: UniqueId) -> Dashboard | None:
        dashboard = AnalyticsMemoryStore.dashboards.get(str(dashboard_id))
        return dashboard if dashboard and dashboard.tenant_id == tenant_id else None

    async def list_by_tenant(self, tenant_id: str) -> list[Dashboard]:
        return [d for d in AnalyticsMemoryStore.dashboards.values() if d.tenant_id == tenant_id]

    async def find_default(self, tenant_id: str) -> Dashboard | None:
        for dashboard in AnalyticsMemoryStore.dashboards.values():
            if dashboard.tenant_id == tenant_id and dashboard.is_default:
                return dashboard
        return None


class InMemoryAlertRuleRepository(IAlertRuleRepository):
    async def save(self, rule: AlertRule) -> None:
        AnalyticsMemoryStore.alerts[str(rule.id)] = rule

    async def list_by_tenant(self, tenant_id: str) -> list[AlertRule]:
        return [a for a in AnalyticsMemoryStore.alerts.values() if a.tenant_id == tenant_id]

    async def list_for_metric(self, tenant_id: str, metric_key: str) -> list[AlertRule]:
        return [
            a
            for a in AnalyticsMemoryStore.alerts.values()
            if a.tenant_id == tenant_id and a.metric_key == metric_key
        ]
