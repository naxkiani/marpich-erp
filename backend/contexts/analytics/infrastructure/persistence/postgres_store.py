"""PostgreSQL repositories — Analytics bounded context."""
from __future__ import annotations

from uuid import UUID

from sqlalchemy import select

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
from shared.infrastructure.database.engine import session_scope
from shared.infrastructure.database.orm import (
    AlertRuleRow,
    DashboardRow,
    MetricDefinitionRow,
    MetricSnapshotRow,
)


class PostgresMetricDefinitionRepository(IMetricDefinitionRepository):
    async def save(self, metric: MetricDefinition) -> None:
        async with session_scope() as session:
            row = await session.scalar(
                select(MetricDefinitionRow).where(
                    MetricDefinitionRow.tenant_id == metric.tenant_id,
                    MetricDefinitionRow.key == metric.key,
                )
            )
            if row is None:
                session.add(
                    MetricDefinitionRow(
                        id=UUID(str(metric.id)),
                        tenant_id=metric.tenant_id,
                        key=metric.key,
                        name=metric.name,
                        event_pattern=metric.event_pattern,
                        description=metric.description,
                        created_at=metric.created_at,
                    )
                )
            else:
                row.name = metric.name
                row.event_pattern = metric.event_pattern
                row.description = metric.description

    async def find_by_key(self, tenant_id: str, key: str) -> MetricDefinition | None:
        async with session_scope() as session:
            row = await session.scalar(
                select(MetricDefinitionRow).where(
                    MetricDefinitionRow.tenant_id == tenant_id,
                    MetricDefinitionRow.key == key.lower(),
                )
            )
            return _metric_from_row(row) if row else None

    async def list_by_tenant(self, tenant_id: str) -> list[MetricDefinition]:
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(MetricDefinitionRow).where(MetricDefinitionRow.tenant_id == tenant_id)
                )
            ).all()
        return [_metric_from_row(r) for r in rows]


class PostgresMetricSnapshotRepository(IMetricSnapshotRepository):
    async def append(self, snapshot: MetricSnapshot) -> None:
        async with session_scope() as session:
            session.add(
                MetricSnapshotRow(
                    id=UUID(str(snapshot.id)),
                    tenant_id=snapshot.tenant_id,
                    metric_key=snapshot.metric_key,
                    value=snapshot.value,
                    event_name=snapshot.event_name,
                    recorded_at=snapshot.recorded_at,
                )
            )

    async def get_current_value(self, tenant_id: str, metric_key: str) -> int:
        async with session_scope() as session:
            row = await session.scalar(
                select(MetricSnapshotRow)
                .where(
                    MetricSnapshotRow.tenant_id == tenant_id,
                    MetricSnapshotRow.metric_key == metric_key,
                )
                .order_by(MetricSnapshotRow.recorded_at.desc())
                .limit(1)
            )
        return row.value if row else 0

    async def list_timeseries(
        self, tenant_id: str, metric_key: str, limit: int = 100
    ) -> list[MetricSnapshot]:
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(MetricSnapshotRow)
                    .where(
                        MetricSnapshotRow.tenant_id == tenant_id,
                        MetricSnapshotRow.metric_key == metric_key,
                    )
                    .order_by(MetricSnapshotRow.recorded_at.desc())
                    .limit(limit)
                )
            ).all()
        return [_snapshot_from_row(r) for r in reversed(rows)]


class PostgresDashboardRepository(IDashboardRepository):
    async def save(self, dashboard: Dashboard) -> None:
        async with session_scope() as session:
            row = await session.get(DashboardRow, UUID(str(dashboard.id)))
            if row is None:
                session.add(
                    DashboardRow(
                        id=UUID(str(dashboard.id)),
                        tenant_id=dashboard.tenant_id,
                        name=dashboard.name,
                        widgets=dashboard.widgets,
                        is_default=dashboard.is_default,
                        created_at=dashboard.created_at,
                    )
                )
            else:
                row.name = dashboard.name
                row.widgets = dashboard.widgets
                row.is_default = dashboard.is_default

    async def find_by_id(self, tenant_id: str, dashboard_id: UniqueId) -> Dashboard | None:
        async with session_scope() as session:
            row = await session.get(DashboardRow, UUID(str(dashboard_id)))
            if row and row.tenant_id == tenant_id:
                return _dashboard_from_row(row)
            return None

    async def list_by_tenant(self, tenant_id: str) -> list[Dashboard]:
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(DashboardRow).where(DashboardRow.tenant_id == tenant_id)
                )
            ).all()
        return [_dashboard_from_row(r) for r in rows]

    async def find_default(self, tenant_id: str) -> Dashboard | None:
        async with session_scope() as session:
            row = await session.scalar(
                select(DashboardRow).where(
                    DashboardRow.tenant_id == tenant_id,
                    DashboardRow.is_default.is_(True),
                )
            )
            return _dashboard_from_row(row) if row else None


class PostgresAlertRuleRepository(IAlertRuleRepository):
    async def save(self, rule: AlertRule) -> None:
        async with session_scope() as session:
            row = await session.get(AlertRuleRow, UUID(str(rule.id)))
            if row is None:
                session.add(
                    AlertRuleRow(
                        id=UUID(str(rule.id)),
                        tenant_id=rule.tenant_id,
                        metric_key=rule.metric_key,
                        name=rule.name,
                        threshold=rule.threshold,
                        operator=rule.operator,
                        is_active=rule.is_active,
                        last_triggered_at=rule.last_triggered_at,
                        created_at=rule.created_at,
                    )
                )
            else:
                row.name = rule.name
                row.threshold = rule.threshold
                row.operator = rule.operator
                row.is_active = rule.is_active
                row.last_triggered_at = rule.last_triggered_at

    async def list_by_tenant(self, tenant_id: str) -> list[AlertRule]:
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(AlertRuleRow).where(AlertRuleRow.tenant_id == tenant_id)
                )
            ).all()
        return [_alert_from_row(r) for r in rows]

    async def list_for_metric(self, tenant_id: str, metric_key: str) -> list[AlertRule]:
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(AlertRuleRow).where(
                        AlertRuleRow.tenant_id == tenant_id,
                        AlertRuleRow.metric_key == metric_key,
                    )
                )
            ).all()
        return [_alert_from_row(r) for r in rows]


def _metric_from_row(row: MetricDefinitionRow) -> MetricDefinition:
    return MetricDefinition(
        id=UniqueId(str(row.id)),
        tenant_id=row.tenant_id,
        key=row.key,
        name=row.name,
        event_pattern=row.event_pattern,
        description=row.description,
        created_at=row.created_at,
    )


def _snapshot_from_row(row: MetricSnapshotRow) -> MetricSnapshot:
    return MetricSnapshot(
        id=UniqueId(str(row.id)),
        tenant_id=row.tenant_id,
        metric_key=row.metric_key,
        value=row.value,
        event_name=row.event_name,
        recorded_at=row.recorded_at,
    )


def _dashboard_from_row(row: DashboardRow) -> Dashboard:
    return Dashboard(
        id=UniqueId(str(row.id)),
        tenant_id=row.tenant_id,
        name=row.name,
        widgets=row.widgets,
        is_default=row.is_default,
        created_at=row.created_at,
    )


def _alert_from_row(row: AlertRuleRow) -> AlertRule:
    return AlertRule(
        id=UniqueId(str(row.id)),
        tenant_id=row.tenant_id,
        metric_key=row.metric_key,
        name=row.name,
        threshold=row.threshold,
        operator=row.operator,
        is_active=row.is_active,
        last_triggered_at=row.last_triggered_at,
        created_at=row.created_at,
    )
