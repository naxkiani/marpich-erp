"""Measurement quantity — unit + value (no domain-specific conversion rules)."""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from enum import StrEnum


class UnitOfMeasure(StrEnum):
    PIECE = "piece"
    KILOGRAM = "kg"
    GRAM = "g"
    LITER = "l"
    METER = "m"
    SQUARE_METER = "m2"
    CUBIC_METER = "m3"
    HOUR = "hour"
    DAY = "day"


@dataclass(frozen=True, slots=True)
class Measurement:
    value: Decimal
    unit: UnitOfMeasure

    def __post_init__(self) -> None:
        if not isinstance(self.value, Decimal):
            object.__setattr__(self, "value", Decimal(str(self.value)))
        if self.value < 0:
            raise ValueError("Measurement value cannot be negative")

    def to_dict(self) -> dict:
        return {"value": str(self.value), "unit": self.unit.value}
