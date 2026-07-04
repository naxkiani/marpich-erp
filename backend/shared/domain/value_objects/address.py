"""Postal address value object."""
from __future__ import annotations

from dataclasses import dataclass

from shared.domain.value_objects.country import Country


@dataclass(frozen=True, slots=True)
class Address:
    line1: str
    city: str
    country: Country
    line2: str = ""
    region: str = ""
    postal_code: str = ""

    def __post_init__(self) -> None:
        if not self.line1.strip():
            raise ValueError("Address line1 is required")
        if not self.city.strip():
            raise ValueError("Address city is required")

    def formatted(self) -> str:
        parts = [self.line1]
        if self.line2:
            parts.append(self.line2)
        parts.append(f"{self.city}, {self.region} {self.postal_code}".strip())
        parts.append(str(self.country))
        return "\n".join(p for p in parts if p)

    def to_dict(self) -> dict:
        return {
            "line1": self.line1,
            "line2": self.line2,
            "city": self.city,
            "region": self.region,
            "postal_code": self.postal_code,
            "country": str(self.country),
        }
