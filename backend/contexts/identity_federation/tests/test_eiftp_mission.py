"""P200-B1.1-A EIFTP Mission foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from contexts.identity_federation.domain.services.eiftp_mission import (
    IDENTITY_CLASSES,
    TRUST_DOMAIN_IDS,
    validate_mission_foundation,
)

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.mark.unit
def test_eiftp_mission_foundation_passes():
    result = validate_mission_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["forbidden_sibling_eiftp_exists"] is False
    assert result["identity_federation_context_exists"] is True


@pytest.mark.unit
def test_identity_taxonomy_four_classes():
    path = REPO_ROOT / "docs/architecture/identity/eiftp/IDENTITY_TAXONOMY.v1.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    found = {c["id"] for c in data["classes"]}
    assert found == set(IDENTITY_CLASSES)


@pytest.mark.unit
def test_trust_domains_catalog_has_eleven():
    path = REPO_ROOT / "docs/architecture/identity/eiftp/TRUST_DOMAINS.v1.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    found = {d["id"] for d in data["domains"]}
    assert set(TRUST_DOMAIN_IDS) <= found
    assert len(found) >= 11
