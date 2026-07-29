"""Cyber Security P210-J AI Ops foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/370-enterprise-cyber-security-ai-ops.md",
    "docs/architecture/ENTERPRISE_CYBER_SECURITY_AI_OPS.md",
    "docs/architecture/cyber_security/CYBER_AI_OPS_CAPABILITIES.v1.yaml",
    "docs/architecture/cyber_security/CYBER_AI_OPS_DDD_CQRS.v1.yaml",
    "docs/architecture/cyber_security/CYBER_AI_OPS_SECURITY.v1.yaml",
    "docs/architecture/cyber_security/CYBER_AI_OPS_VALIDATION.v1.yaml",
    "backend/contexts/cyber_security/domain/services/cs_platform_ai_ops.py",
    "backend/contexts/cyber_security/domain/aggregates/cs_ai_ops_aggregates.py",
    "backend/contexts/cyber_security/infrastructure/acl/cs_ai_ops_acl.py",
    "backend/contexts/cyber_security/application/cs_ai_ops_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/ai_ops",
    "backend/contexts/autonomous_soc",
    "backend/contexts/security_copilot",
    "backend/contexts/soc_platform",
    "backend/contexts/asm",
)


def validate_cs_ai_ops_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.cyber_security.domain.aggregates.cs_ai_ops_aggregates import (
        CsAiOpsAgentCollaborationRoot,
        CsAiOpsAuditedAutonomyRoot,
        CsAiOpsExplainableDecisionRoot,
        CsAiOpsGovernanceCompleteRoot,
        CsAiOpsHumanOversightRoot,
        CsAiOpsInvestigationCompletedRoot,
        CsAiOpsKnowledgeGraphConnectedRoot,
        CsAiOpsModelLifecycleRoot,
    )
    from contexts.cyber_security.domain.services import (
        cs_platform_ai_ops as ai_ops,
    )

    cat = ai_ops.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P210-J"
        and cat.get("adr") == 370
        and cat.get("sor") == "cyber_security"
        and cat["ai_decisions_explainable_required"] is True
        and cat["human_oversight_required"] is True
        and cat["agent_collaboration_supported_required"] is True
        and cat["knowledge_graph_connected_required"] is True
        and cat["autonomous_actions_audited_required"] is True
        and cat["ai_governance_complete_required"] is True
        and cat["model_lifecycle_management_required"] is True
        and cat["module_local_llm_sdk_forbidden"] is True
        and cat["reasoning"]["not_unexplainable"] is True
        and cat["autonomous_response"]["not_without_oversight"] is True
        and cat["agents"]["not_unsupported_collaboration"] is True
        and cat["knowledge_graph"]["not_disconnected"] is True
        and cat["autonomous_response"]["not_unaudited"] is True
        and cat["ai_governance"]["not_incomplete"] is True
        and cat["model_lifecycle"]["not_missing"] is True
        and cat["architecture"]["layer_count"] >= 8
        and cat["agents"]["agent_count"] >= 15
        and cat["cqrs"]["event_count"] >= 8
        and cat["cursor_outputs"]["count"] >= 20
        and "ai_decisions_not_explainable" in cat["quality_gates"]["reject_if"]
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )

    def _bad(fn, **kwargs):
        try:
            fn(**kwargs)
            return True
        except ValueError:
            return False

    checks = []
    checks.append(
        not _bad(
            CsAiOpsExplainableDecisionRoot.decide,
            tenant_id="t1",
            decision_ref="d1",
            explainable=False,
        )
        and CsAiOpsExplainableDecisionRoot.decide(
            tenant_id="t1", decision_ref="d2"
        ).is_unexplainable()
        is False
    )
    checks.append(
        not _bad(
            CsAiOpsHumanOversightRoot.require,
            tenant_id="t1",
            gate_ref="g1",
            oversight_present=False,
        )
        and CsAiOpsHumanOversightRoot.require(
            tenant_id="t1", gate_ref="g2"
        ).is_absent()
        is False
    )
    checks.append(
        not _bad(
            CsAiOpsAgentCollaborationRoot.collaborate,
            tenant_id="t1",
            collaboration_ref="c1",
            supported=False,
        )
        and CsAiOpsAgentCollaborationRoot.collaborate(
            tenant_id="t1", collaboration_ref="c2"
        ).is_unsupported()
        is False
    )
    checks.append(
        not _bad(
            CsAiOpsKnowledgeGraphConnectedRoot.bind,
            tenant_id="t1",
            graph_ref="kg1",
            connected=False,
        )
        and CsAiOpsKnowledgeGraphConnectedRoot.bind(
            tenant_id="t1", graph_ref="kg2"
        ).is_disconnected()
        is False
    )
    checks.append(
        not _bad(
            CsAiOpsAuditedAutonomyRoot.execute,
            tenant_id="t1",
            action_ref="a1",
            audited=False,
        )
        and CsAiOpsAuditedAutonomyRoot.execute(
            tenant_id="t1", action_ref="a2"
        ).is_unaudited()
        is False
    )
    checks.append(
        not _bad(
            CsAiOpsGovernanceCompleteRoot.assert_complete,
            tenant_id="t1",
            governance_ref="gov1",
            complete=False,
        )
        and CsAiOpsGovernanceCompleteRoot.assert_complete(
            tenant_id="t1", governance_ref="gov2"
        ).is_incomplete()
        is False
    )
    checks.append(
        not _bad(
            CsAiOpsModelLifecycleRoot.manage,
            tenant_id="t1",
            model_ref="m1",
            managed=False,
        )
        and CsAiOpsModelLifecycleRoot.manage(
            tenant_id="t1", model_ref="m2"
        ).is_missing()
        is False
    )
    inv = CsAiOpsInvestigationCompletedRoot.complete(
        tenant_id="t1", investigation_ref="inv1", agent_ref="ag1"
    )
    checks.append("InvestigationCompleted" in inv.pending_events)
    aggregates_ok = all(checks)

    acl_path = (
        root / "backend/contexts/cyber_security/infrastructure/acl/cs_ai_ops_acl.py"
    )
    acl_text = acl_path.read_text(encoding="utf-8") if acl_path.exists() else ""
    acl_ok = (
        acl_path.exists()
        and "via_enterprise_ai_platform" in acl_text
        and "module_local_llm_sdk_forbidden" in acl_text
        and "human_oversight_required" in acl_text
        and "model_lifecycle_management_required" in acl_text
        and "connected_required" in acl_text
    )

    router = (
        root / "backend/contexts/cyber_security/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '/ai-ops"' in router
        and "/ai-ops/agents" in router
        and "/ai-ops/copilot" in router
        and "/ai-ops/model-lifecycle" in router
        and "/ai-ops/readiness" in router
    )

    law = (
        root / "docs/architecture/ENTERPRISE_CYBER_SECURITY_AI_OPS.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never AI decisions are not explainable" in law
        and "Never human oversight is absent" in law
        and "Never agent collaboration is unsupported" in law
        and "Never knowledge graph is disconnected" in law
        and "Never autonomous actions are unaudited" in law
        and "Never AI governance is incomplete" in law
        and "Never model lifecycle management is missing" in law
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
        "prompt": "P210-J",
        "adr": 370,
        "passed": passed,
        "missing_artifacts": missing,
        "forbidden_sibling_present": sibling,
        "catalog": catalog_ok,
        "aggregates": aggregates_ok,
        "acl": acl_ok,
        "router": router_ok,
        "documentation": doc_ok,
        "sor": "cyber_security",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
