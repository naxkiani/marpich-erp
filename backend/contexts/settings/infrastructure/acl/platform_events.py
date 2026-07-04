"""ACL — platform events to settings commands."""
from __future__ import annotations

from contexts.settings.application.commands.merge_module_config import MergeModuleConfigCommand
from contexts.settings.application.commands.seed_tenant_settings import SeedTenantSettingsCommand
from shared.contracts.industry_packs import get_industry_pack


class PlatformSettingsAdapter:
    async def parse_tenant_provisioned(self, envelope: dict) -> SeedTenantSettingsCommand:
        payload = envelope["payload"]
        pack_id = payload.get("industry_pack", "")
        pack = get_industry_pack(pack_id)
        locale = pack.default_locale if pack else "en-US"
        return SeedTenantSettingsCommand(
            tenant_id=envelope["tenant_id"],
            correlation_id=envelope["correlation_id"],
            industry_pack=pack_id,
            locale=locale,
            enabled_modules=list(payload.get("enabled_modules", [])),
        )

    async def parse_module_activated(self, envelope: dict) -> MergeModuleConfigCommand:
        payload = envelope["payload"]
        return MergeModuleConfigCommand(
            tenant_id=envelope["tenant_id"],
            correlation_id=envelope["correlation_id"],
            module_id=payload.get("module_id", ""),
        )


async def on_tenant_provisioned(envelope: dict) -> SeedTenantSettingsCommand:
    return await PlatformSettingsAdapter().parse_tenant_provisioned(envelope)


async def on_module_activated(envelope: dict) -> MergeModuleConfigCommand:
    return await PlatformSettingsAdapter().parse_module_activated(envelope)
