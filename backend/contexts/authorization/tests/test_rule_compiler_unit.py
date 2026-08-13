"""AuthZ Rule Compiler foundation tests."""
from __future__ import annotations

import pytest

from contexts.authorization.domain.services import rule_compiler
from contexts.authorization.domain.services.rule_compiler import RuleCompilationError


@pytest.mark.unit
def test_compile_valid_conditions():
    rule = rule_compiler.compile_conditions(
        [
            {"attribute": "department", "operator": "eq", "value": "finance"},
            {"attribute": "roles", "operator": "in", "value": ["teller", "manager"]},
        ]
    )
    assert len(rule.conditions) == 2
    assert rule.to_dicts()[0]["attribute"] == "department"


@pytest.mark.unit
def test_compile_rejects_bad_operator_and_regex():
    with pytest.raises(RuleCompilationError, match="unsupported_operator"):
        rule_compiler.compile_conditions(
            [{"attribute": "x", "operator": "contains", "value": "a"}]
        )
    with pytest.raises(RuleCompilationError, match="invalid_regex"):
        rule_compiler.compile_conditions(
            [{"attribute": "email", "operator": "matches", "value": "("}]
        )


@pytest.mark.unit
def test_empty_conditions_evaluate_true():
    assert rule_compiler.evaluate_conditions([], {"a": 1}) is True
    assert rule_compiler.evaluate_conditions(None, {}) is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_create_abac_policy_compiles():
    from contexts.authorization.container import get_authorization_service, reset_authorization_service

    reset_authorization_service()
    svc = get_authorization_service()
    await svc.seed("tenant-a")
    ok = await svc.create_abac_policy(
        "tenant-a",
        name="Finance only",
        effect="allow",
        permission_pattern="treasury.*",
        conditions=[{"attribute": "department", "operator": "eq", "value": "finance"}],
    )
    assert ok.succeeded, ok.error
    bad = await svc.create_abac_policy(
        "tenant-a",
        name="Bad",
        effect="deny",
        permission_pattern="*",
        conditions=[{"attribute": "x", "operator": "boom", "value": 1}],
    )
    assert bad.succeeded is False
    assert "invalid_abac_conditions" in (bad.error or "")
    reset_authorization_service()
