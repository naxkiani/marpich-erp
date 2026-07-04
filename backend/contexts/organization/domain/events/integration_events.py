"""Organization integration events."""
from __future__ import annotations

from dataclasses import dataclass

from shared.domain.events.integration_event import IntegrationEvent
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(frozen=True, kw_only=True)
class OrgCreatedIntegration(IntegrationEvent):
    organization_id: UniqueId
    name: str

    @property
    def event_name(self) -> str:
        return "organization.org.created"

    @property
    def source_context(self) -> str:
        return "organization"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"organization_id": str(self.organization_id), "name": self.name}


@dataclass(frozen=True, kw_only=True)
class UnitCreatedIntegration(IntegrationEvent):
    unit_id: UniqueId
    organization_id: UniqueId
    unit_type: str
    code: str
    name: str

    @property
    def event_name(self) -> str:
        return "organization.unit.created"

    @property
    def source_context(self) -> str:
        return "organization"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "unit_id": str(self.unit_id),
            "organization_id": str(self.organization_id),
            "unit_type": self.unit_type,
            "code": self.code,
            "name": self.name,
        }


@dataclass(frozen=True, kw_only=True)
class MemberAddedIntegration(IntegrationEvent):
    membership_id: UniqueId
    org_unit_id: UniqueId
    user_id: str
    title: str

    @property
    def event_name(self) -> str:
        return "organization.member.added"

    @property
    def source_context(self) -> str:
        return "organization"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "membership_id": str(self.membership_id),
            "org_unit_id": str(self.org_unit_id),
            "user_id": self.user_id,
            "title": self.title,
        }


@dataclass(frozen=True, kw_only=True)
class MemberRemovedIntegration(IntegrationEvent):
    org_unit_id: UniqueId
    user_id: str

    @property
    def event_name(self) -> str:
        return "organization.member.removed"

    @property
    def source_context(self) -> str:
        return "organization"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"org_unit_id": str(self.org_unit_id), "user_id": self.user_id}
