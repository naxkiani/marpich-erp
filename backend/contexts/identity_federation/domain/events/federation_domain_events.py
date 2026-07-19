"""Tactical domain events raised by federation aggregates (P200-B4)."""
from __future__ import annotations

from dataclasses import dataclass

from shared.domain.events.domain_event import DomainEvent


@dataclass(frozen=True, kw_only=True)
class TrustGranted(DomainEvent):
    trust_ref: str
    trust_score: int

    @property
    def event_name(self) -> str:
        return "federation.domain.trust.granted"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"trust_ref": self.trust_ref, "trust_score": self.trust_score}


@dataclass(frozen=True, kw_only=True)
class TrustRevoked(DomainEvent):
    trust_ref: str
    reason: str = ""

    @property
    def event_name(self) -> str:
        return "federation.domain.trust.revoked"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"trust_ref": self.trust_ref, "reason": self.reason}


@dataclass(frozen=True, kw_only=True)
class SessionTerminated(DomainEvent):
    session_ref: str
    reason: str = "terminated"

    @property
    def event_name(self) -> str:
        return "federation.domain.session.terminated"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"session_ref": self.session_ref, "reason": self.reason}


@dataclass(frozen=True, kw_only=True)
class FederationConnected(DomainEvent):
    provider_ref: str
    protocol: str

    @property
    def event_name(self) -> str:
        return "federation.domain.provider.connected"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"provider_ref": self.provider_ref, "protocol": self.protocol}


@dataclass(frozen=True, kw_only=True)
class FederationDisconnected(DomainEvent):
    provider_ref: str

    @property
    def event_name(self) -> str:
        return "federation.domain.provider.disconnected"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"provider_ref": self.provider_ref}


@dataclass(frozen=True, kw_only=True)
class IdentityLinked(DomainEvent):
    link_ref: str
    user_id: str
    provider_id: str
    external_subject: str

    @property
    def event_name(self) -> str:
        return "federation.domain.identity.linked"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "link_ref": self.link_ref,
            "user_id": self.user_id,
            "provider_id": self.provider_id,
            "external_subject": self.external_subject,
        }


@dataclass(frozen=True, kw_only=True)
class IdentityUnlinked(DomainEvent):
    link_ref: str
    user_id: str

    @property
    def event_name(self) -> str:
        return "federation.domain.identity.unlinked"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"link_ref": self.link_ref, "user_id": self.user_id}


@dataclass(frozen=True, kw_only=True)
class AIIdentityRegistered(DomainEvent):
    agent_ref: str
    owner_principal_id: str

    @property
    def event_name(self) -> str:
        return "federation.domain.ai.registered"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"agent_ref": self.agent_ref, "owner_principal_id": self.owner_principal_id}


@dataclass(frozen=True, kw_only=True)
class AIIdentityRevoked(DomainEvent):
    agent_ref: str
    reason: str = ""

    @property
    def event_name(self) -> str:
        return "federation.domain.ai.revoked"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"agent_ref": self.agent_ref, "reason": self.reason}
