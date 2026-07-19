"""Domain policies — federation-local rules (not Policy Engine SoR)."""
from __future__ import annotations


class FederationEnabledPolicy:
    def allows(self, profile_federation_enabled: bool) -> bool:
        return bool(profile_federation_enabled)


class CrossTenantTrustPolicy:
    """Default deny unless tenant federation explicitly enables cross-tenant."""

    def allows(self, *, cross_tenant_enabled: bool, trust_status: str) -> bool:
        return cross_tenant_enabled and trust_status == "active"


class AiAgentMustHaveOwnerPolicy:
    def allows(self, owner_principal_id: str | None) -> bool:
        return bool(owner_principal_id and owner_principal_id.strip())
