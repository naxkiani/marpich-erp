"""Policy repository ports."""
from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime

from contexts.policy.domain.aggregates.policy import Policy
from contexts.policy.domain.aggregates.policy_version import PolicyVersion
from shared.domain.value_objects.unique_id import UniqueId


class IPolicyRepository(ABC):
    @abstractmethod
    async def save(self, policy: Policy) -> None: ...

    @abstractmethod
    async def find_by_id(self, tenant_id: str, policy_id: UniqueId) -> Policy | None: ...

    @abstractmethod
    async def find_by_key(self, tenant_id: str, domain: str, key: str) -> Policy | None: ...

    @abstractmethod
    async def list_by_tenant(
        self, tenant_id: str, *, domain: str | None = None, status: str | None = None
    ) -> list[Policy]: ...


class IPolicyVersionRepository(ABC):
    @abstractmethod
    async def save(self, version: PolicyVersion) -> None: ...

    @abstractmethod
    async def find_by_policy_and_version(
        self, tenant_id: str, policy_id: str, version: int
    ) -> PolicyVersion | None: ...

    @abstractmethod
    async def list_by_policy(self, tenant_id: str, policy_id: str) -> list[PolicyVersion]: ...

    @abstractmethod
    async def find_active_for_key(
        self,
        tenant_id: str,
        domain: str,
        key: str,
        as_of: datetime,
    ) -> PolicyVersion | None: ...

    @abstractmethod
    async def supersede_active(self, tenant_id: str, policy_id: str, except_version: int) -> None: ...

    @abstractmethod
    async def next_version_number(self, tenant_id: str, policy_id: str) -> int: ...
