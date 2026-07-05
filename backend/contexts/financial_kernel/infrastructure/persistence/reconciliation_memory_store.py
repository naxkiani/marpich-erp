"""In-memory reconciliation repositories."""
from __future__ import annotations

from contexts.financial_kernel.domain.aggregates.reconciliation import (
    ReconciliationAuditLog,
    ReconciliationRun,
)
from contexts.financial_kernel.domain.ports.reconciliation_repositories import (
    IReconciliationAuditRepository,
    IReconciliationRunRepository,
)


class InMemoryReconciliationRunRepository(IReconciliationRunRepository):
    _runs: dict[str, ReconciliationRun] = {}

    @classmethod
    def reset(cls) -> None:
        cls._runs = {}

    async def save(self, run: ReconciliationRun) -> None:
        self._runs[str(run.id)] = run

    async def find_by_id(self, run_id: str) -> ReconciliationRun | None:
        return self._runs.get(run_id)

    async def list_by_tenant(self, tenant_id: str) -> list[ReconciliationRun]:
        items = [r for r in self._runs.values() if r.tenant_id == tenant_id]
        return sorted(items, key=lambda r: r.created_at, reverse=True)

    async def list_by_type(self, tenant_id: str, reconciliation_type: str) -> list[ReconciliationRun]:
        items = [
            r
            for r in self._runs.values()
            if r.tenant_id == tenant_id and r.reconciliation_type == reconciliation_type
        ]
        return sorted(items, key=lambda r: r.created_at, reverse=True)


class InMemoryReconciliationAuditRepository(IReconciliationAuditRepository):
    _entries: list[ReconciliationAuditLog] = []

    @classmethod
    def reset(cls) -> None:
        cls._entries = []

    async def save(self, entry: ReconciliationAuditLog) -> None:
        self._entries.append(entry)

    async def list_by_reconciliation(self, reconciliation_id: str) -> list[ReconciliationAuditLog]:
        return [e for e in self._entries if e.reconciliation_id == reconciliation_id]

    async def list_by_tenant(self, tenant_id: str, *, limit: int = 100) -> list[ReconciliationAuditLog]:
        items = [e for e in self._entries if e.tenant_id == tenant_id]
        return items[-limit:]
