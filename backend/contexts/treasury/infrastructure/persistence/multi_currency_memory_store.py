"""In-memory Multi-Currency Treasury repositories."""
from __future__ import annotations

from contexts.treasury.domain.aggregates.multi_currency_engine import ExchangeRate, FxTransaction


class InMemoryExchangeRateRepository:
    _store: dict[str, ExchangeRate] = {}

    async def save(self, rate: ExchangeRate) -> None:
        self._store[str(rate.id)] = rate

    async def find_by_id(self, rate_id: str) -> ExchangeRate | None:
        return self._store.get(rate_id)

    async def list_by_tenant(self, tenant_id: str) -> list[ExchangeRate]:
        return [r for r in self._store.values() if r.tenant_id == tenant_id]

    async def list_by_type(self, tenant_id: str, rate_type: str) -> list[ExchangeRate]:
        return [r for r in self._store.values() if r.tenant_id == tenant_id and r.rate_type == rate_type]

    @classmethod
    def reset(cls) -> None:
        cls._store = {}


class InMemoryFxTransactionRepository:
    _store: dict[str, FxTransaction] = {}

    async def save(self, transaction: FxTransaction) -> None:
        self._store[str(transaction.id)] = transaction

    async def find_by_id(self, transaction_id: str) -> FxTransaction | None:
        return self._store.get(transaction_id)

    async def list_by_tenant(self, tenant_id: str) -> list[FxTransaction]:
        return [t for t in self._store.values() if t.tenant_id == tenant_id]

    @classmethod
    def reset(cls) -> None:
        cls._store = {}
