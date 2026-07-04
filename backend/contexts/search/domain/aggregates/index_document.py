"""Denormalized search document."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class IndexDocument(AggregateRoot):
    tenant_id: str
    entity_type: str
    entity_id: str
    title: str
    body: str
    facets: dict = field(default_factory=dict)
    source_event: str = ""
    indexed_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def from_event(cls, *, tenant_id: str, envelope: dict) -> IndexDocument:
        event_name = envelope.get("event_name", "unknown")
        payload = envelope.get("payload") or {}
        entity_type = event_name.split(".")[0] if "." in event_name else "event"
        entity_id = str(envelope.get("event_id", UniqueId.generate()))
        title = _title_from_event(event_name, payload)
        body = json.dumps(payload, default=str)
        facets = {"event_name": event_name, "source_context": envelope.get("source_context", "")}
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            entity_type=entity_type,
            entity_id=entity_id,
            title=title,
            body=body,
            facets=facets,
            source_event=event_name,
        )

    def matches_query(self, query: str) -> bool:
        needle = query.lower().strip()
        if not needle:
            return True
        haystack = f"{self.title} {self.body} {self.entity_type}".lower()
        return needle in haystack

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "title": self.title,
            "body": self.body,
            "facets": self.facets,
            "source_event": self.source_event,
            "indexed_at": self.indexed_at.isoformat(),
        }


def _title_from_event(event_name: str, payload: dict) -> str:
    for key in ("title", "name", "display_name", "email", "tenant_slug", "module_id"):
        value = payload.get(key)
        if value:
            return str(value)
    return event_name
