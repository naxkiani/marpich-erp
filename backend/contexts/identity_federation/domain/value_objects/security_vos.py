"""Federation security value objects (P200-B9)."""
from __future__ import annotations

from enum import IntEnum, StrEnum


class SecurityLevel(IntEnum):
    MINIMAL = 0
    STANDARD = 1
    HARDENED = 2
    MAXIMUM = 3


class SecurityClassification(StrEnum):
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"


class ZeroTrustGateAction(StrEnum):
    ALLOW = "allow"
    ALLOW_WITH_CONDITIONS = "allow_with_conditions"
    CHALLENGE = "challenge"
    REQUIRE_MFA = "require_mfa"
    REQUIRE_STEP_UP = "require_step_up"
    DENY = "deny"
    QUARANTINE = "quarantine"
    ESCALATE = "escalate"


class RiskLevel(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


COMPLIANCE_FRAMEWORKS = (
    "ISO_27001",
    "SOC_2",
    "NIST_CSF",
    "CIS",
    "GDPR",
    "PCI_DSS",
    "HIPAA_READY",
)
