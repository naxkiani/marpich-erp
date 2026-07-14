"""P198-A federation engine unit tests."""
import pytest

from contexts.identity_federation.domain.services import (
    broker_engine,
    claims_transformation_engine,
    federation_engine,
    federation_plugin_registry,
    provisioning_engine,
    trust_management_engine,
)


@pytest.mark.unit
def test_claims_transformation_direct():
    result = claims_transformation_engine.transform_claims(
        raw_claims={"email": "user@enterprise.dev", "sub": "ext-123"},
        mappings=[
            {"source_claim": "email", "target_claim": "email", "transform_type": "direct", "enabled": True},
            {"source_claim": "sub", "target_claim": "external_id", "transform_type": "direct", "enabled": True},
        ],
    )
    assert result["email"] == "user@enterprise.dev"
    assert result["external_id"] == "ext-123"


@pytest.mark.unit
def test_broker_routes_by_email_domain():
    providers = [
        {"provider_ref": "idp-google", "name": "Google", "enabled": True, "config": {"domains": ["enterprise.dev"]}},
        {"provider_ref": "idp-okta", "name": "Okta", "enabled": True, "config": {"domains": ["partner.com"]}},
    ]
    route = broker_engine.route_authentication(
        tenant_id="test",
        email="user@enterprise.dev",
        providers=providers,
    )
    assert route["routed"] is True
    assert route["provider"]["provider_ref"] == "idp-google"


@pytest.mark.unit
def test_jit_provisioning():
    result = provisioning_engine.evaluate_jit_provisioning(
        jit_enabled=True,
        claims={"email": "new@enterprise.dev", "name": "New User"},
        rules=[{"enabled": True, "claim": "email", "value": "new@enterprise.dev", "roles": ["viewer"]}],
        default_roles=["member"],
    )
    assert result["provision"] is True
    assert "viewer" in result["roles"]


@pytest.mark.unit
def test_trust_hierarchy():
    result = trust_management_engine.evaluate_trust_hierarchy(
        organization_trust=80,
        partner_trust=70,
        identity_trust=60,
        device_trust=50,
    )
    assert result["composite_trust_score"] > 0
    assert result["weakest_link"] == "device"


@pytest.mark.unit
def test_provider_plugin_registry():
    plugins = federation_plugin_registry.list_provider_plugins()
    assert len(plugins) >= 15
    assert any(p["protocol"] == "entra_id" for p in plugins)


@pytest.mark.unit
def test_federation_lifecycle_transition():
    next_state = federation_engine.transition_lifecycle("registered", "verify")
    assert next_state == "verified"
