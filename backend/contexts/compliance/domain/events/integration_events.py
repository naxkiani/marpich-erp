"""Compliance integration events."""
from __future__ import annotations

from dataclasses import dataclass

from shared.domain.events.integration_event import IntegrationEvent


@dataclass(frozen=True, kw_only=True)
class ViolationDetectedIntegration(IntegrationEvent):
    violation_id: str
    domain: str
    control_id: str
    severity: str
    title: str

    @property
    def event_name(self) -> str:
        return "compliance.violation.detected"

    @property
    def source_context(self) -> str:
        return "compliance"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "violation_id": self.violation_id,
            "domain": self.domain,
            "control_id": self.control_id,
            "severity": self.severity,
            "title": self.title,
        }


@dataclass(frozen=True, kw_only=True)
class AlertTriggeredIntegration(IntegrationEvent):
    violation_id: str
    domain: str
    severity: str

    @property
    def event_name(self) -> str:
        return "compliance.alert.triggered"

    @property
    def source_context(self) -> str:
        return "compliance"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "violation_id": self.violation_id,
            "domain": self.domain,
            "severity": self.severity,
        }


@dataclass(frozen=True, kw_only=True)
class ReportGeneratedIntegration(IntegrationEvent):
    report_id: str
    report_type: str

    @property
    def event_name(self) -> str:
        return "compliance.report.generated"

    @property
    def source_context(self) -> str:
        return "compliance"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "report_id": self.report_id,
            "report_type": self.report_type,
        }
