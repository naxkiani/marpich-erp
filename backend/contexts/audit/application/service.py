"""Audit application service."""
from __future__ import annotations

from datetime import UTC, datetime, timedelta

from contexts.audit.domain.aggregates.audit_entry import AuditEntry, AuditSeverity
from contexts.audit.domain.aggregates.audit_export import AuditExport, ExportFormat
from contexts.audit.domain.aggregates.retention_policy import RetentionPolicy
from contexts.audit.domain.events.integration_events import (
    ExportCompletedIntegration,
    RetentionAppliedIntegration,
)
from contexts.audit.domain.ports.event_mapping import IAuditEventMapper
from contexts.audit.domain.ports.repositories import (
    IAuditEntryRepository,
    IAuditExportRepository,
    IRetentionPolicyRepository,
)
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.domain.value_objects.unique_id import UniqueId
from shared.infrastructure.messaging.event_bus import publish_integration_event


class AuditApplicationService:
    def __init__(
        self,
        entries: IAuditEntryRepository,
        exports: IAuditExportRepository,
        retention: IRetentionPolicyRepository,
        event_mapper: IAuditEventMapper,
    ) -> None:
        self._entries = entries
        self._exports = exports
        self._retention = retention
        self._event_mapper = event_mapper

    async def handle_integration_event(self, envelope: dict) -> None:
        entry = self._event_mapper.map_envelope(envelope)
        await self._entries.append(entry)

    async def handle_tenant_provisioned(self, envelope: dict) -> None:
        tenant_id = envelope["tenant_id"]
        existing = await self._retention.find_by_tenant(tenant_id)
        if not existing:
            await self._retention.save(RetentionPolicy.default_for_tenant(tenant_id))

    async def record_direct(
        self,
        *,
        tenant_id: str,
        correlation_id: str,
        action: str,
        resource_type: str,
        resource_id: str | None,
        actor_id: str | None,
        severity: str = "info",
        payload: dict | None = None,
    ) -> Result[dict]:
        try:
            sev = AuditSeverity(severity)
        except ValueError:
            return Result.fail("audit.errors.invalid_severity")

        entry = AuditEntry.record_direct(
            tenant_id=tenant_id,
            correlation_id=correlation_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            actor_id=actor_id,
            severity=sev,
            payload=payload,
        )
        await self._entries.append(entry)
        return Result.ok(entry.to_dict())

    async def get_entry(self, tenant_id: str, entry_id: str) -> Result[dict]:
        entry = await self._entries.find_by_id(tenant_id, UniqueId.from_string(entry_id))
        if not entry:
            return Result.fail("audit.errors.entry_not_found")
        return Result.ok(entry.to_dict())

    async def query_entries(
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
    ) -> Result[dict]:
        items = await self._entries.query(
            tenant_id,
            event_name=event_name,
            severity=severity,
            actor_id=actor_id,
            date_from=date_from,
            date_to=date_to,
            limit=limit,
            offset=offset,
        )
        total = await self._entries.count(tenant_id)
        return Result.ok(
            {
                "items": [e.to_dict() for e in items],
                "total": total,
                "limit": limit,
                "offset": offset,
            }
        )

    async def get_stats(self, tenant_id: str) -> Result[dict]:
        all_entries = await self._entries.query(tenant_id, limit=10_000)
        now = datetime.now(UTC)
        last_24h = now - timedelta(hours=24)

        by_event: dict[str, int] = {}
        security_count = 0
        last_24h_count = 0
        for entry in all_entries:
            by_event[entry.event_name] = by_event.get(entry.event_name, 0) + 1
            if entry.severity == AuditSeverity.SECURITY:
                security_count += 1
            if entry.occurred_at >= last_24h:
                last_24h_count += 1

        top_events = sorted(by_event.items(), key=lambda x: x[1], reverse=True)[:10]
        return Result.ok(
            {
                "total_entries": len(all_entries),
                "security_events": security_count,
                "last_24h": last_24h_count,
                "top_events": [{"event_name": k, "count": v} for k, v in top_events],
            }
        )

    async def create_export(
        self,
        *,
        tenant_id: str,
        correlation_id: str,
        export_format: str,
        filters: dict,
        requested_by: str | None,
    ) -> Result[dict]:
        try:
            fmt = ExportFormat(export_format)
        except ValueError:
            return Result.fail("audit.errors.invalid_format")

        export = AuditExport.create(
            tenant_id=tenant_id,
            export_format=fmt,
            filters=filters,
            requested_by=requested_by,
        )
        await self._exports.save(export)

        date_from = filters.get("date_from")
        date_to = filters.get("date_to")
        parsed_from = datetime.fromisoformat(date_from) if date_from else None
        parsed_to = datetime.fromisoformat(date_to) if date_to else None

        entries = await self._entries.query(
            tenant_id,
            event_name=filters.get("event_name"),
            severity=filters.get("severity"),
            actor_id=filters.get("actor_id"),
            date_from=parsed_from,
            date_to=parsed_to,
            limit=10_000,
        )
        export.mark_completed([e.to_dict() for e in entries])
        await self._exports.save(export)

        await publish_integration_event(
            ExportCompletedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                export_id=export.id,
                entry_count=export.entry_count,
                format=export.format.value,
            )
        )
        return Result.ok(export.to_dict(include_data=False))

    async def get_export(self, tenant_id: str, export_id: str) -> Result[dict]:
        export = await self._exports.find_by_id(tenant_id, UniqueId.from_string(export_id))
        if not export:
            return Result.fail("audit.errors.export_not_found")
        return Result.ok(export.to_dict())

    async def apply_retention(self, tenant_id: str, correlation_id: str) -> Result[dict]:
        policy = await self._retention.find_by_tenant(tenant_id)
        if not policy or not policy.is_active:
            return Result.fail("audit.errors.no_retention_policy")

        cutoff = datetime.now(UTC) - timedelta(days=policy.retention_days)
        purged = await self._entries.purge_before(tenant_id, cutoff)

        await publish_integration_event(
            RetentionAppliedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                entries_purged=purged,
                retention_days=policy.retention_days,
            )
        )
        return Result.ok({"entries_purged": purged, "retention_days": policy.retention_days})
