"""Analytics integration events."""
from __future__ import annotations

from dataclasses import dataclass

from shared.domain.events.integration_event import IntegrationEvent


@dataclass(frozen=True, kw_only=True)
class AlertTriggeredIntegration(IntegrationEvent):
    alert_id: str
    metric_key: str
    current_value: int
    threshold: int

    @property
    def event_name(self) -> str:
        return "analytics.alert.triggered"

    @property
    def source_context(self) -> str:
        return "analytics"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "alert_id": self.alert_id,
            "metric_key": self.metric_key,
            "current_value": self.current_value,
            "threshold": self.threshold,
        }


@dataclass(frozen=True, kw_only=True)
class ReportGeneratedIntegration(IntegrationEvent):
    dashboard_id: str
    report_name: str

    @property
    def event_name(self) -> str:
        return "analytics.report.generated"

    @property
    def source_context(self) -> str:
        return "analytics"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "dashboard_id": self.dashboard_id,
            "report_name": self.report_name,
        }
