"""AuthZ Rule Compiler — compile/validate ABAC condition IR (not Cedar/Rego).

Ownership: authorization BC only. Business rules stay in Policy Engine.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

SUPPORTED_OPERATORS: frozenset[str] = frozenset(
    {"eq", "ne", "in", "not_in", "gte", "lte", "gt", "lt", "matches"}
)


class RuleCompilationError(ValueError):
    """Raised when ABAC conditions fail compile-time validation."""


@dataclass(frozen=True, slots=True)
class CompiledCondition:
    attribute: str
    operator: str
    value: Any


@dataclass(frozen=True, slots=True)
class CompiledRule:
    conditions: tuple[CompiledCondition, ...]

    def to_dicts(self) -> list[dict]:
        return [
            {"attribute": c.attribute, "operator": c.operator, "value": c.value}
            for c in self.conditions
        ]


def compile_conditions(conditions: list[dict] | None) -> CompiledRule:
    """Validate and normalize ABAC conditions before persistence or evaluation."""
    if not conditions:
        return CompiledRule(conditions=())
    compiled: list[CompiledCondition] = []
    for idx, raw in enumerate(conditions):
        if not isinstance(raw, dict):
            raise RuleCompilationError(f"condition[{idx}].not_object")
        attribute = str(raw.get("attribute") or "").strip()
        operator = str(raw.get("operator") or "eq").strip().lower()
        if not attribute:
            raise RuleCompilationError(f"condition[{idx}].attribute_required")
        if operator not in SUPPORTED_OPERATORS:
            raise RuleCompilationError(f"condition[{idx}].unsupported_operator:{operator}")
        value = raw.get("value")
        if operator in {"in", "not_in"} and not isinstance(value, (list, tuple, set)):
            raise RuleCompilationError(f"condition[{idx}].value_must_be_list")
        if operator == "matches":
            try:
                re.compile(str(value))
            except re.error as exc:
                raise RuleCompilationError(f"condition[{idx}].invalid_regex:{exc}") from exc
        compiled.append(CompiledCondition(attribute=attribute, operator=operator, value=value))
    return CompiledRule(conditions=tuple(compiled))


def evaluate_condition(condition: dict | CompiledCondition, facts: dict) -> bool:
    if isinstance(condition, CompiledCondition):
        attribute = condition.attribute
        operator = condition.operator
        expected = condition.value
    else:
        attribute = str(condition.get("attribute") or "")
        operator = str(condition.get("operator") or "eq")
        expected = condition.get("value")
    actual = facts.get(attribute)

    if operator == "eq":
        return actual == expected
    if operator == "ne":
        return actual != expected
    if operator == "in":
        return actual in (expected or [])
    if operator == "not_in":
        return actual not in (expected or [])
    if operator == "gte":
        return actual is not None and expected is not None and actual >= expected
    if operator == "lte":
        return actual is not None and expected is not None and actual <= expected
    if operator == "gt":
        return actual is not None and expected is not None and actual > expected
    if operator == "lt":
        return actual is not None and expected is not None and actual < expected
    if operator == "matches":
        return bool(actual and re.match(str(expected), str(actual)))
    return False


def evaluate_conditions(conditions: list[dict] | CompiledRule | None, facts: dict) -> bool:
    """Empty conditions always match (unconditional ABAC rule)."""
    if conditions is None:
        return True
    if isinstance(conditions, CompiledRule):
        items = conditions.conditions
        if not items:
            return True
        return all(evaluate_condition(c, facts) for c in items)
    if not conditions:
        return True
    return all(evaluate_condition(c, facts) for c in conditions)


def catalog() -> dict:
    return {
        "operators": sorted(SUPPORTED_OPERATORS),
        "condition_shape": {"attribute": "str", "operator": "str", "value": "any"},
        "owner": "authorization",
        "not_owner": ["policy", "cedar", "rego", "opa"],
    }
