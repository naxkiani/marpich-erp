"""Identity Intelligence P207-D Autonomous Operations foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]

REQUIRED_ARTIFACTS = [
    "docs/adr/319-enterprise-identity-intelligence-autonomous-ops.md",
    "docs/architecture/ENTERPRISE_IDENTITY_INTELLIGENCE_AUTONOMOUS_OPS_RUNTIME.md",
    "docs/architecture/identity/intelligence/II_AUTO_CAPABILITIES.v1.yaml",
    "docs/architecture/identity/intelligence/II_AUTO_DDD_CQRS.v1.yaml",
    "docs/architecture/identity/intelligence/II_AUTO_SECURITY.v1.yaml",
    "docs/architecture/identity/intelligence/II_AUTO_VALIDATION.v1.yaml",
    "backend/contexts/identity_intelligence/domain/services/ii_platform_autonomous.py",
    "backend/contexts/identity_intelligence/domain/aggregates/ii_autonomous_aggregates.py",
    "backend/contexts/identity_intelligence/infrastructure/acl/ii_autonomous_acl.py",
    "backend/contexts/identity_intelligence/domain/services/ii_autonomous_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/ai_identity_ops",
    "backend/contexts/autonomous_iam",
    "backend/contexts/self_healing_iam",
    "backend/contexts/identity_automation",
)


def validate_ii_autonomous_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.identity_intelligence.domain.aggregates.ii_autonomous_aggregates import (
        ActionApprovalGateRoot,
        AutonomousDecisionCaseRoot,
        AutonomousOperationRunRoot,
        LearningFeedbackRecordRoot,
        SelfHealingRemediationRoot,
    )
    from contexts.identity_intelligence.domain.services import (
        ii_platform_autonomous as auto,
    )
    from contexts.identity_intelligence.infrastructure.acl import (
        ii_autonomous_acl as acls,
    )

    cat = auto.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P207-D"
        and cat.get("adr") == 319
        and cat.get("sor") == "identity_intelligence"
        and cat["automation_governance_required"] is True
        and cat["capabilities"]["not_ungoverned"] is True
        and cat["capabilities"]["not_non_explainable"] is True
        and cat["capabilities"]["not_absent_human_oversight"] is True
        and cat["capabilities"]["not_unauditable"] is True
        and cat["capabilities"]["not_missing_recovery"] is True
        and cat["capabilities"]["not_bypassing_security"] is True
        and cat["decision_engine"]["not_skipping_policy"] is True
        and cat["self_healing"]["not_missing"] is True
        and cat["workflows"]["local_approval_engine_forbidden"] is True
        and cat["ai_governance"]["not_non_explainable"] is True
        and cat["ai_governance"]["not_absent_oversight"] is True
        and cat["security"]["not_bypassing"] is True
        and cat["ddd"]["aggregate_count"] >= 7
        and cat["cqrs"]["event_count"] >= 6
        and cat["integrations"]["autonomous_integration_complete"] is True
        and "automation_without_governance" in cat["quality_gates"]["reject_if"]
        and "human_oversight_absent" in cat["quality_gates"]["reject_if"]
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )

    try:
        AutonomousOperationRunRoot.start(
            tenant_id="t1", run_ref="r1", governed=False
        )
        ungov = True
    except ValueError:
        ungov = False

    try:
        AutonomousOperationRunRoot.start(
            tenant_id="t1", run_ref="r2", human_oversight=False
        )
        no_human = True
    except ValueError:
        no_human = False

    try:
        AutonomousOperationRunRoot.start(
            tenant_id="t1", run_ref="r3", auditable=False
        )
        no_audit = True
    except ValueError:
        no_audit = False

    run = AutonomousOperationRunRoot.start(tenant_id="t1", run_ref="r4")
    run_ok = (
        not ungov
        and not no_human
        and not no_audit
        and run.is_ungoverned() is False
        and "IdentityOperationStarted" in run.pending_events
    )

    try:
        AutonomousDecisionCaseRoot.generate(
            tenant_id="t1",
            case_ref="d1",
            explanation="",
        )
        no_exp = True
    except ValueError:
        no_exp = False

    try:
        AutonomousDecisionCaseRoot.generate(
            tenant_id="t1",
            case_ref="d2",
            explanation="ok",
            security_bypassed=True,
        )
        bypass = True
    except ValueError:
        bypass = False

    decision = AutonomousDecisionCaseRoot.generate(
        tenant_id="t1",
        case_ref="d3",
        outcome="request_approval",
        explanation="Elevated risk requires HITL",
    )
    decision_ok = (
        not no_exp
        and not bypass
        and decision.is_non_explainable() is False
        and "DecisionGenerated" in decision.pending_events
        and "ApprovalRequested" in decision.pending_events
    )

    try:
        SelfHealingRemediationRoot.create(
            tenant_id="t1",
            remediation_ref="h1",
            recovery_present=False,
        )
        no_rec = True
    except ValueError:
        no_rec = False

    try:
        SelfHealingRemediationRoot.create(
            tenant_id="t1",
            remediation_ref="h2",
            high_impact=True,
            hitl_approved=False,
        )
        no_hitl = True
    except ValueError:
        no_hitl = False

    heal = SelfHealingRemediationRoot.create(tenant_id="t1", remediation_ref="h3")
    heal.execute()
    heal_ok = (
        not no_rec
        and not no_hitl
        and heal.is_missing_recovery() is False
        and "RemediationCompleted" in heal.pending_events
    )

    try:
        ActionApprovalGateRoot.request(
            tenant_id="t1",
            gate_ref="g1",
            action_ref="a1",
            local_engine=True,
        )
        local = True
    except ValueError:
        local = False

    gate = ActionApprovalGateRoot.request(
        tenant_id="t1", gate_ref="g2", action_ref="a1"
    )
    gate.approve()
    gate_ok = not local and gate.approved is True

    feedback = LearningFeedbackRecordRoot.record(
        tenant_id="t1", feedback_ref="f1", run_ref="r4", success=True
    )
    feedback_ok = "LearningUpdated" in feedback.pending_events

    aggregates_ok = (
        run_ok and decision_ok and heal_ok and gate_ok and feedback_ok
    )

    acl_ok = (
        acls.to_workflow_start(
            tenant_id="t1", workflow_key="ii.remediate", payload={}
        )["local_approval_engine_forbidden"]
        is True
        and acls.to_policy_evaluate(
            tenant_id="t1", policy_key="ii.auto", context={}
        )["security_bypass_forbidden"]
        is True
        and acls.to_ai_infer(tenant_id="t1", surface="decision", context={})[
            "no_hidden_decisions"
        ]
        is True
        and acls.to_authz_check(
            tenant_id="t1", subject_id="u1", action="identity_intelligence.write"
        )["action_authorization_required"]
        is True
        and acls.to_audit(tenant_id="t1", action="ii.execute", resource_ref="r1")[
            "actions_auditable_required"
        ]
        is True
        and acls.to_digital_twin(tenant_id="t1", twin_ref="tw1")[
            "impact_simulation_before_action"
        ]
        is True
        and acls.to_directory_graph(tenant_id="t1", projection_ref="g1")[
            "attack_path_and_impact"
        ]
        is True
        and acls.to_observability(
            tenant_id="t1", metric_name="automation.success", value=1.0
        )["automation_metrics"]
        is True
    )

    router = (
        root
        / "backend/contexts/identity_intelligence/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '@identity_intelligence_router.get("/autonomous"' in router
        and "/autonomous/lifecycle" in router
        and "/autonomous/decision" in router
        and "/autonomous/healing" in router
        and "/autonomous/agents" in router
        and "/autonomous/security" in router
        and "/autonomous/readiness" in router
    )

    law = (
        root
        / "docs/architecture/ENTERPRISE_IDENTITY_INTELLIGENCE_AUTONOMOUS_OPS_RUNTIME.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never automation without governance" in law
        and "Never non-explainable AI decisions" in law
        and "Never absent human oversight" in law
        and "Never unauditable actions" in law
        and "Never missing recovery mechanisms" in law
        and "Never bypass security controls" in law
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
        "prompt": "P207-D",
        "adr": 319,
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
