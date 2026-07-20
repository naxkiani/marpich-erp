"""Identity Intelligence P207-M AI governance foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]

REQUIRED_ARTIFACTS = [
    "docs/adr/328-enterprise-identity-intelligence-ai-security-responsible-governance.md",
    "docs/architecture/ENTERPRISE_IDENTITY_INTELLIGENCE_AI_GOVERNANCE.md",
    "docs/architecture/identity/intelligence/II_AI_GOV_CAPABILITIES.v1.yaml",
    "docs/architecture/identity/intelligence/II_AI_GOV_DDD_CQRS.v1.yaml",
    "docs/architecture/identity/intelligence/II_AI_GOV_SECURITY.v1.yaml",
    "docs/architecture/identity/intelligence/II_AI_GOV_VALIDATION.v1.yaml",
    "backend/contexts/identity_intelligence/domain/services/ii_platform_ai_gov.py",
    "backend/contexts/identity_intelligence/domain/aggregates/ii_ai_gov_aggregates.py",
    "backend/contexts/identity_intelligence/infrastructure/acl/ii_ai_gov_acl.py",
    "backend/contexts/identity_intelligence/domain/services/ii_ai_gov_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/identity_ai_security_platform",
    "backend/contexts/responsible_ai_platform",
    "backend/contexts/identity_ai_gov_bc",
)


def validate_ii_ai_gov_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.identity_intelligence.domain.aggregates.ii_ai_gov_aggregates import (
        AIAgentGovernanceRecordRoot,
        AIAuditComplianceRecordRoot,
        AIDecisionExplanationRoot,
        AIModelAssetRoot,
        AIRiskAssessmentRoot,
        AIThreatProtectionCaseRoot,
        AutonomousActionGovernanceRoot,
    )
    from contexts.identity_intelligence.domain.services import ii_platform_ai_gov as ai_gov
    from contexts.identity_intelligence.infrastructure.acl import ii_ai_gov_acl as acls

    cat = ai_gov.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P207-M"
        and cat.get("adr") == 328
        and cat.get("sor") == "identity_intelligence"
        and cat.get("platform_ai_gov_peer") == "ai_governance"
        and cat["ai_governance_required"] is True
        and cat["explainable_required"] is True
        and cat["capabilities"]["not_ungoverned_ai"] is True
        and cat["capabilities"]["not_uncontrolled_autonomy"] is True
        and cat["capabilities"]["not_unexplainable_decisions"] is True
        and cat["capabilities"]["not_unmonitored_models"] is True
        and cat["capabilities"]["not_undefined_ai_identities"] is True
        and cat["capabilities"]["not_incomplete_audit_trails"] is True
        and cat["capabilities"]["does_not_own_platform_ai_gov_sor"] is True
        and cat["explainability"]["explainable"] is True
        and cat["autonomous_action_governance"]["not_uncontrolled"] is True
        and cat["model_governance"]["not_unmonitored"] is True
        and cat["audit_compliance"]["not_incomplete"] is True
        and cat["ddd"]["aggregate_count"] >= 7
        and cat["cqrs"]["event_count"] >= 6
        and cat["integrations"]["ai_gov_integration_complete"] is True
        and "ai_operates_without_governance" in cat["quality_gates"]["reject_if"]
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )

    try:
        AIModelAssetRoot.register(
            tenant_id="t1",
            model_ref="m1",
            owner_ref="owner1",
            purpose="risk scoring",
            governed=False,
        )
        ungov = True
    except ValueError:
        ungov = False

    try:
        AIModelAssetRoot.register(
            tenant_id="t1",
            model_ref="m2",
            owner_ref="owner1",
            purpose="risk scoring",
            monitored=False,
        )
        unmon = True
    except ValueError:
        unmon = False

    model = AIModelAssetRoot.register(
        tenant_id="t1",
        model_ref="m3",
        owner_ref="owner1",
        purpose="identity risk scoring",
    )
    model_ok = (
        not ungov
        and not unmon
        and model.is_ungoverned() is False
        and model.is_unmonitored() is False
        and "AIModelRegistered" in model.pending_events
    )

    try:
        AIAgentGovernanceRecordRoot.approve(
            tenant_id="t1",
            agent_ref="a1",
            ai_identity_ref="",
        )
        no_id = True
    except ValueError:
        no_id = False

    try:
        AIAgentGovernanceRecordRoot.approve(
            tenant_id="t1",
            agent_ref="a2",
            ai_identity_ref="ai:agent-1",
            via_workflow=False,
        )
        no_wf = True
    except ValueError:
        no_wf = False

    agent = AIAgentGovernanceRecordRoot.approve(
        tenant_id="t1",
        agent_ref="a3",
        ai_identity_ref="ai:agent-1",
    )
    agent_ok = (
        not no_id
        and not no_wf
        and agent.identity_undefined() is False
        and "AgentApproved" in agent.pending_events
    )

    try:
        AIDecisionExplanationRoot.explain(
            tenant_id="t1",
            decision_ref="d1",
            decision="Revoke access",
            reason="",
        )
        no_exp = True
    except ValueError:
        no_exp = False

    decision = AIDecisionExplanationRoot.explain(
        tenant_id="t1",
        decision_ref="d2",
        decision="Revoke unused admin role",
        reason="Role unused for 90 days with high privilege",
        evidence="Access logs and role assignment graph",
        confidence=0.92,
        impact="Reduces privilege escalation surface",
        recommendation="Remove role and notify manager",
    )
    decision_ok = (
        not no_exp
        and decision.is_unexplainable() is False
        and "DecisionExplained" in decision.pending_events
    )

    risk = AIRiskAssessmentRoot.evaluate(
        tenant_id="t1", assessment_ref="r1", subject_ref="u1"
    )
    risk_ok = "RiskDetected" in risk.pending_events

    threat = AIThreatProtectionCaseRoot.protect(
        tenant_id="t1", case_ref="t1", threat_type="prompt_injection"
    )
    threat_ok = threat.input_validated is True

    try:
        AutonomousActionGovernanceRoot.register(
            tenant_id="t1",
            action_ref="act1",
            controllable=False,
        )
        unctrl = True
    except ValueError:
        unctrl = False

    try:
        AutonomousActionGovernanceRoot.register(
            tenant_id="t1",
            action_ref="act2",
            policy_validated=False,
        )
        no_policy = True
    except ValueError:
        no_policy = False

    action = AutonomousActionGovernanceRoot.register(
        tenant_id="t1",
        action_ref="act3",
        autonomy_level="level_2_ai_executes_with_approval",
    )
    action_ok = (
        not unctrl
        and not no_policy
        and action.is_uncontrolled() is False
        and "AIActionAudited" in action.pending_events
    )

    try:
        AIAuditComplianceRecordRoot.record(
            tenant_id="t1",
            record_ref="rec1",
            audit_complete=False,
        )
        no_audit = True
    except ValueError:
        no_audit = False

    audit = AIAuditComplianceRecordRoot.record(
        tenant_id="t1", record_ref="rec2"
    )
    audit_ok = (
        not no_audit
        and audit.audit_incomplete() is False
        and "AIActionAudited" in audit.pending_events
    )

    aggregates_ok = (
        model_ok
        and agent_ok
        and decision_ok
        and risk_ok
        and threat_ok
        and action_ok
        and audit_ok
    )

    acl_ok = (
        acls.to_ai_platform_governance(
            tenant_id="t1", model_ref="m3", action="deploy"
        )["duplicates_platform_ai_governance_sor_forbidden"]
        is True
        and acls.to_ai_infer(tenant_id="t1", surface="ai_gov", context={})[
            "explainable_required"
        ]
        is True
        and acls.to_workflow_approval(
            tenant_id="t1", agent_ref="a3", action_ref="act3"
        )["via_workflow_engine"]
        is True
        and acls.to_authz_check(
            tenant_id="t1", subject_id="ai:agent-1", action="identity_intelligence.write"
        )["bypasses_authorization_pdp_forbidden"]
        is True
        and acls.to_audit(
            tenant_id="t1", action="ii.ai_gov.decision", resource_ref="d2"
        )["audit_trail_complete_required"]
        is True
        and acls.to_agent_governance(tenant_id="t1", agent_ref="a3")["via_p207e"]
        is True
        and acls.to_graph_governance(tenant_id="t1", entity_ref="g1")["via_p207k"]
        is True
        and acls.to_compliance_evidence(
            tenant_id="t1", pack_ref="p1", frameworks=["iso_27001"]
        )["evidence_collection"]
        is True
    )

    router = (
        root / "backend/contexts/identity_intelligence/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '@identity_intelligence_router.get("/ai-gov"' in router
        and "/ai-gov/responsible-ai" in router
        and "/ai-gov/explainability" in router
        and "/ai-gov/autonomous" in router
        and "/ai-gov/audit" in router
        and "/ai-gov/readiness" in router
    )

    law = (
        root / "docs/architecture/ENTERPRISE_IDENTITY_INTELLIGENCE_AI_GOVERNANCE.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never AI operates without governance" in law
        and "Never autonomous actions cannot be controlled" in law
        and "Never decisions cannot be explained" in law
        and "Never models are not monitored" in law
        and "Never AI identities are undefined" in law
        and "Never audit trails are incomplete" in law
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
        "prompt": "P207-M",
        "adr": 328,
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
