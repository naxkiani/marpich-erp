"""Unit tests — domain, validators, specifications."""
from __future__ import annotations

from contexts.module_id.domain.aggregates.example import ExampleAggregate
from contexts.module_id.domain.specifications.active_example import (
    ActiveExampleSpecification,
)


def test_active_example_specification():
    agg = ExampleAggregate.create(tenant_id="t1", name="Alpha")
    assert ActiveExampleSpecification().is_satisfied_by(agg) is True
