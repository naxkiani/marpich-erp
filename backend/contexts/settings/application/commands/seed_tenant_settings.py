"""Command from platform.tenant.provisioned."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SeedTenantSettingsCommand:
    tenant_id: str
    correlation_id: str
    industry_pack: str
    locale: str
    enabled_modules: list[str]
