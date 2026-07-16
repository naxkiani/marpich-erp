"""LiveKit connector adapter — room tokens only (no SDK in messenger domain)."""
from __future__ import annotations

import hashlib
import hmac
import time

from shared.application.result import Result
from shared.connectors.stub_adapter import BaseConnectorAdapter


class LiveKitAdapter(BaseConnectorAdapter):
    def __init__(self) -> None:
        super().__init__(
            "livekit",
            ["create_room_token", "create_room", "test_connection"],
        )

    async def execute(
        self,
        *,
        operation: str,
        payload: dict,
        config: dict,
        secret: str = "",
        idempotency_key: str = "",
    ) -> Result[dict]:
        if operation not in self._operations:
            return Result.fail(f"unsupported_operation:{operation}")
        if operation == "test_connection":
            return await self.test_connection(config=config, secret=secret)
        if operation == "create_room":
            room = str(payload.get("room_name") or f"room-{int(time.time())}")
            return Result.ok({
                "connector_type": self.connector_type,
                "operation": operation,
                "status": "completed",
                "idempotency_key": idempotency_key or None,
                "result": {"room_name": room, "simulated": True},
            })
        room_name = str(payload.get("room_name") or "")
        identity = str(payload.get("identity") or "anonymous")
        if not room_name:
            return Result.fail("livekit.errors.room_name_required")
        api_key = str(config.get("api_key") or secret or "dev-livekit-key")
        ttl = int(config.get("ttl_seconds") or 3600)
        exp = int(time.time()) + ttl
        material = f"{room_name}:{identity}:{exp}"
        token = hmac.new(api_key.encode(), material.encode(), hashlib.sha256).hexdigest()
        return Result.ok({
            "connector_type": self.connector_type,
            "operation": operation,
            "status": "completed",
            "idempotency_key": idempotency_key or None,
            "result": {
                "token": f"lk_{token}",
                "room_name": room_name,
                "identity": identity,
                "expires_at": exp,
                "simulated": True,
            },
        })
