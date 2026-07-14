"""ACL to Adaptive Authentication — Zero Trust PDP (no domain imports)."""
from __future__ import annotations


class AdaptiveAuthAcl:
    async def evaluate_zero_trust(
        self,
        *,
        tenant_id: str,
        user_id: str,
        device_trusted: bool = False,
        device_confidence: float = 0.5,
        session_risk_score: int = 0,
    ) -> dict:
        from contexts.adaptive_authentication.container import get_adaptive_auth_service

        result = await get_adaptive_auth_service().evaluate_zero_trust(
            tenant_id,
            user_id,
            device_trusted=device_trusted,
            device_confidence=device_confidence,
            session_risk_score=session_risk_score,
        )
        return result.unwrap() if result.succeeded else {"allowed": False, "error": result.error}

    async def evaluate_risk(
        self,
        *,
        tenant_id: str,
        user_id: str,
        auth_method: str = "oidc",
        device_fingerprint: str | None = None,
        geo_region: str | None = None,
        correlation_id: str = "",
    ) -> dict:
        from contexts.adaptive_authentication.container import get_adaptive_auth_service

        result = await get_adaptive_auth_service().evaluate(
            tenant_id,
            user_id,
            auth_method=auth_method,
            device_fingerprint=device_fingerprint,
            geo_region=geo_region,
            purpose="federation",
            correlation_id=correlation_id or "federation-zt",
        )
        return result.unwrap() if result.succeeded else {"action": "deny", "error": result.error}
