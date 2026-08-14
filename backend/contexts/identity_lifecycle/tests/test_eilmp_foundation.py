"""P201-A1 EILMP Series Foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.identity_lifecycle.container import (
    get_identity_lifecycle_service,
    reset_identity_lifecycle_service,
)
from contexts.identity_lifecycle.domain.services.eilmp_foundation import (
    validate_eilmp_foundation,
)
from contexts.identity_lifecycle.domain.services import lifecycle_workflow_engine as workflow

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_identity_lifecycle_service()
    yield
    reset_identity_lifecycle_service()


@pytest.mark.unit
def test_eilmp_foundation_passes():
    result = validate_eilmp_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["foundation_for"] == "P201-A2"
    assert result["forbidden_sibling_present"] is False
    assert result["jml_actions"] is True
    assert result["state_aliases"] is True


@pytest.mark.unit
def test_state_machine_aliases_and_jml_catalog():
    surface = workflow.state_machine_surface()
    assert surface["aliases"]["operational"] == "active"
    assert surface["aliases"]["requested"] == "registered"
    actions = {a["action"] for a in surface["jml_actions"]}
    assert {"joiner", "mover", "leaver", "rehire", "transfer", "role_change"} <= actions
    assert workflow.resolve_transition("active", "mover") == "active"
    assert workflow.resolve_transition("active", "leaver") == "soft_deleted"
    assert workflow.resolve_transition("verified", "joiner") == "active"


@pytest.mark.unit
@pytest.mark.asyncio
async def test_jml_apply_and_eilmp_surface():
    svc = get_identity_lifecycle_service()
    surface = await svc.get_eilmp_surface()
    assert surface.succeeded
    data = surface.unwrap()
    assert data["adr"] == 227
    assert data["sor"] == "identity_lifecycle"
    assert "jml" in str(data["apis"]).lower()

    registered = await svc.register(
        "tenant-a",
        email="jml@example.com",
        display_name="JML User",
        identity_type="employee",
        correlation_id="corr-jml-1",
    )
    assert registered.succeeded, registered.error
    case = registered.unwrap()
    assert case["identity_type"] == "employee"
    # registered -> need joiner from registered or verified; joiner allows registered
    applied = await svc.apply_jml(
        "tenant-a",
        case["case_ref"],
        action="joiner",
        reason="hire",
        correlation_id="corr-jml-2",
    )
    assert applied.succeeded, applied.error
    assert applied.unwrap()["state"] == "active"

    moved = await svc.apply_jml(
        "tenant-a",
        case["case_ref"],
        action="mover",
        metadata={"department": "finance"},
        correlation_id="corr-jml-3",
    )
    assert moved.succeeded
    assert moved.unwrap()["state"] == "active"
    assert moved.unwrap()["metadata"].get("department") == "finance"
