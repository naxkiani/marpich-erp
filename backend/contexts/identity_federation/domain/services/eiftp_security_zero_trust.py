"""EIFTP Security / Zero Trust / Compliance posture (P200-B9) foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]

REQUIRED_ARTIFACTS = [
    "docs/adr/223-enterprise-identity-federation-security-zero-trust.md",
    "docs/architecture/ENTERPRISE_IDENTITY_FEDERATION_SECURITY_ZERO_TRUST.md",
    "docs/architecture/identity/eiftp/SECURITY_ZT_ARCHITECTURE.v1.yaml",
    "docs/architecture/identity/eiftp/SECURITY_ZT_SURFACE.v1.yaml",
    "backend/contexts/identity_federation/domain/value_objects/security_vos.py",
    "backend/contexts/identity_federation/domain/aggregates/security_control_platform.py",
    "backend/contexts/identity_federation/domain/services/federation_security_control_plane.py",
    "backend/contexts/identity_federation/infrastructure/persistence/security_control_memory_store.py",
    "backend/contexts/identity_federation/application/commands/security_control_commands.py",
    "backend/contexts/identity_federation/application/queries/security_control_queries.py",
    "backend/contexts/identity_federation/presentation/security_router.py",
]

FORBIDDEN_SIBLING = "backend/contexts/eiftp"


def validate_security_zero_trust_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = (root / FORBIDDEN_SIBLING).exists()
    from contexts.identity_federation.domain.services.federation_security_control_plane import (
        FederationSecurityControlPlane,
        get_federation_security_control_plane,
    )
    from contexts.identity_federation.domain.value_objects.security_vos import ZeroTrustGateAction

    plane = get_federation_security_control_plane()
    methods_ok = all(
        hasattr(FederationSecurityControlPlane, m)
        for m in (
            "evaluate_zero_trust",
            "evaluate_risk",
            "continuous_verification",
            "detect_threat",
            "assess_compliance_posture",
            "govern_ai_action",
        )
    )
    zt = plane.evaluate_zero_trust(
        context={"identity_verified": True, "device_trusted": True, "risk_score": 10, "trust_score": 80}
    )
    no_authz = zt.get("authz_permit_deny") is None
    actions_ok = len(ZeroTrustGateAction) >= 8
    ai = plane.govern_ai_action(
        ai_context={"ai_identity_verified": False, "trust_score": 10}
    )
    ai_blocks = ai.get("blocked") is True
    passed = not missing and not sibling and methods_ok and no_authz and actions_ok and ai_blocks
    return {
        "prompt": "P200-B9",
        "adr": 223,
        "passed": passed,
        "missing_artifacts": missing,
        "forbidden_sibling_present": sibling,
        "control_plane_methods": methods_ok,
        "no_authz_permit_deny": no_authz,
        "gate_actions_complete": actions_ok,
        "ai_governance_blocks_unverified": ai_blocks,
        "foundation_for": "P200-B10",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
