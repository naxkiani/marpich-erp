"""Aggregate root — consistency boundary; emits domain events."""
from __future__ import annotations

from dataclasses import dataclass, field

from shared.domain.aggregates.entity import Entity
from shared.domain.events.domain_event import DomainEvent


@dataclass(eq=False, kw_only=True)
class AggregateRoot(Entity):
    _domain_events: list[DomainEvent] = field(default_factory=list, repr=False)

    @property
    def domain_events(self) -> tuple[DomainEvent, ...]:
        return tuple(self._domain_events)

    def _raise(self, event: DomainEvent) -> None:
        self._domain_events.append(event)

    def clear_events(self) -> list[DomainEvent]:
        events = list(self._domain_events)
        self._domain_events.clear()
        return events
