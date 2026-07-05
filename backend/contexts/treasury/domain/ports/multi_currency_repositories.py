"""Multi-Currency Treasury repository ports."""
from __future__ import annotations

from typing import Protocol

from contexts.treasury.domain.aggregates.multi_currency_engine import ExchangeRate, FxTransaction


class IExchangeRateRepository(Protocol):
    async def save(self, rate: ExchangeRate) -> None: ...

    async def find_by_id(self, rate_id: str) -> ExchangeRate | None: ...

    async def list_by_tenant(self, tenant_id: str) -> list[ExchangeRate]: ...

    async def list_by_type(self, tenant_id: str, rate_type: str) -> list[ExchangeRate]: ...


class IFxTransactionRepository(Protocol):
    async def save(self, transaction: FxTransaction) -> None: ...

    async def find_by_id(self, transaction_id: str) -> FxTransaction | None: ...

    async def list_by_tenant(self, tenant_id: str) -> list[FxTransaction]: ...
