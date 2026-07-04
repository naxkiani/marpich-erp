"""ACL — platform events. NO cross-context imports."""
from __future__ import annotations

from contexts.workflow.application.commands.deploy_module_approval import (
    DeployModuleApprovalCommand,
)


class PlatformModuleActivationAdapter:
    async def parse_module_activated(self, envelope: dict) -> DeployModuleApprovalCommand:
        payload = envelope["payload"]
        return DeployModuleApprovalCommand(
            tenant_id=envelope["tenant_id"],
            correlation_id=envelope["correlation_id"],
            module_id=payload["module_id"],
        )


# Backward-compatible module-level helpers
async def on_module_activated(envelope: dict) -> DeployModuleApprovalCommand:
    return await PlatformModuleActivationAdapter().parse_module_activated(envelope)
