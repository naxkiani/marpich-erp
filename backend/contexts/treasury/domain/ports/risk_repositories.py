"""Enterprise Treasury Risk Platform repository ports."""
from __future__ import annotations

from typing import Protocol

from contexts.treasury.domain.aggregates.risk_engine import RiskAlert, StressTestRun, TreasuryRiskLimit


class IRiskLimitRepository(Protocol):
    async def save(self, limit: TreasuryRiskLimit) -> None: ...

    async def find_by_id(self, limit_id: str) -> TreasuryRiskLimit | None: ...

    async def list_by_tenant(self, tenant_id: str) -> list[TreasuryRiskLimit]: ...


class IRiskAlertRepository(Protocol):
    async def save(self, alert: RiskAlert) -> None: ...

    async def find_by_id(self, alert_id: str) -> RiskAlert | None: ...

    async def list_by_tenant(self, tenant_id: str) -> list[RiskAlert]: ...


class IStressTestRepository(Protocol):
    async def save(self, run: StressTestRun) -> None: ...

    async def list_by_tenant(self, tenant_id: str) -> list[StressTestRun]: ...
