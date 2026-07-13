"""Authentication integration events."""
from __future__ import annotations

from dataclasses import dataclass

from shared.domain.events.integration_event import IntegrationEvent


@dataclass(frozen=True, kw_only=True)
class PasskeyRegisteredIntegration(IntegrationEvent):
    user_id: str
    credential_ref: str

    @property
    def event_name(self) -> str:
        return "authentication.passkey.registered"

    @property
    def source_context(self) -> str:
        return "authentication"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"user_id": self.user_id, "credential_ref": self.credential_ref}


@dataclass(frozen=True, kw_only=True)
class PasskeyRevokedIntegration(IntegrationEvent):
    user_id: str
    credential_ref: str

    @property
    def event_name(self) -> str:
        return "authentication.passkey.revoked"

    @property
    def source_context(self) -> str:
        return "authentication"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"user_id": self.user_id, "credential_ref": self.credential_ref}


@dataclass(frozen=True, kw_only=True)
class OidcProviderRegisteredIntegration(IntegrationEvent):
    provider_ref: str
    name: str

    @property
    def event_name(self) -> str:
        return "authentication.oidc.provider.registered"

    @property
    def source_context(self) -> str:
        return "authentication"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"provider_ref": self.provider_ref, "name": self.name}


@dataclass(frozen=True, kw_only=True)
class AuthenticationLoginSuccessIntegration(IntegrationEvent):
    user_id: str
    auth_method: str

    @property
    def event_name(self) -> str:
        return "authentication.login.success"

    @property
    def source_context(self) -> str:
        return "authentication"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"user_id": self.user_id, "auth_method": self.auth_method}
