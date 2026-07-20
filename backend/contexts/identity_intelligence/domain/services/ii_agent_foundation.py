"""Identity Intelligence P207-E AI Agent Platform foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]

REQUIRED_ARTIFACTS = [
    "docs/adr/320-enterprise-identity-intelligence-ai-agent-platform.md",
    "docs/architecture/ENTERPRISE_IDENTITY_INTELLIGENCE_AI_AGENT_PLATFORM.md",
    "docs/architecture/identity/intelligence/II_AGENT_CAPABILITIES.v1.yaml",
    "docs/architecture/identity/intelligence/II_AGENT_DDD_CQRS.v1.yaml",
    "docs/architecture/identity/intelligence/II_AGENT_SECURITY.v1.yaml",
    "docs/architecture/identity/intelligence/II_AGENT_VALIDATION.v1.yaml",
    "backend/contexts/identity_intelligence/domain/services/ii_platform_agents.py",
    "backend/contexts/identity_intelligence/domain/aggregates/ii_agent_aggregates.py",
    "backend/contexts/identity_intelligence/infrastructure/acl/ii_agent_acl.py",
    "backend/contexts/identity_intelligence/domain/services/ii_agent_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/identity_agent_platform",
    "backend/contexts/identity_copilot_platform",
    "backend/contexts/ai_identity_ops",
    "backend/contexts/identity_ueai",
)


def validate_ii_agent_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.identity_intelligence.domain.aggregates.ii_agent_aggregates import (
        AgentGovernancePolicyRoot,
        AgentRecommendationRoot,
        AgentTaskRoot,
        AgentToolGrantRoot,
        IdentityAiAgentContractRoot,
    )
    from contexts.identity_intelligence.domain.services import (
        ii_platform_agents as agents,
    )
    from contexts.identity_intelligence.infrastructure.acl import (
        ii_agent_acl as acls,
    )

    cat = agents.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P207-E"
        and cat.get("adr") == 320
        and cat.get("sor") == "identity_intelligence"
        and cat["agent_permissions_required"] is True
        and cat["capabilities"]["not_permissionless"] is True
        and cat["capabilities"]["not_non_explainable"] is True
        and cat["capabilities"]["not_uncontrolled_knowledge"] is True
        and cat["capabilities"]["not_missing_human_governance"] is True
        and cat["capabilities"]["not_unaudited"] is True
        and cat["capabilities"]["not_undefined_security"] is True
        and cat["capabilities"]["via_ai_platform"] is True
        and cat["agent_catalog"]["count"] == 6
        and cat["tools"]["not_unscoped"] is True
        and cat["rag"]["not_uncontrolled"] is True
        and cat["decision_model"]["not_non_explainable"] is True
        and cat["human_ai_collaboration"]["not_missing"] is True
        and cat["security"]["not_unaudited"] is True
        and cat["security"]["not_undefined"] is True
        and cat["ddd"]["aggregate_count"] >= 7
        and cat["cqrs"]["event_count"] >= 6
        and cat["integrations"]["agent_integration_complete"] is True
        and "agents_without_permissions" in cat["quality_gates"]["reject_if"]
        and "human_governance_missing" in cat["quality_gates"]["reject_if"]
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )

    try:
        IdentityAiAgentContractRoot.register(
            tenant_id="t1",
            agent_ref="a1",
            kind="identity_analyst",
            permission_scope=(),
        )
        no_perm = True
    except ValueError:
        no_perm = False

    try:
        IdentityAiAgentContractRoot.register(
            tenant_id="t1",
            agent_ref="a2",
            kind="identity_analyst",
            explainable=False,
        )
        no_exp = True
    except ValueError:
        no_exp = False

    try:
        IdentityAiAgentContractRoot.register(
            tenant_id="t1",
            agent_ref="a3",
            kind="identity_analyst",
            via_ai_platform=False,
        )
        embeds = True
    except ValueError:
        embeds = False

    try:
        IdentityAiAgentContractRoot.register(
            tenant_id="t1",
            agent_ref="a4",
            kind="identity_analyst",
            audited=False,
        )
        no_audit = True
    except ValueError:
        no_audit = False

    contract = IdentityAiAgentContractRoot.register(
        tenant_id="t1",
        agent_ref="a5",
        kind="identity_security",
    )
    contract_ok = (
        not no_perm
        and not no_exp
        and not embeds
        and not no_audit
        and contract.is_permissionless() is False
        and "AgentActivated" in contract.pending_events
    )

    try:
        AgentTaskRoot.create(
            tenant_id="t1",
            task_ref="t1",
            agent_ref="a5",
            subject_ref="u1",
            human_governance=False,
        )
        no_gov = True
    except ValueError:
        no_gov = False

    task = AgentTaskRoot.create(
        tenant_id="t1",
        task_ref="t2",
        agent_ref="a5",
        subject_ref="u1",
    )
    try:
        task.complete_analysis(explanation="")
        blank_exp = True
    except ValueError:
        blank_exp = False
    task.complete_analysis(explanation="Subject has elevated risk via peer graph")
    task_ok = (
        not no_gov
        and not blank_exp
        and "AnalysisCompleted" in task.pending_events
    )

    try:
        AgentToolGrantRoot.grant(
            tenant_id="t1",
            grant_ref="g1",
            agent_ref="a5",
            scoped=False,
        )
        unscoped = True
    except ValueError:
        unscoped = False

    grant = AgentToolGrantRoot.grant(
        tenant_id="t1", grant_ref="g2", agent_ref="a5"
    )
    grant_ok = not unscoped and grant.is_unscoped() is False

    try:
        AgentRecommendationRoot.create(
            tenant_id="t1",
            recommendation_ref="r1",
            agent_ref="a5",
            action="revoke",
            explanation="",
        )
        rec_no_exp = True
    except ValueError:
        rec_no_exp = False

    try:
        AgentRecommendationRoot.create(
            tenant_id="t1",
            recommendation_ref="r2",
            agent_ref="a5",
            action="revoke",
            explanation="ok",
            knowledge_controlled=False,
        )
        uncontrolled = True
    except ValueError:
        uncontrolled = False

    try:
        AgentRecommendationRoot.create(
            tenant_id="t1",
            recommendation_ref="r3",
            agent_ref="a5",
            action="revoke",
            explanation="High impact revoke",
            high_impact=True,
            hitl_approved=False,
        )
        no_hitl = True
    except ValueError:
        no_hitl = False

    rec = AgentRecommendationRoot.create(
        tenant_id="t1",
        recommendation_ref="r4",
        agent_ref="a5",
        action="review",
        explanation="Recommend access review",
        high_impact=True,
        hitl_approved=True,
    )
    rec_ok = (
        not rec_no_exp
        and not uncontrolled
        and not no_hitl
        and "RecommendationCreated" in rec.pending_events
        and "ApprovalRequested" in rec.pending_events
    )

    try:
        AgentGovernancePolicyRoot.define(
            tenant_id="t1",
            policy_ref="p1",
            security_boundaries_defined=False,
        )
        undef_sec = True
    except ValueError:
        undef_sec = False

    try:
        AgentGovernancePolicyRoot.define(
            tenant_id="t1",
            policy_ref="p2",
            human_governance=False,
        )
        missing_human = True
    except ValueError:
        missing_human = False

    gov = AgentGovernancePolicyRoot.define(tenant_id="t1", policy_ref="p3")
    gov_ok = (
        not undef_sec
        and not missing_human
        and gov.is_undefined_security() is False
    )

    aggregates_ok = (
        contract_ok and task_ok and grant_ok and rec_ok and gov_ok
    )

    acl_ok = (
        acls.to_ai_infer(tenant_id="t1", surface="agent", context={})[
            "embeds_llm_sdk_forbidden"
        ]
        is True
        and acls.to_authz_check(
            tenant_id="t1", subject_id="u1", action="identity_intelligence.ai.infer"
        )["permissionless_forbidden"]
        is True
        and acls.to_workflow_approval(
            tenant_id="t1", recommendation_ref="r4"
        )["human_governance_required"]
        is True
        and acls.to_audit(tenant_id="t1", action="ii.agent.act", resource_ref="r4")[
            "ai_actions_audited_required"
        ]
        is True
        and acls.to_search_rag(tenant_id="t1", query="risk")[
            "uncontrolled_rag_forbidden"
        ]
        is True
        and acls.to_directory_graph(tenant_id="t1", projection_ref="g1")[
            "agent_graph_tool"
        ]
        is True
        and acls.to_policy_evaluate(
            tenant_id="t1", policy_key="ii.agent", context={}
        )["agent_guardrails"]
        is True
    )

    router = (
        root
        / "backend/contexts/identity_intelligence/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '@identity_intelligence_router.get("/agents"' in router
        and "/agents/catalog" in router
        and "/agents/architecture" in router
        and "/agents/orchestration" in router
        and "/agents/tools" in router
        and "/agents/security" in router
        and "/agents/readiness" in router
    )

    law = (
        root
        / "docs/architecture/ENTERPRISE_IDENTITY_INTELLIGENCE_AI_AGENT_PLATFORM.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never agents without permissions" in law
        and "Never non-explainable decisions" in law
        and "Never uncontrolled knowledge sources" in law
        and "Never missing human governance" in law
        and "Never unaudited AI actions" in law
        and "Never undefined security boundaries" in law
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
        "prompt": "P207-E",
        "adr": 320,
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
