"""AI P214-F Agent & Autonomous Intelligence foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/426-enterprise-ai-agents.md",
    "docs/architecture/ENTERPRISE_AI_AGENTS.md",
    "docs/architecture/enterprise_ai/AI_AGENTS_CAPABILITIES.v1.yaml",
    "docs/architecture/enterprise_ai/AI_AGENTS_DDD_CQRS.v1.yaml",
    "docs/architecture/enterprise_ai/AI_AGENTS_SECURITY.v1.yaml",
    "docs/architecture/enterprise_ai/AI_AGENTS_VALIDATION.v1.yaml",
    "backend/contexts/ai/domain/services/ai_platform_agents.py",
    "backend/contexts/ai/domain/aggregates/ai_agents_aggregates.py",
    "backend/contexts/ai/infrastructure/acl/ai_agents_acl.py",
    "backend/contexts/ai/application/ai_agents_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/ml_platform",
    "backend/contexts/generative_ai",
    "backend/contexts/llm_platform",
    "backend/contexts/ai_core",
    "backend/contexts/vector_intelligence",
    "backend/contexts/ai_agent_platform",
    "backend/contexts/agent_platform",
    "backend/contexts/autonomous_intelligence",
    "backend/contexts/multi_agent_platform",
    "backend/contexts/agent_runtime",
    "backend/contexts/model_lifecycle_platform",
)


def validate_ai_agents_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.ai.domain.aggregates.ai_agents_aggregates import (
        AgentIdentityRoot,
        AgentMemoryRoot,
        AgentPlatformRoot,
        AgentReasoningRoot,
        AgentToolRoot,
        MultiAgentRoot,
    )
    from contexts.ai.domain.services import ai_platform_agents as catmod

    cat = catmod.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P214-F"
        and cat.get("adr") == 426
        and cat.get("sor") == "ai"
        and cat.get("capability") == "CAP-PLT-AI-001"
        and cat.get("principle") == catmod.PRINCIPLE
        and cat.get("fabric") == catmod.FABRIC
        and "digital workers" in cat["principle"]
        and cat["domain_model"]["core_domain"] == catmod.CORE_DOMAIN
        and cat["domain_model"]["supporting_count"] >= 9
        and cat["bounded_contexts"]["context_count"] >= 8
        and cat["lifecycle"]["stage_count"] >= 10
        and cat["enterprise_ai_agent_platform_present_required"] is True
        and cat["autonomous_intelligence_platform_present_required"] is True
        and cat["agent_identity_present_required"] is True
        and cat["agent_memory_present_required"] is True
        and cat["agent_reasoning_present_required"] is True
        and cat["agent_tool_ecosystem_present_required"] is True
        and cat["multi_agent_architecture_present_required"] is True
        and cat["workflow_automation_present_required"] is True
        and cat["agent_governance_present_required"] is True
        and cat["agent_security_present_required"] is True
        and cat["agent_digital_twin_present_required"] is True
        and cat["cqrs_architecture_present_required"] is True
        and cat["event_architecture_present_required"] is True
        and cat["microservices_architecture_present_required"] is True
        and cat["api_first_architecture_present_required"] is True
        and cat["cloud_native_deployment_present_required"] is True
        and cat["sibling_ai_bc_forbidden"] is True
        and cat["identity"]["via_p207"] is True
        and cat["identity"]["via_p208"] is True
        and cat["identity"]["via_p209"] is True
        and cat["memory"]["via_p213_l"] is True
        and cat["memory"]["via_p214_e"] is True
        and cat["knowledge"]["via_p212"] is True
        and cat["deployment"]["via_p213_o"] is True
        and cat["cqrs"]["command_count"] >= 6
        and cat["events"]["core_event_count"] >= 8
        and cat["microservices"]["service_count"] >= 10
        and cat["cursor_outputs"]["count"] >= 20
        and "enterprise_ai_agent_platform_is_missing"
        in cat["quality_gates"]["reject_if"]
        and "P214-E" in cat["builds_on"]
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )

    def _bad(fn, **kwargs):
        try:
            fn(**kwargs)
            return True
        except ValueError:
            return False

    checks = [
        not _bad(
            AgentPlatformRoot.enable,
            tenant_id="t1",
            platform_ref="p1",
            present=False,
        )
        and AgentPlatformRoot.enable(
            tenant_id="t1", platform_ref="p2"
        ).is_missing()
        is False,
        not _bad(
            AgentIdentityRoot.enable,
            tenant_id="t1",
            identity_ref="i1",
            present=False,
        )
        and AgentIdentityRoot.enable(
            tenant_id="t1", identity_ref="i2"
        ).is_missing()
        is False,
        not _bad(
            AgentMemoryRoot.enable,
            tenant_id="t1",
            memory_ref="m1",
            present=False,
        )
        and AgentMemoryRoot.enable(
            tenant_id="t1", memory_ref="m2"
        ).is_missing()
        is False,
        not _bad(
            AgentReasoningRoot.enable,
            tenant_id="t1",
            reasoning_ref="r1",
            present=False,
        )
        and AgentReasoningRoot.enable(
            tenant_id="t1", reasoning_ref="r2"
        ).is_missing()
        is False,
        not _bad(
            AgentToolRoot.enable,
            tenant_id="t1",
            tool_ref="t1",
            present=False,
        )
        and AgentToolRoot.enable(
            tenant_id="t1", tool_ref="t2"
        ).is_missing()
        is False,
        not _bad(
            MultiAgentRoot.enable,
            tenant_id="t1",
            collab_ref="c1",
            present=False,
        )
        and MultiAgentRoot.enable(
            tenant_id="t1", collab_ref="c2"
        ).is_missing()
        is False,
    ]
    aggregates_ok = all(checks)

    acl_path = root / "backend/contexts/ai/infrastructure/acl/ai_agents_acl.py"
    acl_text = acl_path.read_text(encoding="utf-8") if acl_path.exists() else ""
    acl_ok = (
        acl_path.exists()
        and "via_p207" in acl_text
        and "via_p208" in acl_text
        and "via_p209" in acl_text
        and "via_p210" in acl_text
        and "via_p211" in acl_text
        and "via_p212" in acl_text
        and "via_p213_l" in acl_text
        and "via_p213_o" in acl_text
        and "via_p214_a" in acl_text
        and "via_p214_c" in acl_text
        and "via_p214_d" in acl_text
        and "via_p214_e" in acl_text
        and "via_workflow_engine" in acl_text
        and "module_local_agent_runtime_forbidden" in acl_text
    )

    router = (
        root / "backend/contexts/ai/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '@router.get("/agents")' in router
        and "/agents/readiness" in router
        and "/agents/lifecycle" in router
        and "/agents/identity" in router
        and "/agents/memory" in router
        and "/agents/reasoning" in router
        and "/agents/multi-agent" in router
        and "/agents/digital-twin" in router
    )

    law = (root / "docs/architecture/ENTERPRISE_AI_AGENTS.md").read_text(
        encoding="utf-8"
    )
    doc_ok = (
        "Never Enterprise AI Agent platform is missing" in law
        and "Never Autonomous Intelligence platform is missing" in law
        and "Never Agent identity is missing" in law
        and "Never Agent memory is missing" in law
        and "Never Agent reasoning is missing" in law
        and "Never Agent tool ecosystem is missing" in law
        and "Never Multi-agent architecture is missing" in law
        and "Never Workflow automation is missing" in law
        and "Never Agent governance is missing" in law
        and "Never Agent security is missing" in law
        and "Never CQRS architecture is missing" in law
        and "Never Event architecture is missing" in law
        and "Never Microservices architecture is missing" in law
        and "Never API first architecture is missing" in law
        and "Never Cloud native deployment is missing" in law
        and "Never Sibling AI BC" in law
        and "MEOS Autonomous Intelligence Fabric" in law
        and "digital workers" in law
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
        "prompt": "P214-F",
        "adr": 426,
        "passed": passed,
        "missing_artifacts": missing,
        "forbidden_sibling_present": sibling,
        "catalog": catalog_ok,
        "aggregates": aggregates_ok,
        "acl": acl_ok,
        "router": router_ok,
        "documentation": doc_ok,
        "sor": "ai",
        "capability": "CAP-PLT-AI-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
