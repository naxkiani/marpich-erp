from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID, uuid4


@dataclass(frozen=True, slots=True)
class UniqueId:
    value: UUID

    @classmethod
    def generate(cls) -> UniqueId:
        return cls(uuid4())

    @classmethod
    def from_string(cls, raw: str) -> UniqueId:
        return cls(UUID(raw))

    def __str__(self) -> str:
        return str(self.value)
