"""P200-B1.1-D1 EIFTP Enterprise Strategic Goals foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from contexts.identity_federation.domain.services.eiftp_strategic_goals import (
    CONSTRAINTS_NEVER,
    STRATEGIC_GOAL_IDS,
    validate_strategic_goals_foundation,
)

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.mark.unit
def test_eiftp_strategic_goals_foundation_passes():
    result = validate_strategic_goals_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["drivers_gate"] == "ENTERPRISE_GRADE"
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["foundation_for"] == "P200-B1.1-D2"
    assert result["strategic_goal_count"] == 10


@pytest.mark.unit
def test_strategic_goals_sg01_to_sg10():
    path = REPO_ROOT / "docs/architecture/identity/eiftp/GOALS_ENTERPRISE_STRATEGIC_CATALOGUE.v1.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    ids = [g["id"] for g in data["strategic_goals"]]
    assert ids == list(STRATEGIC_GOAL_IDS)
    assert data["immutable"] is True
    for c in CONSTRAINTS_NEVER:
        assert c in data["architectural_constraints_never"]


@pytest.mark.unit
def test_every_goal_cites_driver():
    path = REPO_ROOT / "docs/architecture/identity/eiftp/GOALS_TRACEABILITY_MATRIX.v1.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    for row in data["traceability"]:
        assert row["drivers"], row
        assert row["goal"] in STRATEGIC_GOAL_IDS
    assert set(data["coverage"]["all_primary_drivers_cited"]) == {
        f"P{i}" for i in range(1, 11)
    }


@pytest.mark.unit
def test_sg04_does_not_own_authz():
    path = REPO_ROOT / "docs/architecture/identity/eiftp/GOALS_TO_CAPABILITY.v1.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    sg04 = next(m for m in data["mappings"] if m["goal"] == "SG04")
    assert "CAP_AUTHZ" in sg04["capabilities"]
    assert "authorization" in sg04["note"].lower()


@pytest.mark.unit
def test_d2_foundation_points_forward():
    path = REPO_ROOT / "docs/architecture/identity/eiftp/GOALS_SECURITY_IDENTITY_ZT_FOUNDATION.v1.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert data["next_prompt"] == "P200-B1.1-D2"
    assert len(data["parent_goals"]) == 10


@pytest.mark.unit
def test_architecture_validation_enterprise_grade():
    path = REPO_ROOT / "docs/architecture/identity/eiftp/GOALS_ARCHITECTURE_VALIDATION.v1.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert data["verdict"] == "ENTERPRISE_GRADE"
    assert data["hard_gates"]["no_contexts_eiftp"] == "PASS"
    assert data["hard_gates"]["authz_pdp_unchanged"] == "PASS"
