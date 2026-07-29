"""P211-N Data Security CQRS/events/ops foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.data_security.application.ds_ops_foundation import (
    validate_ds_ops_foundation,
)
from contexts.data_security.container import (
    get_data_security_service,
    reset_data_security_service,
)
from contexts.data_security.domain.services import (
    ds_platform_ops as ops,
)

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_data_security_service()
    yield
    reset_data_security_service()


@pytest.mark.unit
def test_ds_ops_foundation():
    result = validate_ds_ops_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P211-N"
    assert result["adr"] == 389
    assert result["sor"] == "data_security"
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_ds_ops_catalog():
    cat = ops.catalog()
    assert cat["prompt_id"] == "P211-N"
    assert cat["adr"] == 389
    assert cat["services_loosely_coupled_required"] is True
    assert cat["events_immutable_required"] is True
    assert cat["apis_managed_required"] is True
    assert cat["security_decisions_traceable_required"] is True
    assert cat["scaling_possible_required"] is True
    assert cat["audit_history_complete_required"] is True
    assert cat["architecture"]["layer_count"] >= 8
    assert cat["cqrs"]["command_count"] >= 20
    assert cat["event_catalogue"]["event_count"] >= 25
    assert cat["microservices"]["service_count"] >= 15
    assert cat["cursor_outputs"]["count"] >= 16
    assert "services_are_tightly_coupled" in cat["quality_gates"]["reject_if"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /data-security/ops" in ops.ops_surface()["routes"]
    assert "GET /data-security/ops/readiness" in ops.ops_surface()["routes"]


@pytest.mark.unit
def test_ds_ops_acl():
    from contexts.data_security.infrastructure.acl import (
        ds_ops_acl as acls,
    )

    assert acls.to_event_bus(tenant_id="t1", event_name="RiskPredicted")[
        "events_immutable_required"
    ] is True
    assert acls.to_event_bus(tenant_id="t1", event_name="RiskPredicted")[
        "outbox_required"
    ] is True
    assert acls.to_api_gateway(tenant_id="t1", route_ref="r1")[
        "apis_managed_required"
    ] is True
    assert acls.to_audit(tenant_id="t1", decision_ref="d1")[
        "security_decisions_traceable_required"
    ] is True
    assert acls.to_secrets_mesh(tenant_id="t1", service_ref="s1")[
        "mtls_via_p209"
    ] is True
    assert acls.to_twin(tenant_id="t1", twin_ref="tw1")[
        "scaling_possible_required"
    ] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_ops():
    svc = get_data_security_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_ops"]["prompt_id"] == "P211-N"
    assert catalog["platform_ops"]["adr"] == 389
    summary = svc.platform_ops()
    assert summary["prompt_id"] == "P211-N"
    assert "P211-M" in summary["builds_on"]
    assert summary["command_count"] >= 20
    assert summary["event_count"] >= 25
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
