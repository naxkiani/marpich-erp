"""In-memory Enterprise Cash Reconciliation repositories."""
from __future__ import annotations

from contexts.treasury.domain.aggregates.cash_reconciliation_engine import (
    CashReconciliationAudit,
    CashReconciliationRun,
)


class InMemoryCashReconciliationRunRepository:
    _store: dict[str, CashReconciliationRun] = {}

    async def save(self, run: CashReconciliationRun) -> None:
        self._store[str(run.id)] = run

    async def find_by_id(self, run_id: str) -> CashReconciliationRun | None:
        return self._store.get(run_id)

    async def list_by_tenant(self, tenant_id: str) -> list[CashReconciliationRun]:
        return [r for r in self._store.values() if r.tenant_id == tenant_id]

    async def list_by_location(self, location_id: str) -> list[CashReconciliationRun]:
        return [r for r in self._store.values() if r.location_id == location_id]

    async def list_by_branch(self, tenant_id: str, branch_id: str) -> list[CashReconciliationRun]:
        return [
            r for r in self._store.values()
            if r.tenant_id == tenant_id and r.branch_id == branch_id
        ]

    @classmethod
    def reset(cls) -> None:
        cls._store = {}


class InMemoryCashReconciliationAuditRepository:
    _store: dict[str, CashReconciliationAudit] = {}

    async def save(self, entry: CashReconciliationAudit) -> None:
        self._store[str(entry.id)] = entry

    async def list_by_reconciliation(self, reconciliation_id: str) -> list[CashReconciliationAudit]:
        return [e for e in self._store.values() if e.reconciliation_id == reconciliation_id]

    async def list_by_tenant(self, tenant_id: str) -> list[CashReconciliationAudit]:
        return [e for e in self._store.values() if e.tenant_id == tenant_id]

    @classmethod
    def reset(cls) -> None:
        cls._store = {}
