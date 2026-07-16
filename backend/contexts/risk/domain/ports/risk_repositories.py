"""Enterprise Risk Platform repository ports."""
from __future__ import annotations

from abc import ABC, abstractmethod

from contexts.risk.domain.aggregates.risk_platform import (
    EnterpriseRiskItem,
    RiskMatrixSnapshot,
    RiskPrediction,
    RiskTenantProfile,
)


class IRiskTenantProfileRepository(ABC):
    @abstractmethod
    async def save(self, profile: RiskTenantProfile) -> None: ...

    @abstractmethod
    async def find_by_tenant(self, tenant_id: str) -> RiskTenantProfile | None: ...

    @abstractmethod
    def next_profile_ref(self, tenant_id: str) -> str: ...


class IEnterpriseRiskItemRepository(ABC):
    @abstractmethod
    async def save(self, item: EnterpriseRiskItem) -> None: ...

    @abstractmethod
    async def find_by_ref(self, tenant_id: str, risk_ref: str) -> EnterpriseRiskItem | None: ...

    @abstractmethod
    async def list_by_tenant(self, tenant_id: str) -> list[EnterpriseRiskItem]: ...

    @abstractmethod
    def next_risk_ref(self, tenant_id: str) -> str: ...


class IRiskMatrixSnapshotRepository(ABC):
    @abstractmethod
    async def save(self, snapshot: RiskMatrixSnapshot) -> None: ...

    @abstractmethod
    async def list_by_tenant(self, tenant_id: str) -> list[RiskMatrixSnapshot]: ...

    @abstractmethod
    def next_matrix_ref(self, tenant_id: str) -> str: ...


class IRiskPredictionRepository(ABC):
    @abstractmethod
    async def save(self, prediction: RiskPrediction) -> None: ...

    @abstractmethod
    async def list_by_tenant(self, tenant_id: str) -> list[RiskPrediction]: ...

    @abstractmethod
    def next_prediction_ref(self, tenant_id: str) -> str: ...
