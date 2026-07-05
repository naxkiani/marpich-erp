"""In-memory Enterprise Bank Reconciliation repositories."""
from __future__ import annotations

from contexts.treasury.domain.aggregates.bank_reconciliation_engine import (
    BankStatementImport,
    EnterpriseBankReconciliation,
    ReconciliationAuditEntry,
)


class InMemoryBankStatementImportRepository:
    _store: dict[str, BankStatementImport] = {}

    async def save(self, statement: BankStatementImport) -> None:
        self._store[str(statement.id)] = statement

    async def find_by_id(self, statement_id: str) -> BankStatementImport | None:
        return self._store.get(statement_id)

    async def list_by_tenant(self, tenant_id: str) -> list[BankStatementImport]:
        return [s for s in self._store.values() if s.tenant_id == tenant_id]

    @classmethod
    def reset(cls) -> None:
        cls._store = {}


class InMemoryEnterpriseBankReconciliationRepository:
    _store: dict[str, EnterpriseBankReconciliation] = {}

    async def save(self, reconciliation: EnterpriseBankReconciliation) -> None:
        self._store[str(reconciliation.id)] = reconciliation

    async def find_by_id(self, reconciliation_id: str) -> EnterpriseBankReconciliation | None:
        return self._store.get(reconciliation_id)

    async def list_by_tenant(self, tenant_id: str) -> list[EnterpriseBankReconciliation]:
        return [r for r in self._store.values() if r.tenant_id == tenant_id]

    @classmethod
    def reset(cls) -> None:
        cls._store = {}


class InMemoryReconciliationAuditRepository:
    _store: dict[str, ReconciliationAuditEntry] = {}

    async def save(self, entry: ReconciliationAuditEntry) -> None:
        self._store[str(entry.id)] = entry

    async def list_by_reconciliation(self, reconciliation_id: str) -> list[ReconciliationAuditEntry]:
        return [e for e in self._store.values() if e.reconciliation_id == reconciliation_id]

    async def list_by_tenant(self, tenant_id: str) -> list[ReconciliationAuditEntry]:
        return [e for e in self._store.values() if e.tenant_id == tenant_id]

    @classmethod
    def reset(cls) -> None:
        cls._store = {}
