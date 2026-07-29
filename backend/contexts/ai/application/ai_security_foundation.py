"""AI P214-I Security / Adversarial Defense foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/429-enterprise-ai-security.md",
    "docs/architecture/ENTERPRISE_AI_SECURITY.md",
    "docs/architecture/enterprise_ai/AI_SECURITY_CAPABILITIES.v1.yaml",
    "docs/architecture/enterprise_ai/AI_SECURITY_DDD_CQRS.v1.yaml",
    "docs/architecture/enterprise_ai/AI_SECURITY_SECURITY.v1.yaml",
    "docs/architecture/enterprise_ai/AI_SECURITY_VALIDATION.v1.yaml",
    "backend/contexts/ai/domain/services/ai_platform_security.py",
    "backend/contexts/ai/domain/aggregates/ai_security_aggregates.py",
    "backend/contexts/ai/infrastructure/acl/ai_security_acl.py",
    "backend/contexts/ai/application/ai_security_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/ml_platform",
    "backend/contexts/generative_ai",
    "backend/contexts/llm_platform",
    "backend/contexts/ai_core",
    "backend/contexts/vector_intelligence",
    "backend/contexts/ai_security",
    "backend/contexts/adversarial_defense",
    "backend/contexts/llm_security",
    "backend/contexts/prompt_security",
    "backend/contexts/ai_threat_intel",
    "backend/contexts/ai_runtime_protection",
)


def validate_ai_security_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.ai.domain.aggregates.ai_security_aggregates import (
        AdversarialDefenseRoot,
        AgentSecurityRoot,
        AiSecurityPlatformRoot,
        LlmSecurityRoot,
        ModelSecurityRoot,
        PromptSecurityRoot,
    )
    from contexts.ai.domain.services import ai_platform_security as catmod

    cat = catmod.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P214-I"
        and cat.get("adr") == 429
        and cat.get("sor") == "ai"
        and cat.get("capability") == "CAP-PLT-AI-001"
        and cat.get("principle") == catmod.PRINCIPLE
        and cat.get("fabric") == catmod.FABRIC
        and "intelligence layer" in cat["principle"]
        and cat["domain_model"]["core_domain"] == catmod.CORE_DOMAIN
        and cat["domain_model"]["supporting_count"] >= 9
        and cat["bounded_contexts"]["context_count"] >= 8
        and cat["enterprise_ai_security_platform_present_required"] is True
        and cat["ai_model_security_present_required"] is True
        and cat["llm_security_present_required"] is True
        and cat["prompt_security_present_required"] is True
        and cat["agent_security_present_required"] is True
        and cat["adversarial_defense_present_required"] is True
        and cat["ai_threat_intelligence_present_required"] is True
        and cat["runtime_protection_present_required"] is True
        and cat["ai_security_operations_present_required"] is True
        and cat["security_knowledge_graph_present_required"] is True
        and cat["ai_security_digital_twin_present_required"] is True
        and cat["cqrs_architecture_present_required"] is True
        and cat["event_architecture_present_required"] is True
        and cat["microservices_architecture_present_required"] is True
        and cat["api_first_architecture_present_required"] is True
        and cat["zero_trust_security_present_required"] is True
        and cat["cloud_native_deployment_present_required"] is True
        and cat["sibling_ai_bc_forbidden"] is True
        and cat["models"]["via_p209"] is True
        and cat["llm"]["via_p214_e"] is True
        and cat["prompts"]["via_p214_h"] is True
        and cat["agents"]["via_p214_f"] is True
        and cat["threats"]["via_p210"] is True
        and cat["knowledge_graph"]["via_p214_g"] is True
        and cat["soc"]["via_p210"] is True
        and cat["deployment"]["via_p213_o"] is True
        and cat["cqrs"]["command_count"] >= 6
        and cat["events"]["core_event_count"] >= 8
        and cat["microservices"]["service_count"] >= 10
        and cat["cursor_outputs"]["count"] >= 20
        and "enterprise_ai_security_platform_is_missing"
        in cat["quality_gates"]["reject_if"]
        and "P214-H" in cat["builds_on"]
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
            AiSecurityPlatformRoot.enable,
            tenant_id="t1",
            platform_ref="p1",
            present=False,
        )
        and AiSecurityPlatformRoot.enable(
            tenant_id="t1", platform_ref="p2"
        ).is_missing()
        is False,
        not _bad(
            ModelSecurityRoot.enable,
            tenant_id="t1",
            model_ref="m1",
            present=False,
        )
        and ModelSecurityRoot.enable(
            tenant_id="t1", model_ref="m2"
        ).is_missing()
        is False,
        not _bad(
            LlmSecurityRoot.enable,
            tenant_id="t1",
            llm_ref="l1",
            present=False,
        )
        and LlmSecurityRoot.enable(tenant_id="t1", llm_ref="l2").is_missing()
        is False,
        not _bad(
            PromptSecurityRoot.enable,
            tenant_id="t1",
            prompt_ref="pr1",
            present=False,
        )
        and PromptSecurityRoot.enable(
            tenant_id="t1", prompt_ref="pr2"
        ).is_missing()
        is False,
        not _bad(
            AgentSecurityRoot.enable,
            tenant_id="t1",
            agent_ref="a1",
            present=False,
        )
        and AgentSecurityRoot.enable(
            tenant_id="t1", agent_ref="a2"
        ).is_missing()
        is False,
        not _bad(
            AdversarialDefenseRoot.enable,
            tenant_id="t1",
            defense_ref="d1",
            present=False,
        )
        and AdversarialDefenseRoot.enable(
            tenant_id="t1", defense_ref="d2"
        ).is_missing()
        is False,
    ]
    aggregates_ok = all(checks)

    acl_path = root / "backend/contexts/ai/infrastructure/acl/ai_security_acl.py"
    acl_text = acl_path.read_text(encoding="utf-8") if acl_path.exists() else ""
    acl_ok = (
        acl_path.exists()
        and "via_p207" in acl_text
        and "via_p208" in acl_text
        and "via_p209" in acl_text
        and "via_p210" in acl_text
        and "via_p211" in acl_text
        and "via_p214_e" in acl_text
        and "via_p214_f" in acl_text
        and "via_p214_g" in acl_text
        and "via_p214_h" in acl_text
        and "model_signing" in acl_text
        and "module_local_ai_security_forbidden" in acl_text
    )

    router = (
        root / "backend/contexts/ai/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '@router.get("/aisec")' in router
        and "/aisec/readiness" in router
        and "/aisec/models" in router
        and "/aisec/llm" in router
        and "/aisec/prompts" in router
        and "/aisec/agents" in router
        and "/aisec/adversarial" in router
        and "/aisec/soc" in router
    )

    law = (root / "docs/architecture/ENTERPRISE_AI_SECURITY.md").read_text(
        encoding="utf-8"
    )
    doc_ok = (
        "Never Enterprise AI Security platform is missing" in law
        and "Never AI Model Security is missing" in law
        and "Never LLM Security is missing" in law
        and "Never Prompt Security is missing" in law
        and "Never Agent Security is missing" in law
        and "Never Adversarial Defense is missing" in law
        and "Never AI Threat Intelligence is missing" in law
        and "Never Runtime Protection is missing" in law
        and "Never AI Security Operations is missing" in law
        and "Never Security Knowledge Graph is missing" in law
        and "Never AI Security Digital Twin is missing" in law
        and "Never CQRS architecture is missing" in law
        and "Never Event architecture is missing" in law
        and "Never Microservices architecture is missing" in law
        and "Never API first architecture is missing" in law
        and "Never Zero trust security is missing" in law
        and "Never Cloud native deployment is missing" in law
        and "Never Sibling AI BC" in law
        and "MEOS AI Security Fabric" in law
        and "intelligence layer" in law
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
        "prompt": "P214-I",
        "adr": 429,
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
