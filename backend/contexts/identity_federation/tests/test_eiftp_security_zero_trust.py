"""P200-B9 Security / Zero Trust / Compliance posture foundation + CQRS tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.identity_federation.application.commands.security_control_commands import (
    ApproveExceptionCommand,
    CreateSecurityPolicyCommand,
    DetectThreatCommand,
    EvaluateRiskCommand,
    EvaluateZeroTrustCommand,
    GovernAiActionCommand,
    MitigateThreatCommand,
    RegisterSecurityControlCommand,
    RunComplianceAssessmentCommand,
    RunContinuousVerificationCommand,
    handle_approve_exception,
    handle_create_security_policy,
    handle_detect_threat,
    handle_evaluate_risk,
    handle_evaluate_zero_trust,
    handle_govern_ai_action,
    handle_mitigate_threat,
    handle_register_security_control,
    handle_run_compliance_assessment,
    handle_run_continuous_verification,
)
from contexts.identity_federation.application.queries.security_control_queries import (
    handle_get_security_posture,
    handle_get_security_surface,
)
from contexts.identity_federation.container import reset_identity_federation_service
from contexts.identity_federation.domain.services.eiftp_security_zero_trust import (
    validate_security_zero_trust_foundation,
)
from contexts.identity_federation.domain.value_objects.security_vos import ZeroTrustGateAction

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_identity_federation_service()
    yield
    reset_identity_federation_service()


@pytest.mark.unit
def test_security_zero_trust_foundation_passes():
    result = validate_security_zero_trust_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["foundation_for"] == "P200-B10"
    assert result["no_authz_permit_deny"] is True
    assert result["ai_governance_blocks_unverified"] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_zt_risk_cv_threat_compliance_ai_lifecycle():
    control = await handle_register_security_control(
        RegisterSecurityControlCommand(
            tenant_id="tenant-a",
            name="Federation Baseline",
            security_level=2,
            baseline={"mtls_required": True},
        )
    )
    policy = await handle_create_security_policy(
        CreateSecurityPolicyCommand(
            tenant_id="tenant-a",
            control_ref=control["control_ref"],
            policy_key="federation.zero_trust.enabled",
            conditions={"require_mfa_above_risk": 70},
        )
    )
    assert policy["version"] >= 2

    zt = await handle_evaluate_zero_trust(
        EvaluateZeroTrustCommand(
            tenant_id="tenant-a",
            context={
                "identity_verified": True,
                "device_trusted": True,
                "risk_score": 20,
                "trust_score": 80,
                "resource_sensitivity": "confidential",
            },
        )
    )
    assert zt["authz_permit_deny"] is None
    assert zt["gate_action"] in {a.value for a in ZeroTrustGateAction}
    assert zt["never_trust_implicitly"] is True

    risk = await handle_evaluate_risk(
        EvaluateRiskCommand(
            tenant_id="tenant-a",
            subject_type="ai_agent",
            subject_id="agent-1",
            signals={"behavior_risk": 80, "device_risk": 40},
            trust_score=55,
        )
    )
    assert risk["risk_score"] >= 0

    cv = await handle_run_continuous_verification(
        RunContinuousVerificationCommand(
            tenant_id="tenant-a",
            context={
                "identity_verified": True,
                "device_trusted": True,
                "signature_valid": True,
                "trust_score": 70,
            },
        )
    )
    assert cv["triggered"] is True

    threat = await handle_detect_threat(
        DetectThreatCommand(
            tenant_id="tenant-a",
            indicators={"score": 75, "credential_abuse": True},
        )
    )
    assert threat["detected"] is True
    mitigated = await handle_mitigate_threat(
        MitigateThreatCommand(
            tenant_id="tenant-a",
            threat_ref=threat["threat"]["threat_ref"],
            action="revoke_session",
        )
    )
    assert mitigated["status"] == "mitigated"

    compliance = await handle_run_compliance_assessment(
        RunComplianceAssessmentCommand(tenant_id="tenant-a", control_results={})
    )
    assert compliance["status"] == "passed"
    assert compliance["platform_owner"] == "compliance"

    ai_blocked = await handle_govern_ai_action(
        GovernAiActionCommand(
            tenant_id="tenant-a",
            ai_context={"ai_identity_verified": False, "trust_score": 10},
        )
    )
    assert ai_blocked["blocked"] is True

    ai_ok = await handle_govern_ai_action(
        GovernAiActionCommand(
            tenant_id="tenant-a",
            ai_context={
                "ai_identity_verified": True,
                "trust_score": 70,
                "within_capability_scope": True,
                "data_access_allowed": True,
            },
        )
    )
    assert ai_ok["allowed_to_proceed"] is True

    with pytest.raises(ValueError, match="unlimited"):
        await handle_approve_exception(
            ApproveExceptionCommand(
                tenant_id="tenant-a", reason="too broad", scope=["*"]
            )
        )

    posture = handle_get_security_posture(tenant_id="tenant-a")
    assert posture["zero_trust_enabled"] is True
    assert posture["authz_boundary"] == "separate_ways"


@pytest.mark.unit
def test_surface_and_no_sibling_bc():
    surface = handle_get_security_surface()
    assert surface["adr"] == 223
    assert surface["validation"]["passed"] is True
    assert len(surface["gate_actions"]) >= 8
    assert not (REPO_ROOT / "backend/contexts/eiftp").exists()
