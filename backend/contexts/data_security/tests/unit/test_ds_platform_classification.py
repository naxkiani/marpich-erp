"""P211-E Data Security classification / labeling foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.data_security.application.ds_classification_foundation import (
    validate_ds_classification_foundation,
)
from contexts.data_security.container import (
    get_data_security_service,
    reset_data_security_service,
)
from contexts.data_security.domain.services import (
    ds_platform_classification as cls,
)

REPO_ROOT = Path(__file__).resolve().parents[5]


@pytest.fixture(autouse=True)
def _reset():
    reset_data_security_service()
    yield
    reset_data_security_service()


@pytest.mark.unit
def test_ds_classification_foundation():
    result = validate_ds_classification_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P211-E"
    assert result["adr"] == 380
    assert result["sor"] == "data_security"
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_ds_classification_catalog():
    cat = cls.catalog()
    assert cat["prompt_id"] == "P211-E"
    assert cat["adr"] == 380
    assert cat["data_classifiable_required"] is True
    assert cat["sensitive_detection_available_required"] is True
    assert cat["labels_managed_required"] is True
    assert cat["ai_decisions_explainable_required"] is True
    assert cat["classification_policies_present_required"] is True
    assert cat["classification_lifecycle_defined_required"] is True
    assert cat["architecture"]["layer_count"] >= 8
    assert cat["taxonomy"]["level_count"] >= 5
    assert cat["sensitive_detection"]["category_count"] >= 6
    assert cat["cursor_outputs"]["count"] >= 16
    assert "data_cannot_be_classified" in cat["quality_gates"]["reject_if"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /data-security/classification" in cls.classification_surface()["routes"]
    assert (
        "GET /data-security/classification/readiness"
        in cls.classification_surface()["routes"]
    )


@pytest.mark.unit
def test_ds_classification_acl():
    from contexts.data_security.infrastructure.acl import (
        ds_classification_acl as acls,
    )

    assert acls.to_discovery(tenant_id="t1", asset_ref="a1")[
        "data_classifiable_required"
    ] is True
    assert acls.to_enterprise_ai(tenant_id="t1", model_ref="m1")[
        "ai_decisions_explainable_required"
    ] is True
    assert acls.to_policy_engine(tenant_id="t1", policy_ref="p1")[
        "classification_policies_present_required"
    ] is True
    assert acls.to_workflow_review(tenant_id="t1", review_ref="r1")[
        "classification_lifecycle_defined_required"
    ] is True
    assert acls.to_cyber_security(tenant_id="t1", signal_ref="s1")[
        "sensitive_detection_available_required"
    ] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_classification():
    svc = get_data_security_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_classification"]["prompt_id"] == "P211-E"
    assert catalog["platform_classification"]["adr"] == 380
    summary = svc.platform_classification()
    assert summary["prompt_id"] == "P211-E"
    assert "P211-D" in summary["builds_on"]
    assert summary["level_count"] >= 5
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
