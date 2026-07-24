"""EIFTP Enterprise Strategic Goals (P200-B1.1-D1) — mandatory directives."""
from __future__ import annotations

from pathlib import Path

from contexts.identity_federation.domain.services.eiftp_business_drivers import (
    validate_business_drivers_foundation,
)

REPO_ROOT = Path(__file__).resolve().parents[5]

REQUIRED_ARTIFACTS = [
    "docs/adr/215-enterprise-identity-federation-trust-strategic-goals.md",
    "docs/architecture/ENTERPRISE_IDENTITY_FEDERATION_TRUST_STRATEGIC_GOALS.md",
    "docs/architecture/identity/eiftp/GOALS_ENTERPRISE_STRATEGIC_CATALOGUE.v1.yaml",
    "docs/architecture/identity/eiftp/GOALS_TRACEABILITY_MATRIX.v1.yaml",
    "docs/architecture/identity/eiftp/GOALS_TO_CAPABILITY.v1.yaml",
    "docs/architecture/identity/eiftp/GOALS_TO_ARCHITECTURE.v1.yaml",
    "docs/architecture/identity/eiftp/GOALS_TO_POLICY.v1.yaml",
    "docs/architecture/identity/eiftp/GOALS_STRATEGIC_ALIGNMENT.v1.yaml",
    "docs/architecture/identity/eiftp/GOALS_ENTERPRISE_GOVERNANCE_ALIGNMENT.v1.yaml",
    "docs/architecture/identity/eiftp/GOALS_SECURITY_IDENTITY_ZT_FOUNDATION.v1.yaml",
    "docs/architecture/identity/eiftp/GOALS_ARCHITECTURE_VALIDATION.v1.yaml",
]

STRATEGIC_GOAL_IDS = tuple(f"SG{i:02d}" for i in range(1, 11))

CONSTRAINTS_NEVER = (
    "introduce_multiple_identity_authorities",
    "break_tenant_isolation",
    "hardcode_identity_providers",
    "couple_identity_logic_to_business_modules",
    "bypass_policy_evaluation",
    "circumvent_zero_trust_validation",
    "reduce_auditability",
    "weaken_federation_governance",
)


def validate_strategic_goals_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    drivers = validate_business_drivers_foundation(repo_root=root)
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    passed = drivers["passed"] and not missing
    return {
        "prompt": "P200-B1.1-D1",
        "adr": 215,
        "drivers_gate": drivers["verdict"],
        "passed": passed,
        "missing_artifacts": missing,
        "strategic_goal_count": len(STRATEGIC_GOAL_IDS),
        "constraints_count": len(CONSTRAINTS_NEVER),
        "foundation_for": "P200-B1.1-D2",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
