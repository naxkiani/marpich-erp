"""Cross-tenant trust value objects (P200-B8)."""
from __future__ import annotations

from enum import StrEnum


class TenantTrustStatus(StrEnum):
    REQUESTED = "requested"
    PENDING_APPROVAL = "pending_approval"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    REVOKED = "revoked"


class DelegationType(StrEnum):
    USER = "user"
    ORGANIZATION = "organization"
    SERVICE = "service"
    AI_AGENT = "ai_agent"


class ExternalIdentityKind(StrEnum):
    GUEST = "guest"
    CUSTOMER = "customer"
    PARTNER = "partner"
    TEMPORARY = "temporary"
