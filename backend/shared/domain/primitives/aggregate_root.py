from __future__ import annotations

from typing import Generic, TypeVar

from .domain_event import DomainEvent
from .entity import Entity, UniqueId

T = TypeVar("T")


class AggregateRoot(Entity[T], Generic[T]):
    """Consistency boundary — all invariants enforced within aggregate."""

    def __init__(self, props: T, id: UniqueId | None = None) -> None:
        super().__init__(id or UniqueId.generate(), props)
        self._domain_events: list[DomainEvent] = []

    @property
    def domain_events(self) -> tuple[DomainEvent, ...]:
        return tuple(self._domain_events)

    def _raise(self, event: DomainEvent) -> None:
        self._domain_events.append(event)

    def clear_events(self) -> list[DomainEvent]:
        events = list(self._domain_events)
        self._domain_events.clear()
        return events
