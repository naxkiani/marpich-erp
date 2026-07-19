"""P200-B12 Quality / Governance / DoD foundation + series readiness tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.identity_federation.application.commands.qa_commands import (
    CertifyReleaseCommand,
    EvaluateQualityGateCommand,
    RecordQualityAssessmentCommand,
    handle_certify_release,
    handle_evaluate_quality_gate,
    handle_record_quality_assessment,
)
from contexts.identity_federation.application.queries.qa_queries import (
    handle_get_production_readiness,
    handle_get_qa_surface,
)
from contexts.identity_federation.container import reset_identity_federation_service
from contexts.identity_federation.domain.services.eiftp_quality_governance import (
    validate_quality_governance_foundation,
)

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_identity_federation_service()
    yield
    reset_identity_federation_service()


@pytest.mark.unit
def test_quality_governance_foundation_passes():
    result = validate_quality_governance_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["foundation_for"] == "EIFTP_SERIES_COMPLETE"
    assert result["forbidden_sibling_present"] is False
    assert result["series_core_passed"] is True
    assert result["full_foundation_complete"] is False
    assert "P200-B11" in result["series_phases"]
    assert result["series_phases"]["P200-B11"] is True


@pytest.mark.unit
def test_qa_surface_and_readiness():
    surface = handle_get_qa_surface()
    assert surface["adr"] == 226
    assert surface["series_closeout"] is True
    assert surface["gates_count"] >= 10
    readiness = handle_get_production_readiness()
    assert readiness["verdict"] == "ENTERPRISE_GRADE"
    assert readiness["core_series_passed"] is True
    assert readiness["series_status"] == "core_series_complete_with_foundation_backlog"
    assert "P200-B1.Scope" in readiness["foundation_backlog"]


@pytest.mark.unit
@pytest.mark.asyncio
async def test_assessment_gate_and_release_certify():
    assessment = await handle_record_quality_assessment(
        RecordQualityAssessmentCommand(
            tenant_id="tenant-a",
            assessor="arb",
            passed=True,
            notes="core series DoD",
        )
    )
    assert assessment["passed"] is True

    gate = await handle_evaluate_quality_gate(
        EvaluateQualityGateCommand(
            tenant_id="tenant-a",
            gate_id="gate.unit_tests",
            evidence={"ok": True, "suite": "test_eiftp_*"},
        )
    )
    assert gate["passed"] is True
    assert gate["blocking"] is True

    blocked = await handle_evaluate_quality_gate(
        EvaluateQualityGateCommand(
            tenant_id="tenant-a",
            gate_id="gate.security_scan",
            passed=False,
            evidence={"critical": 1},
        )
    )
    assert blocked["passed"] is False

    cert = await handle_certify_release(
        CertifyReleaseCommand(
            tenant_id="tenant-a",
            version="1.0.0",
            boards_approved=["arb", "srb", "apigb", "aigb", "rgb"],
        )
    )
    assert cert["passed"] is True
    assert cert["verdict"] == "CERTIFIED"
    assert cert["gitops_promote_allowed"] is True
    assert cert["authz_permit_deny"] is None

    rejected = await handle_certify_release(
        CertifyReleaseCommand(
            tenant_id="tenant-a",
            version="1.0.1",
            boards_approved=["arb"],
        )
    )
    assert rejected["passed"] is False
    assert rejected["verdict"] == "REJECTED"
