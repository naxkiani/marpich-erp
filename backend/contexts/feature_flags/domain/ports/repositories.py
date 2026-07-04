"""Feature flag repository port."""
from __future__ import annotations

from abc import ABC, abstractmethod

from contexts.feature_flags.domain.aggregates.feature_flag import FeatureFlag
from shared.domain.value_objects.unique_id import UniqueId


class IFeatureFlagRepository(ABC):
    @abstractmethod
    async def save(self, flag: FeatureFlag) -> None: ...

    @abstractmethod
    async def find_by_key(self, tenant_id: str, key: str) -> FeatureFlag | None: ...

    @abstractmethod
    async def list_by_tenant(self, tenant_id: str) -> list[FeatureFlag]: ...

    @abstractmethod
    async def exists(self, tenant_id: str, key: str) -> bool: ...
