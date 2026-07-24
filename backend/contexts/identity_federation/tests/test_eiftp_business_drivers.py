"""P200-B1.1-C EIFTP Business Drivers foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from contexts.identity_federation.domain.services.eiftp_business_drivers import (
    PRIMARY_DRIVER_IDS,
    QUALITY_GATES_REJECT_IF,
    validate_business_drivers_foundation,
)

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.mark.unit
def test_eiftp_business_drivers_foundation_passes():
    result = validate_business_drivers_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["vision_gate"] == "ENTERPRISE_GRADE"
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["foundation_for"] == "P200-B1.1-D1"
    assert result["primary_driver_count"] == 10


@pytest.mark.unit
def test_primary_drivers_p1_to_p10():
    path = REPO_ROOT / "docs/architecture/identity/eiftp/BUSINESS_DRIVER_CATALOGUE.v1.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    ids = [d["id"] for d in data["primary_drivers"]]
    assert ids == list(PRIMARY_DRIVER_IDS)
    assert data["immutable"] is True
    for gate in QUALITY_GATES_REJECT_IF:
        assert gate in data["quality_gates_reject_if"]


@pytest.mark.unit
def test_traceability_covers_all_primary_drivers():
    path = REPO_ROOT / "docs/architecture/identity/eiftp/BUSINESS_CAPABILITY_TRACEABILITY.v1.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    drivers = {row["driver"] for row in data["traceability"]}
    assert drivers == set(PRIMARY_DRIVER_IDS)


@pytest.mark.unit
def test_authz_not_owned_by_federation():
    path = REPO_ROOT / "docs/architecture/identity/eiftp/BUSINESS_CAPABILITY_MAP.v1.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    authz = next(c for c in data["strategic_capabilities"] if c["id"] == "CAP_AUTHZ")
    assert authz["owner_context"] == "authorization"


@pytest.mark.unit
def test_strategic_goals_foundation_points_to_d():
    path = REPO_ROOT / "docs/architecture/identity/eiftp/BUSINESS_STRATEGIC_GOALS_FOUNDATION.v1.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert data["next_prompt"] == "P200-B1.1-D1"
    joined = " ".join(data["rules"])
    assert "P1" in joined and "P10" in joined
