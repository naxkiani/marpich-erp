"""Map integration event envelopes to audit entry fields."""
from __future__ import annotations

from datetime import UTC, datetime

from contexts.audit.domain.aggregates.audit_entry import AuditEntry, AuditSeverity
from contexts.audit.domain.ports.event_mapping import IAuditEventMapper

SECURITY_EVENTS = frozenset(
    {
        "identity.user.logged_in",
        "identity.login.succeeded",
        "identity.login.failed",
        "authentication.login.succeeded",
        "authentication.login.failed",
        "authentication.session.revoked",
        "authorization.access.denied",
    }
)

COMPLIANCE_EVENTS = frozenset(
    {
        "audit.export.completed",
        "audit.retention.applied",
        "organization.member.removed",
        "settings.configuration.changed",
    }
)

RESOURCE_HINTS: dict[str, tuple[str, str]] = {
    "user_id": ("user", "user_id"),
    "patient_id": ("patient", "patient_id"),
    "encounter_id": ("encounter", "encounter_id"),
    "organization_id": ("organization", "organization_id"),
    "unit_id": ("org_unit", "unit_id"),
    "export_id": ("audit_export", "export_id"),
    "journal_id": ("journal", "journal_id"),
    "invoice_id": ("invoice", "invoice_id"),
}


def _parse_occurred_at(value: str | None) -> datetime:
    if not value:
        return datetime.now(UTC)
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return datetime.now(UTC)


def _resolve_resource(payload: dict) -> tuple[str, str | None]:
    for key, (resource_type, payload_key) in RESOURCE_HINTS.items():
        if payload_key in payload and payload[payload_key]:
            return resource_type, str(payload[payload_key])
    return "event", None


def _resolve_actor(payload: dict) -> str | None:
    for key in ("user_id", "actor_id", "requested_by"):
        if payload.get(key):
            return str(payload[key])
    return None


def _resolve_severity(event_name: str) -> AuditSeverity:
    if event_name in SECURITY_EVENTS:
        return AuditSeverity.SECURITY
    if event_name in COMPLIANCE_EVENTS:
        return AuditSeverity.COMPLIANCE
    return AuditSeverity.INFO


def map_envelope_to_entry(envelope: dict) -> AuditEntry:
    event_name = envelope.get("event_name", "unknown")
    payload = envelope.get("payload") or {}
    resource_type, resource_id = _resolve_resource(payload)
    action = event_name.replace(".", "_")

    return AuditEntry.from_integration_event(
        tenant_id=envelope.get("tenant_id", "unknown"),
        event_name=event_name,
        source_context=envelope.get("source_context", "unknown"),
        correlation_id=envelope.get("correlation_id", ""),
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        actor_id=_resolve_actor(payload),
        severity=_resolve_severity(event_name),
        payload=payload,
        occurred_at=_parse_occurred_at(envelope.get("occurred_at")),
    )


class IntegrationEventMapper:
    def map_envelope(self, envelope: dict) -> AuditEntry:
        return map_envelope_to_entry(envelope)
