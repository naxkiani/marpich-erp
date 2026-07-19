"""EIFTP Cross-Tenant Trust (P200-B8) foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]

REQUIRED_ARTIFACTS = [
    "docs/adr/222-enterprise-identity-federation-cross-tenant-trust.md",
    "docs/architecture/ENTERPRISE_IDENTITY_FEDERATION_CROSS_TENANT_TRUST.md",
    "docs/architecture/identity/eiftp/CROSS_TENANT_ARCHITECTURE.v1.yaml",
    "docs/architecture/identity/eiftp/CROSS_TENANT_SURFACE.v1.yaml",
    "backend/contexts/identity_federation/domain/aggregates/cross_tenant_platform.py",
    "backend/contexts/identity_federation/domain/services/cross_tenant_trust_engine.py",
    "backend/contexts/identity_federation/domain/value_objects/cross_tenant_vos.py",
    "backend/contexts/identity_federation/infrastructure/persistence/cross_tenant_memory_store.py",
    "backend/contexts/identity_federation/application/commands/cross_tenant_commands.py",
    "backend/contexts/identity_federation/application/queries/cross_tenant_queries.py",
    "backend/contexts/identity_federation/presentation/cross_tenant_router.py",
]

FORBIDDEN_SIBLING = "backend/contexts/eiftp"


def validate_cross_tenant_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = (root / FORBIDDEN_SIBLING).exists()
    from contexts.identity_federation.domain.aggregates.cross_tenant_platform import (
        DelegationAgreement,
        ExternalIdentity,
        PartnerAccess,
    )
    from contexts.identity_federation.domain.aggregates.federation_platform import TenantFederation
    from contexts.identity_federation.domain.services.cross_tenant_trust_engine import (
        CrossTenantTrustEngine,
    )

    lifecycle_ok = all(
        hasattr(TenantFederation, m)
        for m in ("request_trust", "approve", "activate", "suspend", "revoke", "apply_assessment")
    )
    delegation_ok = hasattr(DelegationAgreement, "create") and hasattr(DelegationAgreement, "approve")
    partner_ok = hasattr(PartnerAccess, "register") and hasattr(PartnerAccess, "assign_access")
    external_ok = hasattr(ExternalIdentity, "invite") and hasattr(ExternalIdentity, "activate")
    facade_ok = hasattr(CrossTenantTrustEngine, "assess_trust_request") and hasattr(
        CrossTenantTrustEngine, "access_gate"
    )
    # Reject unlimited privileges
    try:
        DelegationAgreement.create(
            tenant_id="t",
            delegation_ref="x",
            delegation_type="user",
            owner_id="a",
            delegate_id="b",
            permissions=["*"],
        )
        unlimited_rejected = False
    except ValueError:
        unlimited_rejected = True
    passed = (
        not missing
        and not sibling
        and lifecycle_ok
        and delegation_ok
        and partner_ok
        and external_ok
        and facade_ok
        and unlimited_rejected
    )
    return {
        "prompt": "P200-B8",
        "adr": 222,
        "passed": passed,
        "missing_artifacts": missing,
        "forbidden_sibling_present": sibling,
        "tenant_trust_lifecycle": lifecycle_ok,
        "delegation_aggregate": delegation_ok,
        "partner_access": partner_ok,
        "external_identity": external_ok,
        "engine_facade": facade_ok,
        "unlimited_privileges_rejected": unlimited_rejected,
        "foundation_for": "P200-B9",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
