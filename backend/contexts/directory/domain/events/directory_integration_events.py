"""Directory integration events."""
from __future__ import annotations

from dataclasses import dataclass

from shared.domain.events.integration_event import IntegrationEvent


@dataclass(frozen=True, kw_only=True)
class SamlProviderRegisteredIntegration(IntegrationEvent):
    provider_ref: str
    name: str

    @property
    def event_name(self) -> str:
        return "directory.saml.provider.registered"

    @property
    def source_context(self) -> str:
        return "directory"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"provider_ref": self.provider_ref, "name": self.name}


@dataclass(frozen=True, kw_only=True)
class LdapConnectorRegisteredIntegration(IntegrationEvent):
    connector_ref: str
    name: str

    @property
    def event_name(self) -> str:
        return "directory.ldap.connector.registered"

    @property
    def source_context(self) -> str:
        return "directory"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"connector_ref": self.connector_ref, "name": self.name}


@dataclass(frozen=True, kw_only=True)
class DirectorySyncCompletedIntegration(IntegrationEvent):
    source_type: str
    source_ref: str
    users_synced: int
    users_created: int

    @property
    def event_name(self) -> str:
        return "directory.sync.completed"

    @property
    def source_context(self) -> str:
        return "directory"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "source_type": self.source_type,
            "source_ref": self.source_ref,
            "users_synced": self.users_synced,
            "users_created": self.users_created,
        }


@dataclass(frozen=True, kw_only=True)
class IntegrationDirectorySyncedIntegration(IntegrationEvent):
    source_type: str
    users_synced: int
    users_created: int

    @property
    def event_name(self) -> str:
        return "integration.directory.synced"

    @property
    def source_context(self) -> str:
        return "directory"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "source_type": self.source_type,
            "users_synced": self.users_synced,
            "users_created": self.users_created,
        }


@dataclass(frozen=True, kw_only=True)
class ScimUserProvisionedIntegration(IntegrationEvent):
    user_id: str
    email: str
    provider_ref: str

    @property
    def event_name(self) -> str:
        return "directory.scim.user.provisioned"

    @property
    def source_context(self) -> str:
        return "directory"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"user_id": self.user_id, "email": self.email, "provider_ref": self.provider_ref}
