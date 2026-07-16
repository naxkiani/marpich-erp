"""Enterprise Security Incident Platform engine."""
from __future__ import annotations

from collections import defaultdict
from datetime import UTC, datetime, timedelta

from contexts.security_incident.domain.aggregates.incident_platform import (
    IncidentCapability,
    IncidentClassification,
    IncidentSeverity,
    IncidentStatus,
    SlaStatus,
)

PLATFORM_CATALOG: dict[str, dict] = {
    IncidentCapability.INCIDENT_DETECTION.value: {
        "label": "Incident Detection",
        "delegates_to": "security",
        "no_duplication": True,
    },
    IncidentCapability.INCIDENT_CLASSIFICATION.value: {"label": "Incident Classification"},
    IncidentCapability.INVESTIGATION.value: {"label": "Investigation"},
    IncidentCapability.CONTAINMENT.value: {"label": "Containment"},
    IncidentCapability.RECOVERY.value: {"label": "Recovery"},
    IncidentCapability.ROOT_CAUSE_ANALYSIS.value: {"label": "Root Cause Analysis"},
    IncidentCapability.LESSONS_LEARNED.value: {"label": "Lessons Learned"},
    IncidentCapability.EVIDENCE_COLLECTION.value: {"label": "Evidence Collection"},
    IncidentCapability.DIGITAL_FORENSICS.value: {
        "label": "Digital Forensics",
        "explainable": True,
        "autonomous_execution": False,
    },
    IncidentCapability.ESCALATION.value: {
        "label": "Escalation",
        "delegates_to": "workflow",
        "emergency_lock": True,
    },
    IncidentCapability.NOTIFICATION.value: {"label": "Notification"},
    IncidentCapability.SLA.value: {"label": "SLA"},
    IncidentCapability.INCIDENT_DASHBOARD.value: {"label": "Incident Dashboard"},
}

POLICY_KEYS = [
    "incident.detection.sensitivity_threshold",
    "incident.escalation.severity_threshold",
    "incident.sla.response_hours",
    "incident.sla.resolution_hours",
    "incident.notification.auto_notify",
]

CLASSIFICATION_DELEGATION: dict[str, str | None] = {
    IncidentClassification.CYBER.value: "security",
    IncidentClassification.DATA_BREACH.value: "data_protection",
    IncidentClassification.UNAUTHORIZED_ACCESS.value: "security",
    IncidentClassification.MALWARE.value: "security",
    IncidentClassification.PHISHING.value: "security",
    IncidentClassification.INSIDER_THREAT.value: "security",
    IncidentClassification.DDOS.value: "security",
    IncidentClassification.COMPLIANCE_VIOLATION.value: "grc",
    IncidentClassification.PHYSICAL_SECURITY.value: None,
}

DEFAULT_SEED_INCIDENTS: list[dict] = [
    {
        "title": "Brute-force login attempts detected",
        "description": "Multiple failed login attempts from external IP range",
        "classification": IncidentClassification.UNAUTHORIZED_ACCESS.value,
        "severity": IncidentSeverity.HIGH.value,
        "status": IncidentStatus.INVESTIGATING.value,
        "delegated_to": "security",
    },
    {
        "title": "Suspicious outbound data transfer",
        "description": "Large volume of encrypted data exfiltrated to unknown endpoint",
        "classification": IncidentClassification.DATA_BREACH.value,
        "severity": IncidentSeverity.CRITICAL.value,
        "status": IncidentStatus.CONTAINED.value,
        "delegated_to": "data_protection",
    },
    {
        "title": "Phishing email campaign targeting finance team",
        "description": "Credential harvesting links sent to 12 employees",
        "classification": IncidentClassification.PHISHING.value,
        "severity": IncidentSeverity.MEDIUM.value,
        "status": IncidentStatus.CLASSIFIED.value,
        "delegated_to": "security",
    },
    {
        "title": "Ransomware signature on endpoint",
        "description": "EDR flagged ransomware behavior on workstation",
        "classification": IncidentClassification.MALWARE.value,
        "severity": IncidentSeverity.CRITICAL.value,
        "status": IncidentStatus.RECOVERING.value,
        "delegated_to": "security",
    },
    {
        "title": "DDoS attack on public API gateway",
        "description": "Traffic spike exceeding 10x baseline from botnet",
        "classification": IncidentClassification.DDOS.value,
        "severity": IncidentSeverity.HIGH.value,
        "status": IncidentStatus.RESOLVED.value,
        "delegated_to": "security",
    },
    {
        "title": "Insider access to restricted financial records",
        "description": "Employee accessed records outside assigned role scope",
        "classification": IncidentClassification.INSIDER_THREAT.value,
        "severity": IncidentSeverity.HIGH.value,
        "status": IncidentStatus.DETECTED.value,
        "delegated_to": "security",
    },
]


def list_capability_catalog() -> list[dict]:
    return [{"capability": k, **v} for k, v in PLATFORM_CATALOG.items()]


def list_policy_keys() -> list[str]:
    return list(POLICY_KEYS)


def list_classifications() -> list[dict]:
    return [
        {
            "classification": c.value,
            "label": c.value.replace("_", " ").title(),
            "delegates_to": CLASSIFICATION_DELEGATION.get(c.value),
        }
        for c in IncidentClassification
    ]


