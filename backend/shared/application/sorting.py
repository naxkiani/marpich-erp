"""Sorting primitives."""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class SortOrder(StrEnum):
    ASC = "asc"
    DESC = "desc"


@dataclass(frozen=True, slots=True)
class SortField:
    field: str
    order: SortOrder = SortOrder.ASC

    def __post_init__(self) -> None:
        if not self.field.strip():
            raise ValueError("sort field is required")

    @classmethod
    def parse(cls, value: str, default_order: SortOrder = SortOrder.ASC) -> SortField:
        """Parse `field` or `-field` query style."""
        value = value.strip()
        if value.startswith("-"):
            return cls(field=value[1:], order=SortOrder.DESC)
        if value.startswith("+"):
            return cls(field=value[1:], order=SortOrder.ASC)
        return cls(field=value, order=default_order)


@dataclass(frozen=True, slots=True)
class SortSpec:
    fields: tuple[SortField, ...]

    @classmethod
    def from_query(cls, sort: str | None) -> SortSpec:
        if not sort:
            return cls(fields=())
        parts = [p.strip() for p in sort.split(",") if p.strip()]
        return cls(fields=tuple(SortField.parse(p) for p in parts))
