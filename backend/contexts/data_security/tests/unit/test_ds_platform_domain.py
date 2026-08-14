"""P211-C Data Security domain architecture foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.data_security.application.ds_domain_foundation import (
    validate_ds_domain_foundation,
)
from contexts.data_security.container import (
    get_data_security_service,
    reset_data_security_service,
)
from contexts.data_security.domain.services import ds_platform_domain as pdom

REPO_ROOT = Path(__file__).resolve().parents[5]


@pytest.fixture(autouse=True)
def _reset():
    reset_data_security_service()
    yield
    reset_data_security_service()


@pytest.mark.unit
def test_ds_domain_foundation():
    result = validate_ds_domain_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P211-C"
    assert result["adr"] == 378
    assert result["sor"] == "data_security"
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_ds_domain_catalog():
    cat = pdom.catalog()
    assert cat["prompt_id"] == "P211-C"
    assert cat["adr"] == 378
    assert cat["domains_loosely_coupled_required"] is True
    assert cat["data_ownership_clear_required"] is True
    assert cat["privacy_integrated_with_security_required"] is True
    assert cat["events_present_required"] is True
    assert cat["aggregates_defined_required"] is True
    assert cat["integration_boundaries_clear_required"] is True
    assert cat["bounded_contexts"]["context_count"] >= 12
    assert cat["aggregates"]["aggregate_count"] >= 12
    assert cat["events"]["core_event_count"] >= 12
    assert cat["microservices"]["service_count"] >= 12
    assert cat["cursor_outputs"]["count"] >= 12
    assert "domains_are_tightly_coupled" in cat["quality_gates"]["reject_if"]
    assert cat["privacy_security"]["not_separated"] is True
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /data-security/domain" in pdom.domain_surface()["routes"]
    assert "GET /data-security/domain/readiness" in pdom.domain_surface()["routes"]


@pytest.mark.unit
def test_ds_domain_acl():
    from contexts.data_security.infrastructure.acl import ds_domain_acl as acls

    assert acls.to_consent(tenant_id="t1", subject_ref="s1")[
        "privacy_integrated_with_security_required"
    ] is True
    assert acls.to_authorization(
        tenant_id="t1", principal_ref="u1", action="read"
    )["integration_boundaries_clear_required"] is True
    assert acls.to_secrets(tenant_id="t1", key_ref="k1")[
        "via_p209"
    ] is True
    assert acls.to_ai_governance(tenant_id="t1", model_ref="m1")[
        "via_p210_m"
    ] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_domain():
    svc = get_data_security_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_domain"]["prompt_id"] == "P211-C"
    assert catalog["platform_domain"]["adr"] == 378
    summary = svc.platform_domain()
    assert summary["prompt_id"] == "P211-C"
    assert "P211-B" in summary["builds_on"]
    assert summary["context_count"] >= 12
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
