"""In-memory audit repositories."""
from __future__ import annotations

from datetime import datetime

from contexts.audit.domain.aggregates.audit_entry import AuditEntry
from contexts.audit.domain.aggregates.audit_export import AuditExport
from contexts.audit.domain.aggregates.retention_policy import RetentionPolicy
from contexts.audit.domain.ports.repositories import (
    IAuditEntryRepository,
    IAuditExportRepository,
    IRetentionPolicyRepository,
)
from shared.domain.value_objects.unique_id import UniqueId


class AuditMemoryStore:
    entries: list[AuditEntry] = []
    exports: dict[str, AuditExport] = {}
    policies: dict[str, RetentionPolicy] = {}

    @classmethod
    def reset(cls) -> None:
        cls.entries.clear()
        cls.exports.clear()
        cls.policies.clear()


class InMemoryAuditEntryRepository(IAuditEntryRepository):
    async def append(self, entry: AuditEntry) -> None:
        AuditMemoryStore.entries.append(entry)

    async def find_by_id(self, tenant_id: str, entry_id: UniqueId) -> AuditEntry | None:
        for entry in AuditMemoryStore.entries:
            if entry.tenant_id == tenant_id and str(entry.id) == str(entry_id):
                return entry
        return None

    async def query(
        self,
        tenant_id: str,
        *,
        event_name: str | None = None,
        severity: str | None = None,
        actor_id: str | None = None,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[AuditEntry]:
        results = [e for e in AuditMemoryStore.entries if e.tenant_id == tenant_id]
        if event_name:
            results = [e for e in results if e.event_name == event_name]
        if severity:
            results = [e for e in results if e.severity.value == severity]
        if actor_id:
            results = [e for e in results if e.actor_id == actor_id]
        if date_from:
            results = [e for e in results if e.occurred_at >= date_from]
        if date_to:
            results = [e for e in results if e.occurred_at <= date_to]
        results.sort(key=lambda e: e.occurred_at, reverse=True)
        return results[offset : offset + limit]

    async def count(self, tenant_id: str) -> int:
        return sum(1 for e in AuditMemoryStore.entries if e.tenant_id == tenant_id)

    async def purge_before(self, tenant_id: str, before: datetime) -> int:
        kept = [e for e in AuditMemoryStore.entries if not (e.tenant_id == tenant_id and e.occurred_at < before)]
        purged = len(AuditMemoryStore.entries) - len(kept)
        AuditMemoryStore.entries = kept
        return purged


class InMemoryAuditExportRepository(IAuditExportRepository):
    async def save(self, export: AuditExport) -> None:
        AuditMemoryStore.exports[str(export.id)] = export

    async def find_by_id(self, tenant_id: str, export_id: UniqueId) -> AuditExport | None:
        export = AuditMemoryStore.exports.get(str(export_id))
        return export if export and export.tenant_id == tenant_id else None


class InMemoryRetentionPolicyRepository(IRetentionPolicyRepository):
    async def save(self, policy: RetentionPolicy) -> None:
        AuditMemoryStore.policies[policy.tenant_id] = policy

    async def find_by_tenant(self, tenant_id: str) -> RetentionPolicy | None:
        return AuditMemoryStore.policies.get(tenant_id)
