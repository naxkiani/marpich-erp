from __future__ import annotations

from typing import Protocol

from contexts.organization.application.commands.platform_events import (
    AssignMemberFromUserCreatedCommand,
    BootstrapOrganizationCommand,
)


class IOrganizationEventAdapter(Protocol):
    async def parse_tenant_provisioned(self, envelope: dict) -> BootstrapOrganizationCommand: ...

    async def parse_user_created(self, envelope: dict) -> AssignMemberFromUserCreatedCommand: ...
