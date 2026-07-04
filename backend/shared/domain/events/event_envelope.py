"""Event envelope for Kafka / outbox transport."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class EventEnvelope:
    topic: str
    key: str
    headers: dict[str, str]
    body: dict[str, Any]

    @classmethod
    def from_integration_event(cls, event: dict, topic_prefix: str = "marpich") -> EventEnvelope:
        name = event["event_name"]
        tenant = event["tenant_id"]
        return cls(
            topic=f"{topic_prefix}.{name.replace('.', '-')}",
            key=tenant,
            headers={
                "correlation_id": event["correlation_id"],
                "event_version": str(event["event_version"]),
                "source_context": event["source_context"],
            },
            body=event,
        )
