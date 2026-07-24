"""Identity Intelligence P207-G Predictive Risk foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]

REQUIRED_ARTIFACTS = [
    "docs/adr/322-enterprise-identity-intelligence-predictive-risk.md",
    "docs/architecture/ENTERPRISE_IDENTITY_INTELLIGENCE_PREDICTIVE_RISK.md",
    "docs/architecture/identity/intelligence/II_RISK_CAPABILITIES.v1.yaml",
    "docs/architecture/identity/intelligence/II_RISK_DDD_CQRS.v1.yaml",
    "docs/architecture/identity/intelligence/II_RISK_SECURITY.v1.yaml",
    "docs/architecture/identity/intelligence/II_RISK_VALIDATION.v1.yaml",
    "backend/contexts/identity_intelligence/domain/services/ii_platform_risk.py",
    "backend/contexts/identity_intelligence/domain/aggregates/ii_risk_aggregates.py",
    "backend/contexts/identity_intelligence/infrastructure/acl/ii_risk_acl.py",
    "backend/contexts/identity_intelligence/domain/services/ii_risk_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/identity_risk_platform",
    "backend/contexts/predictive_iam_risk",
    "backend/contexts/risk_intelligence_bc",
)


def validate_ii_risk_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.identity_intelligence.domain.aggregates.ii_risk_aggregates import (
        BehaviorRiskFindingRoot,
        ContinuousTrustScoreRoot,
        IdentityRiskProfileRoot,
        RiskGovernancePolicyRoot,
        RiskMitigationRecommendationRoot,
        RiskPredictionCaseRoot,
        RiskSignalFusionBatchRoot,
    )
    from contexts.identity_intelligence.domain.services import (
        ii_platform_risk as risk,
    )
    from contexts.identity_intelligence.infrastructure.acl import (
        ii_risk_acl as acls,
    )

    cat = risk.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P207-G"
        and cat.get("adr") == 322
        and cat.get("sor") == "identity_intelligence"
        and cat["not_static_only"] is True
        and cat["prediction_required"] is True
        and cat["explanation_required"] is True
        and cat["trust_defined"] is True
        and cat["capabilities"]["not_static"] is True
        and cat["capabilities"]["not_prediction_absent"] is True
        and cat["capabilities"]["not_explanation_unavailable"] is True
        and cat["capabilities"]["not_unauditable_ai"] is True
        and cat["capabilities"]["not_undefined_trust"] is True
        and cat["capabilities"]["not_ungoverned_response"] is True
        and cat["prediction"]["not_absent"] is True
        and cat["trust_engine"]["not_undefined"] is True
        and cat["response_automation"]["not_ungoverned"] is True
        and cat["risk_model"]["not_explanation_unavailable"] is True
        and cat["ddd"]["aggregate_count"] >= 7
        and cat["cqrs"]["event_count"] >= 6
        and cat["integrations"]["risk_integration_complete"] is True
        and "risk_static_only" in cat["quality_gates"]["reject_if"]
        and "prediction_capability_absent" in cat["quality_gates"]["reject_if"]
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )

    try:
        IdentityRiskProfileRoot.calculate(
            tenant_id="t1",
            profile_ref="p1",
            subject_ref="u1",
            static_only=True,
            explanation="x",
        )
        static = True
    except ValueError:
        static = False

    try:
        IdentityRiskProfileRoot.calculate(
            tenant_id="t1",
            profile_ref="p2",
            subject_ref="u1",
            explanation="",
        )
        no_exp = True
    except ValueError:
        no_exp = False

    profile = IdentityRiskProfileRoot.calculate(
        tenant_id="t1",
        profile_ref="p3",
        subject_ref="u1",
        current_score=0.3,
        predicted_score=0.6,
        explanation="Elevated predicted risk from privilege + anomaly signals",
    )
    profile_ok = (
        not static
        and not no_exp
        and profile.is_static_only() is False
        and profile.is_explanation_unavailable() is False
        and "RiskCalculated" in profile.pending_events
        and "RiskIncreased" in profile.pending_events
    )

    fusion = RiskSignalFusionBatchRoot.fuse(tenant_id="t1", batch_ref="b1")
    fusion_ok = "SignalsFused" in fusion.pending_events

    try:
        RiskPredictionCaseRoot.predict(
            tenant_id="t1",
            case_ref="c1",
            subject_ref="u1",
            prediction_present=False,
            forecast="x",
        )
        no_pred = True
    except ValueError:
        no_pred = False

    try:
        RiskPredictionCaseRoot.predict(
            tenant_id="t1",
            case_ref="c2",
            subject_ref="u1",
            forecast="compromise likely",
            auditable=False,
        )
        unaudit = True
    except ValueError:
        unaudit = False

    pred = RiskPredictionCaseRoot.predict(
        tenant_id="t1",
        case_ref="c3",
        subject_ref="u1",
        forecast="Future privilege misuse within 14 days",
    )
    pred_ok = (
        not no_pred
        and not unaudit
        and pred.is_prediction_absent() is False
        and pred.is_unauditable() is False
        and "RiskPredicted" in pred.pending_events
    )

    try:
        ContinuousTrustScoreRoot.evaluate(
            tenant_id="t1",
            trust_ref="tr1",
            subject_ref="u1",
            defined=False,
        )
        undef_trust = True
    except ValueError:
        undef_trust = False

    trust = ContinuousTrustScoreRoot.evaluate(
        tenant_id="t1", trust_ref="tr2", subject_ref="u1"
    )
    trust_ok = (
        not undef_trust
        and trust.is_undefined() is False
        and "TrustUpdated" in trust.pending_events
    )

    finding = BehaviorRiskFindingRoot.analyze(
        tenant_id="t1",
        finding_ref="f1",
        subject_ref="u1",
        threat_detected=True,
    )
    finding_ok = "ThreatDetected" in finding.pending_events

    try:
        RiskMitigationRecommendationRoot.recommend(
            tenant_id="t1",
            mitigation_ref="m1",
            subject_ref="u1",
            governed=False,
        )
        ungov = True
    except ValueError:
        ungov = False

    try:
        RiskMitigationRecommendationRoot.recommend(
            tenant_id="t1",
            mitigation_ref="m2",
            subject_ref="u1",
            tier="critical",
            action="automated_protection",
            hitl_approved=False,
        )
        no_hitl = True
    except ValueError:
        no_hitl = False

    mit = RiskMitigationRecommendationRoot.recommend(
        tenant_id="t1",
        mitigation_ref="m3",
        subject_ref="u1",
        tier="high",
        action="require_approval",
        hitl_approved=True,
    )
    mit_ok = (
        not ungov
        and not no_hitl
        and mit.is_ungoverned() is False
        and "MitigationRecommended" in mit.pending_events
    )

    try:
        RiskGovernancePolicyRoot.define(
            tenant_id="t1",
            policy_ref="g1",
            trust_defined=False,
        )
        gov_bad = True
    except ValueError:
        gov_bad = False

    gov = RiskGovernancePolicyRoot.define(tenant_id="t1", policy_ref="g2")
    gov_ok = not gov_bad and gov.trust_defined is True

    aggregates_ok = (
        profile_ok
        and fusion_ok
        and pred_ok
        and trust_ok
        and finding_ok
        and mit_ok
        and gov_ok
    )

    acl_ok = (
        acls.to_ai_infer(tenant_id="t1", surface="risk", context={})[
            "ai_decisions_auditable_required"
        ]
        is True
        and acls.to_authz_check(
            tenant_id="t1", subject_id="u1", action="identity_intelligence.read"
        )["bypasses_authorization_pdp_forbidden"]
        is True
        and acls.to_directory_graph(tenant_id="t1", projection_ref="g1")[
            "attack_path_discovery"
        ]
        is True
        and acls.to_digital_twin(tenant_id="t1", twin_ref="tw1")["via_p207f"]
        is True
        and acls.to_workflow_approval(tenant_id="t1", mitigation_ref="m3")[
            "automated_response_governed"
        ]
        is True
        and acls.to_audit(tenant_id="t1", action="ii.risk.calc", resource_ref="p3")[
            "ai_decisions_auditable_required"
        ]
        is True
        and acls.to_autonomous_remediate(
            tenant_id="t1", subject_ref="u1", tier="high"
        )["ungoverned_forbidden"]
        is True
        and acls.to_agent_task(
            tenant_id="t1", agent_kind="risk_analyst_agent", subject_ref="u1"
        )["via_p207e"]
        is True
    )

    router = (
        root
        / "backend/contexts/identity_intelligence/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '@identity_intelligence_router.get("/risk"' in router
        and "/risk/model" in router
        and "/risk/prediction" in router
        and "/risk/trust" in router
        and "/risk/response" in router
        and "/risk/security" in router
        and "/risk/readiness" in router
    )

    law = (
        root
        / "docs/architecture/ENTERPRISE_IDENTITY_INTELLIGENCE_PREDICTIVE_RISK.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never risk static only" in law
        and "Never absent prediction" in law
        and "Never unavailable risk explanation" in law
        and "Never unauditable AI decisions" in law
        and "Never undefined trust calculation" in law
        and "Never automated response without governance" in law
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
        "prompt": "P207-G",
        "adr": 322,
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
