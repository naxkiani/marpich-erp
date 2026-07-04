"""ISO 3166-1 alpha-2 country code."""
from __future__ import annotations

import re
from dataclasses import dataclass

_COUNTRY_PATTERN = re.compile(r"^[A-Z]{2}$")


@dataclass(frozen=True, slots=True)
class Country:
    code: str

    def __post_init__(self) -> None:
        normalized = self.code.strip().upper()
        if not _COUNTRY_PATTERN.match(normalized):
            raise ValueError(f"Invalid country code: {self.code}")
        object.__setattr__(self, "code", normalized)

    def __str__(self) -> str:
        return self.code
