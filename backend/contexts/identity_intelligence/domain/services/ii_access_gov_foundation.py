"""Identity Intelligence P207-J Access Governance foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]

REQUIRED_ARTIFACTS = [
    "docs/adr/325-enterprise-identity-intelligence-access-gov-optimization.md",
    "docs/architecture/ENTERPRISE_IDENTITY_INTELLIGENCE_ACCESS_GOV_OPTIMIZATION.md",
    "docs/architecture/identity/intelligence/II_ACCESS_GOV_CAPABILITIES.v1.yaml",
    "docs/architecture/identity/intelligence/II_ACCESS_GOV_DDD_CQRS.v1.yaml",
    "docs/architecture/identity/intelligence/II_ACCESS_GOV_SECURITY.v1.yaml",
    "docs/architecture/identity/intelligence/II_ACCESS_GOV_VALIDATION.v1.yaml",
    "backend/contexts/identity_intelligence/domain/services/ii_platform_access_gov.py",
    "backend/contexts/identity_intelligence/domain/aggregates/ii_access_gov_aggregates.py",
    "backend/contexts/identity_intelligence/infrastructure/acl/ii_access_gov_acl.py",
    "backend/contexts/identity_intelligence/domain/services/ii_access_gov_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/ai_governance_access",
    "backend/contexts/access_optimization_platform",
    "backend/contexts/identity_gov_intelligence_bc",
)


def validate_ii_access_gov_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.identity_intelligence.domain.aggregates.ii_access_gov_aggregates import (
        AccessGovernanceCaseRoot,
        AccessOptimizationRecommendationRoot,
        CertificationInsightRoot,
        EntitlementIntelligenceRecordRoot,
        GovernanceComplianceEvidenceRoot,
        PolicyIntelligenceFindingRoot,
        RoleOptimizationProposalRoot,
    )
    from contexts.identity_intelligence.domain.services import (
        ii_platform_access_gov as access_gov,
    )
    from contexts.identity_intelligence.infrastructure.acl import (
        ii_access_gov_acl as acls,
    )

    cat = access_gov.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P207-J"
        and cat.get("adr") == 325
        and cat.get("sor") == "identity_intelligence"
        and cat["not_periodic_only"] is True
        and cat["continuous_governance"] is True
        and cat["capabilities"]["not_periodic"] is True
        and cat["capabilities"]["not_unexplained"] is True
        and cat["capabilities"]["not_business_blind"] is True
        and cat["capabilities"]["not_human_absent"] is True
        and cat["capabilities"]["not_evidence_unavailable"] is True
        and cat["capabilities"]["not_risk_disconnected"] is True
        and cat["certification"]["not_periodic_only"] is True
        and cat["optimization"]["not_business_blind"] is True
        and cat["risk_integration"]["not_disconnected"] is True
        and cat["security_compliance"]["not_evidence_unavailable"] is True
        and cat["ddd"]["aggregate_count"] >= 7
        and cat["cqrs"]["event_count"] >= 6
        and cat["integrations"]["access_gov_integration_complete"] is True
        and "governance_periodic_only" in cat["quality_gates"]["reject_if"]
        and "risk_intelligence_disconnected" in cat["quality_gates"]["reject_if"]
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )

    try:
        AccessGovernanceCaseRoot.analyze(
            tenant_id="t1",
            case_ref="c1",
            subject_ref="u1",
            periodic_only=True,
            business_context="Finance approver",
        )
        periodic = True
    except ValueError:
        periodic = False

    try:
        AccessGovernanceCaseRoot.analyze(
            tenant_id="t1",
            case_ref="c2",
            subject_ref="u1",
            business_context="",
        )
        no_biz = True
    except ValueError:
        no_biz = False

    case = AccessGovernanceCaseRoot.analyze(
        tenant_id="t1",
        case_ref="c3",
        subject_ref="u1",
        business_context="Finance approver for AP workflows",
    )
    case_ok = (
        not periodic
        and not no_biz
        and case.is_periodic_only() is False
        and "AccessAnalyzed" in case.pending_events
    )

    ent = EntitlementIntelligenceRecordRoot.discover(
        tenant_id="t1", record_ref="e1", subject_ref="u1"
    )
    ent_ok = "RiskDetected" in ent.pending_events

    try:
        AccessOptimizationRecommendationRoot.recommend(
            tenant_id="t1",
            recommendation_ref="r1",
            subject_ref="u1",
            explanation="",
            business_context="Finance",
        )
        no_exp = True
    except ValueError:
        no_exp = False

    try:
        AccessOptimizationRecommendationRoot.recommend(
            tenant_id="t1",
            recommendation_ref="r2",
            subject_ref="u1",
            explanation="Remove unused SAP role",
            business_context="Finance",
            via_p207g=False,
        )
        no_risk = True
    except ValueError:
        no_risk = False

    try:
        AccessOptimizationRecommendationRoot.recommend(
            tenant_id="t1",
            recommendation_ref="r3",
            subject_ref="u1",
            explanation="Remove unused SAP role",
            business_context="Finance",
            human_governance=False,
        )
        no_human = True
    except ValueError:
        no_human = False

    try:
        AccessOptimizationRecommendationRoot.recommend(
            tenant_id="t1",
            recommendation_ref="r4",
            subject_ref="u1",
            explanation="Revoke admin",
            business_context="Finance",
            high_impact=True,
            hitl_approved=False,
        )
        no_hitl = True
    except ValueError:
        no_hitl = False

    rec = AccessOptimizationRecommendationRoot.recommend(
        tenant_id="t1",
        recommendation_ref="r5",
        subject_ref="u1",
        explanation="Remove unused SAP role not used in 90 days",
        business_context="Finance AP approver",
        high_impact=True,
        hitl_approved=True,
    )
    rec.execute()
    rec_ok = (
        not no_exp
        and not no_risk
        and not no_human
        and not no_hitl
        and rec.is_unexplained() is False
        and rec.is_risk_disconnected() is False
        and "OptimizationRecommended" in rec.pending_events
        and "AccessOptimized" in rec.pending_events
    )

    insight = CertificationInsightRoot.generate(
        tenant_id="t1",
        insight_ref="i1",
        subject_ref="u1",
        explanation="Unused entitlement with low business need",
    )
    insight_ok = insight.continuous is True

    try:
        RoleOptimizationProposalRoot.propose(
            tenant_id="t1",
            proposal_ref="p1",
            role_ref="role1",
            duplicates_iga_sor=True,
        )
        dup_iga = True
    except ValueError:
        dup_iga = False

    role = RoleOptimizationProposalRoot.propose(
        tenant_id="t1", proposal_ref="p2", role_ref="role1"
    )
    role_ok = not dup_iga and role.via_p202 is True

    policy = PolicyIntelligenceFindingRoot.evaluate(
        tenant_id="t1", finding_ref="f1", policy_key="ii.access.least_privilege"
    )
    policy_ok = policy.status == "evaluated"

    try:
        GovernanceComplianceEvidenceRoot.generate(
            tenant_id="t1",
            evidence_ref="ev1",
            case_ref="c3",
            available=False,
        )
        no_evidence = True
    except ValueError:
        no_evidence = False

    evidence = GovernanceComplianceEvidenceRoot.generate(
        tenant_id="t1", evidence_ref="ev2", case_ref="c3"
    )
    evidence_ok = (
        not no_evidence
        and evidence.is_unavailable() is False
        and "ComplianceEvidenceGenerated" in evidence.pending_events
    )

    aggregates_ok = (
        case_ok
        and ent_ok
        and rec_ok
        and insight_ok
        and role_ok
        and policy_ok
        and evidence_ok
    )

    acl_ok = (
        acls.to_ai_infer(tenant_id="t1", surface="access_gov", context={})[
            "explainable_required"
        ]
        is True
        and acls.to_risk_calculate(
            tenant_id="t1", subject_ref="u1", access_context={}
        )["disconnected_forbidden"]
        is True
        and acls.to_digital_twin(tenant_id="t1", twin_ref="tw1")["via_p207f"]
        is True
        and acls.to_directory_graph(tenant_id="t1", projection_ref="g1")[
            "toxic_access_detection"
        ]
        is True
        and acls.to_iga(tenant_id="t1", subject_ref="u1")[
            "duplicates_p202_iga_sor_forbidden"
        ]
        is True
        and acls.to_workflow_approval(tenant_id="t1", recommendation_ref="r5")[
            "human_governance_required"
        ]
        is True
        and acls.to_policy_evaluate(
            tenant_id="t1", policy_key="ii.access", context={}
        )["policy_intelligence"]
        is True
        and acls.to_audit(
            tenant_id="t1", action="ii.access_gov.optimize", resource_ref="r5"
        )["compliance_evidence_required"]
        is True
        and acls.to_authz_check(
            tenant_id="t1", subject_id="u1", action="identity_intelligence.write"
        )["bypasses_authorization_pdp_forbidden"]
        is True
        and acls.to_agent_task(
            tenant_id="t1",
            agent_kind="governance_analyst_agent",
            subject_ref="u1",
        )["via_p207e"]
        is True
    )

    router = (
        root
        / "backend/contexts/identity_intelligence/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '@identity_intelligence_router.get("/access-gov"' in router
        and "/access-gov/optimization" in router
        and "/access-gov/certification" in router
        and "/access-gov/risk" in router
        and "/access-gov/security" in router
        and "/access-gov/readiness" in router
    )

    law = (
        root
        / "docs/architecture/ENTERPRISE_IDENTITY_INTELLIGENCE_ACCESS_GOV_OPTIMIZATION.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never governance periodic only" in law
        and "Never unexplained AI recommendations" in law
        and "Never optimization ignoring business context" in law
        and "Never absent human governance" in law
        and "Never unavailable compliance evidence" in law
        and "Never disconnected risk intelligence" in law
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
        "prompt": "P207-J",
        "adr": 325,
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
