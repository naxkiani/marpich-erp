"""Identity adapter for Authorization PDP."""
from __future__ import annotations

from contexts.authorization.domain.ports.authorization_repositories import IPrincipalAccessPort
from contexts.identity.container import get_identity_service
from shared.domain.value_objects.unique_id import UniqueId


class IdentityPrincipalAccessAdapter(IPrincipalAccessPort):
    async def resolve_permissions(self, tenant_id: str, principal_id: str) -> list[str]:
        result = await get_identity_service().get_me(tenant_id, principal_id)
        if not result.succeeded:
            return []
        return result.unwrap().get("permissions", [])

    async def resolve_principal_attributes(self, tenant_id: str, principal_id: str) -> dict:
        result = await get_identity_service().get_me(tenant_id, principal_id)
        if not result.succeeded:
            return {}
        data = result.unwrap()
        return {
            "principal_id": principal_id,
            "email": data.get("email"),
            "roles": data.get("roles", []),
            "locale": data.get("locale"),
            "status": data.get("status"),
        }
