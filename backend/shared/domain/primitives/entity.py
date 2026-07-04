from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar

from .unique_id import UniqueId

T = TypeVar("T")


@dataclass
class Entity(Generic[T]):
    id: UniqueId
    props: T

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Entity):
            return False
        return self.id == other.id
