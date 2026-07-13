"""Identity token delegate for authentication flows."""
from __future__ import annotations

from contexts.identity.container import get_identity_service
from contexts.authentication.domain.ports.authentication_repositories import IIdentityTokenPort


class IdentityTokenAdapter(IIdentityTokenPort):
    async def issue_tokens_for_user(
        self,
        *,
        tenant_id: str,
        user_id: str,
        correlation_id: str,
        ip_address: str | None = None,
        user_agent: str | None = None,
    ) -> dict:
        result = await get_identity_service().issue_tokens_for_user(
            tenant_id=tenant_id,
            user_id=user_id,
            correlation_id=correlation_id,
            ip_address=ip_address,
            user_agent=user_agent,
        )
        if not result.succeeded:
            raise ValueError(result.error or "identity.errors.token_issue_failed")
        tokens = result.unwrap()
        return {
            "access_token": tokens.access_token,
            "refresh_token": tokens.refresh_token,
            "expires_in": tokens.expires_in,
            "mfa_required": tokens.mfa_required,
            "mfa_token": tokens.mfa_token,
        }

    async def find_user_id_by_email(self, tenant_id: str, email: str) -> str | None:
        return await get_identity_service().find_user_id_by_email(tenant_id, email)
