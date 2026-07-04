"""In-memory Treasury persistence."""
from __future__ import annotations

from contexts.treasury.domain.aggregates.bank_reconciliation import BankReconciliation
from contexts.treasury.domain.aggregates.cash_forecast import CashForecast
from contexts.treasury.domain.aggregates.treasury_account import TreasuryAccount
from contexts.treasury.domain.aggregates.treasury_transfer import TreasuryTransfer
from contexts.treasury.domain.ports.repositories import (
    IBankReconciliationRepository,
    ICashForecastRepository,
    ITreasuryAccountRepository,
    ITreasuryTransferRepository,
)


class InMemoryTreasuryAccountRepository(ITreasuryAccountRepository):
    _accounts: dict[str, TreasuryAccount] = {}

    @classmethod
    def reset(cls) -> None:
        cls._accounts = {}

    async def save(self, account: TreasuryAccount) -> None:
        self._accounts[str(account.id)] = account
        self._accounts[f"code:{account.tenant_id}:{account.code}"] = account

    async def find_by_id(self, account_id: str) -> TreasuryAccount | None:
        acc = self._accounts.get(account_id)
        return acc if isinstance(acc, TreasuryAccount) else None

    async def find_by_code(self, tenant_id: str, code: str) -> TreasuryAccount | None:
        acc = self._accounts.get(f"code:{tenant_id}:{code.upper()}")
        return acc if isinstance(acc, TreasuryAccount) else None

    async def list_by_tenant(self, tenant_id: str) -> list[TreasuryAccount]:
        seen: set[str] = set()
        result = []
        for acc in self._accounts.values():
            if isinstance(acc, TreasuryAccount) and acc.tenant_id == tenant_id:
                aid = str(acc.id)
                if aid not in seen:
                    seen.add(aid)
                    result.append(acc)
        return result


class InMemoryTreasuryTransferRepository(ITreasuryTransferRepository):
    _transfers: dict[str, TreasuryTransfer] = {}

    @classmethod
    def reset(cls) -> None:
        cls._transfers = {}

    async def save(self, transfer: TreasuryTransfer) -> None:
        self._transfers[str(transfer.id)] = transfer

    async def find_by_id(self, transfer_id: str) -> TreasuryTransfer | None:
        return self._transfers.get(transfer_id)

    async def list_by_tenant(self, tenant_id: str) -> list[TreasuryTransfer]:
        return [t for t in self._transfers.values() if t.tenant_id == tenant_id]


class InMemoryBankReconciliationRepository(IBankReconciliationRepository):
    _records: dict[str, BankReconciliation] = {}

    @classmethod
    def reset(cls) -> None:
        cls._records = {}

    async def save(self, reconciliation: BankReconciliation) -> None:
        self._records[str(reconciliation.id)] = reconciliation

    async def find_by_id(self, reconciliation_id: str) -> BankReconciliation | None:
        return self._records.get(reconciliation_id)

    async def list_by_tenant(self, tenant_id: str) -> list[BankReconciliation]:
        return [r for r in self._records.values() if r.tenant_id == tenant_id]


class InMemoryCashForecastRepository(ICashForecastRepository):
    _forecasts: dict[str, CashForecast] = {}

    @classmethod
    def reset(cls) -> None:
        cls._forecasts = {}

    async def save(self, forecast: CashForecast) -> None:
        self._forecasts[str(forecast.id)] = forecast

    async def find_by_id(self, forecast_id: str) -> CashForecast | None:
        return self._forecasts.get(forecast_id)

    async def list_by_tenant(self, tenant_id: str) -> list[CashForecast]:
        return [f for f in self._forecasts.values() if f.tenant_id == tenant_id]
