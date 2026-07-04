"""Policy evaluator client — implements IPolicyEvaluator for other modules."""
from __future__ import annotations

from datetime import datetime

from contexts.policy.application.service import PolicyApplicationService
from shared.application.ports.policy import IPolicyEvaluator, PolicyDecision


class PolicyEvaluatorClient(IPolicyEvaluator):
    def __init__(self, service: PolicyApplicationService) -> None:
        self._service = service

    async def evaluate(
        self,
        *,
        tenant_id: str,
        domain: str,
        policy_key: str,
        facts: dict,
        as_of: datetime | None = None,
        organization_id: str | None = None,
    ) -> PolicyDecision:
        eval_facts = dict(facts)
        if organization_id:
            eval_facts.setdefault("organization_id", organization_id)
        result = await self._service.evaluate(
            tenant_id=tenant_id,
            domain=domain,
            policy_key=policy_key,
            facts=eval_facts,
            as_of=as_of,
        )
        if not result.succeeded:
            return PolicyDecision(
                matched=False,
                policy_id=None,
                version=None,
                outcome=None,
                parameters={},
                applied_exception=None,
                evaluation_trace=[{"step": "error", "message": result.error}],
            )
        return PolicyDecision.from_evaluation(result.unwrap())
