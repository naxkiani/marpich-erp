"""ACL to Identity Risk — federation risk scoring (no domain imports)."""
from __future__ import annotations


class IdentityRiskAcl:
    async def score_federation(
        self,
        *,
        tenant_id: str,
        auth_method: str = "oidc",
        is_new_user: bool = False,
        correlation_id: str = "",
    ) -> dict:
        from contexts.identity_risk.container import get_identity_risk_service

        result = await get_identity_risk_service().score_federation(
            tenant_id,
            auth_method=auth_method,
            protocol=auth_method,
            is_new_user=is_new_user,
            correlation_id=correlation_id or "federation-risk",
        )
        return result.unwrap() if result.succeeded else {"score": 50, "error": result.error}
