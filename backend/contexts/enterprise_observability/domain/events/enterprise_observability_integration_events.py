"""Enterprise Observability integration events."""
from __future__ import annotations

from dataclasses import dataclass

from shared.domain.events.integration_event import IntegrationEvent


@dataclass(frozen=True, kw_only=True)
class AlertTriggeredIntegration(IntegrationEvent):
    alert_ref: str
    signal: str
    metric_key: str
    severity: str

    @property
    def event_name(self) -> str:
        return "enterprise_observability.alert.triggered"

    @property
    def source_context(self) -> str:
        return "enterprise_observability"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "alert_ref": self.alert_ref,
            "signal": self.signal,
            "metric_key": self.metric_key,
            "severity": self.severity,
        }


@dataclass(frozen=True, kw_only=True)
class IncidentCreatedIntegration(IntegrationEvent):
    incident_ref: str
    title: str
    severity: str
    source_signal: str

    @property
    def event_name(self) -> str:
        return "enterprise_observability.incident.created"

    @property
    def source_context(self) -> str:
        return "enterprise_observability"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "incident_ref": self.incident_ref,
            "title": self.title,
            "severity": self.severity,
            "source_signal": self.source_signal,
        }


@dataclass(frozen=True, kw_only=True)
class IncidentResolvedIntegration(IntegrationEvent):
    incident_ref: str
    resolution_summary: str

    @property
    def event_name(self) -> str:
        return "enterprise_observability.incident.resolved"

    @property
    def source_context(self) -> str:
        return "enterprise_observability"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "incident_ref": self.incident_ref,
            "resolution_summary": self.resolution_summary,
        }


@dataclass(frozen=True, kw_only=True)
class OperationalDashboardGeneratedIntegration(IntegrationEvent):
    platform_status: str
    active_alerts: int
    open_incidents: int

    @property
    def event_name(self) -> str:
        return "enterprise_observability.dashboard.generated"

    @property
    def source_context(self) -> str:
        return "enterprise_observability"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "platform_status": self.platform_status,
            "active_alerts": self.active_alerts,
            "open_incidents": self.open_incidents,
        }
