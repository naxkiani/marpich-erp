"""Condition matching for policy evaluation."""
from __future__ import annotations


def _get_fact(facts: dict, field_path: str):
    parts = field_path.split(".")
    current = facts
    for part in parts:
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


def match_conditions(conditions: list[dict], facts: dict) -> tuple[bool, list[dict]]:
    trace: list[dict] = []
    if not conditions:
        trace.append({"step": "condition", "result": True, "note": "no conditions"})
        return True, trace

    for condition in conditions:
        field = condition.get("field", "")
        operator = condition.get("operator", "eq")
        expected = condition.get("value")
        actual = _get_fact(facts, field)
        result = _compare(operator, actual, expected)
        trace.append(
            {
                "step": "condition",
                "field": field,
                "operator": operator,
                "expected": expected,
                "actual": actual,
                "result": result,
            }
        )
        if not result:
            return False, trace
    return True, trace


def _compare(operator: str, actual, expected) -> bool:
    if operator == "eq":
        return actual == expected
    if operator == "ne":
        return actual != expected
    if operator == "gt":
        return actual is not None and expected is not None and actual > expected
    if operator == "gte":
        return actual is not None and expected is not None and actual >= expected
    if operator == "lt":
        return actual is not None and expected is not None and actual < expected
    if operator == "lte":
        return actual is not None and expected is not None and actual <= expected
    if operator == "in":
        return actual in (expected or [])
    if operator == "not_in":
        return actual not in (expected or [])
    if operator == "contains":
        return expected in str(actual or "")
    if operator == "matches":
        import re

        return bool(re.match(str(expected), str(actual or "")))
    return False
