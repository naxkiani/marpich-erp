"""Value objects for tactical federation domain model (P200-B4)."""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class ProtocolType(StrEnum):
    OAUTH2 = "oauth2"
    OIDC = "oidc"
    SAML = "saml"
    SCIM = "scim"
    LDAP = "ldap"
    CUSTOM = "custom"


class FederationStatus(StrEnum):
    DRAFT = "draft"
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    ERROR = "error"


class AssuranceLevel(StrEnum):
    AAL1 = "aal1"
    AAL2 = "aal2"
    AAL3 = "aal3"


class SessionState(StrEnum):
    ACTIVE = "active"
    ELEVATED = "elevated"
    SUSPENDED = "suspended"
    TERMINATED = "terminated"
    EXPIRED = "expired"


class RiskLevel(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass(frozen=True, slots=True)
class TrustScore:
    value: int

    def __post_init__(self) -> None:
        if not 0 <= self.value <= 100:
            raise ValueError("trust_score must be 0..100")

    def to_level(self) -> str:
        if self.value >= 80:
            return "high"
        if self.value >= 40:
            return "medium"
        return "low"


@dataclass(frozen=True, slots=True)
class RiskScore:
    value: float

    def __post_init__(self) -> None:
        if not 0.0 <= self.value <= 100.0:
            raise ValueError("risk_score must be 0..100")


@dataclass(frozen=True, slots=True)
class ExternalSubject:
    value: str

    def __post_init__(self) -> None:
        if not self.value or not self.value.strip():
            raise ValueError("external_subject required")


@dataclass(frozen=True, slots=True)
class CapabilitySet:
    capabilities: tuple[str, ...]

    @classmethod
    def of(cls, *caps: str) -> CapabilitySet:
        return cls(capabilities=tuple(sorted(set(caps))))
