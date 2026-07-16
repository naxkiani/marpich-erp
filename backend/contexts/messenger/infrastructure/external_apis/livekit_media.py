"""LiveKit media adapter — calls Integration connector registry only."""
from __future__ import annotations

from shared.application.result import Result
from shared.connectors.registry import get_connector_adapter
from shared.infrastructure.settings import settings


class LiveKitRealtimeMediaAdapter:
    async def create_room_token(
        self,
        *,
        room_name: str,
        identity: str,
        idempotency_key: str = "",
    ) -> Result[dict]:
        adapter = get_connector_adapter("livekit")
        if not adapter:
            return Result.fail("messenger.errors.livekit_unavailable")
        config = {
            "api_key": settings.livekit_api_key or None,
            "api_secret": settings.livekit_api_secret or None,
            "url": settings.livekit_url or None,
            "ttl_seconds": settings.livekit_token_ttl_seconds,
            "environment": "production" if settings.livekit_api_secret else "sandbox",
        }
        # Drop empty values so adapter falls back cleanly
        config = {k: v for k, v in config.items() if v not in (None, "")}
        result = await adapter.execute(
            operation="create_room_token",
            payload={"room_name": room_name, "identity": identity},
            config=config,
            secret=settings.livekit_api_secret or "",
            idempotency_key=idempotency_key,
        )
        if not result.succeeded:
            return result
        inner = result.unwrap().get("result") or {}
        return Result.ok(inner)
