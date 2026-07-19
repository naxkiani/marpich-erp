"""P200-B1.1-B EIFTP Vision foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from contexts.identity_federation.domain.services.eiftp_vision import (
    TRUST_FABRIC_MIN_EDGES,
    VISION_PRINCIPLES,
    validate_vision_foundation,
)

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.mark.unit
def test_eiftp_vision_foundation_passes():
    result = validate_vision_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["mission_gate"] == "ENTERPRISE_GRADE"
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["foundation_for"] == "P200-B1.1-C"


@pytest.mark.unit
def test_vision_principles_eighteen():
    path = REPO_ROOT / "docs/architecture/identity/eiftp/VISION_VALIDATION_CHECKLIST.v1.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert set(data["principles"]) == set(VISION_PRINCIPLES)
    assert len(data["principles"]) == 18


@pytest.mark.unit
def test_trust_fabric_has_required_edges():
    path = REPO_ROOT / "docs/architecture/identity/eiftp/VISION_TRUST_FABRIC.v1.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert len(data["edges"]) >= TRUST_FABRIC_MIN_EDGES


@pytest.mark.unit
def test_ai_identity_never_bypass_law():
    path = REPO_ROOT / "docs/architecture/identity/eiftp/VISION_AI_IDENTITY.v1.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert "never bypass" in data["law"].lower()
    assert "identity" in data["required_attributes"]
    assert "trust_score" in data["required_attributes"]
