"""In-memory Treasury Transaction repository."""
from __future__ import annotations

from contexts.treasury.domain.aggregates.treasury_transaction import TreasuryTransaction


class InMemoryTreasuryTransactionRepository:
    _store: dict[str, TreasuryTransaction] = {}

    async def save(self, transaction: TreasuryTransaction) -> None:
        self._store[str(transaction.id)] = transaction

    async def find_by_id(self, transaction_id: str) -> TreasuryTransaction | None:
        return self._store.get(transaction_id)

    async def list_by_tenant(self, tenant_id: str) -> list[TreasuryTransaction]:
        return [t for t in self._store.values() if t.tenant_id == tenant_id]

    @classmethod
    def reset(cls) -> None:
        cls._store = {}
