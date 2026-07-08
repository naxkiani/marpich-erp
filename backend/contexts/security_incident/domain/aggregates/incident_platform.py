"""Enterprise Security Incident Platform aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class IncidentCapability(StrEnum):
    INCIDENT_DETECTION = "incident_detection"
    INCIDENT_CLASSIFICATION = "incident_classification"
    INVESTIGATION = "investigation"
    CONTAINMENT = "containment"
    RECOVERY = "recovery"
    ROOT_CAUSE_ANALYSIS = "root_cause_analysis"
    LESSONS_LEARNED = "lessons_learned"
    EVIDENCE_COLLECTION = "evidence_collection"
    DIGITAL_FORENSICS = "digital_forensics"
    ESCALATION = "escalation"
    NOTIFICATION = "notification"
    SLA = "sla"
    INCIDENT_DASHBOARD = "incident_dashboard"


class IncidentClassification(StrEnum):
    CYBER = "cyber"
    DATA_BREACH = "data_breach"
    UNAUTHORIZED_ACCESS = "unauthorized_access"
    MALWARE = "malware"
    PHISHING = "phishing"
    INSIDER_THREAT = "insider_threat"
    DDOS = "ddos"
    COMPLIANCE_VIOLATION = "compliance_violation"
    PHYSICAL_SECURITY = "physical_security"


class IncidentStatus(StrEnum):
    DETECTED = "detected"
    CLASSIFIED = "classified"
    INVESTIGATING = "investigating"
    CONTAINED = "contained"
    RECOVERING = "recovering"
    RESOLVED = "resolved"
    CLOSED = "closed"
    ESCALATED = "escalated"


class IncidentSeverity(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class SlaStatus(StrEnum):
    ON_TRACK = "on_track"
    AT_RISK = "at_risk"
    BREACHED = "breached"


@dataclass(eq=False, kw_only=True)
class IncidentTenantProfile(AggregateRoot):
    tenant_id: str
    profile_ref: str
    response_sla_hours: int = 4
    resolution_sla_hours: int = 72
    escalation_severity: str = "high"
    auto_notify: bool = True
    forensics_enabled: bool = True
    enabled_classifications: list[str] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        profile_ref: str,
        enabled_classifications: list[str],
        metadata: dict | None = None,
    ) -> IncidentTenantProfile:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            profile_ref=profile_ref,
            enabled_classifications=enabled_classifications,
            metadata=metadata or {},
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "profile_ref": self.profile_ref,
            "tenant_id": self.tenant_id,
            "response_sla_hours": self.response_sla_hours,
            "resolution_sla_hours": self.resolution_sla_hours,
            "escalation_severity": self.escalation_severity,
            "auto_notify": self.auto_notify,
            "forensics_enabled": self.forensics_enabled,
            "enabled_classifications": self.enabled_classifications,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class SecurityIncident(AggregateRoot):
    tenant_id: str
    incident_ref: str
    title: str
    description: str
    classification: str
    severity: str
    status: str
    detected_by: str = ""
    assigned_to: str = ""
    source_module: str = ""
    delegated_to: str | None = None
    root_cause: str = ""
    containment_actions: list[str] = field(default_factory=list)
    recovery_actions: list[str] = field(default_factory=list)
    forensics_summary: str = ""
    sla_status: str = SlaStatus.ON_TRACK.value
    response_due_at: str | None = None
    resolution_due_at: str | None = None
    metadata: dict = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def detect(
        cls,
        *,
        tenant_id: str,
        incident_ref: str,
        title: str,
        description: str,
        classification: str,
        severity: str,
        detected_by: str = "",
        source_module: str = "",
        delegated_to: str | None = None,
        response_due_at: str | None = None,
        resolution_due_at: str | None = None,
        metadata: dict | None = None,
    ) -> SecurityIncident:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            incident_ref=incident_ref,
            title=title,
            description=description,
            classification=classification,
            severity=severity,
            status=IncidentStatus.DETECTED.value,
            detected_by=detected_by,
            source_module=source_module,
            delegated_to=delegated_to,
            response_due_at=response_due_at,
            resolution_due_at=resolution_due_at,
            metadata=metadata or {},
        )

    def classify(self, classification: str, severity: str) -> None:
        self.classification = classification
        self.severity = severity
        self.status = IncidentStatus.CLASSIFIED.value
        self.updated_at = datetime.now(UTC)

    def start_investigation(self, assigned_to: str = "") -> None:
        self.status = IncidentStatus.INVESTIGATING.value
        if assigned_to:
            self.assigned_to = assigned_to
        self.updated_at = datetime.now(UTC)

    def contain(self, actions: list[str]) -> None:
        self.containment_actions.extend(actions)
        self.status = IncidentStatus.CONTAINED.value
        self.updated_at = datetime.now(UTC)

    def recover(self, actions: list[str]) -> None:
        self.recovery_actions.extend(actions)
        self.status = IncidentStatus.RECOVERING.value
        self.updated_at = datetime.now(UTC)

    def set_root_cause(self, root_cause: str) -> None:
        self.root_cause = root_cause
        self.updated_at = datetime.now(UTC)

    def set_forensics(self, summary: str) -> None:
        self.forensics_summary = summary
        self.updated_at = datetime.now(UTC)

    def escalate(self) -> None:
        self.status = IncidentStatus.ESCALATED.value
        self.updated_at = datetime.now(UTC)

    def resolve(self) -> None:
        self.status = IncidentStatus.RESOLVED.value
        self.updated_at = datetime.now(UTC)

    def update_sla(self, sla_status: str) -> None:
        self.sla_status = sla_status
        self.updated_at = datetime.now(UTC)

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "incident_ref": self.incident_ref,
            "tenant_id": self.tenant_id,
            "title": self.title,
            "description": self.description,
            "classification": self.classification,
            "severity": self.severity,
            "status": self.status,
            "detected_by": self.detected_by,
            "assigned_to": self.assigned_to,
            "source_module": self.source_module,
            "delegated_to": self.delegated_to,
            "root_cause": self.root_cause,
            "containment_actions": self.containment_actions,
            "recovery_actions": self.recovery_actions,
            "forensics_summary": self.forensics_summary,
            "sla_status": self.sla_status,
            "response_due_at": self.response_due_at,
            "resolution_due_at": self.resolution_due_at,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class IncidentEvidence(AggregateRoot):
    tenant_id: str
    evidence_ref: str
    incident_ref: str
    evidence_type: str
    description: str
    collected_by: str = ""
    hash_digest: str = ""
    chain_of_custody: list[dict] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def collect(
        cls,
        *,
        tenant_id: str,
        evidence_ref: str,
        incident_ref: str,
        evidence_type: str,
        description: str,
        collected_by: str = "",
        hash_digest: str = "",
        metadata: dict | None = None,
    ) -> IncidentEvidence:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            evidence_ref=evidence_ref,
            incident_ref=incident_ref,
            evidence_type=evidence_type,
            description=description,
            collected_by=collected_by,
            hash_digest=hash_digest,
            chain_of_custody=[{
                "action": "collected",
                "by": collected_by,
                "at": datetime.now(UTC).isoformat(),
            }],
            metadata=metadata or {},
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "evidence_ref": self.evidence_ref,
            "tenant_id": self.tenant_id,
            "incident_ref": self.incident_ref,
            "evidence_type": self.evidence_type,
            "description": self.description,
            "collected_by": self.collected_by,
            "hash_digest": self.hash_digest,
            "chain_of_custody": self.chain_of_custody,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class IncidentNotification(AggregateRoot):
    tenant_id: str
    notification_ref: str
    incident_ref: str
    channel: str
    recipient: str
    subject: str
    message: str
    sent_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def send(
        cls,
        *,
        tenant_id: str,
        notification_ref: str,
        incident_ref: str,
        channel: str,
        recipient: str,
        subject: str,
        message: str,
    ) -> IncidentNotification:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            notification_ref=notification_ref,
            incident_ref=incident_ref,
            channel=channel,
            recipient=recipient,
            subject=subject,
            message=message,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "notification_ref": self.notification_ref,
            "tenant_id": self.tenant_id,
            "incident_ref": self.incident_ref,
            "channel": self.channel,
            "recipient": self.recipient,
            "subject": self.subject,
            "message": self.message,
            "sent_at": self.sent_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class IncidentLessonLearned(AggregateRoot):
    tenant_id: str
    lesson_ref: str
    incident_ref: str
    title: str
    summary: str
    recommendations: list[str] = field(default_factory=list)
    author_id: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def record(
        cls,
        *,
        tenant_id: str,
        lesson_ref: str,
        incident_ref: str,
        title: str,
        summary: str,
        recommendations: list[str],
        author_id: str = "",
    ) -> IncidentLessonLearned:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            lesson_ref=lesson_ref,
            incident_ref=incident_ref,
            title=title,
            summary=summary,
            recommendations=recommendations,
            author_id=author_id,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "lesson_ref": self.lesson_ref,
            "tenant_id": self.tenant_id,
            "incident_ref": self.incident_ref,
            "title": self.title,
            "summary": self.summary,
            "recommendations": self.recommendations,
            "author_id": self.author_id,
            "created_at": self.created_at.isoformat(),
        }
