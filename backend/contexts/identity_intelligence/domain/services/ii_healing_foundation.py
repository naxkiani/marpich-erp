"""Identity Intelligence P207-I Self-Healing Fabric foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]

REQUIRED_ARTIFACTS = [
    "docs/adr/324-enterprise-identity-intelligence-self-healing-fabric.md",
    "docs/architecture/ENTERPRISE_IDENTITY_INTELLIGENCE_SELF_HEALING_FABRIC.md",
    "docs/architecture/identity/intelligence/II_HEALING_CAPABILITIES.v1.yaml",
    "docs/architecture/identity/intelligence/II_HEALING_DDD_CQRS.v1.yaml",
    "docs/architecture/identity/intelligence/II_HEALING_SECURITY.v1.yaml",
    "docs/architecture/identity/intelligence/II_HEALING_VALIDATION.v1.yaml",
    "backend/contexts/identity_intelligence/domain/services/ii_platform_healing.py",
    "backend/contexts/identity_intelligence/domain/aggregates/ii_healing_aggregates.py",
    "backend/contexts/identity_intelligence/infrastructure/acl/ii_healing_acl.py",
    "backend/contexts/identity_intelligence/domain/services/ii_healing_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/self_healing_iam",
    "backend/contexts/identity_healing_platform",
    "backend/contexts/identity_reliability_bc",
)


def validate_ii_healing_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.identity_intelligence.domain.aggregates.ii_healing_aggregates import (
        HealingLearningRecordRoot,
        HealingSecurityPolicyRoot,
        IdentityFailureIncidentRoot,
        IdentityHealthProfileRoot,
        RecoveryValidationRoot,
        RemediationRunRoot,
        RootCauseAnalysisCaseRoot,
    )
    from contexts.identity_intelligence.domain.services import (
        ii_platform_healing as healing,
    )
    from contexts.identity_intelligence.infrastructure.acl import (
        ii_healing_acl as acls,
    )

    cat = healing.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P207-I"
        and cat.get("adr") == 324
        and cat.get("sor") == "identity_intelligence"
        and cat["not_fully_manual"] is True
        and cat["remediation_governed"] is True
        and cat["rca_required"] is True
        and cat["twin_simulation_required"] is True
        and cat["capabilities"]["not_manual_only"] is True
        and cat["capabilities"]["not_ungoverned_remediation"] is True
        and cat["capabilities"]["not_rca_missing"] is True
        and cat["capabilities"]["not_unaudited"] is True
        and cat["capabilities"]["not_twin_sim_absent"] is True
        and cat["capabilities"]["not_security_validation_undefined"] is True
        and cat["root_cause_analysis"]["not_missing"] is True
        and cat["remediation"]["not_ungoverned"] is True
        and cat["digital_twin"]["not_absent"] is True
        and cat["security"]["not_undefined"] is True
        and cat["ddd"]["aggregate_count"] >= 7
        and cat["cqrs"]["event_count"] >= 6
        and cat["integrations"]["healing_integration_complete"] is True
        and "recovery_fully_manual" in cat["quality_gates"]["reject_if"]
        and "digital_twin_simulation_absent" in cat["quality_gates"]["reject_if"]
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )

    try:
        IdentityHealthProfileRoot.check(
            tenant_id="t1",
            profile_ref="h1",
            subject_ref="u1",
            fully_manual=True,
        )
        manual = True
    except ValueError:
        manual = False

    health = IdentityHealthProfileRoot.check(
        tenant_id="t1", profile_ref="h2", subject_ref="u1"
    )
    health.restore()
    health_ok = (
        not manual
        and health.is_fully_manual() is False
        and "HealthRestored" in health.pending_events
    )

    incident = IdentityFailureIncidentRoot.detect(
        tenant_id="t1",
        incident_ref="i1",
        subject_ref="u1",
        failure_kind="failed_sync",
    )
    incident_ok = "IdentityIssueDetected" in incident.pending_events

    try:
        RootCauseAnalysisCaseRoot.analyze(
            tenant_id="t1",
            case_ref="r1",
            incident_ref="i1",
            root_cause="",
        )
        no_rca = True
    except ValueError:
        no_rca = False

    rca = RootCauseAnalysisCaseRoot.analyze(
        tenant_id="t1",
        case_ref="r2",
        incident_ref="i1",
        root_cause="Directory connector timeout after schema drift",
    )
    rca_ok = (
        not no_rca
        and rca.is_rca_missing() is False
        and "RootCauseIdentified" in rca.pending_events
    )

    try:
        RemediationRunRoot.start(
            tenant_id="t1",
            run_ref="run1",
            incident_ref="i1",
            governed=False,
        )
        ungov = True
    except ValueError:
        ungov = False

    try:
        RemediationRunRoot.start(
            tenant_id="t1",
            run_ref="run2",
            incident_ref="i1",
            twin_simulated=False,
        )
        no_twin = True
    except ValueError:
        no_twin = False

    try:
        RemediationRunRoot.start(
            tenant_id="t1",
            run_ref="run3",
            incident_ref="i1",
            auditable=False,
        )
        no_audit = True
    except ValueError:
        no_audit = False

    try:
        RemediationRunRoot.start(
            tenant_id="t1",
            run_ref="run4",
            incident_ref="i1",
            level=2,
            hitl_approved=False,
        )
        no_hitl = True
    except ValueError:
        no_hitl = False

    rem = RemediationRunRoot.start(
        tenant_id="t1",
        run_ref="run5",
        incident_ref="i1",
        level=2,
        hitl_approved=True,
    )
    rem.complete()
    rem_ok = (
        not ungov
        and not no_twin
        and not no_audit
        and not no_hitl
        and rem.is_ungoverned() is False
        and rem.is_twin_sim_absent() is False
        and rem.is_unauditable() is False
        and "RecoveryStarted" in rem.pending_events
        and "RecoveryCompleted" in rem.pending_events
        and "RemediationApproved" in rem.pending_events
    )

    try:
        RecoveryValidationRoot.validate(
            tenant_id="t1",
            validation_ref="v1",
            run_ref="run5",
            security_validated=False,
        )
        no_sec = True
    except ValueError:
        no_sec = False

    val = RecoveryValidationRoot.validate(
        tenant_id="t1", validation_ref="v2", run_ref="run5"
    )
    val_ok = not no_sec and val.is_security_undefined() is False

    learning = HealingLearningRecordRoot.record(
        tenant_id="t1", record_ref="l1", incident_ref="i1"
    )
    learning_ok = "LearningUpdated" in learning.pending_events

    try:
        HealingSecurityPolicyRoot.define(
            tenant_id="t1",
            policy_ref="p1",
            security_validation_defined=False,
        )
        pol_bad = True
    except ValueError:
        pol_bad = False

    pol = HealingSecurityPolicyRoot.define(tenant_id="t1", policy_ref="p2")
    pol_ok = not pol_bad and pol.remediation_governed is True

    aggregates_ok = (
        health_ok
        and incident_ok
        and rca_ok
        and rem_ok
        and val_ok
        and learning_ok
        and pol_ok
    )

    acl_ok = (
        acls.to_digital_twin(tenant_id="t1", twin_ref="tw1")[
            "simulation_absent_forbidden"
        ]
        is True
        and acls.to_directory_graph(tenant_id="t1", projection_ref="g1")[
            "failure_propagation_analysis"
        ]
        is True
        and acls.to_ai_infer(tenant_id="t1", surface="healing", context={})[
            "rca_required"
        ]
        is True
        and acls.to_workflow_approval(tenant_id="t1", run_ref="run5")[
            "hitl_for_level_2_plus"
        ]
        is True
        and acls.to_audit(
            tenant_id="t1", action="ii.healing.remediate", resource_ref="run5"
        )["actions_auditable_required"]
        is True
        and acls.to_authz_check(
            tenant_id="t1", subject_id="u1", action="identity_intelligence.write"
        )["bypasses_authorization_pdp_forbidden"]
        is True
        and acls.to_autonomous_orchestrate(tenant_id="t1", incident_ref="i1")[
            "via_p207d"
        ]
        is True
        and acls.to_agent_task(
            tenant_id="t1",
            agent_kind="identity_recovery_agent",
            incident_ref="i1",
        )["via_p207e"]
        is True
    )

    router = (
        root
        / "backend/contexts/identity_intelligence/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '@identity_intelligence_router.get("/healing"' in router
        and "/healing/health" in router
        and "/healing/rca" in router
        and "/healing/remediation" in router
        and "/healing/twins" in router
        and "/healing/security" in router
        and "/healing/readiness" in router
    )

    law = (
        root
        / "docs/architecture/ENTERPRISE_IDENTITY_INTELLIGENCE_SELF_HEALING_FABRIC.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never recovery fully manual" in law
        and "Never remediation without governance" in law
        and "Never missing root cause analysis" in law
        and "Never unaudited actions" in law
        and "Never absent Digital Twin simulation" in law
        and "Never undefined security validation" in law
        and "HITL" in law
    )

    passed = (
        not missing
        and not sibling
        and catalog_ok
        and aggregates_ok
        and acl_ok
        and router_ok
        and doc_ok
    )
    return {
        "prompt": "P207-I",
        "adr": 324,
        "passed": passed,
        "missing_artifacts": missing,
        "forbidden_sibling_present": sibling,
        "catalog": catalog_ok,
        "aggregates": aggregates_ok,
        "acl": acl_ok,
        "router": router_ok,
        "documentation": doc_ok,
        "sor": "identity_intelligence",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
