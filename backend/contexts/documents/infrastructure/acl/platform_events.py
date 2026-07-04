"""ACL — platform events."""
from __future__ import annotations

from contexts.documents.application.commands.bootstrap_root_folder import BootstrapRootFolderCommand


class DocumentsPlatformAdapter:
    async def parse_tenant_provisioned(self, envelope: dict) -> BootstrapRootFolderCommand:
        payload = envelope["payload"]
        return BootstrapRootFolderCommand(
            tenant_id=envelope["tenant_id"],
            correlation_id=envelope["correlation_id"],
            name=payload.get("name", envelope["tenant_id"]),
        )


async def on_tenant_provisioned(envelope: dict) -> BootstrapRootFolderCommand:
    return await DocumentsPlatformAdapter().parse_tenant_provisioned(envelope)
