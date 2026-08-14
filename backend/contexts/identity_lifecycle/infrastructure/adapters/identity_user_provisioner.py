"""Identity user provisioner — ACL to Identity SoR (no domain coupling)."""
from __future__ import annotations

from contexts.identity.container import get_identity_service
from contexts.identity_lifecycle.domain.ports.provisioning import IIdentityUserProvisioner


class IdentityUserProvisionerAdapter(IIdentityUserProvisioner):
    async def provision_user(
        self,
        *,
        tenant_id: str,
        email: str,
        display_name: str,
        external_id: str,
        correlation_id: str,
    ) -> dict:
        result = await get_identity_service().provision_directory_user(
            tenant_id=tenant_id,
            email=email,
            display_name=display_name,
            external_id=external_id,
            correlation_id=correlation_id,
        )
        if not result.succeeded:
            raise ValueError(result.error or "identity.errors.provision_failed")
        return result.unwrap()
