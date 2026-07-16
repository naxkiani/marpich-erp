"""AI integration events."""
from __future__ import annotations

from dataclasses import dataclass

from shared.domain.events.integration_event import IntegrationEvent
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(frozen=True, kw_only=True)
class InsightGeneratedIntegration(IntegrationEvent):
    session_id: UniqueId
    module_id: str
    surface: str
    summary: str

    @property
    def event_name(self) -> str:
        return "ai.insight.generated"

    @property
    def source_context(self) -> str:
        return "ai"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "session_id": str(self.session_id),
            "module_id": self.module_id,
            "surface": self.surface,
            "summary": self.summary,
        }
