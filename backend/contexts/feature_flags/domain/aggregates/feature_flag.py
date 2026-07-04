"""Feature flag aggregate with multi-scope rules."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class FeatureFlag(AggregateRoot):
    tenant_id: str
    key: str
    name: str
    version: int
    default_enabled: bool
    emergency_disabled: bool = False
    emergency_reason: str | None = None
    tenant_rules: dict[str, bool] = field(default_factory=dict)
    organization_rules: dict[str, bool] = field(default_factory=dict)
    user_rules: dict[str, bool] = field(default_factory=dict)
    environment_rules: dict[str, bool] = field(default_factory=dict)
    country_rules: dict[str, bool] = field(default_factory=dict)
    industry_rules: dict[str, bool] = field(default_factory=dict)
    rollout_percentage: int = 100
    rollout_stage: str = "full"
    ab_test_enabled: bool = False
    ab_variants: list[dict] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        key: str,
        name: str,
        default_enabled: bool = False,
        industry_rules: dict[str, bool] | None = None,
    ) -> FeatureFlag:
        flag = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            key=key.strip().lower(),
            name=name.strip(),
            version=1,
            default_enabled=default_enabled,
            industry_rules=industry_rules or {},
        )
        flag._record_history("created")
        return flag

    def _snapshot(self) -> dict:
        return {
            "version": self.version,
            "default_enabled": self.default_enabled,
            "emergency_disabled": self.emergency_disabled,
            "rollout_percentage": self.rollout_percentage,
            "rollout_stage": self.rollout_stage,
            "ab_test_enabled": self.ab_test_enabled,
            "updated_at": self.updated_at.isoformat(),
        }

    def _record_history(self, action: str) -> None:
        self.history.append({**self._snapshot(), "action": action})

    def bump_version(self, action: str) -> None:
        self.version += 1
        self.updated_at = datetime.now(UTC)
        self._record_history(action)

    def set_emergency_disable(self, reason: str) -> None:
        self.emergency_disabled = True
        self.emergency_reason = reason
        self.bump_version("emergency_disabled")

    def clear_emergency_disable(self) -> None:
        self.emergency_disabled = False
        self.emergency_reason = None
        self.bump_version("emergency_enabled")

    def update_rollout(self, percentage: int, stage: str) -> None:
        self.rollout_percentage = max(0, min(100, percentage))
        self.rollout_stage = stage
        self.bump_version("rollout_updated")

    def configure_ab_test(self, variants: list[dict]) -> None:
        self.ab_test_enabled = True
        self.ab_variants = variants
        self.bump_version("ab_test_configured")

    def rollback_to(self, target_version: int) -> bool:
        for entry in reversed(self.history):
            if entry.get("version") == target_version:
                self.default_enabled = entry["default_enabled"]
                self.emergency_disabled = entry.get("emergency_disabled", False)
                self.rollout_percentage = entry.get("rollout_percentage", 100)
                self.rollout_stage = entry.get("rollout_stage", "full")
                self.ab_test_enabled = entry.get("ab_test_enabled", False)
                self.version = target_version
                self.updated_at = datetime.now(UTC)
                self._record_history("rollback")
                return True
        return False

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "key": self.key,
            "name": self.name,
            "version": self.version,
            "default_enabled": self.default_enabled,
            "emergency_disabled": self.emergency_disabled,
            "emergency_reason": self.emergency_reason,
            "tenant_rules": self.tenant_rules,
            "organization_rules": self.organization_rules,
            "user_rules": self.user_rules,
            "environment_rules": self.environment_rules,
            "country_rules": self.country_rules,
            "industry_rules": self.industry_rules,
            "rollout_percentage": self.rollout_percentage,
            "rollout_stage": self.rollout_stage,
            "ab_test_enabled": self.ab_test_enabled,
            "ab_variants": self.ab_variants,
            "metadata": self.metadata,
            "updated_at": self.updated_at.isoformat(),
        }
