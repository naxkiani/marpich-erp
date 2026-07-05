"""Enterprise Investment Management repository ports."""
from __future__ import annotations

from typing import Protocol

from contexts.treasury.domain.aggregates.investment_engine import Investment, InvestmentTransaction


class IInvestmentRepository(Protocol):
    async def save(self, investment: Investment) -> None: ...

    async def find_by_id(self, investment_id: str) -> Investment | None: ...

    async def list_by_tenant(self, tenant_id: str) -> list[Investment]: ...

    async def list_by_portfolio(self, tenant_id: str, portfolio_name: str) -> list[Investment]: ...


class IInvestmentTransactionRepository(Protocol):
    async def save(self, transaction: InvestmentTransaction) -> None: ...

    async def list_by_investment(self, investment_id: str) -> list[InvestmentTransaction]: ...

    async def list_by_tenant(self, tenant_id: str) -> list[InvestmentTransaction]: ...
