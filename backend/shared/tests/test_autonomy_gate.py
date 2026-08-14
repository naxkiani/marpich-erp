"""Unit — AutonomyGate deny-by-default."""
from __future__ import annotations

import pytest

from shared.application.ports.autonomy_gate import AutonomyGate


class _Flags:
    def __init__(self, enabled: bool) -> None:
        self.enabled = enabled

    async def is_enabled(self, *, tenant_id: str, flag_key: str) -> bool:
        return self.enabled


class _Policies:
    def __init__(self, outcome: str) -> None:
        self.outcome = outcome

    async def evaluate(self, *, tenant_id: str, domain: str, policy_key: str, facts: dict) -> dict:
        return {"outcome": self.outcome}


@pytest.mark.asyncio
async def test_autonomy_denied_when_flag_off():
    gate = AutonomyGate(flags=_Flags(False), policies=_Policies("allow"))
    d = await gate.authorize(tenant_id="t1", action="heal.db", human_approved=True)
    assert d.allowed is False
    assert "flag" in d.reason


@pytest.mark.asyncio
async def test_autonomy_denied_when_policy_denies():
    gate = AutonomyGate(flags=_Flags(True), policies=_Policies("deny"))
    d = await gate.authorize(tenant_id="t1", action="heal.db", human_approved=True)
    assert d.allowed is False
    assert "policy" in d.reason


@pytest.mark.asyncio
async def test_autonomy_denied_without_human_approval():
    gate = AutonomyGate(flags=_Flags(True), policies=_Policies("allow"))
    d = await gate.authorize(tenant_id="t1", action="heal.db", human_approved=False)
    assert d.allowed is False
    assert d.requires_workflow is True


@pytest.mark.asyncio
async def test_autonomy_allowed_when_all_gates_pass():
    gate = AutonomyGate(flags=_Flags(True), policies=_Policies("allow"))
    d = await gate.authorize(tenant_id="t1", action="heal.db", human_approved=True)
    assert d.allowed is True
