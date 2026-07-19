"""Event ownership registry — only owning BC may publish."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class EventOwnership:
    logical_name: str
    owner_bc: str
    wire_name: str | None = None


# Strategic events from P200-B3 matrix (logical → owner)
EVENT_OWNERSHIP: tuple[EventOwnership, ...] = (
    EventOwnership("IdentityCreated", "identity"),
    EventOwnership("IdentityUpdated", "identity"),
    EventOwnership("IdentityDeleted", "identity"),
    EventOwnership("UserInvited", "identity"),
    EventOwnership("UserActivated", "identity"),
    EventOwnership("UserDisabled", "identity"),
    EventOwnership("FederationEstablished", "identity_federation", "federation.provider.registered"),
    EventOwnership("FederationRemoved", "identity_federation", "federation.provider.removed"),
    EventOwnership("TrustGranted", "identity_federation", "federation.trust.changed"),
    EventOwnership("TrustRevoked", "identity_federation", "federation.trust.changed"),
    EventOwnership("MFAEnabled", "mfa"),
    EventOwnership("SessionCreated", "identity_federation", "federation.session.created"),
    EventOwnership("SessionExpired", "identity_federation", "federation.session.expired"),
    EventOwnership("TokenIssued", "identity_federation", "federation.token.issued"),
    EventOwnership("TokenRevoked", "identity_federation", "federation.token.revoked"),
    EventOwnership("PolicyChanged", "policy"),
    EventOwnership("AIIdentityRegistered", "identity_federation", "federation.ai.agent.registered"),
)


def owner_for(logical_name: str) -> str | None:
    for row in EVENT_OWNERSHIP:
        if row.logical_name == logical_name:
            return row.owner_bc
    return None


def federation_may_publish(logical_name: str) -> bool:
    return owner_for(logical_name) == "identity_federation"
