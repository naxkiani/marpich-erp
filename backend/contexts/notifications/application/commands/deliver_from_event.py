from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DeliverFromEventCommand:
    tenant_id: str
    correlation_id: str
    source_event: str
    user_id: str | None
    recipient_email: str | None
    template_key: str
    title: str
    body: str
    category: str
    channel: str
