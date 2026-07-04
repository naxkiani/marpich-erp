"""PostgreSQL repositories — Audit bounded context."""
from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import delete, func, select

from contexts.audit.domain.aggregates.audit_entry import AuditEntry, AuditSeverity
from contexts.audit.domain.aggregates.audit_export import AuditExport, ExportFormat, ExportStatus
from contexts.audit.domain.aggregates.retention_policy import RetentionPolicy
from contexts.audit.domain.ports.repositories import (
    IAuditEntryRepository,
    IAuditExportRepository,
    IRetentionPolicyRepository,
)
from shared.domain.value_objects.unique_id import UniqueId
from shared.infrastructure.database.engine import session_scope
from shared.infrastructure.database.orm import AuditEntryRow, AuditExportRow, RetentionPolicyRow


class PostgresAuditEntryRepository(IAuditEntryRepository):
    async def append(self, entry: AuditEntry) -> None:
        async with session_scope() as session:
            session.add(
                AuditEntryRow(
                    id=UUID(str(entry.id)),
                    tenant_id=entry.tenant_id,
                    event_name=entry.event_name,
                    source_context=entry.source_context,
                    correlation_id=entry.correlation_id,
                    action=entry.action,
                    resource_type=entry.resource_type,
                    resource_id=entry.resource_id,
                    actor_id=entry.actor_id,
                    severity=entry.severity.value,
                    payload=entry.payload,
                    occurred_at=entry.occurred_at,
                    recorded_at=entry.recorded_at,
                )
            )

    async def find_by_id(self, tenant_id: str, entry_id: UniqueId) -> AuditEntry | None:
        async with session_scope() as session:
            row = await session.get(AuditEntryRow, UUID(str(entry_id)))
            if row and row.tenant_id == tenant_id:
                return _entry_from_row(row)
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
        async with session_scope() as session:
            stmt = select(AuditEntryRow).where(AuditEntryRow.tenant_id == tenant_id)
            if event_name:
                stmt = stmt.where(AuditEntryRow.event_name == event_name)
            if severity:
                stmt = stmt.where(AuditEntryRow.severity == severity)
            if actor_id:
                stmt = stmt.where(AuditEntryRow.actor_id == actor_id)
            if date_from:
                stmt = stmt.where(AuditEntryRow.occurred_at >= date_from)
            if date_to:
                stmt = stmt.where(AuditEntryRow.occurred_at <= date_to)
            stmt = stmt.order_by(AuditEntryRow.occurred_at.desc()).offset(offset).limit(limit)
            rows = (await session.scalars(stmt)).all()
        return [_entry_from_row(r) for r in rows]

    async def count(self, tenant_id: str) -> int:
        async with session_scope() as session:
            return await session.scalar(
                select(func.count()).select_from(AuditEntryRow).where(
                    AuditEntryRow.tenant_id == tenant_id
                )
            ) or 0

    async def purge_before(self, tenant_id: str, before: datetime) -> int:
        async with session_scope() as session:
            result = await session.execute(
                delete(AuditEntryRow).where(
                    AuditEntryRow.tenant_id == tenant_id,
                    AuditEntryRow.occurred_at < before,
                )
            )
            return result.rowcount


class PostgresAuditExportRepository(IAuditExportRepository):
    async def save(self, export: AuditExport) -> None:
        async with session_scope() as session:
            row = await session.get(AuditExportRow, UUID(str(export.id)))
            if row is None:
                row = AuditExportRow(
                    id=UUID(str(export.id)),
                    tenant_id=export.tenant_id,
                    status=export.status.value,
                    format=export.format.value,
                    filters=export.filters,
                    entry_count=export.entry_count,
                    data=export.data,
                    error=export.error,
                    requested_by=export.requested_by,
                    created_at=export.created_at,
                    completed_at=export.completed_at,
                )
                session.add(row)
            else:
                row.status = export.status.value
                row.entry_count = export.entry_count
                row.data = export.data
                row.error = export.error
                row.completed_at = export.completed_at

    async def find_by_id(self, tenant_id: str, export_id: UniqueId) -> AuditExport | None:
        async with session_scope() as session:
            row = await session.get(AuditExportRow, UUID(str(export_id)))
            if row and row.tenant_id == tenant_id:
                return _export_from_row(row)
            return None


class PostgresRetentionPolicyRepository(IRetentionPolicyRepository):
    async def save(self, policy: RetentionPolicy) -> None:
        async with session_scope() as session:
            row = await session.scalar(
                select(RetentionPolicyRow).where(RetentionPolicyRow.tenant_id == policy.tenant_id)
            )
            if row is None:
                row = RetentionPolicyRow(
                    id=UUID(str(policy.id)),
                    tenant_id=policy.tenant_id,
                    retention_days=policy.retention_days,
                    is_active=policy.is_active,
                    updated_at=policy.updated_at,
                )
                session.add(row)
            else:
                row.retention_days = policy.retention_days
                row.is_active = policy.is_active
                row.updated_at = policy.updated_at

    async def find_by_tenant(self, tenant_id: str) -> RetentionPolicy | None:
        async with session_scope() as session:
            row = await session.scalar(
                select(RetentionPolicyRow).where(RetentionPolicyRow.tenant_id == tenant_id)
            )
            return _policy_from_row(row) if row else None


def _entry_from_row(row: AuditEntryRow) -> AuditEntry:
    return AuditEntry(
        id=UniqueId(str(row.id)),
        tenant_id=row.tenant_id,
        event_name=row.event_name,
        source_context=row.source_context,
        correlation_id=row.correlation_id,
        action=row.action,
        resource_type=row.resource_type,
        resource_id=row.resource_id,
        actor_id=row.actor_id,
        severity=AuditSeverity(row.severity),
        payload=row.payload,
        occurred_at=row.occurred_at,
        recorded_at=row.recorded_at,
    )


def _export_from_row(row: AuditExportRow) -> AuditExport:
    return AuditExport(
        id=UniqueId(str(row.id)),
        tenant_id=row.tenant_id,
        status=ExportStatus(row.status),
        format=ExportFormat(row.format),
        filters=row.filters,
        entry_count=row.entry_count,
        data=row.data,
        error=row.error,
        requested_by=row.requested_by,
        created_at=row.created_at,
        completed_at=row.completed_at,
    )


def _policy_from_row(row: RetentionPolicyRow) -> RetentionPolicy:
    return RetentionPolicy(
        id=UniqueId(str(row.id)),
        tenant_id=row.tenant_id,
        retention_days=row.retention_days,
        is_active=row.is_active,
        updated_at=row.updated_at,
    )
