import pytest
from contexts.identity_digital_twin.domain.aggregates.identity_digital_twin_platform import DigitalTwin
from contexts.identity_digital_twin.domain.services import twin_engine, twin_simulation_engine, twin_drift_engine
@pytest.mark.unit
def test_create_twin():
    twin=DigitalTwin.create(tenant_id="t1", twin_ref="twin-t1-0001", identity_ref="identity-1", attributes={"department":"ops"})
    assert twin.to_dict()["identity_ref"] == "identity-1"
@pytest.mark.unit
def test_sync_normalizes_reference_sets():
    projection=twin_engine.normalize_projection({"role_refs":["role-b","role-a","role-a"],"session_refs":["session-1"]})
    assert projection["role_refs"] == ["role-a","role-b"]
@pytest.mark.unit
def test_simulate_access_change_is_non_mutating():
    result=twin_simulation_engine.simulate({"role_refs":["viewer"],"federation_link_refs":[],"lifecycle_state":"active"},"access_change",{"role_refs":["admin"]})
    assert result["mutation_applied"] is False and result["roles_added"] == ["admin"]
@pytest.mark.unit
def test_detect_drift():
    result=twin_drift_engine.detect({"attributes":{"team":"a"},"role_refs":[],"session_refs":[],"federation_link_refs":[],"lifecycle_state":"active"},{"attributes":{"team":"b"},"role_refs":["r"],"session_refs":[],"federation_link_refs":[],"lifecycle_state":"suspended"})
    assert result["detected"] is True and result["severity"] == "critical"
