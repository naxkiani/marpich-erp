"""Hospital AI Platform ACL — 14 surfaces; never embeds LLM SDKs."""
from __future__ import annotations

from shared.application.result import Result

_AI_SURFACES = (
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


class HospitalAIService:
    """Module AI ACL — delegates to Core AI Platform (/api/v1/ai)."""

    SURFACES = _AI_SURFACES

    async def list_surfaces(self) -> Result[dict]:
        return Result.ok(
            {
                "module": "hospital",
                "surfaces": {s: True for s in self.SURFACES},
                "permissions": ["hospital.ai.read", "hospital.ai.infer"],
                "delegates_to": "/api/v1/ai",
                "embedded_llm_forbidden": True,
                "prompt_templates": [
                    "hospital.encounter.summary",
                    "hospital.admission.risk_flags",
                ],
            }
        )

    async def infer(
        self,
        tenant_id: str,
        *,
        surface: str,
        payload: dict,
        correlation_id: str = "",
    ) -> Result[dict]:
        if surface not in self.SURFACES:
            return Result.fail("hospital.errors.unknown_ai_surface")
        prompt = "hospital.admission.risk_flags"
        if surface in ("summaries", "report_explanation", "insights"):
            prompt = "hospital.encounter.summary"
        return Result.ok(
            {
                "surface": surface,
                "tenant_id": tenant_id,
                "correlation_id": correlation_id or None,
                "status": "delegated",
                "delegates_to": "/api/v1/ai",
                "prompt_template": prompt,
                "payload_keys": sorted(payload.keys()),
                "embedded_llm": False,
            }
        )
