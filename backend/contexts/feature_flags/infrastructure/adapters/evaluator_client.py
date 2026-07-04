"""Feature flag evaluator client."""
from __future__ import annotations

from contexts.feature_flags.application.service import FeatureFlagApplicationService
from shared.application.ports.feature_flags import FlagEvaluation, IFeatureFlagEvaluator


class FeatureFlagEvaluatorClient(IFeatureFlagEvaluator):
    def __init__(self, service: FeatureFlagApplicationService) -> None:
        self._service = service

    async def evaluate(
        self,
        *,
        tenant_id: str,
        keys: list[str],
        context: dict | None = None,
    ) -> dict[str, FlagEvaluation]:
        result = await self._service.evaluate(tenant_id, keys, context)
        if not result.succeeded:
            return {k: FlagEvaluation(False, None, "error", 0) for k in keys}
        return {k: FlagEvaluation.from_dict(v) for k, v in result.unwrap().items()}

    async def is_enabled(
        self,
        *,
        tenant_id: str,
        key: str,
        context: dict | None = None,
    ) -> bool:
        evaluations = await self.evaluate(tenant_id=tenant_id, keys=[key], context=context)
        return evaluations[key].enabled
