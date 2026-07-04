"""Audit integration events."""
from __future__ import annotations

from dataclasses import dataclass

from shared.domain.events.integration_event import IntegrationEvent
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(frozen=True, kw_only=True)
class ExportCompletedIntegration(IntegrationEvent):
    export_id: UniqueId
    entry_count: int
    format: str

    @property
    def event_name(self) -> str:
        return "audit.export.completed"

    @property
    def source_context(self) -> str:
        return "audit"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "export_id": str(self.export_id),
            "entry_count": self.entry_count,
            "format": self.format,
        }


@dataclass(frozen=True, kw_only=True)
class RetentionAppliedIntegration(IntegrationEvent):
    entries_purged: int
    retention_days: int

    @property
    def event_name(self) -> str:
        return "audit.retention.applied"

    @property
    def source_context(self) -> str:
        return "audit"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "entries_purged": self.entries_purged,
            "retention_days": self.retention_days,
        }
