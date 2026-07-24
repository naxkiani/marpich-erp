"""P200-B3 EIFTP DDD Strategic Design foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from contexts.identity_federation.domain.services.eiftp_ddd_strategic import (
    EXPECTED_DOMAIN_COUNT,
    validate_ddd_strategic_foundation,
)
from contexts.identity_federation.domain.strategic import (
    FederatedSubjectKind,
    federation_may_publish,
    has_circular_dependency,
)
from contexts.identity_federation.infrastructure.acl import (
    IdentityEventAcl,
    IntegrationConnectorAcl,
)

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.mark.unit
def test_ddd_strategic_foundation_passes():
    result = validate_ddd_strategic_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["foundation_for"] == "P200-B4"
    assert result["domain_count"] >= EXPECTED_DOMAIN_COUNT
    assert set(result["core_domains"]) == {"DOM_FEDERATION", "DOM_TRUST"}


@pytest.mark.unit
def test_no_circular_context_coupling():
    assert has_circular_dependency() is False


@pytest.mark.unit
def test_federation_event_ownership():
    assert federation_may_publish("TrustGranted") is True
    assert federation_may_publish("IdentityCreated") is False
    assert federation_may_publish("AIIdentityRegistered") is True


@pytest.mark.unit
def test_ubiquitous_subject_kinds():
    assert FederatedSubjectKind.AI_AGENT.value == "ai_agent"
    assert "human" in {k.value for k in FederatedSubjectKind}


@pytest.mark.unit
def test_acl_strips_vendor_keys():
    acl = IntegrationConnectorAcl()
    out = acl.translate_inbound(
        {
            "protocol": "oidc",
            "sub": "ext-1",
            "provider_ref": "p1",
            "okta_raw": {"x": 1},
            "claims": {"email": "a@b.c"},
        }
    )
    assert "okta_raw" not in out
    assert out["external_subject"] == "ext-1"
    assert out["command"] == "federation.external_assertion_accepted"


@pytest.mark.unit
def test_identity_acl_to_local_command():
    out = IdentityEventAcl().translate_inbound(
        {"tenant_id": "t1", "user_id": "u1", "status": "disabled", "event_name": "UserDisabled"}
    )
    assert out["command"] == "federation.sync_principal_state"
    assert out["subject_id"] == "u1"


@pytest.mark.unit
def test_aggregate_catalog_lists_ten():
    path = REPO_ROOT / "docs/architecture/identity/eiftp/DDD_AGGREGATE_CATALOG.v1.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert len(data["federation_aggregates"]) == 10


@pytest.mark.unit
def test_separate_ways_authz_in_mapping():
    path = REPO_ROOT / "docs/architecture/identity/eiftp/DDD_CONTEXT_MAPPING.v1.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    sw = [r for r in data["relationships"] if r["type"] == "separate_ways"]
    assert sw
    assert "authorization" in str(sw[0]["parties"])
