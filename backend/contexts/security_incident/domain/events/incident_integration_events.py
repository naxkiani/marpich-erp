"""Enterprise Security Incident Platform integration events."""
from __future__ import annotations

from dataclasses import dataclass

from shared.domain.events.integration_event import IntegrationEvent


@dataclass(frozen=True, kw_only=True)
class IncidentDetectedIntegration(IntegrationEvent):
    incident_ref: str
    classification: str
    severity: str

    @property
    def event_name(self) -> str:
        return "incident.detected"

    @property
    def source_context(self) -> str:
        return "security_incident"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "incident_ref": self.incident_ref,
            "classification": self.classification,
            "severity": self.severity,
        }


@dataclass(frozen=True, kw_only=True)
class IncidentClassifiedIntegration(IntegrationEvent):
    incident_ref: str
    classification: str
    severity: str

    @property
    def event_name(self) -> str:
        return "incident.classified"

    @property
    def source_context(self) -> str:
        return "security_incident"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "incident_ref": self.incident_ref,
            "classification": self.classification,
            "severity": self.severity,
        }


@dataclass(frozen=True, kw_only=True)
class IncidentEscalatedIntegration(IntegrationEvent):
    incident_ref: str
    severity: str

    @property
    def event_name(self) -> str:
        return "incident.escalated"

    @property
    def source_context(self) -> str:
        return "security_incident"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"incident_ref": self.incident_ref, "severity": self.severity}


@dataclass(frozen=True, kw_only=True)
class IncidentContainedIntegration(IntegrationEvent):
    incident_ref: str
    actions: list[str]

    @property
    def event_name(self) -> str:
        return "incident.contained"

    @property
    def source_context(self) -> str:
        return "security_incident"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"incident_ref": self.incident_ref, "actions": self.actions}


@dataclass(frozen=True, kw_only=True)
class IncidentResolvedIntegration(IntegrationEvent):
    incident_ref: str
    root_cause: str

    @property
    def event_name(self) -> str:
        return "incident.resolved"

    @property
    def source_context(self) -> str:
        return "security_incident"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"incident_ref": self.incident_ref, "root_cause": self.root_cause}


@dataclass(frozen=True, kw_only=True)
class IncidentEvidenceCollectedIntegration(IntegrationEvent):
    incident_ref: str
    evidence_ref: str
    evidence_type: str

    @property
    def event_name(self) -> str:
        return "incident.evidence.collected"

    @property
    def source_context(self) -> str:
        return "security_incident"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "incident_ref": self.incident_ref,
            "evidence_ref": self.evidence_ref,
            "evidence_type": self.evidence_type,
        }


@dataclass(frozen=True, kw_only=True)
class IncidentNotificationSentIntegration(IntegrationEvent):
    incident_ref: str
    notification_ref: str
    channel: str

    @property
    def event_name(self) -> str:
        return "incident.notification.sent"

    @property
    def source_context(self) -> str:
        return "security_incident"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "incident_ref": self.incident_ref,
            "notification_ref": self.notification_ref,
            "channel": self.channel,
        }
