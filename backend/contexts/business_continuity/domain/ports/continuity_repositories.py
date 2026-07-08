"""Enterprise Business Continuity Platform repository ports."""
from __future__ import annotations

from abc import ABC, abstractmethod

from contexts.business_continuity.domain.aggregates.continuity_platform import (
    BackupStrategy,
    ContinuityPlan,
    ContinuityTenantProfile,
    FailoverRecord,
    RecoveryTest,
)


class IContinuityTenantProfileRepository(ABC):
    @abstractmethod
    async def save(self, profile: ContinuityTenantProfile) -> None: ...

    @abstractmethod
    async def find_by_tenant(self, tenant_id: str) -> ContinuityTenantProfile | None: ...

    @abstractmethod
    def next_profile_ref(self, tenant_id: str) -> str: ...


class IContinuityPlanRepository(ABC):
    @abstractmethod
    async def save(self, plan: ContinuityPlan) -> None: ...

    @abstractmethod
    async def find_by_ref(self, tenant_id: str, plan_ref: str) -> ContinuityPlan | None: ...

    @abstractmethod
    async def list_by_tenant(self, tenant_id: str) -> list[ContinuityPlan]: ...

    @abstractmethod
    def next_plan_ref(self, tenant_id: str) -> str: ...


class IBackupStrategyRepository(ABC):
    @abstractmethod
    async def save(self, strategy: BackupStrategy) -> None: ...

    @abstractmethod
    async def list_by_tenant(self, tenant_id: str) -> list[BackupStrategy]: ...

    @abstractmethod
    def next_strategy_ref(self, tenant_id: str) -> str: ...


class IFailoverRecordRepository(ABC):
    @abstractmethod
    async def save(self, record: FailoverRecord) -> None: ...

    @abstractmethod
    async def find_by_ref(self, tenant_id: str, failover_ref: str) -> FailoverRecord | None: ...

    @abstractmethod
    async def list_by_tenant(self, tenant_id: str) -> list[FailoverRecord]: ...

    @abstractmethod
    def next_failover_ref(self, tenant_id: str) -> str: ...


class IRecoveryTestRepository(ABC):
    @abstractmethod
    async def save(self, test: RecoveryTest) -> None: ...

    @abstractmethod
    async def list_by_tenant(self, tenant_id: str) -> list[RecoveryTest]: ...

    @abstractmethod
    def next_test_ref(self, tenant_id: str) -> str: ...
