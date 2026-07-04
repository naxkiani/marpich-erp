"""ISO 4217 currency code."""
from __future__ import annotations

import re
from dataclasses import dataclass

_CURRENCY_PATTERN = re.compile(r"^[A-Z]{3}$")


@dataclass(frozen=True, slots=True)
class Currency:
    code: str

    def __post_init__(self) -> None:
        normalized = self.code.strip().upper()
        if not _CURRENCY_PATTERN.match(normalized):
            raise ValueError(f"Invalid currency code: {self.code}")
        object.__setattr__(self, "code", normalized)

    def __str__(self) -> str:
        return self.code
