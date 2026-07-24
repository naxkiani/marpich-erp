"""Identity Provider value objects (P200-B7)."""
from __future__ import annotations

from enum import IntEnum, StrEnum

from contexts.identity_federation.domain.value_objects.trust_levels import (
    EnterpriseTrustLevel,
    level_name,
)


class ProviderType(StrEnum):
    INTERNAL = "internal"
    EXTERNAL_ENTERPRISE = "external_enterprise"
    GOVERNMENT = "government"
    BANKING = "banking"
    UNIVERSITY = "university"
    SOCIAL = "social"
    PARTNER = "partner"
    DIRECTORY = "directory"
    MACHINE = "machine"
    AI_AGENT = "ai_agent"
    CUSTOM = "custom"


class ProviderStatus(StrEnum):
    REGISTERED = "registered"
    VERIFIED = "verified"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    DEPROVISIONED = "deprovisioned"
    ARCHIVED = "archived"


class ProviderTrustLevel(IntEnum):
    """Aligned to Trust Fabric EnterpriseTrustLevel 0–5."""

    UNKNOWN = EnterpriseTrustLevel.UNKNOWN
    LIMITED = EnterpriseTrustLevel.LIMITED
    VERIFIED = EnterpriseTrustLevel.VERIFIED
    ENTERPRISE = EnterpriseTrustLevel.ENTERPRISE
    STRATEGIC = EnterpriseTrustLevel.STRATEGIC
    CONTINUOUS_ADAPTIVE = EnterpriseTrustLevel.CONTINUOUS_ADAPTIVE


ALLOWED_STATUS_TRANSITIONS: dict[str, set[str]] = {
    ProviderStatus.REGISTERED.value: {
        ProviderStatus.VERIFIED.value,
        ProviderStatus.SUSPENDED.value,
        ProviderStatus.DEPROVISIONED.value,
    },
    ProviderStatus.VERIFIED.value: {
        ProviderStatus.ACTIVE.value,
        ProviderStatus.SUSPENDED.value,
        ProviderStatus.DEPROVISIONED.value,
    },
    ProviderStatus.ACTIVE.value: {
        ProviderStatus.SUSPENDED.value,
        ProviderStatus.DEPROVISIONED.value,
    },
    ProviderStatus.SUSPENDED.value: {
        ProviderStatus.ACTIVE.value,
        ProviderStatus.VERIFIED.value,
        ProviderStatus.DEPROVISIONED.value,
    },
    ProviderStatus.DEPROVISIONED.value: {ProviderStatus.ARCHIVED.value},
    ProviderStatus.ARCHIVED.value: set(),
}


def normalize_provider_type(value: str | None) -> str:
    raw = (value or ProviderType.CUSTOM.value).strip().lower()
    try:
        return ProviderType(raw).value
    except ValueError:
        return ProviderType.CUSTOM.value


def can_transition_status(*, from_status: str, to_status: str) -> dict:
    allowed = ALLOWED_STATUS_TRANSITIONS.get(from_status, set())
    if to_status == from_status:
        return {"allowed": True, "reason": "unchanged"}
    if to_status not in allowed:
        return {"allowed": False, "reason": "illegal_transition", "from": from_status, "to": to_status}
    return {"allowed": True, "reason": "transition_ok"}


def provider_trust_label(level: int) -> str:
    return level_name(int(level))
