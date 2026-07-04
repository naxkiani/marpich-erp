"""Audit repository ports."""
from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime

from contexts.audit.domain.aggregates.audit_entry import AuditEntry
from contexts.audit.domain.aggregates.audit_export import AuditExport
from contexts.audit.domain.aggregates.retention_policy import RetentionPolicy
from shared.domain.value_objects.unique_id import UniqueId


class IAuditEntryRepository(ABC):
    @abstractmethod
    async def append(self, entry: AuditEntry) -> None: ...

    @abstractmethod
    async def find_by_id(self, tenant_id: str, entry_id: UniqueId) -> AuditEntry | None: ...

    @abstractmethod
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
    ) -> list[AuditEntry]: ...

    @abstractmethod
    async def count(self, tenant_id: str) -> int: ...

    @abstractmethod
    async def purge_before(self, tenant_id: str, before: datetime) -> int: ...


class IAuditExportRepository(ABC):
    @abstractmethod
    async def save(self, export: AuditExport) -> None: ...

    @abstractmethod
    async def find_by_id(self, tenant_id: str, export_id: UniqueId) -> AuditExport | None: ...


class IRetentionPolicyRepository(ABC):
    @abstractmethod
    async def save(self, policy: RetentionPolicy) -> None: ...

    @abstractmethod
    async def find_by_tenant(self, tenant_id: str) -> RetentionPolicy | None: ...
