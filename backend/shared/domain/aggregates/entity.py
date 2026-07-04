"""Entity base — identity equality within aggregate boundary."""
from __future__ import annotations

from dataclasses import dataclass
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class Entity:
    id: UniqueId

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Entity):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)
