"""EIFTP Vision (P200-B1.1-B) — validation without inventing a sibling BC."""
from __future__ import annotations

from pathlib import Path

from contexts.identity_federation.domain.services.eiftp_mission import validate_mission_foundation

REPO_ROOT = Path(__file__).resolve().parents[5]

REQUIRED_ARTIFACTS = [
    "docs/adr/213-enterprise-identity-federation-trust-vision.md",
    "docs/architecture/ENTERPRISE_IDENTITY_FEDERATION_TRUST_VISION.md",
    "docs/architecture/identity/eiftp/VISION_FUTURE_STATE_ARCHITECTURE.v1.yaml",
    "docs/architecture/identity/eiftp/VISION_TRUST_FABRIC.v1.yaml",
    "docs/architecture/identity/eiftp/VISION_IDENTITY_STRATEGY.v1.yaml",
    "docs/architecture/identity/eiftp/VISION_SECURITY.v1.yaml",
    "docs/architecture/identity/eiftp/VISION_AI_IDENTITY.v1.yaml",
    "docs/architecture/identity/eiftp/VISION_CAPABILITY_MATRIX.v1.yaml",
    "docs/architecture/identity/eiftp/VISION_VALIDATION_CHECKLIST.v1.yaml",
    "docs/architecture/identity/eiftp/VISION_ARCHITECTURE_COMPLIANCE.v1.yaml",
]

VISION_PRINCIPLES = (
    "identity_first",
    "trust_first",
    "policy_first",
    "zero_trust",
    "cloud_native",
    "api_first",
    "ai_native",
    "metadata_driven",
    "configuration_driven",
    "policy_driven",
    "knowledge_graph_native",
    "digital_twin_native",
    "plugin_first",
    "compliance_first",
    "security_by_design",
    "privacy_by_design",
    "audit_by_design",
    "resilience_by_design",
)

TRUST_FABRIC_MIN_EDGES = 12


def validate_vision_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    mission = validate_mission_foundation(repo_root=root)
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    passed = mission["passed"] and not missing
    return {
        "prompt": "P200-B1.1-B",
        "adr": 213,
        "mission_gate": mission["verdict"],
        "passed": passed,
        "missing_artifacts": missing,
        "vision_principles_count": len(VISION_PRINCIPLES),
        "foundation_for": "P200-B1.1-C",  # Business Drivers (ADR-214)
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
