"""Identity user source for principal sync."""
from __future__ import annotations

from contexts.identity.container import get_identity_service
from contexts.data_isolation.domain.ports.data_isolation_repositories import IIdentityPrincipalSource


class IdentityPrincipalSourceAdapter(IIdentityPrincipalSource):
    async def list_users(self, tenant_id: str) -> list[dict]:
        result = await get_identity_service().list_users(tenant_id)
        if not result.succeeded:
            return []
        return result.unwrap()
