"""EIFTP Mission (P200-B1.1-A) — validation without inventing a sibling BC."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]

REQUIRED_ARTIFACTS = [
    "docs/adr/212-enterprise-identity-federation-trust-mission.md",
    "docs/architecture/ENTERPRISE_IDENTITY_FEDERATION_TRUST_PLATFORM.md",
    "docs/architecture/identity/eiftp/IDENTITY_TAXONOMY.v1.yaml",
    "docs/architecture/identity/eiftp/TRUST_DOMAINS.v1.yaml",
    "docs/architecture/identity/eiftp/ZERO_TRUST_MISSION_MODEL.v1.yaml",
    "docs/architecture/identity/eiftp/MISSION_VALIDATION_RULES.v1.yaml",
    "docs/architecture/identity/eiftp/MISSION_ARCHITECTURE_COMPLIANCE.v1.yaml",
]

IDENTITY_CLASSES = ("human", "machine", "ai", "external")

TRUST_DOMAIN_IDS = (
    "internal",
    "external",
    "partner",
    "government",
    "banking",
    "healthcare",
    "academic",
    "cross_tenant",
    "ai",
    "service",
    "device",
)

FORBIDDEN_SIBLING = "backend/contexts/eiftp"


def validate_mission_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    federation_ok = (root / "backend/contexts/identity_federation").is_dir()
    sibling_forbidden = (root / FORBIDDEN_SIBLING).exists()
    return {
        "prompt": "P200-B1.1-A",
        "adr": 212,
        "passed": not missing and federation_ok and not sibling_forbidden,
        "missing_artifacts": missing,
        "identity_federation_context_exists": federation_ok,
        "forbidden_sibling_eiftp_exists": sibling_forbidden,
        "identity_classes": list(IDENTITY_CLASSES),
        "trust_domains": list(TRUST_DOMAIN_IDS),
        "verdict": "ENTERPRISE_GRADE" if (not missing and federation_ok and not sibling_forbidden) else "BELOW_THRESHOLD",
    }
