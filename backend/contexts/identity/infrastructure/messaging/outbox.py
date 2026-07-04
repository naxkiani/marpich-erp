"""Identity outbox — delegates to enterprise event fabric."""
from __future__ import annotations

import json
from datetime import UTC, datetime

from shared.infrastructure.messaging.event_fabric import EventFabric


class ConsoleAuditLogger:
    async def log(
        self,
        *,
        tenant_id: str,
        correlation_id: str,
        action: str,
        resource_type: str,
        resource_id: str | None = None,
        actor_id: str | None = None,
        payload: dict | None = None,
        ip_address: str | None = None,
    ) -> None:
        entry = {
            "type": "audit",
            "tenant_id": tenant_id,
            "correlation_id": correlation_id,
            "actor_id": actor_id,
            "action": action,
            "resource_type": resource_type,
            "resource_id": resource_id,
            "payload": payload,
            "ip_address": ip_address,
            "occurred_at": datetime.now(UTC).isoformat(),
        }
        print(json.dumps(entry))


class ConsoleOutboxPublisher:
    async def publish(self, event: object) -> None:
        await EventFabric.publish(event)
