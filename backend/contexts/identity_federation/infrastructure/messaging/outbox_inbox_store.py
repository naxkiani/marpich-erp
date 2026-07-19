"""Federation outbox / inbox memory stores — idempotent messaging (P200-B10)."""
from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import uuid4


class FederationOutboxInboxStore:
    outbox: list[dict] = []
    inbox: dict[str, dict] = {}
    published_ids: set[str] = set()

    @classmethod
    def reset(cls) -> None:
        cls.outbox.clear()
        cls.inbox.clear()
        cls.published_ids.clear()

    @classmethod
    def enqueue_outbox(
        cls,
        *,
        tenant_id: str,
        event_name: str,
        payload: dict[str, Any],
        event_version: int = 1,
        correlation_id: str = "",
    ) -> dict:
        entry = {
            "outbox_id": str(uuid4()),
            "tenant_id": tenant_id,
            "event_name": event_name,
            "event_version": event_version,
            "payload": payload,
            "correlation_id": correlation_id or str(uuid4()),
            "status": "pending",
            "created_at": datetime.now(UTC).isoformat(),
        }
        cls.outbox.append(entry)
        cls.outbox = cls.outbox[-1000:]
        return entry

    @classmethod
    def mark_published(cls, outbox_id: str) -> dict | None:
        for item in cls.outbox:
            if item["outbox_id"] == outbox_id:
                item["status"] = "published"
                item["published_at"] = datetime.now(UTC).isoformat()
                cls.published_ids.add(outbox_id)
                return item
        return None

    @classmethod
    def list_outbox(cls, *, tenant_id: str, limit: int = 50) -> list[dict]:
        items = [o for o in cls.outbox if o["tenant_id"] == tenant_id]
        return items[-limit:]

    @classmethod
    def ingest_inbox(
        cls,
        *,
        tenant_id: str,
        event_id: str,
        event_name: str,
        consumer_id: str,
        payload: dict | None = None,
    ) -> dict:
        key = f"{tenant_id}:{event_id}:{consumer_id}"
        if key in cls.inbox:
            return {**cls.inbox[key], "duplicate": True}
        entry = {
            "inbox_key": key,
            "tenant_id": tenant_id,
            "event_id": event_id,
            "event_name": event_name,
            "consumer_id": consumer_id,
            "payload": payload or {},
            "status": "processed",
            "duplicate": False,
            "at": datetime.now(UTC).isoformat(),
        }
        cls.inbox[key] = entry
        return entry

    @classmethod
    def list_inbox(cls, *, tenant_id: str, limit: int = 50) -> list[dict]:
        items = [v for v in cls.inbox.values() if v["tenant_id"] == tenant_id]
        return items[-limit:]


def reset_outbox_inbox_store() -> None:
    FederationOutboxInboxStore.reset()
