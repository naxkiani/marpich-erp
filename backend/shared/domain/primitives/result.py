from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")
E = TypeVar("E")


@dataclass(frozen=True, slots=True)
class Result(Generic[T]):
    value: T | None
    error: str | None

    @property
    def succeeded(self) -> bool:
        return self.error is None

    @classmethod
    def ok(cls, value: T) -> Result[T]:
        return cls(value=value, error=None)

    @classmethod
    def fail(cls, error: str) -> Result[T]:
        return cls(value=None, error=error)

    def unwrap(self) -> T:
        if self.error is not None:
            raise ValueError(self.error)
        assert self.value is not None
        return self.value
