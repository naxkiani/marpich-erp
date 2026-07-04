"""Unique identifier value object."""
from __future__ import annotations

import uuid
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class UniqueId:
    value: str

    @classmethod
    def generate(cls) -> UniqueId:
        return cls(str(uuid.uuid4()))

    @classmethod
    def from_string(cls, value: str) -> UniqueId:
        uuid.UUID(value)  # validates format
        return cls(value)

    def __str__(self) -> str:
        return self.value
