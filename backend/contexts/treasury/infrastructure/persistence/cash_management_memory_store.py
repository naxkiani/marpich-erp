"""In-memory Cash Management persistence."""
from __future__ import annotations

from contexts.treasury.domain.aggregates.cash_management import (
    CashClosing,
    CashCount,
    CashLocation,
    CashReconciliation,
    CashTransaction,
    CashVerification,
)
from contexts.treasury.domain.ports.cash_management_repositories import (
    ICashClosingRepository,
    ICashCountRepository,
    ICashLocationRepository,
    ICashReconciliationRepository,
    ICashTransactionRepository,
    ICashVerificationRepository,
)


class InMemoryCashLocationRepository(ICashLocationRepository):
    _locations: dict[str, CashLocation] = {}

    @classmethod
    def reset(cls) -> None:
        cls._locations = {}

    async def save(self, location: CashLocation) -> None:
        self._locations[str(location.id)] = location

    async def find_by_id(self, location_id: str) -> CashLocation | None:
        return self._locations.get(location_id)

    async def find_by_code(self, tenant_id: str, code: str) -> CashLocation | None:
        return next(
            (l for l in self._locations.values() if l.tenant_id == tenant_id and l.code == code.upper()),
            None,
        )

    async def list_by_tenant(
        self, tenant_id: str, organization_id: str | None = None
    ) -> list[CashLocation]:
        locs = [l for l in self._locations.values() if l.tenant_id == tenant_id]
        if organization_id:
            locs = [l for l in locs if l.organization_id == organization_id]
        return locs


class InMemoryCashTransactionRepository(ICashTransactionRepository):
    _transactions: dict[str, CashTransaction] = {}

    @classmethod
    def reset(cls) -> None:
        cls._transactions = {}

    async def save(self, transaction: CashTransaction) -> None:
        self._transactions[str(transaction.id)] = transaction

    async def find_by_id(self, transaction_id: str) -> CashTransaction | None:
        return self._transactions.get(transaction_id)

    async def list_by_tenant(self, tenant_id: str) -> list[CashTransaction]:
        return [t for t in self._transactions.values() if t.tenant_id == tenant_id]

    async def list_by_location(self, location_id: str) -> list[CashTransaction]:
        return [t for t in self._transactions.values() if t.location_id == location_id]


class InMemoryCashCountRepository(ICashCountRepository):
    _counts: dict[str, CashCount] = {}

    @classmethod
    def reset(cls) -> None:
        cls._counts = {}

    async def save(self, count: CashCount) -> None:
        self._counts[str(count.id)] = count

    async def find_by_id(self, count_id: str) -> CashCount | None:
        return self._counts.get(count_id)

    async def list_by_tenant(self, tenant_id: str) -> list[CashCount]:
        return [c for c in self._counts.values() if c.tenant_id == tenant_id]

    async def list_by_location(self, location_id: str) -> list[CashCount]:
        return [c for c in self._counts.values() if c.location_id == location_id]


class InMemoryCashVerificationRepository(ICashVerificationRepository):
    _verifications: dict[str, CashVerification] = {}

    @classmethod
    def reset(cls) -> None:
        cls._verifications = {}

    async def save(self, verification: CashVerification) -> None:
        self._verifications[str(verification.id)] = verification

    async def list_by_count(self, cash_count_id: str) -> list[CashVerification]:
        return [v for v in self._verifications.values() if v.cash_count_id == cash_count_id]


class InMemoryCashClosingRepository(ICashClosingRepository):
    _closings: dict[str, CashClosing] = {}

    @classmethod
    def reset(cls) -> None:
        cls._closings = {}

    async def save(self, closing: CashClosing) -> None:
        self._closings[str(closing.id)] = closing

    async def find_by_id(self, closing_id: str) -> CashClosing | None:
        return self._closings.get(closing_id)

    async def list_by_tenant(self, tenant_id: str) -> list[CashClosing]:
        return [c for c in self._closings.values() if c.tenant_id == tenant_id]

    async def list_open_by_location(self, location_id: str) -> list[CashClosing]:
        return [
            c for c in self._closings.values()
            if c.location_id == location_id and c.status == "open"
        ]


class InMemoryCashReconciliationRepository(ICashReconciliationRepository):
    _reconciliations: dict[str, CashReconciliation] = {}

    @classmethod
    def reset(cls) -> None:
        cls._reconciliations = {}

    async def save(self, reconciliation: CashReconciliation) -> None:
        self._reconciliations[str(reconciliation.id)] = reconciliation

    async def find_by_id(self, reconciliation_id: str) -> CashReconciliation | None:
        return self._reconciliations.get(reconciliation_id)

    async def list_by_tenant(self, tenant_id: str) -> list[CashReconciliation]:
        return [r for r in self._reconciliations.values() if r.tenant_id == tenant_id]
