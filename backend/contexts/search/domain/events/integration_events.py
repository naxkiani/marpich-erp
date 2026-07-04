"""Search integration events."""
from __future__ import annotations

from dataclasses import dataclass, field

from shared.domain.events.integration_event import IntegrationEvent


@dataclass(frozen=True, kw_only=True)
class IndexUpdatedIntegration(IntegrationEvent):
    entity_type: str
    entity_id: str
    action: str

    @property
    def event_name(self) -> str:
        return "search.index.updated"

    @property
    def source_context(self) -> str:
        return "search"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "action": self.action,
        }


@dataclass(frozen=True, kw_only=True)
class ReindexCompletedIntegration(IntegrationEvent):
    document_count: int

    @property
    def event_name(self) -> str:
        return "search.reindex.completed"

    @property
    def source_context(self) -> str:
        return "search"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"document_count": self.document_count}