def dependency_map() -> dict:
    nodes = [{"id": "security_incident", "type": "platform", "label": "Security Incident Platform"}]
    edges = []
    for mod in ("security", "workflow", "audit", "grc", "data_protection", "fraud_detection"):
        nodes.append({"id": mod, "type": "module", "label": mod})
        edges.append({"from": mod, "to": "security_incident", "type": "feeds_incident"})
    for svc in ("policy",):
        nodes.append({"id": svc, "type": "shared_service", "label": svc})
        edges.append({"from": "security_incident", "to": svc, "type": "delegates"})
    return {"nodes": nodes, "edges": edges, "no_incident_duplication": True}


def severity_rank(severity: str) -> int:
    ranks = {
        IncidentSeverity.LOW.value: 1,
        IncidentSeverity.MEDIUM.value: 2,
        IncidentSeverity.HIGH.value: 3,
        IncidentSeverity.CRITICAL.value: 4,
    }
    return ranks.get(severity, 0)


def should_auto_escalate(severity: str, threshold: str) -> bool:
    return severity_rank(severity) >= severity_rank(threshold)


def compute_sla_deadlines(
    *,
    response_hours: int,
    resolution_hours: int,
    detected_at: datetime | None = None,
) -> dict[str, str]:
    base = detected_at or datetime.now(UTC)
    return {
        "response_due_at": (base + timedelta(hours=response_hours)).isoformat(),
        "resolution_due_at": (base + timedelta(hours=resolution_hours)).isoformat(),
    }


def evaluate_sla(
    *,
    incident: dict,
    response_hours: int,
    resolution_hours: int,
) -> str:
    if incident.get("status") in (IncidentStatus.RESOLVED.value, IncidentStatus.CLOSED.value):
        return SlaStatus.ON_TRACK.value

    now = datetime.now(UTC)
    resolution_due = incident.get("resolution_due_at")
    response_due = incident.get("response_due_at")

    if resolution_due:
        due = datetime.fromisoformat(resolution_due)
        if now > due:
            return SlaStatus.BREACHED.value
        if now > due - timedelta(hours=resolution_hours * 0.25):
            return SlaStatus.AT_RISK.value

    if response_due and incident.get("status") == IncidentStatus.DETECTED.value:
        due = datetime.fromisoformat(response_due)
        if now > due:
            return SlaStatus.BREACHED.value

    return SlaStatus.ON_TRACK.value


def build_dashboard(
    *,
    profile: dict | None,
    incidents: list[dict],
    evidence: list[dict],
    notifications: list[dict],
    lessons: list[dict],
) -> dict:
    open_statuses = {
        IncidentStatus.DETECTED.value,
        IncidentStatus.CLASSIFIED.value,
        IncidentStatus.INVESTIGATING.value,
        IncidentStatus.CONTAINED.value,
        IncidentStatus.RECOVERING.value,
        IncidentStatus.ESCALATED.value,
    }
    open_incidents = [i for i in incidents if i.get("status") in open_statuses]
    by_status: dict[str, int] = defaultdict(int)
    by_severity: dict[str, int] = defaultdict(int)
    by_classification: dict[str, int] = defaultdict(int)
    sla_breached = 0

    for inc in incidents:
        by_status[inc.get("status", "unknown")] += 1
        by_severity[inc.get("severity", "low")] += 1
        by_classification[inc.get("classification", "unknown")] += 1
        if inc.get("sla_status") == SlaStatus.BREACHED.value:
            sla_breached += 1

    return {
        "summary": {
            "total_incidents": len(incidents),
            "open_incidents": len(open_incidents),
            "escalated_incidents": len([i for i in incidents if i.get("status") == IncidentStatus.ESCALATED.value]),
            "resolved_incidents": len([i for i in incidents if i.get("status") == IncidentStatus.RESOLVED.value]),
            "sla_breached": sla_breached,
            "capabilities": len(PLATFORM_CATALOG),
            "evidence_items": len(evidence),
            "notifications_sent": len(notifications),
            "lessons_recorded": len(lessons),
            "enabled_classifications": profile.get("enabled_classifications", []) if profile else [],
        },
        "by_status": dict(by_status),
        "by_severity": dict(by_severity),
        "by_classification": dict(by_classification),
        "recent_incidents": sorted(incidents, key=lambda i: i.get("created_at", ""), reverse=True)[:5],
        "delegation": {
            "security_attack_monitoring": True,
            "workflow_emergency_lock": True,
            "audit_trail": True,
            "local_incident_duplication": False,
        },
        "generated_at": datetime.now(UTC).isoformat(),
    }


def digital_forensics_analysis(*, incident: dict, evidence: list[dict]) -> dict:
    related = [e for e in evidence if e.get("incident_ref") == incident.get("incident_ref")]
    findings = []
    if incident.get("classification") in (
        IncidentClassification.MALWARE.value,
        IncidentClassification.DATA_BREACH.value,
    ):
        findings.append({
            "finding": "malware_artifacts_present",
            "confidence": 0.85,
            "evidence_count": len(related),
        })
    if incident.get("classification") == IncidentClassification.UNAUTHORIZED_ACCESS.value:
        findings.append({
            "finding": "authentication_anomaly",
            "confidence": 0.78,
            "evidence_count": len(related),
        })

    return {
        "incident_ref": incident.get("incident_ref"),
        "findings": findings,
        "evidence_reviewed": len(related),
        "timeline_events": len(related) + 2,
        "explainable": True,
        "autonomous_execution": False,
        "recommendations": [
            "Preserve chain of custody for all collected evidence",
            "Correlate with security attack events from security platform",
        ],
    }
