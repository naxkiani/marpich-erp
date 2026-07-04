"""ACL — platform events to localization commands."""
from __future__ import annotations

from contexts.localization.application.commands.seed_tenant_locales import SeedTenantLocalesCommand
from shared.contracts.industry_packs import get_industry_pack


class PlatformLocalizationAdapter:
    async def parse_tenant_provisioned(self, envelope: dict) -> SeedTenantLocalesCommand:
        payload = envelope["payload"]
        pack_id = payload.get("industry_pack", "")
        pack = get_industry_pack(pack_id)
        default_locale = (
            pack.default_locale.split("-")[0] if pack and pack.default_locale else "en"
        ).lower()
        return SeedTenantLocalesCommand(
            tenant_id=envelope["tenant_id"],
            correlation_id=envelope["correlation_id"],
            default_locale=default_locale,
        )


async def on_tenant_provisioned(envelope: dict) -> SeedTenantLocalesCommand:
    return await PlatformLocalizationAdapter().parse_tenant_provisioned(envelope)
