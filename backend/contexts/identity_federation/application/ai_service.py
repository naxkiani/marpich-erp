"""Federation AI Platform ACL — surfaces routes to Core AI; never embeds LLM SDKs."""
from __future__ import annotations

from contexts.identity_federation.application.fabric_intelligence_service import (
    FabricIntelligenceApplicationService,
)
from shared.application.result import Result


class IdentityFederationAIService:
    """Module AI ACL implementing AI Platform Standard surfaces."""

    SURFACES = (
        "insights",
        "predictions",
        "recommendations",
        "summaries",
        "search",
        "assistant",
        "automation",
        "document_intelligence",
        "voice_commands",
        "chat",
        "report_explanation",
        "anomaly_detection",
        "forecasting",
        "optimization",
    )

    def __init__(self, intelligence: FabricIntelligenceApplicationService) -> None:
        self._intel = intelligence

    async def list_surfaces(self) -> Result[dict]:
        return Result.ok({
            "module": "identity_federation",
            "surfaces": {s: True for s in self.SURFACES},
            "permissions": [
                "federation.ai.read",
                "federation.ai.infer",
                "federation.ai.admin",
            ],
            "delegates_to": "/api/v1/ai",
        })

    async def infer(self, tenant_id: str, *, surface: str, payload: dict, correlation_id: str = "") -> Result[dict]:
        """Route surface requests to local explainable engines (platform AI when available)."""
        if surface in ("predictions", "anomaly_detection", "forecasting"):
            return await self._intel.predict(
                tenant_id,
                model_id=payload.get("model_id", "identity_risk_predictor_v1"),
                features=payload.get("features"),
                correlation_id=correlation_id,
            )
        if surface in ("assistant", "chat"):
            return await self._intel.copilot(
                tenant_id,
                question=str(payload.get("question") or payload.get("prompt") or "help"),
                context=payload.get("context"),
            )
        if surface in ("insights", "summaries", "report_explanation"):
            return await self._intel.analytics(tenant_id)
        if surface in ("recommendations", "optimization"):
            return await self._intel.security_recommendations(tenant_id)
        if surface == "automation":
            return await self._intel.suggest_policies(tenant_id)
        if surface == "search":
            return await self._intel.summarize_audit(tenant_id)
        if surface in ("document_intelligence", "voice_commands"):
            return Result.ok({
                "surface": surface,
                "status": "delegated",
                "message": "Handled by Core AI Platform /api/v1/ai",
            })
        return Result.fail("federation.errors.unknown_ai_surface")
