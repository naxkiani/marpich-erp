"""Tenant settings aggregate — config, features, branding."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class TenantSettings(AggregateRoot):
    tenant_id: str
    industry_pack: str
    config: dict = field(default_factory=dict)
    features: dict[str, bool] = field(default_factory=dict)
    branding: dict = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def seed(
        cls,
        *,
        tenant_id: str,
        industry_pack: str,
        locale: str,
        enabled_modules: list[str],
    ) -> TenantSettings:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            industry_pack=industry_pack,
            config={
                "locale": locale,
                "timezone": "UTC",
                "date_format": "YYYY-MM-DD",
                "currency": "USD",
                "enabled_modules": enabled_modules,
            },
            features={
                "saved_listings": False,
                "image_attachments": True,
                "multi_org": False,
                "advanced_analytics": industry_pack in ("hospital", "bank", "university"),
            },
            branding={
                "app_name": tenant_id.replace("-", " ").title(),
                "primary_color": "#2563eb",
                "logo_url": None,
            },
        )

    def set_config(self, key: str, value: object) -> None:
        self.config[key] = value
        self.updated_at = datetime.now(UTC)

    def toggle_feature(self, key: str, enabled: bool) -> None:
        self.features[key] = enabled
        self.updated_at = datetime.now(UTC)

    def merge_module_config(self, module_id: str, defaults: dict) -> None:
        module_key = f"module.{module_id}"
        existing = self.config.get(module_key, {})
        if isinstance(existing, dict):
            merged = {**defaults, **existing}
        else:
            merged = defaults
        self.config[module_key] = merged
        self.updated_at = datetime.now(UTC)

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "industry_pack": self.industry_pack,
            "config": self.config,
            "features": self.features,
            "branding": self.branding,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
