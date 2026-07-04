"""Console email channel — production uses SMTP/SES."""
from __future__ import annotations

import json
from datetime import UTC, datetime


class ConsoleEmailChannel:
    async def send(self, *, recipient: str, subject: str, body: str) -> None:
        print(
            json.dumps(
                {
                    "type": "email",
                    "recipient": recipient,
                    "subject": subject,
                    "body": body,
                    "occurred_at": datetime.now(UTC).isoformat(),
                }
            )
        )
