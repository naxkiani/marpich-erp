"""Federation Security Control Plane commands (P200-B9)."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta

from contexts.identity_federation.domain.aggregates.security_control_platform import (
    CompliancePostureSnapshot,
    RiskAssessment,
    SecurityControl,
    SecurityException,
    ThreatEvent,
)
from contexts.identity_federation.domain.services.federation_security_control_plane import (
    get_federation_security_control_plane,
)
from contexts.identity_federation.infrastructure.observability import federation_trust_metrics
from contexts.identity_federation.infrastructure.persistence.security_control_memory_store import (
    SecurityControlMemoryStore,
)
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(frozen=True, slots=True)
class RegisterSecurityControlCommand:
    tenant_id: str
    name: str
    control_ref: str | None = None
    security_level: int = 1
    classification: str = "internal"
    baseline: dict = field(default_factory=dict)
    rules: list[dict] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class CreateSecurityPolicyCommand:
    tenant_id: str
    control_ref: str
    policy_key: str
    conditions: dict = field(default_factory=dict)
    version: str = "1.0.0"


@dataclass(frozen=True, slots=True)
class EvaluateZeroTrustCommand:
    tenant_id: str
    context: dict = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class EvaluateRiskCommand:
    tenant_id: str
    subject_type: str = "session"
    subject_id: str = ""
    signals: dict = field(default_factory=dict)
    trust_score: int = 50


@dataclass(frozen=True, slots=True)
class RunContinuousVerificationCommand:
    tenant_id: str
    context: dict = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class DetectThreatCommand:
    tenant_id: str
    indicators: dict = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class MitigateThreatCommand:
    tenant_id: str
    threat_ref: str
    action: str = "contain"
    notes: str = ""


@dataclass(frozen=True, slots=True)
class RunComplianceAssessmentCommand:
    tenant_id: str
    control_results: dict = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class GovernAiActionCommand:
    tenant_id: str
    ai_context: dict = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class ApproveExceptionCommand:
    tenant_id: str
    reason: str
    scope: list[str] = field(default_factory=list)
    days: int = 7
    exception_ref: str | None = None


@dataclass(frozen=True, slots=True)
class RevokeExceptionCommand:
    tenant_id: str
    exception_ref: str
    reason: str = "revoked"


async def handle_register_security_control(command: RegisterSecurityControlCommand) -> dict:
    ref = command.control_ref or SecurityControlMemoryStore._next(command.tenant_id, "ctrl")
    control = SecurityControl.register(
        tenant_id=command.tenant_id,
        control_ref=ref,
        name=command.name,
        security_level=command.security_level,
        classification=command.classification,
        baseline=command.baseline,
        rules=command.rules,
    )
    SecurityControlMemoryStore.controls[f"{command.tenant_id}:{ref}"] = control
    SecurityControlMemoryStore.append_event(
        {
            "event": "SecurityPolicyActivated" if command.rules else "SecurityControlRegistered",
            "tenant_id": command.tenant_id,
            "control_ref": ref,
            "at": datetime.now(UTC).isoformat(),
        }
    )
    federation_trust_metrics.increment("security_control_registered_total")
    return control.to_dict()


async def handle_create_security_policy(command: CreateSecurityPolicyCommand) -> dict:
    key = f"{command.tenant_id}:{command.control_ref}"
    control = SecurityControlMemoryStore.controls.get(key)
    if control is None:
        raise ValueError("security.control_not_found")
    control.activate_policy(
        policy={
            "policy_key": command.policy_key,
            "conditions": command.conditions,
            "version": command.version,
        }
    )
    SecurityControlMemoryStore.controls[key] = control
    SecurityControlMemoryStore.append_event(
        {
            "event": "SecurityPolicyCreated",
            "tenant_id": command.tenant_id,
            "control_ref": command.control_ref,
            "policy_key": command.policy_key,
            "at": datetime.now(UTC).isoformat(),
        }
    )
    federation_trust_metrics.increment("security_policy_created_total")
    return control.to_dict()


async def handle_evaluate_zero_trust(command: EvaluateZeroTrustCommand) -> dict:
    plane = get_federation_security_control_plane()
    ctx = {**command.context, "tenant_id": command.tenant_id}
    decision = plane.evaluate_zero_trust(context=ctx)
    SecurityControlMemoryStore.last_zt[command.tenant_id] = decision
    SecurityControlMemoryStore.append_event(
        {
            "event": "ZeroTrustDecisionCreated",
            "tenant_id": command.tenant_id,
            "gate_action": decision["gate_action"],
            "at": datetime.now(UTC).isoformat(),
        }
    )
    if decision["gate_action"] in ("deny", "quarantine"):
        SecurityControlMemoryStore.append_event(
            {
                "event": "SecurityViolationDetected",
                "tenant_id": command.tenant_id,
                "gate_action": decision["gate_action"],
                "at": datetime.now(UTC).isoformat(),
            }
        )
    federation_trust_metrics.increment("zero_trust_evaluated_total")
    return decision


async def handle_evaluate_risk(command: EvaluateRiskCommand) -> dict:
    plane = get_federation_security_control_plane()
    result = plane.evaluate_risk(
        signals=command.signals,
        subject={"subject_type": command.subject_type, "subject_id": command.subject_id, "trust_score": command.trust_score},
    )
    ref = SecurityControlMemoryStore._next(command.tenant_id, "risk")
    assessment = RiskAssessment(
        id=UniqueId.generate(),
        tenant_id=command.tenant_id,
        assessment_ref=ref,
        subject_type=command.subject_type,
        subject_id=command.subject_id or "unknown",
        risk_score=result["risk_score"],
        risk_level=result["level"],
        signals=result.get("signals") or {},
        factors=list((result.get("adaptive") or {}).keys()),
    )
    SecurityControlMemoryStore.risks[f"{command.tenant_id}:{ref}"] = assessment
    SecurityControlMemoryStore.append_event(
        {
            "event": "RiskCalculated",
            "tenant_id": command.tenant_id,
            "assessment_ref": ref,
            "risk_level": assessment.risk_level,
            "at": datetime.now(UTC).isoformat(),
        }
    )
    federation_trust_metrics.increment("risk_evaluated_total")
    return {**assessment.to_dict(), "evaluation": result}


async def handle_run_continuous_verification(
    command: RunContinuousVerificationCommand,
) -> dict:
    plane = get_federation_security_control_plane()
    ctx = {**command.context, "tenant_id": command.tenant_id}
    result = plane.continuous_verification(context=ctx)
    SecurityControlMemoryStore.append_event(
        {
            "event": "ContinuousVerificationTriggered",
            "tenant_id": command.tenant_id,
            "gate_action": result["zero_trust"]["gate_action"],
            "at": datetime.now(UTC).isoformat(),
        }
    )
    federation_trust_metrics.increment("continuous_verification_total")
    return result


async def handle_detect_threat(command: DetectThreatCommand) -> dict:
    plane = get_federation_security_control_plane()
    detection = plane.detect_threat(indicators=command.indicators)
    if not detection["detected"]:
        return {**detection, "threat": None}
    ref = SecurityControlMemoryStore._next(command.tenant_id, "threat")
    threat = ThreatEvent(
        id=UniqueId.generate(),
        tenant_id=command.tenant_id,
        threat_ref=ref,
        threat_type=(detection["threat_types"] or ["anomaly"])[0],
        severity=detection["severity"],
        indicators=command.indicators,
        status="open",
    )
    SecurityControlMemoryStore.threats[f"{command.tenant_id}:{ref}"] = threat
    SecurityControlMemoryStore.append_event(
        {
            "event": "ThreatDetected",
            "tenant_id": command.tenant_id,
            "threat_ref": ref,
            "severity": threat.severity,
            "at": datetime.now(UTC).isoformat(),
        }
    )
    federation_trust_metrics.increment("threat_detected_total")
    return {**detection, "threat": threat.to_dict()}


async def handle_mitigate_threat(command: MitigateThreatCommand) -> dict:
    key = f"{command.tenant_id}:{command.threat_ref}"
    threat = SecurityControlMemoryStore.threats.get(key)
    if threat is None:
        raise ValueError("security.threat_not_found")
    threat.mitigate(action=command.action, notes=command.notes)
    SecurityControlMemoryStore.threats[key] = threat
    SecurityControlMemoryStore.append_event(
        {
            "event": "ThreatMitigated",
            "tenant_id": command.tenant_id,
            "threat_ref": command.threat_ref,
            "at": datetime.now(UTC).isoformat(),
        }
    )
    federation_trust_metrics.increment("threat_mitigated_total")
    return threat.to_dict()


async def handle_run_compliance_assessment(command: RunComplianceAssessmentCommand) -> dict:
    plane = get_federation_security_control_plane()
    posture = plane.assess_compliance_posture(control_results=command.control_results)
    ref = SecurityControlMemoryStore._next(command.tenant_id, "comp")
    snap = CompliancePostureSnapshot(
        id=UniqueId.generate(),
        tenant_id=command.tenant_id,
        assessment_ref=ref,
        frameworks=list(posture["frameworks"]),
        controls_passed=posture["controls_passed"],
        controls_failed=posture["controls_failed"],
        violations=list(posture["violations"]),
        evidence_refs=[f"evidence://federation/{command.tenant_id}/{ref}"],
        status=posture["status"],
    )
    SecurityControlMemoryStore.compliance[f"{command.tenant_id}:{ref}"] = snap
    SecurityControlMemoryStore.append_event(
        {
            "event": "ComplianceAssessmentStarted",
            "tenant_id": command.tenant_id,
            "assessment_ref": ref,
            "at": datetime.now(UTC).isoformat(),
        }
    )
    evt = "CompliancePassed" if snap.status == "passed" else "ComplianceViolationDetected"
    SecurityControlMemoryStore.append_event(
        {
            "event": evt,
            "tenant_id": command.tenant_id,
            "assessment_ref": ref,
            "at": datetime.now(UTC).isoformat(),
        }
    )
    federation_trust_metrics.increment("compliance_assessed_total")
    return snap.to_dict()


async def handle_govern_ai_action(command: GovernAiActionCommand) -> dict:
    plane = get_federation_security_control_plane()
    result = plane.govern_ai_action(ai_context=command.ai_context)
    if result["blocked"]:
        SecurityControlMemoryStore.append_event(
            {
                "event": "AIActionBlocked",
                "tenant_id": command.tenant_id,
                "reasons": result["reasons"],
                "at": datetime.now(UTC).isoformat(),
            }
        )
    federation_trust_metrics.increment("ai_security_governed_total")
    return result


async def handle_approve_exception(command: ApproveExceptionCommand) -> dict:
    if "*" in command.scope:
        raise ValueError("security.unlimited_exception_forbidden")
    ref = command.exception_ref or SecurityControlMemoryStore._next(command.tenant_id, "exc")
    exc = SecurityException(
        id=UniqueId.generate(),
        tenant_id=command.tenant_id,
        exception_ref=ref,
        reason=command.reason,
        scope=list(command.scope),
        status="approved",
        expires_at=datetime.now(UTC) + timedelta(days=max(1, min(command.days, 30))),
    )
    SecurityControlMemoryStore.exceptions[f"{command.tenant_id}:{ref}"] = exc
    federation_trust_metrics.increment("security_exception_approved_total")
    return exc.to_dict()


async def handle_revoke_exception(command: RevokeExceptionCommand) -> dict:
    key = f"{command.tenant_id}:{command.exception_ref}"
    exc = SecurityControlMemoryStore.exceptions.get(key)
    if exc is None:
        raise ValueError("security.exception_not_found")
    exc.revoke(reason=command.reason)
    SecurityControlMemoryStore.exceptions[key] = exc
    federation_trust_metrics.increment("security_exception_revoked_total")
    return exc.to_dict()
