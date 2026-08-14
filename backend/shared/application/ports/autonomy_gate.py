"""Autonomy gate — deny-by-default until Policy + Workflow approvals exist.

Modules must call `AutonomyGate.authorize` before high-risk autonomous mutations.
This is Shared Kernel application port material (no industry logic).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True, slots=True)
class AutonomyDecision:
    allowed: bool
    reason: str
    requires_workflow: bool = True


class IPolicyEvaluatorPort(Protocol):
    async def evaluate(
        self, *, tenant_id: str, domain: str, policy_key: str, facts: dict
    ) -> dict: ...


class IFeatureFlagPort(Protocol):
    async def is_enabled(self, *, tenant_id: str, flag_key: str) -> bool: ...


class AutonomyGate:
    """Deny-by-default gate for Wave 05 autonomy."""

    FLAG_KEY = "autonomy.agents.enabled"
    POLICY_DOMAIN = "autonomy"
    POLICY_KEY = "high_risk"

    def __init__(
        self,
        *,
        flags: IFeatureFlagPort | None = None,
        policies: IPolicyEvaluatorPort | None = None,
    ) -> None:
        self._flags = flags
        self._policies = policies

    async def authorize(
        self,
        *,
        tenant_id: str,
        action: str,
        facts: dict | None = None,
        human_approved: bool = False,
    ) -> AutonomyDecision:
        if not tenant_id or not action:
            return AutonomyDecision(False, "autonomy.errors.invalid_request")

        if self._flags is not None:
            enabled = await self._flags.is_enabled(
                tenant_id=tenant_id, flag_key=self.FLAG_KEY
            )
            if not enabled:
                return AutonomyDecision(False, "autonomy.errors.flag_disabled")

        if self._policies is not None:
            result = await self._policies.evaluate(
                tenant_id=tenant_id,
                domain=self.POLICY_DOMAIN,
                policy_key=self.POLICY_KEY,
                facts={"action": action, **(facts or {})},
            )
            outcome = str(result.get("outcome") or result.get("decision") or "").lower()
            if outcome not in {"allow", "allowed", "permit"}:
                return AutonomyDecision(False, "autonomy.errors.policy_denied")

        if not human_approved:
            return AutonomyDecision(
                False,
                "autonomy.errors.workflow_approval_required",
                requires_workflow=True,
            )

        return AutonomyDecision(True, "autonomy.allowed", requires_workflow=False)
