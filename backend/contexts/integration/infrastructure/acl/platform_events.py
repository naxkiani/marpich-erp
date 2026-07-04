"""ACL — platform events."""
from __future__ import annotations

from contexts.integration.application.commands.provision_connectors import ProvisionConnectorsCommand


class IntegrationPlatformAdapter:
    async def parse_tenant_provisioned(self, envelope: dict) -> ProvisionConnectorsCommand:
        payload = envelope["payload"]
        return ProvisionConnectorsCommand(
            tenant_id=envelope["tenant_id"],
            correlation_id=envelope["correlation_id"],
            name=payload.get("name", envelope["tenant_id"]),
        )


async def on_tenant_provisioned(envelope: dict) -> ProvisionConnectorsCommand:
    return await IntegrationPlatformAdapter().parse_tenant_provisioned(envelope)
