"""P213-N BI CQRS/Events/APIs/Microservices foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.analytics.application.bi_ops_foundation import (
    validate_bi_ops_foundation,
)
from contexts.analytics.container import (
    get_analytics_service,
    reset_analytics_service,
)
from contexts.analytics.domain.services import bi_platform_ops as mod

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_analytics_service()
    yield
    reset_analytics_service()


@pytest.mark.unit
def test_bi_ops_foundation():
    result = validate_bi_ops_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P213-N"
    assert result["adr"] == 418
    assert result["sor"] == "analytics"
    assert result["capability"] == "CAP-PLT-BI-001"
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_bi_ops_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P213-N"
    assert cat["adr"] == 418
    assert cat["principle"] == mod.PRINCIPLE
    assert cat["fabric"] == mod.FABRIC
    assert "durable enterprise event" in cat["principle"]
    assert cat["cqrs_architecture_present_required"] is True
    assert cat["event_sourcing_platform_present_required"] is True
    assert cat["event_streaming_platform_present_required"] is True
    assert cat["api_management_platform_present_required"] is True
    assert cat["enterprise_integration_platform_present_required"] is True
    assert cat["microservices_platform_present_required"] is True
    assert cat["via_enterprise_event_fabric"] is True
    assert cat["via_api_gateway"] is True
    assert cat["module_local_event_bus_forbidden"] is True
    assert cat["sibling_business_intelligence_bc_forbidden"] is True
    assert cat["domain_model"]["core_domain"] == (
        "enterprise_analytics_integration_platform"
    )
    assert cat["domain_model"]["aggregate"]["name"] == (
        "IntegrationPlatformAggregate"
    )
    assert cat["bounded_contexts"]["context_count"] >= 6
    assert cat["cqrs"]["command_count"] >= 6
    assert cat["cqrs"]["query_count"] >= 6
    assert cat["events"]["core_event_count"] >= 10
    assert cat["microservices"]["service_count"] >= 10
    assert cat["read_models"]["type_count"] >= 8
    assert cat["cursor_outputs"]["count"] >= 20
    assert (
        "event_sourcing_platform_is_missing"
        in cat["quality_gates"]["reject_if"]
    )
    assert "P213-M" in cat["builds_on"]
    assert "ADR-417" in cat["builds_on"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /analytics/ops" in mod.ops_surface()["routes"]
    assert "GET /analytics/ops/cqrs" in mod.ops_surface()["routes"]
    assert "GET /analytics/ops/microservices" in mod.ops_surface()["routes"]


@pytest.mark.unit
def test_bi_ops_acl():
    from contexts.analytics.infrastructure.acl import bi_ops_acl as acls

    assert acls.to_enterprise_event_fabric(tenant_id="t1", event_ref="e1")[
        "module_local_event_bus_forbidden"
    ] is True
    assert acls.to_api_gateway(tenant_id="t1", route_ref="r1")[
        "module_local_gateway_forbidden"
    ] is True
    assert acls.to_observability(tenant_id="t1", span_ref="s1")[
        "via_platform_observability"
    ] is True
    assert acls.to_ai_native(tenant_id="t1", decision_ref="d1")[
        "via_p213_m"
    ] is True
    assert acls.to_cryptographic_trust(tenant_id="t1", trust_ref="t1")[
        "mtls"
    ] is True
    assert acls.to_authorization(
        tenant_id="t1", principal_ref="u1", action="ops.read"
    )["fine_grained_authorization"] is True
    assert acls.to_enterprise_ai(tenant_id="t1", model_ref="m1")[
        "module_local_llm_sdk_forbidden"
    ] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_ops():
    svc = get_analytics_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_ops"]["prompt_id"] == "P213-N"
    assert catalog["platform_ops"]["adr"] == 418
    assert catalog["platform_ops"]["principle"] == mod.PRINCIPLE
    assert catalog["platform_ops"]["fabric"] == mod.FABRIC
    assert catalog["sor"] == "analytics"
    summary = svc.platform_ops()
    assert summary["prompt_id"] == "P213-N"
    assert summary["principle"] == mod.PRINCIPLE
    assert summary["fabric"] == mod.FABRIC
    assert "P213-M" in summary["builds_on"]
    assert summary["context_count"] >= 6
    assert summary["microservice_count"] >= 10
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert svc.ops_readiness()["passed"] is True
    assert svc.ops_cqrs()["command_count"] >= 6
    assert svc.ops_event_sourcing()["via_enterprise_event_fabric"] is True
    assert svc.ops_microservices()["service_count"] >= 10
