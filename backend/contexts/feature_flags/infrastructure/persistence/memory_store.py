"""In-memory feature flag repository."""
from __future__ import annotations

from contexts.feature_flags.domain.aggregates.feature_flag import FeatureFlag
from contexts.feature_flags.domain.ports.repositories import IFeatureFlagRepository
from shared.domain.value_objects.unique_id import UniqueId


class FeatureFlagMemoryStore:
    flags: dict[str, FeatureFlag] = {}

    @classmethod
    def reset(cls) -> None:
        cls.flags.clear()


class InMemoryFeatureFlagRepository(IFeatureFlagRepository):
    async def save(self, flag: FeatureFlag) -> None:
        FeatureFlagMemoryStore.flags[f"{flag.tenant_id}:{flag.key}"] = flag

    async def find_by_key(self, tenant_id: str, key: str) -> FeatureFlag | None:
        return FeatureFlagMemoryStore.flags.get(f"{tenant_id}:{key.strip().lower()}")

    async def list_by_tenant(self, tenant_id: str) -> list[FeatureFlag]:
        return [f for f in FeatureFlagMemoryStore.flags.values() if f.tenant_id == tenant_id]

    async def exists(self, tenant_id: str, key: str) -> bool:
        return f"{tenant_id}:{key.strip().lower()}" in FeatureFlagMemoryStore.flags
