"""Map integration events to compliance violations."""
from __future__ import annotations

VIOLATION_RULES: tuple[dict, ...] = (
    {
        "event_name": "policy.evaluation.denied",
        "domain": "internal_policies",
        "control_id": "POL-001",
        "severity": "high",
        "title": "Required policy not active",
    },
    {
        "event_name": "authorization.access.denied",
        "domain": "security_compliance",
        "control_id": "SEC-002",
        "severity": "medium",
        "title": "Unauthorized access attempt",
    },
    {
        "event_name": "identity.login.failed",
        "domain": "security_compliance",
        "control_id": "SEC-001",
        "severity": "high",
        "title": "Failed login attempt",
    },
    {
        "event_name": "audit.retention.applied",
        "domain": "retention_policies",
        "control_id": "AUD-002",
        "severity": "high",
        "title": "Audit retention purge applied",
    },
    {
        "event_name": "hospital.patient.accessed",
        "domain": "healthcare_compliance",
        "control_id": "HIPAA-164.312-b",
        "severity": "critical",
        "title": "PHI access compliance check",
        "missing_payload_field": "reason",
        "missing_payload_message": "PHI access without documented reason",
    },
    {
        "event_name": "university.student.record.accessed",
        "domain": "educational_compliance",
        "control_id": "FERPA-001",
        "severity": "critical",
        "title": "Student record accessed",
    },
)


def match_violation(envelope: dict) -> dict | None:
    event_name = envelope.get("event_name", "")
    for rule in VIOLATION_RULES:
        if rule["event_name"] != event_name:
            continue
        missing_field = rule.get("missing_payload_field")
        if missing_field:
            payload = envelope.get("payload") or {}
            if payload.get(missing_field):
                continue
            return {
                **rule,
                "title": rule.get("missing_payload_message", rule["title"]),
            }
        if event_name == "authorization.access.denied":
            continue
        if event_name == "identity.login.failed":
            continue
        return rule
    return None
