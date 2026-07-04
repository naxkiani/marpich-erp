"""Policy evaluation runtime."""
from __future__ import annotations

from datetime import UTC, datetime

from contexts.policy.domain.aggregates.policy_version import PolicyVersion
from contexts.policy.domain.services.condition_matcher import match_conditions


def evaluate_version(
    version: PolicyVersion,
    facts: dict,
    *,
    as_of: datetime | None = None,
    require_active: bool = True,
) -> dict:
    as_of = as_of or datetime.now(UTC)
    trace: list[dict] = []

    if require_active and not version.is_effective_at(as_of):
        return {
            "matched": False,
            "policy_id": version.policy_id,
            "version": version.version,
            "outcome": None,
            "parameters": {},
            "applied_exception": None,
            "evaluation_trace": [
                {"step": "status", "result": False, "status": version.status.value}
            ],
        }

    for exc in version.exceptions:
        exc_conditions = exc.get("conditions", [])
        matched, exc_trace = match_conditions(exc_conditions, facts)
        trace.extend(exc_trace)
        if matched:
            rules = exc.get("rules") or []
            if rules:
                rule = rules[0]
                trace.append({"step": "exception", "id": exc.get("id"), "result": True})
                return {
                    "matched": True,
                    "policy_id": version.policy_id,
                    "version": version.version,
                    "outcome": rule.get("outcome"),
                    "parameters": rule.get("parameters") or {},
                    "applied_exception": exc.get("id") or exc.get("name"),
                    "evaluation_trace": trace,
                }

    matched, cond_trace = match_conditions(version.conditions, facts)
    trace.extend(cond_trace)
    if not matched:
        return {
            "matched": False,
            "policy_id": version.policy_id,
            "version": version.version,
            "outcome": None,
            "parameters": {},
            "applied_exception": None,
            "evaluation_trace": trace,
        }

    if not version.rules:
        return {
            "matched": False,
            "policy_id": version.policy_id,
            "version": version.version,
            "outcome": None,
            "parameters": {},
            "applied_exception": None,
            "evaluation_trace": trace + [{"step": "rules", "result": False, "note": "empty"}],
        }

    rule = version.rules[0]
    trace.append({"step": "rule", "outcome": rule.get("outcome")})
    return {
        "matched": True,
        "policy_id": version.policy_id,
        "version": version.version,
        "outcome": rule.get("outcome"),
        "parameters": rule.get("parameters") or {},
        "applied_exception": None,
        "evaluation_trace": trace,
    }


def run_test_cases(version: PolicyVersion, test_cases: list[dict]) -> list[dict]:
    results = []
    for case in test_cases:
        facts = case.get("facts") or {}
        expected = case.get("expect") or {}
        actual = evaluate_version(version, facts, require_active=False)
        passed = actual.get("matched") == bool(expected.get("matched", True))
        if passed and expected.get("outcome") is not None:
            passed = actual.get("outcome") == expected.get("outcome")
        if passed and expected.get("parameters"):
            for key, val in expected["parameters"].items():
                if actual.get("parameters", {}).get(key) != val:
                    passed = False
                    break
        results.append(
            {
                "name": case.get("name", "unnamed"),
                "passed": passed,
                "expected": expected,
                "actual": {
                    "matched": actual.get("matched"),
                    "outcome": actual.get("outcome"),
                    "parameters": actual.get("parameters"),
                },
            }
        )
    return results
