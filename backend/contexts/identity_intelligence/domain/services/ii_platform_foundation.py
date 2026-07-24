"""Identity Intelligence P207-A strategy foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]

REQUIRED_ARTIFACTS = [
    "docs/adr/316-enterprise-identity-intelligence-autonomous-ops.md",
    "docs/architecture/ENTERPRISE_IDENTITY_INTELLIGENCE_AUTONOMOUS_OPS.md",
    "docs/architecture/identity/intelligence/P207_MASTER_SERIES_ROADMAP.v1.yaml",
    "docs/architecture/identity/intelligence/II_CAPABILITIES.v1.yaml",
    "docs/architecture/identity/intelligence/II_DDD_CQRS.v1.yaml",
    "docs/architecture/identity/intelligence/II_SECURITY.v1.yaml",
    "docs/architecture/identity/intelligence/II_AI_AGENTS.v1.yaml",
    "docs/architecture/identity/intelligence/II_VALIDATION.v1.yaml",
    "backend/contexts/identity_intelligence/domain/services/ii_platform_strategy.py",
    "backend/contexts/identity_intelligence/domain/aggregates/ii_strategy_aggregates.py",
    "backend/contexts/identity_intelligence/infrastructure/acl/ii_platform_acl.py",
    "backend/contexts/identity_intelligence/domain/services/ii_platform_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/ai_identity_ops",
    "backend/contexts/autonomous_iam",
    "backend/contexts/identity_ueai",
    "backend/contexts/identity_ai_brain",
)


def validate_ii_strategy_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.identity_intelligence.domain.aggregates.ii_strategy_aggregates import (
        AutonomousOperationRunRoot,
        DigitalTwinOrchestrationRoot,
        IdentityAiAgentContractRoot,
        IdentityIntelligenceProfileRoot,
        IdentityRiskPredictionRoot,
        KnowledgeGraphIntegrationRoot,
    )
    from contexts.identity_intelligence.domain.services import (
        ii_platform_strategy as strat,
    )
    from contexts.identity_intelligence.infrastructure.acl import (
        ii_platform_acl as acls,
    )

    cat = strat.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P207-A"
        and cat.get("adr") == 316
        and cat.get("sor") == "identity_intelligence"
        and cat["chatbot_only_forbidden"] is True
        and cat["human_control_required"] is True
        and cat["digital_twin_required"] is True
        and cat["capabilities"]["chatbot_only_forbidden"] is True
        and cat["capabilities"]["automation_governance_required"] is True
        and cat["capabilities"]["explainable_decisions_required"] is True
        and cat["capabilities"]["digital_twin_required"] is True
        and cat["capabilities"]["identity_graph_integration_required"] is True
        and cat["capabilities"]["risk_prediction_measurable_required"] is True
        and cat["capabilities"]["human_control_required"] is True
        and cat["capabilities"]["embeds_llm_forbidden"] is True
        and cat["autonomous_operations"]["not_ungoverned"] is True
        and cat["ai_agents"]["not_chatbot_only"] is True
        and cat["digital_twin"]["not_absent"] is True
        and cat["knowledge_graph"]["not_missing"] is True
        and cat["predictive_risk"]["not_unmeasurable"] is True
        and cat["ai_security_governance"]["not_removed_human_control"] is True
        and cat["ai_security_governance"]["not_non_explainable"] is True
        and cat["scope"]["domain_count"] >= 12
        and cat["ddd"]["logical_count"] >= 12
        and cat["ddd"]["aggregate_count"] >= 8
        and cat["cqrs"]["event_count"] >= 6
        and cat["integrations"]["foundation_integration_complete"] is True
        and "ai_only_chatbot" in cat["quality_gates"]["reject_if"]
        and "human_control_removed" in cat["quality_gates"]["reject_if"]
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )

    principles_ok = (
        "never_chatbot_only" in strat.PRINCIPLES
        and "never_ungoverned_automation" in strat.PRINCIPLES
        and "never_non_explainable_decisions" in strat.PRINCIPLES
        and "never_absent_digital_twin" in strat.PRINCIPLES
        and "never_missing_graph_integration" in strat.PRINCIPLES
        and "never_remove_human_control" in strat.PRINCIPLES
        and "never_embed_llm_sdk" in strat.PRINCIPLES
        and len(strat.PRINCIPLES) >= 20
    )

    try:
        IdentityIntelligenceProfileRoot.define(
            tenant_id="t1", profile_ref="p1", chatbot_only=True
        )
        chatbot = True
    except ValueError:
        chatbot = False

    try:
        IdentityIntelligenceProfileRoot.define(
            tenant_id="t1", profile_ref="p2", explainable=False
        )
        non_exp = True
    except ValueError:
        non_exp = False

    profile = IdentityIntelligenceProfileRoot.define(
        tenant_id="t1", profile_ref="p3"
    )
    profile_ok = (
        not chatbot
        and not non_exp
        and profile.is_chatbot_only() is False
        and "InsightGenerated" in profile.pending_events
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
            tenant_id="t1", run_ref="r2", human_control=False
        )
        no_human = True
    except ValueError:
        no_human = False

    try:
        AutonomousOperationRunRoot.start(
            tenant_id="t1",
            run_ref="r3",
            high_impact=True,
            hitl_approved=False,
        )
        no_hitl = True
    except ValueError:
        no_hitl = False

    run = AutonomousOperationRunRoot.start(tenant_id="t1", run_ref="r4")
    run.execute_remediation()
    run_ok = (
        not ungov
        and not no_human
        and not no_hitl
        and "RemediationExecuted" in run.pending_events
    )

    try:
        IdentityAiAgentContractRoot.register(
            tenant_id="t1",
            agent_ref="a1",
            kind="security",
            via_ai_platform=False,
        )
        embed = True
    except ValueError:
        embed = False

    agent = IdentityAiAgentContractRoot.register(
        tenant_id="t1", agent_ref="a1", kind="security"
    )
    agent_ok = not embed and agent.via_ai_platform is True

    try:
        DigitalTwinOrchestrationRoot.bind(
            tenant_id="t1",
            orchestration_ref="o1",
            twin_ref="tw1",
            twin_present=False,
        )
        no_twin = True
    except ValueError:
        no_twin = False

    try:
        DigitalTwinOrchestrationRoot.bind(
            tenant_id="t1",
            orchestration_ref="o2",
            twin_ref="tw1",
            owns_twin_sor=True,
        )
        owns_twin = True
    except ValueError:
        owns_twin = False

    twin = DigitalTwinOrchestrationRoot.bind(
        tenant_id="t1", orchestration_ref="o3", twin_ref="tw1"
    )
    twin_ok = not no_twin and not owns_twin and twin.is_absent() is False

    try:
        IdentityRiskPredictionRoot.predict(
            tenant_id="t1",
            prediction_ref="pr1",
            subject_ref="u1",
            score=0.8,
            explanation="elevated",
            measurable=False,
        )
        unmeas = True
    except ValueError:
        unmeas = False

    risk = IdentityRiskPredictionRoot.predict(
        tenant_id="t1",
        prediction_ref="pr2",
        subject_ref="u1",
        score=0.72,
        explanation="Unusual privilege path via graph",
    )
    risk_ok = (
        not unmeas
        and risk.is_unmeasurable() is False
        and "RiskPredicted" in risk.pending_events
    )

    try:
        KnowledgeGraphIntegrationRoot.connect(
            tenant_id="t1",
            integration_ref="g1",
            graph_integrated=False,
        )
        no_graph = True
    except ValueError:
        no_graph = False

    graph = KnowledgeGraphIntegrationRoot.connect(
        tenant_id="t1", integration_ref="g1"
    )
    graph_ok = not no_graph and graph.is_missing() is False

    aggregates_ok = (
        profile_ok and run_ok and agent_ok and twin_ok and risk_ok and graph_ok
    )

    acl_ok = (
        acls.to_ai_infer(tenant_id="t1", surface="risk_prediction", context={})[
            "embeds_llm_sdk_forbidden"
        ]
        is True
        and acls.to_ai_infer(tenant_id="t1", surface="risk_prediction", context={})[
            "hitl_required"
        ]
        is True
        and acls.to_ai_infer(tenant_id="t1", surface="risk_prediction", context={})[
            "chatbot_only_forbidden"
        ]
        is True
        and acls.to_policy_evaluate(
            tenant_id="t1", policy_key="ii.remediate", context={}
        )["automation_governance_required"]
        is True
        and acls.to_authz_check(
            tenant_id="t1", subject_id="u1", action="identity_intelligence.read"
        )["local_pdp_forbidden"]
        is True
        and acls.to_digital_twin(tenant_id="t1", twin_ref="tw1")[
            "digital_twin_required"
        ]
        is True
        and acls.to_directory_graph(tenant_id="t1", projection_ref="g1")[
            "identity_graph_integration_required"
        ]
        is True
        and acls.to_audit(tenant_id="t1", action="ii.predict", resource_ref="r1")[
            "explainability_trail"
        ]
        is True
    )

    router = (
        root
        / "backend/contexts/identity_intelligence/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        'prefix="/identity-intelligence"' in router
        and '/strategy"' in router
        and "/strategy/capabilities" in router
        and "/strategy/agents" in router
        and "/strategy/twins" in router
        and "/strategy/risk" in router
        and "/strategy/readiness" in router
    )

    registry = (root / "backend/contexts/registry.py").read_text(encoding="utf-8")
    registry_ok = (
        'id="identity_intelligence"' in registry
        and "IDENTITY_INTELLIGENCE" in registry
    )

    law = (
        root
        / "docs/architecture/ENTERPRISE_IDENTITY_INTELLIGENCE_AUTONOMOUS_OPS.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never AI only a chatbot" in law
        and "Never automation without governance" in law
        and "Never non-explainable decisions" in law
        and "Never absent Digital Twin" in law
        and "Never missing identity graph integration" in law
        and "Never remove human control" in law
        and "HITL" in law
    )

    passed = (
        not missing
        and not sibling
        and catalog_ok
        and principles_ok
        and aggregates_ok
        and acl_ok
        and router_ok
        and registry_ok
        and doc_ok
    )
    return {
        "prompt": "P207-A",
        "adr": 316,
        "passed": passed,
        "missing_artifacts": missing,
        "forbidden_sibling_present": sibling,
        "catalog": catalog_ok,
        "principles": principles_ok,
        "aggregates": aggregates_ok,
        "acl": acl_ok,
        "router": router_ok,
        "registry": registry_ok,
        "documentation": doc_ok,
        "sor": "identity_intelligence",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
