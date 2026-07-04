"""Result type for application layer."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass(frozen=True, slots=True)
class Result(Generic[T]):
    succeeded: bool
    value: T | None = None
    error: str | None = None

    @classmethod
    def ok(cls, value: T) -> Result[T]:
        return cls(succeeded=True, value=value)

    @classmethod
    def fail(cls, error: str) -> Result[T]:
        return cls(succeeded=False, error=error)

    def unwrap(self) -> T:
        if not self.succeeded or self.value is None:
            raise ValueError(self.error or "Result has no value")
        return self.value
