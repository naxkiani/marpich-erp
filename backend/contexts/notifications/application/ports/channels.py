from __future__ import annotations

from typing import Protocol

from contexts.notifications.application.commands.deliver_from_event import DeliverFromEventCommand


class INotificationEventAdapter(Protocol):
    async def parse_integration_event(self, envelope: dict) -> DeliverFromEventCommand | None: ...


class IEmailChannel(Protocol):
    async def send(self, *, recipient: str, subject: str, body: str) -> None: ...
