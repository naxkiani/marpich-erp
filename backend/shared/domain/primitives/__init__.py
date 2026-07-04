"""Shared domain primitives — no business logic, no cross-context imports."""

from .entity import Entity
from .aggregate_root import AggregateRoot
from .value_object import ValueObject
from .domain_event import DomainEvent, EventMetadata
from .tenant_id import TenantId
from .unique_id import UniqueId
from .result import Result

__all__ = [
    "Entity",
    "AggregateRoot",
    "ValueObject",
    "DomainEvent",
    "EventMetadata",
    "TenantId",
    "UniqueId",
    "Result",
]
