"""Identity Intelligence P207-H Behavioral Analytics foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]

REQUIRED_ARTIFACTS = [
    "docs/adr/323-enterprise-identity-intelligence-behavioral-analytics.md",
    "docs/architecture/ENTERPRISE_IDENTITY_INTELLIGENCE_BEHAVIORAL_ANALYTICS.md",
    "docs/architecture/identity/intelligence/II_BEHAVIOR_CAPABILITIES.v1.yaml",
    "docs/architecture/identity/intelligence/II_BEHAVIOR_DDD_CQRS.v1.yaml",
    "docs/architecture/identity/intelligence/II_BEHAVIOR_SECURITY.v1.yaml",
    "docs/architecture/identity/intelligence/II_BEHAVIOR_VALIDATION.v1.yaml",
    "backend/contexts/identity_intelligence/domain/services/ii_platform_behavior.py",
    "backend/contexts/identity_intelligence/domain/aggregates/ii_behavior_aggregates.py",
    "backend/contexts/identity_intelligence/infrastructure/acl/ii_behavior_acl.py",
    "backend/contexts/identity_intelligence/domain/services/ii_behavior_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/identity_behavior_platform",
    "backend/contexts/ueba_platform",
    "backend/contexts/behavior_analytics_bc",
)


def validate_ii_behavior_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.identity_intelligence.domain.aggregates.ii_behavior_aggregates import (
        AnomalyDetectionCaseRoot,
        BehaviorBaselineRoot,
        BehaviorPrivacyPolicyRoot,
        BehaviorRiskSignalRoot,
        BehaviorTrustSignalRoot,
        IdentityBehaviorProfileRoot,
        UebaEntityProfileRoot,
    )
    from contexts.identity_intelligence.domain.services import (
        ii_platform_behavior as behavior,
    )
    from contexts.identity_intelligence.infrastructure.acl import (
        ii_behavior_acl as acls,
    )

    cat = behavior.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P207-H"
        and cat.get("adr") == 323
        and cat.get("sor") == "identity_intelligence"
        and cat["not_rule_only"] is True
        and cat["learning_required"] is True
        and cat["privacy_required"] is True
        and cat["risk_integration_required"] is True
        and cat["capabilities"]["not_rule_only_analysis"] is True
        and cat["capabilities"]["not_learning_absent"] is True
        and cat["capabilities"]["not_unexplained_anomaly"] is True
        and cat["capabilities"]["not_privacy_missing"] is True
        and cat["capabilities"]["not_ai_ungoverned"] is True
        and cat["capabilities"]["not_risk_integration_absent"] is True
        and cat["baseline"]["not_absent"] is True
        and cat["anomaly_detection"]["not_unexplained"] is True
        and cat["behavioral_risk"]["not_absent"] is True
        and cat["security_privacy"]["not_privacy_missing"] is True
        and cat["ddd"]["aggregate_count"] >= 7
        and cat["cqrs"]["event_count"] >= 6
        and cat["integrations"]["behavior_integration_complete"] is True
        and "behavioral_analysis_rule_only" in cat["quality_gates"]["reject_if"]
        and "learning_capability_absent" in cat["quality_gates"]["reject_if"]
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )

    try:
        IdentityBehaviorProfileRoot.create(
            tenant_id="t1",
            profile_ref="bp1",
            subject_ref="u1",
            rule_only=True,
        )
        rule_only = True
    except ValueError:
        rule_only = False

    try:
        IdentityBehaviorProfileRoot.create(
            tenant_id="t1",
            profile_ref="bp2",
            subject_ref="u1",
            learning_enabled=False,
        )
        no_learn = True
    except ValueError:
        no_learn = False

    profile = IdentityBehaviorProfileRoot.create(
        tenant_id="t1", profile_ref="bp3", subject_ref="u1"
    )
    profile.analyze()
    profile_ok = (
        not rule_only
        and not no_learn
        and profile.is_rule_only() is False
        and profile.is_learning_absent() is False
        and "BehaviorProfileCreated" in profile.pending_events
        and "BehaviorAnalyzed" in profile.pending_events
    )

    baseline = BehaviorBaselineRoot.learn(
        tenant_id="t1", baseline_ref="bl1", subject_ref="u1"
    )
    baseline_ok = "BaselineLearned" in baseline.pending_events

    try:
        AnomalyDetectionCaseRoot.detect(
            tenant_id="t1",
            case_ref="a1",
            subject_ref="u1",
            anomaly_type="impossible_travel",
            explanation="",
        )
        no_exp = True
    except ValueError:
        no_exp = False

    try:
        AnomalyDetectionCaseRoot.detect(
            tenant_id="t1",
            case_ref="a2",
            subject_ref="u1",
            anomaly_type="impossible_travel",
            explanation="Travel between NYC and Tokyo in 1h",
            high_impact=True,
            hitl_approved=False,
        )
        no_hitl = True
    except ValueError:
        no_hitl = False

    anomaly = AnomalyDetectionCaseRoot.detect(
        tenant_id="t1",
        case_ref="a3",
        subject_ref="u1",
        anomaly_type="impossible_travel",
        explanation="Travel between NYC and Tokyo in 1h",
        high_impact=True,
        hitl_approved=True,
    )
    anomaly.start_investigation()
    anomaly_ok = (
        not no_exp
        and not no_hitl
        and anomaly.is_unexplained() is False
        and "AnomalyDetected" in anomaly.pending_events
        and "InvestigationStarted" in anomaly.pending_events
    )

    ueba = UebaEntityProfileRoot.profile(
        tenant_id="t1", entity_ref="svc1", entity_kind="service_account"
    )
    ueba_ok = ueba.learning_enabled is True

    try:
        BehaviorRiskSignalRoot.emit(
            tenant_id="t1",
            signal_ref="rs1",
            subject_ref="u1",
            explanation="deviation",
            via_p207g=False,
        )
        no_risk = True
    except ValueError:
        no_risk = False

    risk_sig = BehaviorRiskSignalRoot.emit(
        tenant_id="t1",
        signal_ref="rs2",
        subject_ref="u1",
        explanation="High deviation from role baseline with sensitive access",
    )
    risk_ok = (
        not no_risk
        and risk_sig.is_risk_integration_absent() is False
        and "RiskUpdated" in risk_sig.pending_events
    )

    trust = BehaviorTrustSignalRoot.update(
        tenant_id="t1", trust_ref="tr1", subject_ref="u1", score=0.55
    )
    trust_ok = "TrustChanged" in trust.pending_events

    try:
        BehaviorPrivacyPolicyRoot.define(
            tenant_id="t1",
            policy_ref="pr1",
            privacy_controls=False,
        )
        no_priv = True
    except ValueError:
        no_priv = False

    try:
        BehaviorPrivacyPolicyRoot.define(
            tenant_id="t1",
            policy_ref="pr2",
            ai_governed=False,
        )
        no_ai_gov = True
    except ValueError:
        no_ai_gov = False

    privacy = BehaviorPrivacyPolicyRoot.define(tenant_id="t1", policy_ref="pr3")
    privacy_ok = (
        not no_priv
        and not no_ai_gov
        and privacy.is_privacy_missing() is False
        and privacy.is_ai_ungoverned() is False
    )

    aggregates_ok = (
        profile_ok
        and baseline_ok
        and anomaly_ok
        and ueba_ok
        and risk_ok
        and trust_ok
        and privacy_ok
    )

    acl_ok = (
        acls.to_ai_infer(tenant_id="t1", surface="behavior", context={})[
            "ai_models_governed_required"
        ]
        is True
        and acls.to_risk_calculate(
            tenant_id="t1", subject_ref="u1", behavior_signal={}
        )["integration_absent_forbidden"]
        is True
        and acls.to_directory_graph(tenant_id="t1", projection_ref="g1")[
            "relationship_anomaly_detection"
        ]
        is True
        and acls.to_digital_twin(tenant_id="t1", twin_ref="tw1")["via_p207f"]
        is True
        and acls.to_authz_check(
            tenant_id="t1", subject_id="u1", action="identity_intelligence.read"
        )["bypasses_authorization_pdp_forbidden"]
        is True
        and acls.to_audit(
            tenant_id="t1", action="ii.behavior.detect", resource_ref="a3"
        )["privacy_access_logged"]
        is True
        and acls.to_agent_task(
            tenant_id="t1",
            agent_kind="behavior_analyst_agent",
            subject_ref="u1",
        )["via_p207e"]
        is True
        and acls.to_ai_governance(tenant_id="t1", model_ref="m1")[
            "ungoverned_forbidden"
        ]
        is True
    )

    router = (
        root
        / "backend/contexts/identity_intelligence/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '@identity_intelligence_router.get("/behavior"' in router
        and "/behavior/profile" in router
        and "/behavior/baseline" in router
        and "/behavior/anomaly" in router
        and "/behavior/ueba" in router
        and "/behavior/risk" in router
        and "/behavior/security" in router
        and "/behavior/readiness" in router
    )

    law = (
        root
        / "docs/architecture/ENTERPRISE_IDENTITY_INTELLIGENCE_BEHAVIORAL_ANALYTICS.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never behavioral analysis rule-only" in law
        and "Never absent learning capability" in law
        and "Never unavailable anomaly explanations" in law
        and "Never missing privacy controls" in law
        and "Never ungoverned AI models" in law
        and "Never absent risk intelligence integration" in law
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
        "prompt": "P207-H",
        "adr": 323,
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
