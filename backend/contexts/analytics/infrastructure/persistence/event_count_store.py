"""In-memory event count store for analytics summaries."""
from __future__ import annotations

from contexts.analytics.infrastructure.persistence.memory_store import AnalyticsMemoryStore


class EventCountMemoryStore:
    def increment(self, tenant_id: str, event_name: str) -> None:
        count_key = f"{tenant_id}:{event_name}"
        AnalyticsMemoryStore.event_counts[count_key] = (
            AnalyticsMemoryStore.event_counts.get(count_key, 0) + 1
        )

    def summary(self, tenant_id: str) -> dict[str, int]:
        prefix = f"{tenant_id}:"
        counts: dict[str, int] = {}
        for key, count in AnalyticsMemoryStore.event_counts.items():
            if key.startswith(prefix):
                counts[key[len(prefix) :]] = count
        return counts
