"""Analytics P213-M BI AI native foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/417-enterprise-business-intelligence-ai.md",
    "docs/architecture/ENTERPRISE_BUSINESS_INTELLIGENCE_AI.md",
    "docs/architecture/business_intelligence/BI_AI_CAPABILITIES.v1.yaml",
    "docs/architecture/business_intelligence/BI_AI_DDD_CQRS.v1.yaml",
    "docs/architecture/business_intelligence/BI_AI_SECURITY.v1.yaml",
    "docs/architecture/business_intelligence/BI_AI_VALIDATION.v1.yaml",
    "backend/contexts/analytics/domain/services/bi_platform_ai.py",
    "backend/contexts/analytics/domain/aggregates/bi_ai_aggregates.py",
    "backend/contexts/analytics/infrastructure/acl/bi_ai_acl.py",
    "backend/contexts/analytics/application/bi_ai_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/business_intelligence",
    "backend/contexts/decision_intelligence",
    "backend/contexts/reporting_platform",
    "backend/contexts/metric_governance_platform",
    "backend/contexts/visualization_platform",
    "backend/contexts/bi_core",
)


def validate_bi_ai_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.analytics.domain.aggregates.bi_ai_aggregates import (
        BiAgentPlatformRoot,
        BiAiGovernanceRoot,
        BiAiProfileRoot,
        BiAutonomousDecisionRoot,
        BiExecutiveCopilotRoot,
        BiMultiAgentCollaborationRoot,
    )
    from contexts.analytics.domain.services import bi_platform_ai as catmod

    cat = catmod.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P213-M"
        and cat.get("adr") == 417
        and cat.get("sor") == "analytics"
        and cat.get("capability") == "CAP-PLT-BI-001"
        and cat.get("principle") == catmod.PRINCIPLE
        and cat.get("fabric") == catmod.FABRIC
        and "AI reasoning" in cat["principle"]
        and cat["ai_native_analytics_platform_present_required"] is True
        and cat["autonomous_decision_intelligence_present_required"] is True
        and cat["enterprise_ai_agent_platform_present_required"] is True
        and cat["multi_agent_collaboration_present_required"] is True
        and cat["executive_ai_copilot_present_required"] is True
        and cat["ai_governance_platform_present_required"] is True
        and cat["knowledge_graph_integration_present_required"] is True
        and cat["digital_twin_integration_present_required"] is True
        and cat["cqrs_architecture_present_required"] is True
        and cat["event_sourcing_architecture_present_required"] is True
        and cat["microservice_architecture_present_required"] is True
        and cat["api_first_architecture_present_required"] is True
        and cat["zero_trust_security_present_required"] is True
        and cat["cloud_native_deployment_present_required"] is True
        and cat["architecture_present_required"] is True
        and cat["sibling_business_intelligence_bc_forbidden"] is True
        and cat["via_enterprise_ai_only"] is True
        and cat["domain_model"]["supporting_count"] >= 8
        and cat["bounded_contexts"]["context_count"] >= 6
        and cat["agents"]["agent_count"] >= 16
        and cat["autonomy"]["level_count"] >= 5
        and cat["reasoning"]["mode_count"] >= 11
        and cat["agents"]["via_enterprise_ai"] is True
        and cat["agents"]["module_local_llm_sdk_forbidden"] is True
        and cat["knowledge_graph"]["via_p212_j"] is True
        and cat["knowledge_graph"]["via_p213_l"] is True
        and cat["digital_twin"]["via_p212_l"] is True
        and cat["predictive_integration"]["via_p213_j"] is True
        and cat["prescriptive_integration"]["via_p213_k"] is True
        and cat["cqrs"]["command_count"] >= 6
        and cat["cqrs"]["query_count"] >= 5
        and cat["events"]["core_event_count"] >= 9
        and cat["microservices"]["service_count"] >= 10
        and cat["deployment"]["cloud_native"] is True
        and cat["cursor_outputs"]["count"] >= 20
        and "ai_native_decision_architecture_is_incomplete"
        in cat["quality_gates"]["reject_if"]
        and "executive_ai_copilot_is_missing"
        in cat["quality_gates"]["reject_if"]
        and "P213-L" in cat["builds_on"]
        and "P212-J" in cat["builds_on"]
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
            BiAiProfileRoot.publish,
            tenant_id="t1",
            profile_ref="r1",
            complete=False,
        )
        and BiAiProfileRoot.publish(
            tenant_id="t1", profile_ref="r2"
        ).is_incomplete()
        is False
    )
    checks.append(
        not _bad(
            BiAutonomousDecisionRoot.enable,
            tenant_id="t1",
            decision_ref="d1",
            present=False,
        )
        and BiAutonomousDecisionRoot.enable(
            tenant_id="t1", decision_ref="d2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            BiAgentPlatformRoot.enable,
            tenant_id="t1",
            agent_ref="a1",
            present=False,
        )
        and BiAgentPlatformRoot.enable(
            tenant_id="t1", agent_ref="a2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            BiExecutiveCopilotRoot.enable,
            tenant_id="t1",
            copilot_ref="c1",
            present=False,
        )
        and BiExecutiveCopilotRoot.enable(
            tenant_id="t1", copilot_ref="c2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            BiAiGovernanceRoot.enable,
            tenant_id="t1",
            gov_ref="g1",
            present=False,
        )
        and BiAiGovernanceRoot.enable(
            tenant_id="t1", gov_ref="g2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            BiMultiAgentCollaborationRoot.enable,
            tenant_id="t1",
            collab_ref="m1",
            present=False,
        )
        and BiMultiAgentCollaborationRoot.enable(
            tenant_id="t1", collab_ref="m2"
        ).is_missing()
        is False
    )
    aggregates_ok = all(checks)

    acl_path = (
        root / "backend/contexts/analytics/infrastructure/acl/bi_ai_acl.py"
    )
    acl_text = acl_path.read_text(encoding="utf-8") if acl_path.exists() else ""
    acl_ok = (
        acl_path.exists()
        and "via_p207" in acl_text
        and "via_p208" in acl_text
        and "via_p209" in acl_text
        and "via_p210" in acl_text
        and "via_p211" in acl_text
        and "via_p212" in acl_text
        and "via_p212_j" in acl_text
        and "via_p212_l" in acl_text
        and "via_p213_g" in acl_text
        and "via_p213_j" in acl_text
        and "via_p213_k" in acl_text
        and "via_p213_l" in acl_text
        and "via_enterprise_ai" in acl_text
        and "module_local_llm_sdk_forbidden" in acl_text
        and "agent_identity" in acl_text
    )

    router = (
        root / "backend/contexts/analytics/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '@router.get("/ai")' in router
        and "/ai/readiness" in router
        and "/ai/vision" in router
        and "/ai/agents" in router
        and "/ai/copilot" in router
        and "/ai/governance" in router
        and "/ai/autonomy" in router
        and "/ai/multi-agent" in router
    )

    law = (
        root / "docs/architecture/ENTERPRISE_BUSINESS_INTELLIGENCE_AI.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never AI native analytics platform is missing" in law
        and "Never Autonomous decision intelligence is missing" in law
        and "Never Enterprise AI agent platform is missing" in law
        and "Never Multi-agent collaboration is missing" in law
        and "Never Executive AI copilot is missing" in law
        and "Never AI governance platform is missing" in law
        and "Never Knowledge graph integration is missing" in law
        and "Never Digital twin integration is missing" in law
        and "Never CQRS architecture is missing" in law
        and "Never Event sourcing architecture is missing" in law
        and "Never Microservice architecture is missing" in law
        and "Never API first architecture is missing" in law
        and "Never Zero trust security is missing" in law
        and "Never Cloud native deployment is missing" in law
        and "Never AI-native decision architecture is incomplete" in law
        and "Never Sibling business intelligence BC" in law
        and "MEOS Autonomous Decision Intelligence Fabric" in law
        and "AI reasoning" in law
        and "Module-local LLM SDKs" in law
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
        "prompt": "P213-M",
        "adr": 417,
        "passed": passed,
        "missing_artifacts": missing,
        "forbidden_sibling_present": sibling,
        "catalog": catalog_ok,
        "aggregates": aggregates_ok,
        "acl": acl_ok,
        "router": router_ok,
        "documentation": doc_ok,
        "sor": "analytics",
        "capability": "CAP-PLT-BI-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
