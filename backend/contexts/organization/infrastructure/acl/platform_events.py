"""ACL — platform/identity events."""
from __future__ import annotations

from contexts.organization.application.commands.platform_events import (
    AssignMemberFromUserCreatedCommand,
    BootstrapOrganizationCommand,
)


class OrganizationEventAdapter:
    async def parse_tenant_provisioned(self, envelope: dict) -> BootstrapOrganizationCommand:
        payload = envelope["payload"]
        return BootstrapOrganizationCommand(
            tenant_id=envelope["tenant_id"],
            correlation_id=envelope["correlation_id"],
            name=payload.get("name", envelope["tenant_id"]),
        )

    async def parse_user_created(self, envelope: dict) -> AssignMemberFromUserCreatedCommand:
        payload = envelope["payload"]
        return AssignMemberFromUserCreatedCommand(
            tenant_id=envelope["tenant_id"],
            correlation_id=envelope["correlation_id"],
            user_id=payload["user_id"],
            display_name=payload.get("display_name", "Member"),
        )


async def on_tenant_provisioned(envelope: dict) -> BootstrapOrganizationCommand:
    return await OrganizationEventAdapter().parse_tenant_provisioned(envelope)


async def on_user_created(envelope: dict) -> AssignMemberFromUserCreatedCommand:
    return await OrganizationEventAdapter().parse_user_created(envelope)
