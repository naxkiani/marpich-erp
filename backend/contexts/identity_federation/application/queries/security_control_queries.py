"""Federation Security Control Plane queries (P200-B9)."""
from __future__ import annotations

from dataclasses import dataclass

from contexts.identity_federation.domain.services.eiftp_security_zero_trust import (
    validate_security_zero_trust_foundation,
)
from contexts.identity_federation.domain.services.federation_security_control_plane import (
    get_federation_security_control_plane,
)
from contexts.identity_federation.infrastructure.persistence.security_control_memory_store import (
    SecurityControlMemoryStore,
)


@dataclass(frozen=True, slots=True)
class GetRiskAssessmentQuery:
    tenant_id: str
    assessment_ref: str


@dataclass(frozen=True, slots=True)
class GetThreatStatusQuery:
    tenant_id: str
    limit: int = 50


@dataclass(frozen=True, slots=True)
class GetComplianceStatusQuery:
    tenant_id: str


@dataclass(frozen=True, slots=True)
class GetSecurityEventsQuery:
    tenant_id: str
    limit: int = 50


def handle_get_security_posture(*, tenant_id: str) -> dict:
    controls = [c for k, c in SecurityControlMemoryStore.controls.items() if k.startswith(f"{tenant_id}:")]
    threats = [
        t
        for k, t in SecurityControlMemoryStore.threats.items()
        if k.startswith(f"{tenant_id}:") and t.status == "open"
    ]
    comps = [c for k, c in SecurityControlMemoryStore.compliance.items() if k.startswith(f"{tenant_id}:")]
    last_comp = comps[-1].status if comps else None
    return get_federation_security_control_plane().security_posture(
        summary={
            "controls_count": len(controls),
            "open_threats": len(threats),
            "last_compliance_status": last_comp,
        }
    )


async def handle_get_risk_assessment(query: GetRiskAssessmentQuery) -> dict:
    item = SecurityControlMemoryStore.risks.get(f"{query.tenant_id}:{query.assessment_ref}")
    if item is None:
        raise ValueError("security.risk_not_found")
    return item.to_dict()


async def handle_get_threat_status(query: GetThreatStatusQuery) -> dict:
    items = [
        t.to_dict()
        for k, t in SecurityControlMemoryStore.threats.items()
        if k.startswith(f"{query.tenant_id}:")
    ]
    return {"threats": items[-min(query.limit, 100) :], "count": len(items)}


async def handle_get_compliance_status(query: GetComplianceStatusQuery) -> dict:
    items = [
        c.to_dict()
        for k, c in SecurityControlMemoryStore.compliance.items()
        if k.startswith(f"{query.tenant_id}:")
    ]
    latest = items[-1] if items else None
    return {"latest": latest, "history_count": len(items)}


async def handle_get_security_events(query: GetSecurityEventsQuery) -> dict:
    events = [
        e
        for e in SecurityControlMemoryStore.events
        if e.get("tenant_id") == query.tenant_id
    ]
    return {"events": events[-min(query.limit, 100) :], "count": len(events)}


def handle_get_zero_trust_decision(*, tenant_id: str) -> dict:
    decision = SecurityControlMemoryStore.last_zt.get(tenant_id)
    if decision is None:
        raise ValueError("security.zt_decision_not_found")
    return decision


def handle_get_security_surface() -> dict:
    return {
        **get_federation_security_control_plane().surface(),
        "validation": validate_security_zero_trust_foundation(),
    }
