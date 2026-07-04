"""Platform event adapter port."""
from __future__ import annotations

from typing import Protocol

from contexts.settings.application.commands.merge_module_config import MergeModuleConfigCommand
from contexts.settings.application.commands.seed_tenant_settings import SeedTenantSettingsCommand


class IPlatformSettingsAdapter(Protocol):
    async def parse_tenant_provisioned(self, envelope: dict) -> SeedTenantSettingsCommand: ...

    async def parse_module_activated(self, envelope: dict) -> MergeModuleConfigCommand: ...
