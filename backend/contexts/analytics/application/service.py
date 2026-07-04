"""Analytics application service."""
from __future__ import annotations

from contexts.analytics.application.constants.default_metrics import DEFAULT_METRICS, DEFAULT_WIDGETS
from contexts.analytics.domain.aggregates.alert_rule import AlertRule
from contexts.analytics.domain.aggregates.dashboard import Dashboard
from contexts.analytics.domain.aggregates.metric_definition import MetricDefinition
from contexts.analytics.domain.aggregates.metric_snapshot import MetricSnapshot
from contexts.analytics.domain.events.integration_events import AlertTriggeredIntegration
from contexts.analytics.domain.ports.event_counts import IEventCountStore
from contexts.analytics.domain.ports.repositories import (
    IAlertRuleRepository,
    IDashboardRepository,
    IMetricDefinitionRepository,
    IMetricSnapshotRepository,
)
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.domain.value_objects.unique_id import UniqueId
from shared.infrastructure.messaging.event_bus import publish_integration_event

class AnalyticsApplicationService:
    def __init__(
        self,
        metrics: IMetricDefinitionRepository,
        snapshots: IMetricSnapshotRepository,
        dashboards: IDashboardRepository,
        alerts: IAlertRuleRepository,
        event_counts: IEventCountStore,
    ) -> None:
        self._metrics = metrics
        self._snapshots = snapshots
        self._dashboards = dashboards
        self._alerts = alerts
        self._event_counts = event_counts

    async def handle_tenant_provisioned(self, envelope: dict) -> None:
        tenant_id = envelope["tenant_id"]
        existing = await self._dashboards.find_default(tenant_id)
        if existing:
            return

        for key, name, pattern in DEFAULT_METRICS:
            metric = MetricDefinition.create(
                tenant_id=tenant_id,
                key=key,
                name=name,
                event_pattern=pattern,
            )
            await self._metrics.save(metric)
            await self._record_metric(tenant_id, key, 0, None)

        dashboard = Dashboard.create(
            tenant_id=tenant_id,
            name="Overview",
            widgets=DEFAULT_WIDGETS,
            is_default=True,
        )
        await self._dashboards.save(dashboard)

    async def handle_integration_event(self, envelope: dict) -> None:
        event_name = envelope.get("event_name", "")
        if event_name.startswith("analytics."):
            return

        tenant_id = envelope.get("tenant_id", "")
        if not tenant_id:
            return

        self._event_counts.increment(tenant_id, event_name)

        await self._increment_metric(tenant_id, "events.total", event_name)

        definitions = await self._metrics.list_by_tenant(tenant_id)
        for definition in definitions:
            if definition.key == "events.total":
                continue
            if definition.matches(event_name):
                await self._increment_metric(tenant_id, definition.key, event_name)

    async def _increment_metric(self, tenant_id: str, metric_key: str, event_name: str | None) -> None:
        current = await self._snapshots.get_current_value(tenant_id, metric_key)
        new_value = current + 1
        await self._record_metric(tenant_id, metric_key, new_value, event_name)
        await self._check_alerts(tenant_id, metric_key, new_value)

    async def _record_metric(
        self, tenant_id: str, metric_key: str, value: int, event_name: str | None
    ) -> None:
        snapshot = MetricSnapshot.record(
            tenant_id=tenant_id,
            metric_key=metric_key,
            value=value,
            event_name=event_name,
        )
        await self._snapshots.append(snapshot)

    async def _check_alerts(self, tenant_id: str, metric_key: str, value: int) -> None:
        rules = await self._alerts.list_for_metric(tenant_id, metric_key)
        for rule in rules:
            if rule.should_trigger(value):
                rule.mark_triggered()
                await self._alerts.save(rule)
                await publish_integration_event(
                    AlertTriggeredIntegration(
                        tenant_id=TenantId.create(tenant_id),
                        correlation_id=f"alert-{rule.id}",
                        alert_id=str(rule.id),
                        metric_key=metric_key,
                        current_value=value,
                        threshold=rule.threshold,
                    )
                )

    async def list_metrics(self, tenant_id: str) -> Result[list[dict]]:
        definitions = await self._metrics.list_by_tenant(tenant_id)
        result = []
        for definition in definitions:
            current = await self._snapshots.get_current_value(tenant_id, definition.key)
            result.append(definition.to_dict(current_value=current))
        return Result.ok(result)

    async def get_timeseries(self, tenant_id: str, metric_key: str) -> Result[dict]:
        definition = await self._metrics.find_by_key(tenant_id, metric_key)
        if not definition:
            return Result.fail("analytics.errors.metric_not_found")

        series = await self._snapshots.list_timeseries(tenant_id, metric_key)
        return Result.ok(
            {
                "metric": definition.to_dict(
                    current_value=await self._snapshots.get_current_value(tenant_id, metric_key)
                ),
                "points": [p.to_dict() for p in series],
            }
        )

    async def list_dashboards(self, tenant_id: str) -> Result[list[dict]]:
        items = await self._dashboards.list_by_tenant(tenant_id)
        return Result.ok([d.to_dict() for d in items])

    async def get_dashboard(self, tenant_id: str, dashboard_id: str) -> Result[dict]:
        dashboard = await self._dashboards.find_by_id(tenant_id, UniqueId.from_string(dashboard_id))
        if not dashboard:
            return Result.fail("analytics.errors.dashboard_not_found")

        widget_data = []
        for widget in dashboard.widgets:
            metric_key = widget.get("metric_key")
            value = await self._snapshots.get_current_value(tenant_id, metric_key) if metric_key else 0
            widget_data.append({**widget, "value": value})

        return Result.ok({"dashboard": dashboard.to_dict(), "widgets": widget_data})

    async def create_alert(
        self,
        *,
        tenant_id: str,
        metric_key: str,
        name: str,
        threshold: int,
        operator: str = "gte",
    ) -> Result[dict]:
        metric = await self._metrics.find_by_key(tenant_id, metric_key)
        if not metric:
            return Result.fail("analytics.errors.metric_not_found")

        rule = AlertRule.create(
            tenant_id=tenant_id,
            metric_key=metric_key,
            name=name,
            threshold=threshold,
            operator=operator,
        )
        await self._alerts.save(rule)
        return Result.ok(rule.to_dict())

    async def list_alerts(self, tenant_id: str) -> Result[list[dict]]:
        items = await self._alerts.list_by_tenant(tenant_id)
        return Result.ok([a.to_dict() for a in items])

    async def get_events_summary(self, tenant_id: str) -> Result[dict]:
        counts = self._event_counts.summary(tenant_id)
        total = sum(counts.values())

        top_events = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:10]
        return Result.ok(
            {
                "total_events": total,
                "unique_event_types": len(counts),
                "top_events": [{"event_name": k, "count": v} for k, v in top_events],
            }
        )
