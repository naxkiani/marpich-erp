"""Release registry must not claim a production release without evidence."""
from __future__ import annotations

from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[3]
REGISTRY = REPO / "docs" / "meos" / "execution" / "MEOS_RELEASE_REGISTRY.v1.yaml"
FORBIDDEN_STATES = frozenset(
    {"APPROVED", "DEPLOYED", "VERIFIED", "PRODUCTION_RELEASE", "RELEASE_CANDIDATE"}
)


def test_release_registry_does_not_claim_production():
    data = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    assert data["production_release_count"] == 0
    assert data["overall_status"] not in FORBIDDEN_STATES
    assert data["overall_status"] in {
        "NOT_RELEASE_CANDIDATE",
        "DEVELOPMENT",
        "BLOCKED",
    }
    for release in data.get("releases", []):
        assert release.get("production_release") is not True
        assert release.get("deployment_status") not in {"DEPLOYED", "VERIFIED"}
        assert release.get("certification_status") != "CERTIFIED"
