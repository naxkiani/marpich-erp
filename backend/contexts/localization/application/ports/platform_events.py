"""Platform event adapter port."""
from __future__ import annotations

from typing import Protocol

from contexts.localization.application.commands.seed_tenant_locales import SeedTenantLocalesCommand


class IPlatformLocalizationAdapter(Protocol):
    async def parse_tenant_provisioned(self, envelope: dict) -> SeedTenantLocalesCommand: ...
