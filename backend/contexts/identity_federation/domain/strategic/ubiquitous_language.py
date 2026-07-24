"""Ubiquitous language registry — P200-B3 strategic DDD (code-enforced terms)."""
from __future__ import annotations

from enum import StrEnum


class FederatedSubjectKind(StrEnum):
    HUMAN = "human"
    MACHINE = "machine"
    SERVICE = "service"
    AI_AGENT = "ai_agent"
    DEVICE = "device"
    PARTNER = "partner"
    API = "api"


class TrustStatus(StrEnum):
    PENDING = "pending"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    REVOKED = "revoked"
    EXPIRED = "expired"


class TrustLevel(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


# Canonical terms that MUST NOT be confused across BCs
UL_FORBIDDEN_ALIASES = {
    "authorization_decision_as_trust_score": "Trust Facts are not Permit/Deny",
    "user_for_all_subjects": "Use FederatedSubjectKind for non-human subjects",
    "vendor_connector_as_aggregate": "Connectors execute in Integration Platform",
}

CORE_DOMAINS = ("DOM_FEDERATION", "DOM_TRUST")
