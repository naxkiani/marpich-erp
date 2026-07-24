"""EIFTP Business Drivers (P200-B1.1-C) — immutable architectural inputs."""
from __future__ import annotations

from pathlib import Path

from contexts.identity_federation.domain.services.eiftp_vision import validate_vision_foundation

REPO_ROOT = Path(__file__).resolve().parents[5]

REQUIRED_ARTIFACTS = [
    "docs/adr/214-enterprise-identity-federation-trust-business-drivers.md",
    "docs/architecture/ENTERPRISE_IDENTITY_FEDERATION_TRUST_BUSINESS_DRIVERS.md",
    "docs/architecture/identity/eiftp/BUSINESS_DRIVER_CATALOGUE.v1.yaml",
    "docs/architecture/identity/eiftp/BUSINESS_CAPABILITY_MAP.v1.yaml",
    "docs/architecture/identity/eiftp/BUSINESS_MOTIVATION_MODEL.v1.yaml",
    "docs/architecture/identity/eiftp/BUSINESS_STRATEGIC_DRIVER_MATRIX.v1.yaml",
    "docs/architecture/identity/eiftp/BUSINESS_IDENTITY_VALUE_CHAIN.v1.yaml",
    "docs/architecture/identity/eiftp/BUSINESS_OUTCOME_MATRIX.v1.yaml",
    "docs/architecture/identity/eiftp/BUSINESS_CAPABILITY_TRACEABILITY.v1.yaml",
    "docs/architecture/identity/eiftp/BUSINESS_ARCHITECTURE_ALIGNMENT.v1.yaml",
    "docs/architecture/identity/eiftp/BUSINESS_COMPLIANCE_ALIGNMENT.v1.yaml",
    "docs/architecture/identity/eiftp/BUSINESS_STRATEGIC_GOALS_FOUNDATION.v1.yaml",
]

PRIMARY_DRIVER_IDS = tuple(f"P{i}" for i in range(1, 11))

QUALITY_GATES_REJECT_IF = (
    "multiple_identity_authorities",
    "tenant_isolation_violated",
    "zero_trust_principles_broken",
    "identity_coupled_to_business_modules",
    "provider_specific_logic_hardcoded",
    "future_federation_prevented",
    "ai_identity_governance_prevented",
    "vendor_lock_in_introduced",
)


def validate_business_drivers_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    vision = validate_vision_foundation(repo_root=root)
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    passed = vision["passed"] and not missing
    return {
        "prompt": "P200-B1.1-C",
        "adr": 214,
        "vision_gate": vision["verdict"],
        "passed": passed,
        "missing_artifacts": missing,
        "primary_driver_count": len(PRIMARY_DRIVER_IDS),
        "quality_gates_count": len(QUALITY_GATES_REJECT_IF),
        "foundation_for": "P200-B1.1-D1",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
