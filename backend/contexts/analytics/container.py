"""Analytics DI + event subscriptions."""
from __future__ import annotations

from contexts.analytics.application.service import AnalyticsApplicationService
from contexts.analytics.infrastructure.persistence.event_count_store import EventCountMemoryStore
from contexts.analytics.infrastructure.persistence.memory_store import (
    InMemoryAlertRuleRepository,
    InMemoryDashboardRepository,
    InMemoryMetricDefinitionRepository,
    InMemoryMetricSnapshotRepository,
)
from contexts.analytics.infrastructure.persistence.postgres_store import (
    PostgresAlertRuleRepository,
    PostgresDashboardRepository,
    PostgresMetricDefinitionRepository,
    PostgresMetricSnapshotRepository,
)
from shared.infrastructure.messaging.event_bus import InProcessEventBus
from shared.infrastructure.settings import use_postgres

_service: AnalyticsApplicationService | None = None
_registered = False


def get_analytics_service() -> AnalyticsApplicationService:
    global _service, _registered
    if _service is None:
        if use_postgres():
            _service = AnalyticsApplicationService(
                metrics=PostgresMetricDefinitionRepository(),
                snapshots=PostgresMetricSnapshotRepository(),
                dashboards=PostgresDashboardRepository(),
                alerts=PostgresAlertRuleRepository(),
                event_counts=EventCountMemoryStore(),
            )
        else:
            _service = AnalyticsApplicationService(
                metrics=InMemoryMetricDefinitionRepository(),
                snapshots=InMemoryMetricSnapshotRepository(),
                dashboards=InMemoryDashboardRepository(),
                alerts=InMemoryAlertRuleRepository(),
                event_counts=EventCountMemoryStore(),
            )
    if not _registered:
        InProcessEventBus.subscribe("*", _service.handle_integration_event)
        InProcessEventBus.subscribe(
            "platform.tenant.provisioned",
            _service.handle_tenant_provisioned,
        )
        _registered = True
    return _service


def reset_analytics_service() -> None:
    global _service, _registered
    _service = None
    _registered = False
