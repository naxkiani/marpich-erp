"""In-memory subledger repositories."""
from __future__ import annotations

from contexts.financial_kernel.domain.aggregates.subledger import (
    Subledger,
    SubledgerEntry,
    SubledgerReconciliation,
)
from contexts.financial_kernel.domain.ports.subledger_repositories import (
    ISubledgerEntryRepository,
    ISubledgerReconciliationRepository,
    ISubledgerRepository,
)


class InMemorySubledgerRepository(ISubledgerRepository):
    _subledgers: dict[str, Subledger] = {}

    @classmethod
    def reset(cls) -> None:
        cls._subledgers = {}

    async def save(self, subledger: Subledger) -> None:
        self._subledgers[str(subledger.id)] = subledger

    async def find_by_id(self, subledger_id: str) -> Subledger | None:
        return self._subledgers.get(subledger_id)

    async def find_by_type(self, tenant_id: str, subledger_type: str) -> Subledger | None:
        for subledger in self._subledgers.values():
            if subledger.tenant_id == tenant_id and subledger.subledger_type == subledger_type:
                return subledger
        return None

    async def list_by_tenant(self, tenant_id: str) -> list[Subledger]:
        return [s for s in self._subledgers.values() if s.tenant_id == tenant_id]


class InMemorySubledgerEntryRepository(ISubledgerEntryRepository):
    _entries: dict[str, SubledgerEntry] = {}
    _idempotency: dict[str, SubledgerEntry] = {}

    @classmethod
    def reset(cls) -> None:
        cls._entries = {}
        cls._idempotency = {}

    async def save(self, entry: SubledgerEntry) -> None:
        self._entries[str(entry.id)] = entry
        self._idempotency[f"{entry.tenant_id}:{entry.idempotency_key}"] = entry

    async def find_by_id(self, entry_id: str) -> SubledgerEntry | None:
        return self._entries.get(entry_id)

    async def find_by_idempotency(self, tenant_id: str, key: str) -> SubledgerEntry | None:
        return self._idempotency.get(f"{tenant_id}:{key}")

    async def list_by_subledger(self, subledger_id: str) -> list[SubledgerEntry]:
        return [e for e in self._entries.values() if e.subledger_id == subledger_id]

    async def list_by_tenant(self, tenant_id: str) -> list[SubledgerEntry]:
        return [e for e in self._entries.values() if e.tenant_id == tenant_id]


class InMemorySubledgerReconciliationRepository(ISubledgerReconciliationRepository):
    _reconciliations: dict[str, SubledgerReconciliation] = {}

    @classmethod
    def reset(cls) -> None:
        cls._reconciliations = {}

    async def save(self, reconciliation: SubledgerReconciliation) -> None:
        self._reconciliations[str(reconciliation.id)] = reconciliation

    async def find_by_id(self, reconciliation_id: str) -> SubledgerReconciliation | None:
        return self._reconciliations.get(reconciliation_id)

    async def list_by_subledger(self, subledger_id: str) -> list[SubledgerReconciliation]:
        items = [r for r in self._reconciliations.values() if r.subledger_id == subledger_id]
        return sorted(items, key=lambda r: r.created_at, reverse=True)

    async def list_by_tenant(self, tenant_id: str) -> list[SubledgerReconciliation]:
        items = [r for r in self._reconciliations.values() if r.tenant_id == tenant_id]
        return sorted(items, key=lambda r: r.created_at, reverse=True)
