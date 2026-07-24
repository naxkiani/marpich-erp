"""EIFTP Trust Fabric (P200-B6) foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]

REQUIRED_ARTIFACTS = [
    "docs/adr/220-enterprise-identity-federation-trust-fabric.md",
    "docs/architecture/ENTERPRISE_IDENTITY_FEDERATION_TRUST_FABRIC.md",
    "docs/architecture/identity/eiftp/TRUST_FABRIC_ARCHITECTURE.v1.yaml",
    "docs/architecture/identity/eiftp/TRUST_FABRIC_LEVELS.v1.yaml",
    "docs/architecture/identity/eiftp/TRUST_FABRIC_SCORE_ENGINE.v1.yaml",
    "docs/architecture/identity/eiftp/TRUST_FABRIC_SURFACE.v1.yaml",
    "backend/contexts/identity_federation/domain/value_objects/trust_levels.py",
    "backend/contexts/identity_federation/domain/services/trust_score_engine.py",
    "backend/contexts/identity_federation/domain/services/trust_fabric_engine.py",
    "backend/contexts/identity_federation/infrastructure/persistence/trust_evidence_store.py",
    "backend/contexts/identity_federation/application/commands/trust_fabric_commands.py",
    "backend/contexts/identity_federation/application/queries/trust_fabric_queries.py",
    "backend/contexts/identity_federation/presentation/trust_fabric_router.py",
]

FORBIDDEN_SIBLING = "backend/contexts/eiftp"


def validate_trust_fabric_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = (root / FORBIDDEN_SIBLING).exists()
    from contexts.identity_federation.domain.services.trust_score_engine import (
        compute_continuous_score,
    )
    from contexts.identity_federation.domain.value_objects.trust_levels import (
        EnterpriseTrustLevel,
        level_from_score,
    )

    sample = compute_continuous_score(inputs={"identity_assurance": 90, "risk_signals": 10})
    explainable = sample.get("explainable") is True and "factors" in sample
    levels_ok = len(EnterpriseTrustLevel) == 6 and level_from_score(95) == 5
    no_permit = sample.get("permit_deny") is None
    passed = not missing and not sibling and explainable and levels_ok
    return {
        "prompt": "P200-B6",
        "adr": 220,
        "passed": passed,
        "missing_artifacts": missing,
        "forbidden_sibling_present": sibling,
        "explainable_scores": explainable,
        "levels_0_to_5": levels_ok,
        "no_permit_deny_in_score": no_permit,
        "foundation_for": "P200-B7",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
