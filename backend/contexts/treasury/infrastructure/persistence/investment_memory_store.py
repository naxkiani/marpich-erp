"""In-memory Enterprise Investment Management repositories."""
from __future__ import annotations

from contexts.treasury.domain.aggregates.investment_engine import Investment, InvestmentTransaction


class InMemoryInvestmentRepository:
    _store: dict[str, Investment] = {}

    async def save(self, investment: Investment) -> None:
        self._store[str(investment.id)] = investment

    async def find_by_id(self, investment_id: str) -> Investment | None:
        return self._store.get(investment_id)

    async def list_by_tenant(self, tenant_id: str) -> list[Investment]:
        return [i for i in self._store.values() if i.tenant_id == tenant_id]

    async def list_by_portfolio(self, tenant_id: str, portfolio_name: str) -> list[Investment]:
        return [
            i for i in self._store.values()
            if i.tenant_id == tenant_id and i.portfolio_name == portfolio_name
        ]

    @classmethod
    def reset(cls) -> None:
        cls._store = {}


class InMemoryInvestmentTransactionRepository:
    _store: dict[str, InvestmentTransaction] = {}

    async def save(self, transaction: InvestmentTransaction) -> None:
        self._store[str(transaction.id)] = transaction

    async def list_by_investment(self, investment_id: str) -> list[InvestmentTransaction]:
        return [t for t in self._store.values() if t.investment_id == investment_id]

    async def list_by_tenant(self, tenant_id: str) -> list[InvestmentTransaction]:
        return [t for t in self._store.values() if t.tenant_id == tenant_id]

    @classmethod
    def reset(cls) -> None:
        cls._store = {}
