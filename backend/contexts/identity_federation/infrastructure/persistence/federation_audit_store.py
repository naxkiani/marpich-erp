"""Immutable federation audit trail (in-memory; maps to federation.federation_audit)."""
from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import uuid4


class FederationAuditStore:
    _entries: list[dict[str, Any]] = []

    @classmethod
    def append(
        cls,
        *,
        tenant_id: str,
        event_type: str,
        actor: str = "system",
        resource: str = "",
        decision: str | None = None,
        detail: dict | None = None,
        correlation_id: str = "",
    ) -> dict:
        entry = {
            "audit_id": str(uuid4()),
            "tenant_id": tenant_id,
            "event_type": event_type,
            "actor": actor,
            "resource": resource,
            "decision": decision,
            "detail": detail or {},
            "correlation_id": correlation_id,
            "occurred_at": datetime.now(UTC).isoformat(),
            "immutable": True,
        }
        cls._entries.append(entry)
        return entry

    @classmethod
    def list_by_tenant(cls, tenant_id: str, *, limit: int = 50) -> list[dict]:
        items = [e for e in cls._entries if e["tenant_id"] == tenant_id]
        return list(reversed(items[-limit:]))

    @classmethod
    def reset(cls) -> None:
        cls._entries.clear()
