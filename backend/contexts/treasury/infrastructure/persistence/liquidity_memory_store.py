"""In-memory Enterprise Liquidity Engine repositories."""
from __future__ import annotations

from contexts.treasury.domain.aggregates.liquidity_engine import (
    CashPool,
    FundingNeed,
    LiquiditySnapshot,
)


class InMemoryCashPoolRepository:
    _store: dict[str, CashPool] = {}

    async def save(self, pool: CashPool) -> None:
        self._store[str(pool.id)] = pool

    async def find_by_id(self, pool_id: str) -> CashPool | None:
        return self._store.get(pool_id)

    async def find_by_code(self, tenant_id: str, code: str) -> CashPool | None:
        for pool in self._store.values():
            if pool.tenant_id == tenant_id and pool.code == code.upper():
                return pool
        return None

    async def list_by_tenant(self, tenant_id: str) -> list[CashPool]:
        return [p for p in self._store.values() if p.tenant_id == tenant_id]

    @classmethod
    def reset(cls) -> None:
        cls._store = {}


class InMemoryLiquiditySnapshotRepository:
    _store: dict[str, LiquiditySnapshot] = {}

    async def save(self, snapshot: LiquiditySnapshot) -> None:
        self._store[str(snapshot.id)] = snapshot

    async def list_by_tenant(self, tenant_id: str) -> list[LiquiditySnapshot]:
        return [s for s in self._store.values() if s.tenant_id == tenant_id]

    @classmethod
    def reset(cls) -> None:
        cls._store = {}


class InMemoryFundingNeedRepository:
    _store: dict[str, FundingNeed] = {}

    async def save(self, need: FundingNeed) -> None:
        self._store[str(need.id)] = need

    async def list_by_tenant(self, tenant_id: str) -> list[FundingNeed]:
        return [n for n in self._store.values() if n.tenant_id == tenant_id]

    @classmethod
    def reset(cls) -> None:
        cls._store = {}
