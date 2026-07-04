"""Specification — reusable business predicate."""
from __future__ import annotations

from contexts.module_id.domain.aggregates.example import ExampleAggregate


class ActiveExampleSpecification:
    def is_satisfied_by(self, aggregate: ExampleAggregate) -> bool:
        return bool(aggregate.name.strip())
