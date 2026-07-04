"""Console webhook channel — dev delivery without external HTTP."""
from __future__ import annotations

import json


class ConsoleWebhookChannel:
    deliveries: list[dict] = []

    @classmethod
    def reset(cls) -> None:
        cls.deliveries.clear()

    async def deliver(self, *, target_url: str, payload: dict, secret: str = "") -> None:
        entry = {
            "target_url": target_url,
            "payload": payload,
            "has_secret": bool(secret),
        }
        self.deliveries.append(entry)
        print(json.dumps({"type": "webhook_delivery", **entry}, default=str))
