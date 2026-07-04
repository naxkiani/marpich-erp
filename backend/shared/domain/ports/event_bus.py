"""Event bus port — infrastructure implements; domains never call each other."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Awaitable, Callable

from shared.domain.events.domain_event import DomainEvent
from shared.domain.events.integration_event import IntegrationEvent

IntegrationHandler = Callable[[IntegrationEvent], Awaitable[None]]


class IEventBus(ABC):
    @abstractmethod
    async def publish_domain(self, event: DomainEvent) -> None: ...

    @abstractmethod
    async def publish_integration(self, event: IntegrationEvent) -> None: ...

    @abstractmethod
    def subscribe(
        self,
        event_name: str,
        handler: IntegrationHandler,
        consumer_group: str,
    ) -> None: ...
