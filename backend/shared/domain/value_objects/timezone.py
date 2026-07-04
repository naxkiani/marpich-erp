"""IANA timezone identifier."""
from __future__ import annotations

from dataclasses import dataclass
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


@dataclass(frozen=True, slots=True)
class TimeZone:
    name: str

    def __post_init__(self) -> None:
        normalized = self.name.strip()
        try:
            ZoneInfo(normalized)
        except ZoneInfoNotFoundError as exc:
            raise ValueError(f"Invalid timezone: {self.name}") from exc
        object.__setattr__(self, "name", normalized)

    def __str__(self) -> str:
        return self.name
