"""ACL ports — platform integration event adapters."""
from __future__ import annotations

from typing import Protocol

from contexts.workflow.application.commands.deploy_module_approval import (
    DeployModuleApprovalCommand,
)


class IModuleActivationAdapter(Protocol):
    async def parse_module_activated(self, envelope: dict) -> DeployModuleApprovalCommand: ...
