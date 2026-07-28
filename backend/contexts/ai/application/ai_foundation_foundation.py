"""AI P214-A foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/421-enterprise-ai-platform-foundation.md",
    "docs/architecture/ENTERPRISE_AI_PLATFORM_FOUNDATION.md",
    "docs/architecture/enterprise_ai/AI_FOUNDATION_CAPABILITIES.v1.yaml",
    "docs/architecture/enterprise_ai/AI_FOUNDATION_DDD_CQRS.v1.yaml",
    "docs/architecture/enterprise_ai/AI_FOUNDATION_SECURITY.v1.yaml",
    "docs/architecture/enterprise_ai/AI_FOUNDATION_VALIDATION.v1.yaml",
    "docs/architecture/enterprise_ai/P214_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/ai/domain/services/ai_platform_foundation.py",
    "backend/contexts/ai/domain/aggregates/ai_foundation_aggregates.py",
    "backend/contexts/ai/infrastructure/acl/ai_foundation_acl.py",
    "backend/contexts/ai/application/ai_foundation_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/ml_platform",
    "backend/contexts/generative_ai",
    "backend/contexts/llm_platform",
    "backend/contexts/ai_core",
    "backend/contexts/vector_intelligence",
    "backend/contexts/model_lifecycle_platform",
)


def validate_ai_foundation_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.ai.domain.aggregates.ai_foundation_aggregates import (
        AiAgentFoundationRoot,
        AiFoundationProfileRoot,
        AiGenerativePlatformRoot,
        AiGovernanceFoundationRoot,
        AiMlPlatformRoot,
        AiVectorIntelligenceRoot,
    )
    from contexts.ai.domain.services import ai_platform_foundation as catmod

    cat = catmod.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P214-A"
        and cat.get("adr") == 421
        and cat.get("sor") == "ai"
        and cat.get("capability") == "CAP-PLT-AI-001"
        and cat.get("principle") == catmod.PRINCIPLE
        and cat.get("fabric") == catmod.FABRIC
        and "intelligence foundation" in cat["principle"]
        and cat.get("core_domain")
        == "enterprise_artificial_intelligence_management"
        and cat.get("aggregate") == "EnterpriseAIAggregate"
        and cat["enterprise_ai_platform_foundation_present_required"] is True
        and cat["machine_learning_platform_present_required"] is True
        and cat["generative_ai_platform_present_required"] is True
        and cat["llm_platform_present_required"] is True
        and cat["ai_model_lifecycle_present_required"] is True
        and cat["mlops_foundation_present_required"] is True
        and cat["vector_intelligence_present_required"] is True
        and cat["ai_governance_foundation_present_required"] is True
        and cat["ai_agent_foundation_present_required"] is True
        and cat["knowledge_graph_integration_present_required"] is True
        and cat["digital_twin_integration_present_required"] is True
        and cat["cqrs_architecture_present_required"] is True
        and cat["event_architecture_present_required"] is True
        and cat["microservices_architecture_present_required"] is True
        and cat["api_first_architecture_present_required"] is True
        and cat["zero_trust_security_present_required"] is True
        and cat["cloud_native_deployment_present_required"] is True
        and cat["sibling_ai_bc_forbidden"] is True
        and cat["module_local_llm_sdk_forbidden"] is True
        and cat["domain_model"]["supporting_count"] >= 8
        and cat["bounded_contexts"]["context_count"] >= 6
        and cat["ai_paas"]["capability_count"] >= 10
        and cat["ml_platform"]["lifecycle_step_count"] >= 10
        and cat["generative_ai"]["capability_count"] >= 10
        and cat["vector_intelligence"]["present_required"] is True
        and cat["ai_agent_foundation"]["via_p213_m"] is True
        and cat["knowledge_integration"]["via_p213_l"] is True
        and cat["digital_twin_integration"]["via_p212_l"] is True
        and cat["cqrs"]["command_count"] >= 6
        and cat["events"]["core_event_count"] >= 7
        and cat["microservices"]["service_count"] >= 10
        and cat["api_first"]["via_api_gateway"] is True
        and cat["deployment"]["via_p213_o"] is True
        and cat["cursor_outputs"]["count"] >= 20
        and "enterprise_ai_platform_foundation_is_missing"
        in cat["quality_gates"]["reject_if"]
        and "sibling_ai_bc" in cat["quality_gates"]["reject_if"]
        and "P213" in cat["builds_on"]
        and "P212" in cat["builds_on"]
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
            AiFoundationProfileRoot.publish,
            tenant_id="t1",
            profile_ref="r1",
            complete=False,
        )
        and AiFoundationProfileRoot.publish(
            tenant_id="t1", profile_ref="r2"
        ).is_incomplete()
        is False
    )
    checks.append(
        not _bad(
            AiMlPlatformRoot.enable,
            tenant_id="t1",
            platform_ref="m1",
            present=False,
        )
        and AiMlPlatformRoot.enable(
            tenant_id="t1", platform_ref="m2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            AiGenerativePlatformRoot.enable,
            tenant_id="t1",
            gen_ref="g1",
            present=False,
        )
        and AiGenerativePlatformRoot.enable(
            tenant_id="t1", gen_ref="g2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            AiVectorIntelligenceRoot.enable,
            tenant_id="t1",
            vector_ref="v1",
            present=False,
        )
        and AiVectorIntelligenceRoot.enable(
            tenant_id="t1", vector_ref="v2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            AiGovernanceFoundationRoot.enable,
            tenant_id="t1",
            governance_ref="gov1",
            present=False,
        )
        and AiGovernanceFoundationRoot.enable(
            tenant_id="t1", governance_ref="gov2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            AiAgentFoundationRoot.enable,
            tenant_id="t1",
            agent_ref="a1",
            present=False,
        )
        and AiAgentFoundationRoot.enable(
            tenant_id="t1", agent_ref="a2"
        ).is_missing()
        is False
    )
    aggregates_ok = all(checks)

    acl_path = (
        root / "backend/contexts/ai/infrastructure/acl/ai_foundation_acl.py"
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
        and "via_p213_l" in acl_text
        and "via_p213_m" in acl_text
        and "via_p213_o" in acl_text
        and "via_enterprise_ai" in acl_text
        and "module_local_llm_sdk_forbidden" in acl_text
        and "via_api_gateway" in acl_text
    )

    router = (
        root / "backend/contexts/ai/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '@router.get("/foundation")' in router
        and "/foundation/readiness" in router
        and "/foundation/vision" in router
        and "/foundation/ml" in router
        and "/foundation/generative" in router
        and "/foundation/vectors" in router
        and "/foundation/agents" in router
        and "/foundation/security" in router
    )

    registry = (root / "backend/contexts/registry.py").read_text(encoding="utf-8")
    registry_ok = 'id="ai"' in registry and "CAP-PLT-AI-001" in registry

    law = (
        root / "docs/architecture/ENTERPRISE_AI_PLATFORM_FOUNDATION.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never Enterprise AI platform foundation is missing" in law
        and "Never Machine learning platform is missing" in law
        and "Never Generative AI platform is missing" in law
        and "Never LLM platform is missing" in law
        and "Never AI model lifecycle is missing" in law
        and "Never MLOps foundation is missing" in law
        and "Never Vector intelligence is missing" in law
        and "Never AI governance foundation is missing" in law
        and "Never AI agent foundation is missing" in law
        and "Never Knowledge graph integration is missing" in law
        and "Never Digital twin integration is missing" in law
        and "Never CQRS architecture is missing" in law
        and "Never Event architecture is missing" in law
        and "Never Microservices architecture is missing" in law
        and "Never API first architecture is missing" in law
        and "Never Zero trust security is missing" in law
        and "Never Cloud native deployment is missing" in law
        and "Never Sibling AI BC" in law
        and "MEOS Enterprise AI Intelligence Fabric" in law
        and "intelligence foundation" in law
    )

    passed = (
        not missing
        and not sibling
        and catalog_ok
        and aggregates_ok
        and acl_ok
        and router_ok
        and registry_ok
        and doc_ok
    )
    return {
        "prompt": "P214-A",
        "adr": 421,
        "passed": passed,
        "missing_artifacts": missing,
        "forbidden_sibling_present": sibling,
        "catalog": catalog_ok,
        "aggregates": aggregates_ok,
        "acl": acl_ok,
        "router": router_ok,
        "registry": registry_ok,
        "documentation": doc_ok,
        "sor": "ai",
        "capability": "CAP-PLT-AI-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
