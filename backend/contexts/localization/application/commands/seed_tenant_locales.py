"""Command from platform.tenant.provisioned."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SeedTenantLocalesCommand:
    tenant_id: str
    correlation_id: str
    default_locale: str
