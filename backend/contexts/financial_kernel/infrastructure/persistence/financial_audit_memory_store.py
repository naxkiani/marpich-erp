"""In-memory financial audit repository — append-only, deletion forbidden."""
from __future__ import annotations

from contexts.financial_kernel.domain.aggregates.financial_audit import FinancialAuditEntry
from contexts.financial_kernel.domain.ports.financial_audit_repositories import (
    IFinancialAuditRepository,
)
from contexts.financial_kernel.domain.services.financial_audit_engine import (
    assert_deletion_forbidden,
)


class InMemoryFinancialAuditRepository(IFinancialAuditRepository):
    _entries: dict[str, FinancialAuditEntry] = {}
    _chain: dict[str, list[str]] = {}

    @classmethod
    def reset(cls) -> None:
        cls._entries = {}
        cls._chain = {}

    async def save(self, entry: FinancialAuditEntry) -> None:
        self._entries[str(entry.id)] = entry
        self._chain.setdefault(entry.tenant_id, []).append(entry.tamper_hash)

    async def find_by_id(self, entry_id: str) -> FinancialAuditEntry | None:
        return self._entries.get(entry_id)

    async def list_by_tenant(self, tenant_id: str) -> list[FinancialAuditEntry]:
        items = [e for e in self._entries.values() if e.tenant_id == tenant_id]
        return sorted(items, key=lambda e: e.occurred_at)

    async def list_by_resource(
        self, tenant_id: str, resource_type: str, resource_id: str
    ) -> list[FinancialAuditEntry]:
        items = [
            e
            for e in self._entries.values()
            if e.tenant_id == tenant_id
            and e.resource_type == resource_type
            and e.resource_id == resource_id
        ]
        return sorted(items, key=lambda e: e.occurred_at)

    async def last_tamper_hash(self, tenant_id: str) -> str | None:
        chain = self._chain.get(tenant_id, [])
        return chain[-1] if chain else None

    async def delete(self, entry_id: str) -> None:
        assert_deletion_forbidden()
