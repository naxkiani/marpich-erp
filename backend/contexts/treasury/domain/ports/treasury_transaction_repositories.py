"""Treasury Transaction Engine repository ports."""
from __future__ import annotations

from typing import Protocol

from contexts.treasury.domain.aggregates.treasury_transaction import TreasuryTransaction


class ITreasuryTransactionRepository(Protocol):
    async def save(self, transaction: TreasuryTransaction) -> None: ...
    async def find_by_id(self, transaction_id: str) -> TreasuryTransaction | None: ...
    async def list_by_tenant(self, tenant_id: str) -> list[TreasuryTransaction]: ...
