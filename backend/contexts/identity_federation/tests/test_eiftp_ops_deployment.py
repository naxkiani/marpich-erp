"""P200-B11 Ops Deployment / DevSecOps / Observability foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.identity_federation.application.commands.ops_commands import (
    RecordDrDrillCommand,
    RequestAiOpsRecommendationCommand,
    SignalIncidentCommand,
    handle_record_dr_drill,
    handle_request_ai_ops_recommendation,
    handle_signal_incident,
)
from contexts.identity_federation.application.queries.ops_queries import (
    handle_get_ops_health,
    handle_get_ops_surface,
    handle_get_slo_status,
)
from contexts.identity_federation.container import reset_identity_federation_service
from contexts.identity_federation.domain.services.eiftp_ops_deployment import (
    validate_ops_deployment_foundation,
)

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_identity_federation_service()
    yield
    reset_identity_federation_service()


@pytest.mark.unit
def test_ops_foundation_passes():
    result = validate_ops_deployment_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["foundation_for"] == "P200-B12"
    assert result["gitops"] is True
    assert result["helm"] is True
    assert result["distributed_tracing"] is True
    assert not result["secret_scan_hits"]
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_ops_surface_and_health():
    surface = handle_get_ops_surface()
    assert surface["adr"] == 225
    assert surface["deployment"]["manual_deploy_forbidden"] is True
    assert "rollback" in surface["pipeline"]["stages"]
    health = handle_get_ops_health()
    assert health["status"] == "healthy"
    assert all(health["checks"].values())


@pytest.mark.unit
def test_slo_error_budget_freeze():
    ok = handle_get_slo_status(availability_ratio=0.99995)
    assert ok["error_budget_exhausted"] is False
    assert ok["freeze_risky_deploys"] is False
    bad = handle_get_slo_status(availability_ratio=0.999)
    assert bad["error_budget_exhausted"] is True
    assert bad["freeze_risky_deploys"] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_incident_dr_ai_ops_commands():
    incident = await handle_signal_incident(
        SignalIncidentCommand(
            tenant_id="tenant-a",
            incident_class="outbox_backlog",
            severity="high",
            summary="pending outbox growing",
            signals={"outbox_lag_seconds": 120},
        )
    )
    assert incident["status"] == "open"
    assert incident["tenant_id"] == "tenant-a"

    drill = await handle_record_dr_drill(
        RecordDrDrillCommand(
            tenant_id="tenant-a",
            mode="active_passive",
            steps_completed=["announce_drill", "verify_ops_health"],
            passed=True,
        )
    )
    assert drill["passed"] is True

    rec = await handle_request_ai_ops_recommendation(
        RequestAiOpsRecommendationCommand(
            tenant_id="tenant-a",
            context={"outbox_lag_seconds": 120, "error_budget_exhausted": True},
        )
    )
    assert "scale_outbox_dispatcher" in rec["hints"]
    assert "freeze_risky_deploys" in rec["hints"]
    assert rec["authz_permit_deny"] is None
