"""P211-D Data Security discovery / inventory foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.data_security.application.ds_discovery_foundation import (
    validate_ds_discovery_foundation,
)
from contexts.data_security.container import (
    get_data_security_service,
    reset_data_security_service,
)
from contexts.data_security.domain.services import (
    ds_platform_discovery as disc,
)

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_data_security_service()
    yield
    reset_data_security_service()


@pytest.mark.unit
def test_ds_discovery_foundation():
    result = validate_ds_discovery_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P211-D"
    assert result["adr"] == 379
    assert result["sor"] == "data_security"
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_ds_discovery_catalog():
    cat = disc.catalog()
    assert cat["prompt_id"] == "P211-D"
    assert cat["adr"] == 379
    assert cat["data_assets_discoverable_required"] is True
    assert cat["inventory_complete_required"] is True
    assert cat["metadata_available_required"] is True
    assert cat["ownership_determinable_required"] is True
    assert cat["shadow_data_visible_required"] is True
    assert cat["ai_discovery_required"] is True
    assert cat["relationships_analyzable_required"] is True
    assert cat["architecture"]["layer_count"] >= 8
    assert cat["connectors"]["connector_count"] >= 20
    assert cat["cursor_outputs"]["count"] >= 18
    assert "data_assets_cannot_be_discovered" in cat["quality_gates"]["reject_if"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /data-security/discovery" in disc.discovery_surface()["routes"]
    assert (
        "GET /data-security/discovery/readiness"
        in disc.discovery_surface()["routes"]
    )


@pytest.mark.unit
def test_ds_discovery_acl():
    from contexts.data_security.infrastructure.acl import (
        ds_discovery_acl as acls,
    )

    assert acls.to_integration_connector(tenant_id="t1", connector_ref="c1")[
        "vendor_sdk_embed_forbidden"
    ] is True
    assert acls.to_enterprise_ai(tenant_id="t1", model_ref="m1")[
        "ai_discovery_required"
    ] is True
    assert acls.to_cyber_security(tenant_id="t1", signal_ref="s1")[
        "shadow_data_visible_required"
    ] is True
    assert acls.to_secrets(tenant_id="t1", secret_ref="sec1")[
        "via_p209"
    ] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_discovery():
    svc = get_data_security_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_discovery"]["prompt_id"] == "P211-D"
    assert catalog["platform_discovery"]["adr"] == 379
    summary = svc.platform_discovery()
    assert summary["prompt_id"] == "P211-D"
    assert "P211-C" in summary["builds_on"]
    assert summary["connector_count"] >= 20
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
