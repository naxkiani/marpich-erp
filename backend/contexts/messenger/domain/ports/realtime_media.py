"""Realtime A/V port — LiveKit via Integration connector (no SDK in domain)."""
from __future__ import annotations

from typing import Protocol

from shared.application.result import Result


class IRealtimeMediaPort(Protocol):
    async def create_room_token(
        self,
        *,
        room_name: str,
        identity: str,
        idempotency_key: str = "",
    ) -> Result[dict]:
        """Return token metadata: token, room_name, identity, expires_at, simulated, url."""
        ...
