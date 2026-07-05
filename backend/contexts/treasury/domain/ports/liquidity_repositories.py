"""Enterprise Liquidity Engine repository ports."""
from __future__ import annotations

from typing import Protocol

from contexts.treasury.domain.aggregates.liquidity_engine import (
    CashPool,
    FundingNeed,
    LiquiditySnapshot,
)


class ICashPoolRepository(Protocol):
    async def save(self, pool: CashPool) -> None: ...
    async def find_by_id(self, pool_id: str) -> CashPool | None: ...
    async def find_by_code(self, tenant_id: str, code: str) -> CashPool | None: ...
    async def list_by_tenant(self, tenant_id: str) -> list[CashPool]: ...


class ILiquiditySnapshotRepository(Protocol):
    async def save(self, snapshot: LiquiditySnapshot) -> None: ...
    async def list_by_tenant(self, tenant_id: str) -> list[LiquiditySnapshot]: ...


class IFundingNeedRepository(Protocol):
    async def save(self, need: FundingNeed) -> None: ...
    async def list_by_tenant(self, tenant_id: str) -> list[FundingNeed]: ...
