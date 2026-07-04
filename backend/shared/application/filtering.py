"""Filtering primitives."""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any


class FilterOperator(StrEnum):
    EQ = "eq"
    NE = "ne"
    GT = "gt"
    GTE = "gte"
    LT = "lt"
    LTE = "lte"
    IN = "in"
    CONTAINS = "contains"
    STARTS_WITH = "starts_with"


@dataclass(frozen=True, slots=True)
class FilterClause:
    field: str
    operator: FilterOperator
    value: Any

    def __post_init__(self) -> None:
        if not self.field.strip():
            raise ValueError("filter field is required")


@dataclass(frozen=True, slots=True)
class FilterSpec:
    clauses: tuple[FilterClause, ...]

    @classmethod
    def empty(cls) -> FilterSpec:
        return cls(clauses=())

    def with_clause(self, field: str, operator: FilterOperator, value: Any) -> FilterSpec:
        return FilterSpec(clauses=(*self.clauses, FilterClause(field=field, operator=operator, value=value)))
